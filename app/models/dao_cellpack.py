from services.main import AppCRUD
from models.tables import TCellPack
from schemas.vrla.cellpack_model import CellPackModel
from sqlalchemy import and_

class CellPackCRUD(AppCRUD):

    def create_record(self, item: CellPackModel) -> TCellPack:
        record = TCellPack(ts=item.ts,
                           did=item.did,
                           dclz=item.dclz,
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
                           cellSoc=item.cellSoc
                           )
        self.db.add(record)
        self.db.commit()
        self.db.refresh(record)
        return record

    def get_record(self, did: str) -> TCellPack:
        record = self.db.query(TCellPack).filter(TCellPack.did == did).first()
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
