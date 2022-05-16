from pydantic import BaseModel


class MetricMappingModel(BaseModel):
    metric_name: str
    metric_alias: str
    equip_type: str
    metric_describe: str

    class Config:
        orm_mode = True
