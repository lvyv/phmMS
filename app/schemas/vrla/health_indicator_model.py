from schemas.base_model import BaseDataModel


class HealthIndicatorModel(BaseDataModel):
    state: int  # 健康状态
    soh: float  # 健康指标 【state of health】

    class Config:
        orm_mode = True
