from pydantic import BaseModel


class MetricMappingModel(BaseModel):
    metric_code: str    # 测点编码
    metric_name: str    # 测点名称
    metric_alias: str   # 测点别名
    equip_type: str     # 装备类型
    equip_code: str     # 装备编码
    equip_name: str     # 装备名称
    metric_describe: str  # 测点描述
    equip_type_code: str  # 装备类型编码
    metric_unit: str      # 测点单位

    class Config:
        orm_mode = True
