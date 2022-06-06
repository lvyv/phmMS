from typing import Optional

from fastapi import APIRouter, Depends

import constants
from schemas.vrla.cellpack_model import CellPackModel
from schemas.vrla.cluster_model import ClusterModel
from schemas.vrla.self_relation_model import SelfRelationModel
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.health_eval_util import HealthEvalUtil
from services.convert.self_relation_util import SelfRelationUtil
from services.dashboardManagerService import DashboardManagerService
from services.metricMappingService import MetricMappingService
from services.schedule.beg_for_service import BegForService
from services.schedule.time_grap_util import TimeGrapUtil
from services.sjzy.sjzy_manager import SjzyManager
from services.validate.evalModelValidate import EvalModelValidate
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
    tags=["电池组历史统计微服务"],
    responses={404: {"description": "Not found"}},
)


# 定义规则，所有数据均取历史数据，都需要通过reqId获取


# 回写电池评估数据
@router.post("/writeEval", response_model=CellPackModel)
async def writeHealthEval(item: CellPackModel, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.create_item(item)
    return handle_result(result)


# 电池评估只针对单个电池 或者 单个电池组
# payload:  {"range":{"from":"2022-02-13T22:09:59.457Z","to":"2022-02-14T04:09:59.457Z"}}
# equipCode: 设备编码
# equipType:  battery,cellpack
@router.post("/eval")
async def healthEval(equipType: str, equipCode: str, metrics: str, payload: dict,
                     timeSegment: Optional[str] = None, db: get_db = Depends()):

    # 评估模型校验
    support = EvalModelValidate.support(equipCode)
    if support is False:
        return handle_result(ServiceResult("评估只支持单设备模型建立..."))

    # 数据同步
    sjzyManager.dataSync(equipCode, equipType, db)

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # 评估界面获取所有测点的数据，用于评估计算 健康值，健康状态，电压不平衡度，内阻不平衡度
    result = MetricMappingService(db).get_all_mapping_by_equip_type_code(equipCode)
    allMetrics = ",".join(metricName for metricName in result.values())
    if timeGrapUtil.canClick() is True:
        # 调用模型
        BegForService(db).exec(equipCode, allMetrics, HealthEvalUtil.DISPLAY_HEALTH_EVAL, payload)

    # 数据展示
    so = CellPackService(db)
    result = so.health_eval(equipType, equipCode, metrics, payload, allMetrics)
    return handle_result(result)


# 健康指标
@router.post("/healthIndicator")
async def healthIndicator(equipType: str, equipCode: str, reqType: str, db: get_db = Depends()):
    so = HealthIndicatorService(db)
    result = so.health_indicator(equipType, equipCode, reqType)
    return handle_result(result)


# 聚类接口
# payload:  {"range":{"from":"2022-02-13T22:09:59.457Z","to":"2022-02-14T04:09:59.457Z"}}
@router.post("/cluster")
async def clusterDisplay(equipType: str, equipCode: str, metrics: str, displayType: str, payload: dict,
                         timeSegment: Optional[str] = None,
                         db: get_db = Depends()):
    # 数据同步
    sjzyManager.dataSync(equipCode, equipType, db)

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # 调用模型
    BegForService(db).exec(equipCode, metrics, displayType, payload)

    # 数据展示
    so = ClusterDisplayService(db)
    result = so.clusterDisplay(equipType, equipCode, metrics, displayType, payload)
    return handle_result(result)


# 回写聚类接口
@router.post("/writeCluster", response_model=ClusterModel)
async def writeClusterDisplay(item: ClusterModel, db: get_db = Depends()):
    so = ClusterDisplayService(db)
    result = so.create_item(item)
    return handle_result(result)


# 自相关接口  针对单个设备，单个测点进行
@router.post("/relation")
async def trendRelation(equipType: str, equipCode: str, metrics: str,
                        leftTag: int, rightTag: int, step: int, unit: int,
                        payload: dict,  timeSegment: Optional[str] = None, db: get_db = Depends()):

    # 自相关模型支持判断
    support = RelationModelValidate.support(equipCode, metrics)
    if support is False:
        return handle_result(ServiceResult("自相关只支持单设备单测点模型建立..."))

    # 数据同步
    sjzyManager.dataSync(equipCode, equipType, db)

    # 更新playload
    if timeSegment is not None:
        pl = BegForService.getPlayLoadByTimeSegment(timeSegment)
        if pl is not None:
            payload = pl

    # 调用模型
    BegForService(db).exec(equipCode, metrics, SelfRelationUtil.DISPLAY_SELF_RELATION, payload,
                           leftTag, rightTag, step, unit)
    # 数据展示
    so = SelfRelationService(db)
    result = so.selfRelation(equipType, equipCode, metrics, leftTag, rightTag, step, unit, payload)
    return handle_result(result)


@router.post("/writeRelation")
async def writeClusterDisplay(item: SelfRelationModel, db: get_db = Depends()):
    so = SelfRelationService(db)
    result = so.create_item(item)
    return handle_result(result)


@router.get("/dashboards")
async def get_trend_dashboard(query, filter):
    return DashboardManagerService.getDashboardList(query, filter)
