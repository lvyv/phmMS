import json
from services.convert.convertor import IConvertor


class CellPackConvertor(IConvertor):

    def __init__(self):
        IConvertor.__init__(self)
        self.ownMetrics = ["ts", "remainLife", "voc", "workVoc", "soc",
                           "soh", "imbalance", "current", "minTemp", "maxTemp",
                           "cellMaxVoc", "cellMinVoc", "cellMaxVol", "cellMinVol", "cellAvgVol",
                           "envTemp", "cellVol", "cellSoc"]

    @staticmethod
    def __parse_str_to_json(value):
        load_dict = None
        try:
            load_dict = json.loads(value)
        finally:
            return load_dict

    @staticmethod
    def __has_special_key(key):
        if key in ["envTemp", "cellVol", "cellSoc"]:
            return True
        return False

    def get_metric_value(self, item, metric):
        values = {
            "ts": item.ts,
            "remainLife": item.remainLife,
            "voc": item.voc,
            "workVoc": item.workVoc,
            "soc": item.soc,
            "soh": item.soh,
            "imbalance": item.imbalance,
            "current": item.current,
            "minTemp": item.minTemp,
            "maxTemp": item.maxTemp,
            "cellMaxVoc": item.cellMaxVoc,
            "cellMinVoc": item.cellMaxVoc,
            "cellMaxVol": item.cellMaxVol,
            "cellMinVol": item.cellMinVol,
            "cellAvgVol": item.cellAvgVol,
            "envTemp": item.envTemp,
            "cellVol": item.cellVol,
            "cellSoc": item.cellSoc
        }
        return values.get(metric, None)

    def get_own_metrics(self):
        return self.ownMetrics

    def __convert_special(self, key, dataS):
        tmpDict = {}
        for data in dataS:
            items = self.__parse_str_to_json(data)
            if items is None:
                continue
            i = 0
            for item in items:
                combineKey = key + str(i)
                if combineKey in tmpDict.keys():
                    tmpDict[combineKey].append(item)
                else:
                    tmpDict[combineKey] = [item]
                i = i + 1

        ret = []
        for key in tmpDict.keys():
            ret.append({"name": key, "type": "number", "values": tmpDict[key]})
        return ret

    def convert(self, items, metrics):
        IConvertor.convert(self, items, metrics)
        ret = []
        for key in self.tmpDict.keys():
            if self.__has_special_key(key):
                convert_items = self.__convert_special(key, self.tmpDict[key])
                for it in convert_items:
                    ret.append(it)
            else:
                ret.append({"name": key, "type": self.get_metric_type(key), "values": self.tmpDict[key]})
        return ret
