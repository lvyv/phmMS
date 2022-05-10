from fastapi import APIRouter, Depends
from schemas.vrla.cellpack_model import CellPackModel
from schemas.vrla.cluster_model import ClusterModel
from schemas.vrla.health_indicator_model import HealthIndicatorModel
from schemas.vrla.self_relation_model import SelfRelationModel
from services.dashboardManagerService import DashboardManagerService
from utils.service_result import handle_result
from phmconfig.database import get_db
from services.cellpackService import CellPackService
from services.healthIndicatorService import HealthIndicatorService
from services.clusterDisplayService import ClusterDisplayService
from services.selfRelationService import SelfRelationService

router = APIRouter(
    prefix="/api/v1/cellpack",
    tags=["电池组历史统计微服务"],
    responses={404: {"description": "Not found"}},
)


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
async def healthEval(equipType: str, equipCode: str, metrics: str, payload: dict, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.health_eval(equipType, equipCode, metrics, payload)
    return handle_result(result)


# 健康指标
@router.post("/healthIndicator")
async def healthIndicator(equipType: str, equipCode: str, reqType: str, db: get_db = Depends()):
    so = HealthIndicatorService(db)
    result = so.health_indicator2(equipType, equipCode, reqType)
    return handle_result(result)


# 回写健康指标数据
@router.post("/writeHealthIndicator")
async def writeHealthIndicator(item: HealthIndicatorModel, db: get_db = Depends()):
    so = HealthIndicatorService(db)
    result = so.create_item(item)
    return handle_result(result)


# 聚类接口
# payload:  {"range":{"from":"2022-02-13T22:09:59.457Z","to":"2022-02-14T04:09:59.457Z"}}
@router.post("/cluster")
async def clusterDisplay(equipType: str, equipCode: str, metrics: str, displayType: str, payload: dict,
                         db: get_db = Depends()):
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
                        payload: dict, db: get_db = Depends()):
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
