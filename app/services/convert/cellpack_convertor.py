import json
# import threading

from services.convert.convertor import IConvertor
from services.convert.metric_mapping_utils import MetricMappingUtils


class CellPackConvertor(IConvertor):
    # _instance_lock = threading.Lock()
    # init_first = False

    def __init__(self):
        IConvertor.__init__(self)
        # if CellPackConvertor.init_first is False:
        #     CellPackConvertor.init_first = True
        self.metricMappingUtils = MetricMappingUtils("battery")
        self.ownMetrics = self.metricMappingUtils.get_own_metrics(["ts", "remainLife", "voc", "workVoc", "soc",
                                                                   "soh", "imbalance", "current", "minTemp",
                                                                   "maxTemp",
                                                                   "cellMaxVoc", "cellMinVoc", "cellMaxVol",
                                                                   "cellMinVol", "cellAvgVol",
                                                                   "envTemp", "cellVol", "cellSoc", "state"])

    # def __new__(cls, *args, **kwargs):
    #     if not hasattr(cls, '_instance'):
    #         with CellPackConvertor._instance_lock:
    #             if not hasattr(CellPackConvertor, '_instance'):
    #                 CellPackConvertor._instance = super().__new__(cls)
    #     return CellPackConvertor._instance

    @staticmethod
    def __parse_str_to_json(value):
        load_dict = None
        try:
            load_dict = json.loads(value)
        finally:
            return load_dict

    def __has_special_key(self, key):
        if key in self.metricMappingUtils.get_own_metrics(["envTemp", "cellVol", "cellSoc"]):
            return True
        return False

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
            self.metricMappingUtils.get_own_metric("cellMaxVoc"): item.cellMaxVoc,
            self.metricMappingUtils.get_own_metric("cellMinVoc"): item.cellMaxVoc,
            self.metricMappingUtils.get_own_metric("cellMaxVol"): item.cellMaxVol,
            self.metricMappingUtils.get_own_metric("cellMinVol"): item.cellMinVol,
            self.metricMappingUtils.get_own_metric("cellAvgVol"): item.cellAvgVol,
            self.metricMappingUtils.get_own_metric("envTemp"): item.envTemp,
            self.metricMappingUtils.get_own_metric("cellVol"): item.cellVol,
            self.metricMappingUtils.get_own_metric("cellSoc"): item.cellSoc,
            self.metricMappingUtils.get_own_metric("state"): item.state
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
