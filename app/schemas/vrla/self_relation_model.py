from schemas.time_model import TimeModel


class SelfRelationModel(TimeModel):
    reqId: int  # 执行请求ID 关联历史记录表
    lag: int    # x轴坐标 时间轴
    value: float  # 自相关系数
    own_key: str  # 设备^测点

    class Config:
        orm_mode = True