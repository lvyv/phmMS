import logging
from typing import Optional

from fastapi import APIRouter, Depends

import json

from phmconfig import constants
from services.convert.health_eval_util import HealthEvalUtil
from services.convert.self_relation_util import SelfRelationUtil
from services.equipTypeMappingService import EquipTypeMappingService
from services.metricMappingService import MetricMappingService
from services.schedule.beg_for_service import BegForService
from services.schedule.time_grap_util import TimeGrapUtil
from services.sjzy.sjzy_manager import SjzyManager
from services.validate.evalModelValidate import EvalModelValidate
from services.validate.publicModelValidate import PublicModelValidate
from services.validate.relationModelValidate import RelationModelValidate
from utils.service_result import handle_result, ServiceResult
from phmconfig.database import get_db
from services.cellpackService import CellPackService
from services.healthIndicatorService import HealthIndicatorService
from services.clusterDisplayService import ClusterDisplayService
from services.selfRelationService import SelfRelationService

sjzyManager = SjzyManager()
timeGrapUtil = TimeGrapUtil()

router = APIRouter(
    prefix="/api/v1/cellpack",
    tags=["微服务"],
    responses={404: {"description": "Not found"}},
)


# 健康指标
@router.post("/healthIndicator")
async def healthIndicator(equipType: str, equipCode: str, reqType: str, db: get_db = Depends()):
    equipTypeCode = equipType
    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipType)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"

    so = HealthIndicatorService(db)
    result = so.health_indicator(equipTypeCode, equipCode, reqType)
    return handle_result(result)


# 定义规则，所有数据均取历史数据，都需要通过reqId获取


# 电池评估只针对单个电池 或者 单个电池组
# payload:  {"range":{"from":"2022-02-13T22:09:59.457Z","to":"2022-02-14T04:09:59.457Z"}}
# equipCode: 设备编码
# equipType:  battery,cellpack
@router.post("/eval")
async def healthEval(equipType: str, equipCode: str, metrics: str, payload: dict,
                     timeSegment: Optional[str] = None, db: get_db = Depends()):
    equipTypeCode = equipType

    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipType)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"

    support, equipCode, metrics = PublicModelValidate.support(equipCode, metrics)
    if support is False:
        return "请输入不为空的设备编码或测点"

    # 评估模型校验
    support = EvalModelValidate.support(equipCode)
    if support is False:
        return handle_result(ServiceResult("评估只支持单设备模型建立..."))

    # 评估界面获取所有测点的数据，用于评估计算 健康值，健康状态，电压不平衡度，内阻不平衡度
    result = MetricMappingService(db).get_all_mapping_by_equip_type_code(equipTypeCode)
    allMetrics = ",".join(metricName for metricName in result.values())
    if timeGrapUtil.canClick() is True:
        # 调用模型 (使用payload)
        BegForService(db).exec(equipTypeCode, equipCode, allMetrics, HealthEvalUtil.DISPLAY_HEALTH_EVAL, payload)

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # 数据展示 （使用timeSegment, 如果没有timeSegment使用payload）
    so = CellPackService(db)
    result = so.health_eval(equipTypeCode, equipCode, metrics, payload, allMetrics)
    return handle_result(result)


# 回写电池评估数据
@router.post("/writeEvalBatch")
async def writeHealthEvalBatch(reqid: int, payload: dict, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.create_batch(reqid, json.loads(payload["items"]))
    return handle_result(result)


# 聚类接口
# payload:  {"range":{"from":"2022-02-13T22:09:59.457Z","to":"2022-02-14T04:09:59.457Z"}}
@router.post("/cluster")
async def clusterDisplay(equipType: str, equipCode: str, metrics: str, displayType: str, payload: dict,
                         timeSegment: Optional[str] = None,
                         db: get_db = Depends()):
    equipTypeCode = equipType

    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipType)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"

    support, equipCode, metrics = PublicModelValidate.support(equipCode, metrics)
    if support is False:
        return "请输入不为空的设备编码或测点"

    # 调用模型
    BegForService(db).exec(equipTypeCode, equipCode, metrics, displayType, payload)

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # 数据展示
    so = ClusterDisplayService(db)
    result = so.clusterDisplay(equipTypeCode, equipCode, metrics, displayType, payload)
    return handle_result(result)


@router.post("/writeClusterBatch")
async def writeClusterDisplay(reqid: int, displayType: str, payload: dict, db: get_db = Depends()):
    so = ClusterDisplayService(db)
    result = so.create_batch(reqid, displayType, json.loads(payload["items"]))
    return handle_result(result)


# 自相关接口  针对单个设备，单个测点进行
# 注意：(自相关折线图数据 复用聚类折线图)  &from=$__from&to=$__to
@router.post("/relation")
async def trendRelation(equipType: str, equipCode: str, metrics: str, payload: dict,
                        timeSegment: str, params: str,
                        subFrom: str, subTo: str,
                        db: get_db = Depends()):
    equipTypeCode = equipType

    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipType)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"

    support, equipCode, metrics = PublicModelValidate.support(equipCode, metrics)
    if support is False:
        return "请输入不为空的设备编码或测点"

    # 自相关模型支持判断
    if constants.SUPPORT_MUTIL_RELATION is False:
        support = RelationModelValidate.support(equipCode, metrics)
        if support is False:
            return "自相关只支持单设备单测点模型建立..."

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # TODO 自相关调度 ，采用 timeSegment + subFrom + subTo

    try:
        sub_from = SelfRelationUtil.getTagInfoByTime(subFrom)
        sub_to = SelfRelationUtil.getTagInfoByTime(subTo)
        canSchedule = True
    except Exception as e:
        # logging.info(e)
        sub_from = sub_to = -1
        canSchedule = False
        # return "请选择参与自相关运算的时间窗口【起点】与【终点】"

    if canSchedule is True:
        # 调用模型
        BegForService(db).exec(equipTypeCode, equipCode, metrics, SelfRelationUtil.DISPLAY_SELF_RELATION, payload,
                               sub_from, sub_to)

    # TODO 数据展示， 采用 timeSegment + params

    try:
        paramsPayload = BegForService.getPlayLoadByTimeSegment(params)
        sub_from, sub_to = SelfRelationUtil.getTagInfoByPayload(paramsPayload)
    except Exception as e:
        # logging.info(e)
        sub_from = sub_to = -1
        return "请选择参与自相关运算的历史时间窗口"

    # 数据展示
    so = SelfRelationService(db)
    result = so.selfRelation(equipTypeCode, equipCode, metrics, payload, sub_from, sub_to)
    return handle_result(result)


@router.post("/writeRelationBatch")
async def writeClusterDisplay(reqid: int, payload: dict, db: get_db = Depends()):
    so = SelfRelationService(db)
    result = so.create_batch(reqid, json.loads(payload["items"]))
    return handle_result(result)
