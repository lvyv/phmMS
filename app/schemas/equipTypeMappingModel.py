from pydantic import BaseModel


class EquipTypeMappingModel(BaseModel):

    equip_type: str      # 装备类型 内部使用
    equip_type_code: str  # 装备类型编码

    class Config:
        orm_mode = True
