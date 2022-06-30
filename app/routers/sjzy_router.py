from typing import Optional
from fastapi import APIRouter, Depends
from services.equipTypeMappingService import EquipTypeMappingService
from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from utils.service_result import handle_result

router = APIRouter(
    prefix="/api/v1/public",
    tags=["数据资源"],
    responses={404: {"description": "Not found"}},
)


# 绑定装备类型映射
@router.post("/updateEquipType")
async def updateEquipType(equipTypeCode: str, equipType, db: get_db = Depends()):
    # TODO 同步测点
    metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)
    MetricMappingService(db).update_all_mapping(equipTypeCode, metrics, equipType)
    # TODO 类型绑定
    result = EquipTypeMappingService(db).updateMapping(equipTypeCode, equipType)
    return handle_result(result)


# 根据装备类型
@router.post("/updateMetrics")
async def dataMapping(equipTypeCode: str, metricName: str, metric_alias: str,
                      metric_describe: Optional[str] = '',
                      db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.update_all_metric_alias(equipTypeCode, metricName, metric_alias, metric_describe)
    return handle_result(result)


@router.post("/getAllMetrics")
async def getAllMetrics(equipTypeCode: str, db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.get_items_by_equip_type_code(equipTypeCode)
    return handle_result(result)
