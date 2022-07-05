from schemas.time_model import TimeModel


class SelfRelationModel(TimeModel):
    reqId: int  # 执行请求ID 关联历史记录表
    lag: int
    value: float
    own_key: str

    class Config:
        orm_mode = True