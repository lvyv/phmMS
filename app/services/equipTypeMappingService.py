import logging

from phmconfig import constants
from models.dao_equip_type_mapping import EquipTypeMappingCRUD
from schemas.equipTypeMappingModel import EquipTypeMappingModel
from services.main import AppService
from utils.service_result import ServiceResult


class EquipTypeMappingService(AppService):

    def create_item(self, pi) -> ServiceResult:
        item = EquipTypeMappingCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def create_batch(self, batch):
        items = EquipTypeMappingCRUD(self.db).get_all()
        if items is None:
            mappings = []
            for bt in batch:
                mappings.append(EquipTypeMappingModel(
                        equip_type_code=bt["equipTypeCode"],
                        equip_type=''
                    ))
            items = EquipTypeMappingCRUD(self.db).create_batch(mappings)
        else:
            for bt in batch:
                found = False
                for item in items:
                    if item.equip_type_code == bt["equipTypeCode"]:
                        found = True
                if found is False:
                    mmm = EquipTypeMappingModel(
                        equip_type_code=bt["equipTypeCode"],
                        equip_type=''
                    )
                    self.create_item(mmm)
        return ServiceResult(items)

    def update_item(self, pi) -> ServiceResult:
        item = EquipTypeMappingCRUD(self.db).update_record(pi)
        return ServiceResult(item)

    def updateMapping(self, equipTypeCode, equipType) -> ServiceResult:
        items = EquipTypeMappingCRUD(self.db).get_all()
        if items is None:
            mmm = EquipTypeMappingModel(
                                     equip_type=equipType,
                                     equip_type_code=equipTypeCode,
                                     )
            self.create_item(mmm)
        else:
            found = False
            for item in items:
                if item.equip_type_code == equipTypeCode:
                    found = True
                    if item.equip_type != equipType:
                        item.equip_type = equipType
                        self.update_item(item)
            if found is False:
                mmm = EquipTypeMappingModel(
                    equip_type=equipType,
                    equip_type_code=equipTypeCode,
                )
                self.create_item(mmm)
        item = EquipTypeMappingCRUD(self.db).get_one(equipTypeCode)
        return ServiceResult(item)

    def getEquipTypeMapping(self, equipTypeCode):
        item = EquipTypeMappingCRUD(self.db).get_one(equipTypeCode)
        if item is None:
            return None
        return item.equip_type

    def getAllEquipTypeMapping(self):
        items = EquipTypeMappingCRUD(self.db).get_all()
        types = []
        for item in items:
            types.append(item.equip_type_code)
        return types
