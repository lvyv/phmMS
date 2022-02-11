from schemas.vrla.battery_model import BatteryModel


class CellPackModel(BatteryModel):
    cellMaxVoc: float  # 电池单元的最大开路电压
    cellMinVoc: float  # 电池单元的最小开路电压
    cellMaxVol: float  # 电池单元的最大端电压
    cellMinVol: float  # 电池单元的最小端电压
    cellAvgVol: float  # 电池单元的均值端电压
    envTemp: str        # 电池组的环境温度（存在多个测点）eg: "[19.0,192.0]"
    cellVol: str        # 电池单元端电压集合 eg: "[19.0,192.0]"
    cellSoc: str        # 电池单元容量集合 eg: "[19.0,192.0]"

    class Config:
        orm_mode = True
