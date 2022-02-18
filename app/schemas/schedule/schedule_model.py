from pydantic import BaseModel


class ScheduleModel(BaseModel):
    dids: str
    dtags: str
    enable: bool
    initDelay: int
    delay: int
    execUrl: str
    startTime: int

    class Config:
        orm_mode = True
