from fastapi import APIRouter
from typing import Optional

from services.configManagerService import ConfigManagerService

router = APIRouter(
    prefix="/api/v1/public",
    tags=["公共配置"],
    responses={404: {"description": "Not found"}},
)


@router.post("/conf/params")
async def modify_primary_conf_params(msHost: Optional[str] = None, mdHost: Optional[str] = None,
                                     dbHost: Optional[str] = None, dbUser: Optional[str] = None,
                                     dbPw: Optional[str] = None, dbName: Optional[str] = None,
                                     grafanaHost: Optional[str] = None, sjzyHost: Optional[str] = None,
                                     schema: Optional[bool] = None, sample: Optional[int] = None,
                                     multiSelf: Optional[bool] = None, clickGap: Optional[int] = None):
    return ConfigManagerService.update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
                                       grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap)


@router.get("/conf/getParams")
async def query_primary_conf_params():
    return ConfigManagerService.query()
