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

        self.ownMetrics = self.metricMappingUtils.get_own_metrics(["ts",
                                                                   "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9",
                                                                   "M10", "M11", "M12", "M13", "M14", "M15", "M16",
                                                                   "M17", "M18", "M19", "M20", "M21", "M22", "M23",
                                                                   "M24", "M25", "M26", "M27", "M28", "M29", "M30",
                                                                   "M31", "M32", "M33", "M34", "M35", "M36", "M37",
                                                                   "M38", "M39", "AM1", "AM2", "AM3", "AM4", "AM5",
                                                                   "FM1", "FM2", "FM3", "FM4", "FM5", "IM1"])

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
        if key in self.metricMappingUtils.get_own_metrics(["AM1", "AM2", "AM3", "AM4", "AM5"]):
            return True
        return False

    def get_metric_value(self, item, metric):
        values = {
            "ts": item.ts,
            self.metricMappingUtils.get_own_metric("M1"): item.M1,
            self.metricMappingUtils.get_own_metric("M2"): item.M2,
            self.metricMappingUtils.get_own_metric("M3"): item.M3,
            self.metricMappingUtils.get_own_metric("M4"): item.M4,
            self.metricMappingUtils.get_own_metric("M5"): item.M5,
            self.metricMappingUtils.get_own_metric("M6"): item.M6,
            self.metricMappingUtils.get_own_metric("M7"): item.M7,
            self.metricMappingUtils.get_own_metric("M8"): item.M8,
            self.metricMappingUtils.get_own_metric("M9"): item.M9,
            self.metricMappingUtils.get_own_metric("M10"): item.M10,
            self.metricMappingUtils.get_own_metric("M11"): item.M11,
            self.metricMappingUtils.get_own_metric("M12"): item.M12,
            self.metricMappingUtils.get_own_metric("M13"): item.M13,
            self.metricMappingUtils.get_own_metric("M14"): item.M14,
            self.metricMappingUtils.get_own_metric("M15"): item.M15,
            self.metricMappingUtils.get_own_metric("M16"): item.M16,
            self.metricMappingUtils.get_own_metric("M17"): item.M17,
            self.metricMappingUtils.get_own_metric("M18"): item.M18,
            self.metricMappingUtils.get_own_metric("M19"): item.M19,
            self.metricMappingUtils.get_own_metric("M20"): item.M20,
            self.metricMappingUtils.get_own_metric("M21"): item.M21,
            self.metricMappingUtils.get_own_metric("M22"): item.M22,
            self.metricMappingUtils.get_own_metric("M23"): item.M23,
            self.metricMappingUtils.get_own_metric("M24"): item.M24,
            self.metricMappingUtils.get_own_metric("M25"): item.M25,
            self.metricMappingUtils.get_own_metric("M26"): item.M26,
            self.metricMappingUtils.get_own_metric("M27"): item.M27,
            self.metricMappingUtils.get_own_metric("M28"): item.M28,
            self.metricMappingUtils.get_own_metric("M29"): item.M29,
            self.metricMappingUtils.get_own_metric("M30"): item.M30,
            self.metricMappingUtils.get_own_metric("M31"): item.M31,
            self.metricMappingUtils.get_own_metric("M32"): item.M32,
            self.metricMappingUtils.get_own_metric("M33"): item.M33,
            self.metricMappingUtils.get_own_metric("M34"): item.M34,
            self.metricMappingUtils.get_own_metric("M35"): item.M35,
            self.metricMappingUtils.get_own_metric("M36"): item.M36,
            self.metricMappingUtils.get_own_metric("M37"): item.M37,
            self.metricMappingUtils.get_own_metric("M38"): item.M38,
            self.metricMappingUtils.get_own_metric("M39"): item.M39,
            self.metricMappingUtils.get_own_metric("IM1"): item.IM1,
            self.metricMappingUtils.get_own_metric("AM1"): item.AM1,
            self.metricMappingUtils.get_own_metric("AM2"): item.AM2,
            self.metricMappingUtils.get_own_metric("AM3"): item.AM3,
            self.metricMappingUtils.get_own_metric("AM4"): item.AM4,
            self.metricMappingUtils.get_own_metric("AM5"): item.AM5,
            self.metricMappingUtils.get_own_metric("FM1"): item.FM1,
            self.metricMappingUtils.get_own_metric("FM2"): item.FM2,
            self.metricMappingUtils.get_own_metric("FM3"): item.FM3,
            self.metricMappingUtils.get_own_metric("FM4"): item.FM4,
            self.metricMappingUtils.get_own_metric("FM5"): item.FM5
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
