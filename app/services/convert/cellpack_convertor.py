import json


class CellPackConvertor:

    @staticmethod
    def __parse_str_to_json(value):
        load_dict = None
        try:
            load_dict = json.loads(value)
        finally:
            return load_dict

    @staticmethod
    def __get_metric_value(item, metric):
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

    @staticmethod
    def __get_metric_type(key):
        if key in ["ts"]:
            return "time"
        return "number"

    @staticmethod
    def __has_special_key(key):
        if key in ["envTemp", "cellVol", "cellSoc"]:
            return True
        return False

    @staticmethod
    def convert(items, metrics):
        useMetrics = metrics.split(",")
        useMetrics.insert(0, "ts")
        tmpDict = {}
        for item in items:
            for m in useMetrics:
                if m in tmpDict.keys():
                    tmpDict[m].append(CellPackConvertor.__get_metric_value(item, m))
                else:
                    tmpDict[m] = [CellPackConvertor.__get_metric_value(item, m)]
        ret = []
        for key in tmpDict.keys():
            if CellPackConvertor.__has_special_key(key):
                convert_items = CellPackConvertor.convert_special(key, tmpDict[key])
                for it in convert_items:
                    ret.append(it)
            else:
                ret.append({"name": key, "type": CellPackConvertor.__get_metric_type(key), "values": tmpDict[key]})
        return ret

    @staticmethod
    def convert_special(key, datas):
        tmpDict = {}
        for data in datas:
            items = CellPackConvertor.__parse_str_to_json(data)
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
