from services.main import AppCRUD
from models.tables import TCellPack
from schemas.vrla.cellpack_model import CellPackModel
from sqlalchemy import and_, desc


class CellPackCRUD(AppCRUD):

    def create_record(self, item: CellPackModel) -> TCellPack:
        record = TCellPack(ts=item.ts,
                           did=item.did,
                           dclz=item.dclz,
                           reqId=item.reqId,
                           remainLife=item.remainLife,
                           voc=item.voc,
                           workVoc=item.workVoc,
                           soc=item.soc,
                           soh=item.soh,
                           imbalance=item.imbalance,
                           current=item.current,
                           minTemp=item.minTemp,
                           maxTemp=item.maxTemp,
                           cellMaxVoc=item.cellMaxVoc,
                           cellMinVoc=item.cellMinVoc,
                           cellMaxVol=item.cellMaxVol,
                           cellMinVol=item.cellMinVol,
                           cellAvgVol=item.cellAvgVol,
                           envTemp=item.envTemp,
                           cellVol=item.cellVol,
                           cellSoc=item.cellSoc,
                           state=item.state,
                           M1=item.M1,
                           M2=item.M2,
                           M3=item.M3,
                           M4=item.M4,
                           M5=item.M5,
                           M6=item.M6,
                           M7=item.M7,
                           M8=item.M8
                           )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_record(self, did: str) -> TCellPack:
        record = self.db.query(TCellPack).filter(TCellPack.did == did).order_by(desc(TCellPack.ts)).first()
        if record:
            return record
        return None

    def get_records(self, did: str, start: int, end: int) -> TCellPack:
        records = self.db.query(TCellPack).filter(and_(TCellPack.did == did,
                                                       TCellPack.ts.between(start, end)
                                                       )).all()
        if records:
            return records
        return None

    def get_records_by_reqIds(self, reqIds: []) -> TCellPack:
        records = self.db.query(TCellPack).filter(and_(TCellPack.reqId.in_(reqIds))).all()
        if records:
            return records
        return None

    def get_record_latest_by_id(self, dev, reqid: str) -> TCellPack:
        record = self.db.query(TCellPack).filter(
            and_(TCellPack.reqId == reqid,
                 TCellPack.did == dev)).order_by(desc(TCellPack.ts)).first()
        if record:
            return record
        return None

    def get_records_latest_by_reqIds(self, devs: [], reqIds: []) -> TCellPack:
        items = []
        for reqId in reqIds:
            for dev in devs:
                record = self.get_record_latest_by_id(dev, reqId)
                if record:
                    items.append(record)
        if len(items) == 0:
            return None
        return items

    def get_records_by_devs(self, dids: [], start: int, end: int) -> TCellPack:
        records = self.db.query(TCellPack).filter(and_(TCellPack.did.in_(dids),
                                                       TCellPack.ts.between(start, end)
                                                       )).all()
        if records:
            return records
        return None

    def get_records_latest(self, dids: []) -> TCellPack:
        items = []
        for did in dids:
            record = self.get_record(did)
            if record:
                items.append(record)
        if len(items) == 0:
            return None
        return items

    def get_records_by_limit(self, dids, limit) -> TCellPack:
        items = []
        for did in dids:
            item = self.db.query(TCellPack).filter(TCellPack.did == did) \
                .order_by(desc(TCellPack.ts)).limit(limit).all()
            if item:
                items.append(item)
        if len(items) == 0:
            return None
        return items
