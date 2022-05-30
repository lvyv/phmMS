from schemas.base_model import BaseDataModel


class BatteryModel(BaseDataModel):
    remainLife: float     # 剩余寿命
    voc: float            # 开路电压 【电池处于断路状态时的电压，即非工作电压】
    workVoc: float        # 端电压 【电池处于闭路状态时的电池正负极之间的电压，即工作电压】
    soc: float            # 容量 【state of charge】
    soh: float            # 健康指标 【state of health】
    imbalance: float      # 内阻不平衡度
    current: float        # 冲放电电流
    minTemp: float        # 最小温度
    maxTemp: float        # 最大温度
    state:  int           # 健康状态

    # extend
    M1: float
    M2: float
    M3: float
    M4: float
    M5: float
    M6: float
    M7: float
    M8: float
