from pydantic import BaseModel


class EquipTypeMappingModel(BaseModel):

    equip_type: str
    equip_type_code: str

    class Config:
        orm_mode = True
