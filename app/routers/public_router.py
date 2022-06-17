import json
from typing import Optional

from fastapi import APIRouter, Depends

from services.convert.health_eval_util import HealthEvalUtil
from services.convert.metric_mapping_utils import MetricMappingUtils
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.http.dataCenterService import DataCenterService
from services.reqhistoryService import ReqHistoryService
from utils.service_result import handle_result, ServiceResult

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


# 查询装备编码类型
@router.get("/getEquipTypeCode")
async def getEquipTypeCode():
    metrics = DataCenterService.download_zb_metric()
    equipTypeCode = DataCenterService.filter_zb_equip_type_code(metrics)
    return equipTypeCode


# equipTypeCode 设备类型编码
@router.post("/sync")
async def dataSync(equipTypeCode: str, db: get_db = Depends()):
    so = MetricMappingService(db)
    metrics = DataCenterService.download_zb_metric(equipTypeCode)
    # 同步电池测点映射数据
    result = so.update_all_mapping(equipTypeCode, metrics)
    return handle_result(result)


# 根据装备类型
@router.post("/mapping")
async def dataMapping(equipTypeCode: str, metricName: str, metric_alias: str,
                      equipType, metric_describe: Optional[str] = '',
                      db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.update_all_metric_alias(equipTypeCode, metricName, metric_alias, equipType, metric_describe)
    # 设置
    MetricMappingUtils.init_first = False
    return handle_result(result)


# 根据装备类型获取mapping
@router.get("/getMapping")
async def getMapping(equipCode: str, db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.get_all_mapping_by_equip_type_code(equipCode)
    return handle_result(ServiceResult(result))


@router.put("/updateHistoryRecord")
async def updateHistoryRecord(reqid: str, res: str, db: get_db = Depends()):
    reqs = ReqHistoryService(db)
    result = reqs.update_item(reqid, res)
    return handle_result(result)


# @router.get("/plugin/info")
async def getPluginAllInfo(displayType, db: get_db = Depends()):
    so = ReqHistoryService(db)
    result = so.get_plugin_all_info(displayType)
    return handle_result(result)


# 获取装备类型
@router.get("/plugin/equipType")
async def getEquipTypeByPlugin():
    result = ServiceResult(["battery", "cellpack"])
    return handle_result(result)


# 获取装备编码
@router.get("/plugin/equipCode")
async def getEquipCodeByPlugin(equipType, displayType, db: get_db = Depends()):
    so = ReqHistoryService(db)
    result = so.get_equip_code(displayType)
    return handle_result(result)


# 获取装备编码
@router.get("/plugin/metric")
async def getMetricByPlugin(equipType, equipCode, displayType, db: get_db = Depends()):
    so = ReqHistoryService(db)
    result = so.get_equip_metric(equipCode, displayType)
    return handle_result(result)


# 获取时间段
@router.get("/plugin/timeSegment")
async def getTimeSegmentByPlugin(equipType, equipCode, metric, displayType, db: get_db = Depends()):
    so = ReqHistoryService(db)
    if displayType in [HealthEvalUtil.DISPLAY_HEALTH_EVAL]:
        # 评估界面获取所有测点的数据，用于评估计算 健康值，健康状态，电压不平衡度，内阻不平衡度
        result = MetricMappingService(db).get_all_mapping_by_equip_type_code(equipCode)
        allMetrics = ",".join(metricName for metricName in result.values())
        result = so.get_time_segment(equipCode, allMetrics, displayType)
    else:
        result = so.get_time_segment(equipCode, metric, displayType)
    return handle_result(result)


# 提供给 IOT-Json 插件测量标志
@router.get("/plugin/indicator")
async def getEquipTypeByPlugin():
    result = ServiceResult(["$equipType.$equipCode.$metrics.2D", "$equipType.$equipCode.$metrics.3D",
                            "$equipType.$equipCode.$metrics.AGG2D", "$equipType.$equipCode.$metrics.AGG3D",
                            "$equipType.$equipCode.$metrics.SELF_RELATION",
                            "$equipType.$equipCode.$metrics.SELF_POLYLINE",
                            "$equipType.$equipCode.$metrics.SCATTER",
                            "$equipType.$equipCode.$metrics.POLYLINE",
                            "$equipType.$equipCode.SOH.EVAL"])
    return handle_result(result)
