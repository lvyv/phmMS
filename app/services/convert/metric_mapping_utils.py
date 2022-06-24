import threading

import database
from services.metricMappingService import MetricMappingService


class MetricMappingUtils:
    _instance_lock = threading.Lock()
    init_first = False

    def __init__(self, clz):
        if MetricMappingUtils.init_first is False:
            MetricMappingUtils.init_first = True
            db = database.SessionLocal()
            so = MetricMappingService(db)
            self.items = so.get_all_mapping(clz)
        # db = database.SessionLocal()
        # so = MetricMappingService(db)
        # self.items = so.get_all_mapping(clz)

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with MetricMappingUtils._instance_lock:
                if not hasattr(cls, '_instance'):
                    MetricMappingUtils._instance = super().__new__(cls)
        return MetricMappingUtils._instance

    def get_own_metrics(self, metrics):
        ret = []
        for metric in metrics:
            if metric in ["ts"]:
                ret.append("ts")
            else:
                if metric in self.items.keys():
                    ret.append(self.items[metric])
                else:
                    ret.append(metric)
        return ret

    def get_own_metric(self, metric):
        if metric in ["ts"]:
            return "ts"
        if metric in self.items.keys():
            return self.items[metric]
        else:
            return metric
