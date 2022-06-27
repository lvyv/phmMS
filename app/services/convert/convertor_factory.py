from services.convert.cellpack_convertor import CellPackConvertor


class ConvertorFactory:

    convertorCache = {}

    @staticmethod
    def get_convertor(clz):
        if clz in ConvertorFactory.convertorCache.keys():
            return ConvertorFactory.convertorCache[clz]
        else:
            convertor = CellPackConvertor(clz)
            ConvertorFactory.convertorCache[clz] = convertor
            return convertor
