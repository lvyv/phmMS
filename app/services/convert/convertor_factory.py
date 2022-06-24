from services.convert.cellpack_convertor import CellPackConvertor


class ConvertorFactory:
    @staticmethod
    def get_convertor(clz):
        values = {
            "battery": CellPackConvertor()
        }
        return values.get(clz, None)
