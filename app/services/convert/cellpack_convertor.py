import json


class CellPackConvertor:

    @staticmethod
    def __parse_str_to_json(value):
        try:
            return json.loads(value)
        finally:
            return None

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
            ret.append({"name": key, "type": CellPackConvertor.__get_metric_type(key), "values": tmpDict[key]})
        return ret
