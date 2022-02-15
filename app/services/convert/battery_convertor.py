from services.convert.convertor import IConvertor


class BatteryConvertor(IConvertor):

    def __init__(self):
        IConvertor.__init__(self)
        self.ownMetrics = ["ts", "remainLife", "voc", "workVoc", "soc",
                           "soh", "imbalance", "current", "minTemp", "maxTemp"]

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
            "maxTemp": item.maxTemp
        }
        return values.get(metric, None)

    def get_own_metrics(self):
        return self.ownMetrics

    def convert(self, items, metrics):
        IConvertor.convert(self, items, metrics)
        ret = []
        for key in self.tmpDict.keys():
            ret.append({"name": key, "type": self.get_metric_type(key), "values": self.tmpDict[key]})
        return ret
