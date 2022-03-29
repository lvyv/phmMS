from schemas.time_model import TimeModel


class ClusterModel(TimeModel):
    reqId: int  # 执行请求ID 关联历史记录表
    x: float  # x 轴坐标
    y: float  # y 轴坐标
    z: float  # z 轴坐标
    color: str  # 颜色值 eg: "red", "green", "yellow", "blue", "gray","black", "orange"
    size: float  # 大小
    shape: str  # 形状 eg: "circle", "star","square", "cross", "diamond"
    name: str  # 装备ID

    class Config:
        orm_mode = True
