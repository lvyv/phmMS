from schemas.time_model import TimeModel


class BaseDataModel(TimeModel):
    did: str   # 设备ID
    dclz: str  # 设备类型
    reqId: int  # 请求历史记录ID
