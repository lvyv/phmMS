from services.convert.cellpack_convertor import CellPackConvertor
from services.convert.battery_convertor import BatteryConvertor


class ConvertorFactory:
    @staticmethod
    def get_convertor(clz):
        values = {
            # "cellpack": CellPackConvertor(),
            # "battery": BatteryConvertor()
            "battery": CellPackConvertor()
        }
        return values.get(clz, None)
