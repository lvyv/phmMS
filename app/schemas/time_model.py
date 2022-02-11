from pydantic import BaseModel


class TimeModel(BaseModel):
    ts: int  # 时间
