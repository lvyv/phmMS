from services.main import AppCRUD
from models.tables import TSchedule
from schemas.schedule.schedule_model import ScheduleModel


class ScheduleCRUD(AppCRUD):

    def create_record(self, item: ScheduleModel) -> TSchedule:
        record = TSchedule(dids=item.dids,
                           dtags=item.dtags,
                           enable=item.enable,
                           initDelay=item.initDelay,
                           delay=item.delay,
                           execUrl=item.execUrl,
                           startTime=item.startTime
                           )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_record(self, id: str) -> TSchedule:
        record = self.db.query(TSchedule).filter(TSchedule.id == id).first()
        return record

    def del_record(self, id: str) -> TSchedule:

        record = self.get_record(id)
        if record:
            self.db.delete(record)
            self.db.commit()
            return record
        return None

    def get_records(self) -> TSchedule:
        records = self.db.query(TSchedule).all()
        if records:
            return records
        return None

    def del_records(self) -> TSchedule:
        records = self.get_records()
        if records:
            for record in records:
                self.db.delete(record)
            self.db.commit()
            return records
        return None
