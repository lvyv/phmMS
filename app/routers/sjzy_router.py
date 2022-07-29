from typing import Optional
from fastapi import APIRouter, Depends

from models.dao_metric_mapping import MetricMappingCRUD
from services.equipTypeMappingService import EquipTypeMappingService
from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
from phmconfig.database import get_db
from services.sjzy.AutomaticMetricBind import AutomaticMetricBind
from utils.service_result import handle_result

router = APIRouter(
    prefix="/api/v1/mapping",
    tags=["映射配置"],
    responses={404: {"description": "Not found"}},
)


# 查询装备编码类型
@router.get("/getTypeByName")
async def getEquipTypeCodeByName(equipName: str, equipCode: Optional[str] = None):
    """
    通过装备名称获取装备类型
    :param equipName:  装备名称
    :param equipCode:  装备编码
    :return:
    """
    return DataCenterService.filter_zb_equip_type_code(DataCenterService.download_zb_type_code(equipName, equipCode))


# 绑定装备类型映射
@router.post("/updateEquipType")
async def updateEquipType(equipTypeCode: str, equipType, db: get_db = Depends()):
    # TODO 同步测点
    metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)

    if metrics is None:
        return "装备类型编码，未找到测点数据，不进行类型绑定。"

    # TODO 自动绑定
    # 通过装备编码类型从数据库中获取测点。
    ownMetrics = MetricMappingCRUD(db).get_all(equipTypeCode)
    if ownMetrics is None:
        metrics = AutomaticMetricBind.autoRun(metrics)
    else:
        metrics = AutomaticMetricBind.autobind(metrics, ownMetrics)

    # TODO 更新测定绑定
    mms = MetricMappingService(db)
    mms.update_all_mapping(equipTypeCode, metrics, equipType)

    # TODO 类型绑定
    result = EquipTypeMappingService(db).updateMapping(equipTypeCode, equipType)
    return handle_result(result)


# 根据装备类型
@router.post("/updateMetrics")
async def dataMapping(equipTypeCode: str, metricName: str, metric_alias: str,
                      metric_describe: Optional[str] = '',
                      db: get_db = Depends()):
    so = MetricMappingService(db)
    result = so.update_all_metric_alias(equipTypeCode, metricName, metric_alias, metric_describe)
    return handle_result(result)


@router.post("/getAllMetrics")
async def getAllMetrics(equipTypeCode: str, db: get_db = Depends()):
    """
    根据装备类型获取所有的测点
    :param equipTypeCode:
    :param db:
    :return:
    """
    so = MetricMappingService(db)
    result = so.get_items_by_equip_type_code(equipTypeCode)
    return handle_result(result)


@router.post("/syncMetrics")
async def dataSync(equipTypeCode: str, db: get_db = Depends()):
    equipType = EquipTypeMappingService(db).getEquipTypeMapping(equipTypeCode)
    if equipType is None or equipType is '':
        return "请先建立装备类型编码与装备类型映射表。"
    # TODO 同步测点
    metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)
    # TODO 自动绑定
    ownMetrics = MetricMappingCRUD(db).get_all(equipTypeCode)
    if ownMetrics is None:
        metrics = AutomaticMetricBind.autoRun(metrics)
    else:
        metrics = AutomaticMetricBind.autobind(metrics, ownMetrics)

    # TODO 更新测定绑定
    mms = MetricMappingService(db)
    result = mms.update_all_mapping(equipTypeCode, metrics, equipType)

    return handle_result(result)
