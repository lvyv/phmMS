import json
from typing import Optional

from fastapi import APIRouter, Depends
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
