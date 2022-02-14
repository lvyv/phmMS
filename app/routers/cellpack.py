from fastapi import APIRouter, Depends
from services.cellpack import CellPackService
from schemas.vrla.cellpack_model import CellPackModel
from utils.service_result import handle_result
from phmconfig.database import get_db

router = APIRouter(
    prefix="/api/v1/cellpack",
    tags=["电池组历史统计微服务"],
    responses={404: {"description": "Not found"}},
)


@router.post("/item", response_model=CellPackModel)
async def create_item(item: CellPackModel, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.create_item(item)
    return handle_result(result)


@router.get("/item/{item_id}")
async def get_item(item_id: str, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.get_item(item_id)
    return handle_result(result)


@router.post("/eval")
async def healthEval(equipType: str, equipCode: str, metrics: str, payload: dict, db: get_db = Depends()):
    so = CellPackService(db)
    result = so.health_eval(equipType, equipCode, metrics, payload)
    return handle_result(result)
