from schemas.base_model import BaseDataModel


# 剩余寿命
# 开路电压 【电池处于断路状态时的电压，即非工作电压】
# 端电压 【电池处于闭路状态时的电池正负极之间的电压，即工作电压】
# 容量 【state of charge】
# 健康指标 【state of health】
# 内阻不平衡度
# 冲放电电流
# 最小温度
# 最大温度
# 健康状态

# 电池单元的最大开路电压
# 电池单元的最小开路电压
# 电池单元的最大端电压
# 电池单元的最小端电压
# 电池单元的均值端电压
# 电池组的环境温度（存在多个测点）eg: "[19.0,192.0]"
# 电池单元端电压集合 eg: "[19.0,192.0]"
# 电池单元容量集合 eg: "[19.0,192.0]"

class CellPackModel(BaseDataModel):
    # 普通采集测点
    M1: float
    M2: float
    M3: float
    M4: float
    M5: float
    M6: float
    M7: float
    M8: float
    M9: float
    M10: float
    M11: float
    M12: float
    M13: float
    M14: float
    M15: float
    M16: float
    M17: float
    M18: float
    M19: float
    M20: float
    M21: float
    M22: float
    M23: float
    M24: float
    M25: float
    M26: float
    M27: float
    M28: float
    M29: float
    M30: float
    M31: float
    M32: float
    M33: float
    M34: float
    M35: float
    M36: float
    M37: float
    M38: float
    M39: float

    AM1: str
    AM2: str
    AM3: str
    AM4: str
    AM5: str

    IM1: int

    FM1: float
    FM2: float
    FM3: float
    FM4: float
    FM5: float

    class Config:
        orm_mode = True
