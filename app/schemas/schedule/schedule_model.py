from pydantic import BaseModel


class ScheduleModel(BaseModel):
    did: str
    enable: bool
    initDelay: int
    delay: int
    execUrl: str
    execParams: str

    class Config:
        orm_mode = True
