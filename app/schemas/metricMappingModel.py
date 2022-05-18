from pydantic import BaseModel


class MetricMappingModel(BaseModel):
    metric_code: str
    metric_name: str
    metric_alias: str
    equip_type: str
    equip_code: str
    equip_name: str
    metric_describe: str

    class Config:
        orm_mode = True
