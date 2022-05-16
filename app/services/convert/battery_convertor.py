from services.convert.convertor import IConvertor


class BatteryConvertor(IConvertor):

    def __init__(self):
        IConvertor.__init__(self)

        self.ownMetrics = self.metricMappingUtils.get_own_metrics(["ts", "remainLife", "voc", "workVoc", "soc",
                                                                   "soh", "imbalance", "current", "minTemp", "maxTemp",
                                                                   "state"])

    def get_metric_value(self, item, metric):
        values = {
            "ts": item.ts,
            self.metricMappingUtils.get_own_metric("remainLife"): item.remainLife,
            self.metricMappingUtils.get_own_metric("voc"): item.voc,
            self.metricMappingUtils.get_own_metric("workVoc"): item.workVoc,
            self.metricMappingUtils.get_own_metric("soc"): item.soc,
            self.metricMappingUtils.get_own_metric("soh"): item.soh,
            self.metricMappingUtils.get_own_metric("imbalance"): item.imbalance,
            self.metricMappingUtils.get_own_metric("current"): item.current,
            self.metricMappingUtils.get_own_metric("minTemp"): item.minTemp,
            self.metricMappingUtils.get_own_metric("maxTemp"): item.maxTemp,
            self.metricMappingUtils.get_own_metric("state"): item.state
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
