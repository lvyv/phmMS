from services.main import AppCRUD
from models.tables import TSchedule
from schemas.schedule.schedule_model import ScheduleModel


class ScheduleCRUD(AppCRUD):

    def create_record(self, item: ScheduleModel) -> TSchedule:
        record = self.get_record(item.did)
        if record:
            record.did = item.did
            record.enable = item.enable
            record.initDelay = item.initDelay
            record.delay = item.delay
            record.execUrl = item.execUrl
            record.execParams = item.execParams
        else:
            record = TSchedule(did=item.did,
                               enable=item.enable,
                               initDelay=item.initDelay,
                               delay=item.delay,
                               execUrl=item.execUrl,
                               execParams=item.execParams
                               )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_record(self, did: str) -> TSchedule:
        record = self.db.query(TSchedule).filter(TSchedule.did == did).first()
        return record

    def get_records(self) -> TSchedule:
        records = self.db.query(TSchedule).all()
        if records:
            return records
        return None

    def del_record(self, did: str) -> TSchedule:

        record = self.get_record(did)
        if record:
            self.db.delete(record)
            self.db.commit()
            return record
        return None

    def del_records(self) -> TSchedule:
        records = self.get_records()
        if records:
            for record in records:
                self.db.delete(record)
            self.db.commit()
            return records
        return None
