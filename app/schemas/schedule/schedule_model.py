from pydantic import BaseModel


class ScheduleModel(BaseModel):
    did: str
    enable: bool
    initDelay: int
    delay: int

    class Config:
        orm_mode = True
