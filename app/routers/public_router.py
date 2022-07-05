from fastapi import APIRouter, Depends
from typing import Optional

from services.configManagerService import ConfigManagerService
from services.dashboardManagerService import DashboardManagerService
from services.equipTypeMappingService import EquipTypeMappingService
from services.grafanaManagerService import GrafanaMangerService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.reqhistoryService import ReqHistoryService
from utils.service_result import handle_result, ServiceResult

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


@router.get("/getEquipType")
async def getEquipType(equipTypeCode: str, db: get_db = Depends()):
    so = EquipTypeMappingService(db)
    result = so.getEquipTypeMapping(equipTypeCode)
    return handle_result(ServiceResult(result))


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
async def get_trend_dashboard(query: Optional[str] = None, filter: Optional[str] = None):
    return DashboardManagerService.getDashboardList(query, filter)


@router.get("/grafana/syncHost")
async def grafana_sync_host(host: Optional[str] = None,
                            timeSegmentLabel: Optional[str] = None,
                            username: Optional[str] = "admin", password: Optional[str] = "admin"):
    return GrafanaMangerService.syncHost(host, timeSegmentLabel, username, password)


# TODO 同步修改重要的配置参数
@router.post("/conf/params")
async def modify_primary_conf_params(msHost: Optional[str] = None, mdHost: Optional[str] = None,
                                     dbHost: Optional[str] = None, dbUser: Optional[str] = None,
                                     dbPw: Optional[str] = None, dbName: Optional[str] = None,
                                     grafanaHost: Optional[str] = None, sjzyHost: Optional[str] = None,
                                     schema: Optional[bool] = None, sample: Optional[int] = None,
                                     multiSelf: Optional[bool] = None, clickGap: Optional[int] = None):
    return ConfigManagerService.update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
                                       grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap)
