from fastapi import APIRouter, Depends
from services.cellpack import CellPackService
from schemas.vrla.cellpack_model import CellPackModel
from utils.service_result import handle_result
from phmconfig.database import get_db
from services.healthIndicatorService import HealthIndicatorService
from schemas.vrla.health_indicator_model import HealthIndicatorModel

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
    result = so.health_indicator(equipType, equipCode, reqType)
    return handle_result(result)


# 回写健康指标数据
@router.post("/writeHealthIndicator")
async def writeHealthIndicator(item: HealthIndicatorModel, db: get_db = Depends()):
    so = HealthIndicatorService(db)
    result = so.create_item(item)
    return handle_result(result)
