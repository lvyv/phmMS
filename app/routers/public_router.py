import json

from fastapi import APIRouter, Depends
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.http.dataCenterService import DataCenterService

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
    so.update_all_mapping("电池", metrics)
    return None
