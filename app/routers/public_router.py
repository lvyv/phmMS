from typing import Optional

from fastapi import APIRouter, Depends

from phmconfig import constants
from services.dashboardManagerService import DashboardManagerService
from services.equipTypeMappingService import EquipTypeMappingService
from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.reqhistoryService import ReqHistoryService
from services.sjzy.AutomaticMetricBind import AutomaticMetricBind
from utils.service_result import handle_result, ServiceResult

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


# 查询装备编码类型
@router.get("/getALLEquipTypeCode")
async def getAllEquipTypeCode():
    return DataCenterService.filter_zb_equip_type_code(DataCenterService.download_zb_type_code())


@router.get("/getEquipType")
async def getEquipType(equipTypeCode: str, db: get_db = Depends()):
    so = EquipTypeMappingService(db)
    result = so.getEquipTypeMapping(equipTypeCode)
    return handle_result(ServiceResult(result))


@router.post("/syncMetrics")
async def dataSync(equipTypeCode: str, autoPwd: Optional[str] = None,
                   db: get_db = Depends()):
    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipTypeCode)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"

    so = MetricMappingService(db)
    metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)

    if autoPwd is not None and autoPwd == constants.API_AUTH_AUTO_PASSWORD:
        so.delete_by_equip_type_code(equipTypeCode)
        metrics = AutomaticMetricBind.autoRun(metrics)

    # 同步电池测点映射数据
    result = so.update_all_mapping(equipTypeCode, metrics, equipType)
    return handle_result(result)


# 根据装备类型获取mapping
@router.get("/getMapping")
async def getMapping(equipTypeCode: str, db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.get_all_mapping_by_equip_type_code(equipTypeCode)
    return handle_result(ServiceResult(result))


@router.put("/updateHistoryRecord")
async def updateHistoryRecord(reqid: str, res: str, db: get_db = Depends()):
    reqs = ReqHistoryService(db)
    result = reqs.update_item(reqid, res)
    return handle_result(result)


@router.get("/dashboards")
async def get_trend_dashboard(query, filter):
    return DashboardManagerService.getDashboardList(query, filter)
