from schemas.equipTypeMappingModel import EquipTypeMappingModel
from services.main import AppCRUD
from models.tables import TEquipTypeMapping
from sqlalchemy import and_, desc


class EquipTypeMappingCRUD(AppCRUD):

    def create_record(self, item: EquipTypeMappingModel) -> TEquipTypeMapping:
        record = TEquipTypeMapping(
            equip_type=item.equip_type,
            equip_type_code=item.equip_type_code
        )
        self.db.add(record)
        self.db.commit()
        return record

    def create_batch(self, items) -> TEquipTypeMapping:
        batch = []
        for im in items:
            record = TEquipTypeMapping(
                               equip_type_code=im["equipTypeCode"],
                               equip_type=im["equipType"] if 'equipType' in im.keys() else ''
                               )
            batch.append(record)
        self.db.add_all(batch)
        self.db.commit()
        return batch

    def update_record(self, item) -> TEquipTypeMapping:
        self.db.add(item)
        self.db.commit()
        return None

    def get_all(self) -> TEquipTypeMapping:
        records = self.db.query(TEquipTypeMapping).all()
        if records:
            return records
        return None

    def get_one(self, equipTypeCode) -> TEquipTypeMapping:
        return self.db.query(TEquipTypeMapping).filter(TEquipTypeMapping.equip_type_code == equipTypeCode).first()
