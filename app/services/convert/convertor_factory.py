from services.convert.cellpack_convertor import CellPackConvertor


class ConvertorFactory:
    @staticmethod
    def get_convertor(clz):
        return CellPackConvertor(clz)
