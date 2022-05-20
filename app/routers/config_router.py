import json

from fastapi import APIRouter, Depends
from services.schedule.schedule_service import ScheduleService
from schemas.schedule.schedule_model import ScheduleModel
from utils.service_result import handle_result
from phmconfig.database import get_db
from services.schedule.dynamic_task import DynamicTask

router = APIRouter(
    prefix="/api/v1/config",
    tags=["装备模型调度配置"],
    responses={404: {"description": "Not found"}},
)


@router.post("/add")
async def createSchedule(item: ScheduleModel, db: get_db = Depends()):
    so = ScheduleService(db)
    # fix
    dids = item.dids.split(',')
    dids.sort()
    tags = item.dtags.split(',')
    tags.sort()
    item.dids = json.dumps(dids, ensure_ascii=False)
    item.dtags = json.dumps(tags, ensure_ascii=False)

    result = so.create_item(item)
    ret = handle_result(result)
    DynamicTask().push(ret)
    return ret


@router.get("/getAll")
async def getAllSchedule(db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.get_items()
    return handle_result(result)


@router.delete("/delete")
async def deleteSchedule(id: str, db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.del_item(id)
    ret = handle_result(result)
    DynamicTask().pop(ret)
    return ret


@router.delete("/deleteAll")
async def delAllSchedule(db: get_db = Depends()):
    so = ScheduleService(db)
    result = so.del_items()
    rets = handle_result(result)
    DynamicTask().popAll(rets)
    return rets
