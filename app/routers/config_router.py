from fastapi import APIRouter, Depends
from services.schedule.schedule_service import ScheduleService
from schemas.schedule.schedule_model import ScheduleModel
from utils.service_result import handle_result
from phmconfig.database import get_db

router = APIRouter(
    prefix="/api/v1/config",
    tags=["装备分析调度配置"],
    responses={404: {"description": "Not found"}},
)


@router.post("/item")
async def create_item(item: ScheduleModel, db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.create_item(item)
    ret = handle_result(result)
    return ret


@router.get("/items")
async def get_items(db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.get_items()
    return handle_result(result)


@router.delete("/item")
async def del_item(id: str, db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.del_item(id)
    ret = handle_result(result)
    return ret


@router.delete("/items")
async def del_items(db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.del_items()
    rets = handle_result(result)
    return rets
