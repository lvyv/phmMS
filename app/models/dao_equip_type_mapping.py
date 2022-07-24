from schemas.equipTypeMappingModel import EquipTypeMappingModel
from services.main import AppCRUD
from models.tables import TEquipTypeMapping
from sqlalchemy import and_, desc


class EquipTypeMappingCRUD(AppCRUD):
    """
    装备类型映射CRUD
    """

    def create_record(self, item: EquipTypeMappingModel) -> TEquipTypeMapping:
        """
        添加一条记录
        """
        record = TEquipTypeMapping(
            equip_type=item.equip_type,
            equip_type_code=item.equip_type_code
        )
        self.db.add(record)
        self.db.commit()
        return record

    def create_batch(self, items) -> TEquipTypeMapping:
        """
        批量添加记录
        """
        batch = []
        for im in items:
            record = TEquipTypeMapping(
                               equip_type_code=im.equip_type_code,
                               equip_type=im.equip_type
                               )
            batch.append(record)
        self.db.add_all(batch)
        self.db.commit()
        return batch

    def update_record(self, item) -> TEquipTypeMapping:
        """
        更新记录
        """
        self.db.add(item)
        self.db.commit()
        return None

    def get_all(self) -> TEquipTypeMapping:
        """
        获取所有记录
        """
        records = self.db.query(TEquipTypeMapping).all()
        if records:
            return records
        return None

    def get_one(self, equipTypeCode) -> TEquipTypeMapping:
        """
        根据装备类型编码查询记录
        """
        return self.db.query(TEquipTypeMapping).filter(TEquipTypeMapping.equip_type_code == equipTypeCode).first()
