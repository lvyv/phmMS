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
    """
    更新MD服务配置
    :param msHost:
    :param mdHost:
    :param dbHost:
    :param dbUser:
    :param dbPw:
    :param dbName:
    :param grafanaHost:
    :param sjzyHost:
    :param schema:
    :param sample:
    :param multiSelf:
    :param clickGap:
    :return:
    """
    return ConfigManagerService.update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
                                       grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap)


# 查询 MD服务配置
@router.get("/conf/getParams")
async def query_primary_conf_params():
    return ConfigManagerService.query()
