from pydantic import BaseModel


class EquipmentItemBase(BaseModel):
    """

    """
    id: int
    devclass: str

    dis_voltage: float
    dis_current: float
    dis_resistance: float
    dis_temperature: float
    dis_dischargecycles: int

    chg_voltage: float
    chg_current: float
    chg_resistance: float
    chg_temperature: float
    chg_dischargecycles: int


class EquipmentItemCreate(EquipmentItemBase):
    """
    创建的时候必须提供模型timestamp，以毫秒为单位。
    """
    ts: int


class EquipmentItem(EquipmentItemBase):
    """
    获取记录必须提供关键字id。
    """
    ts: int

    class Config:
        orm_mode = True
