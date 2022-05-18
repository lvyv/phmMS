import json
from typing import Optional

from fastapi import APIRouter, Depends
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.http.dataCenterService import DataCenterService
from utils.service_result import handle_result

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


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
