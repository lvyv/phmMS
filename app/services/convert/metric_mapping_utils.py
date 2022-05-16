import threading

import database
from services.metricMappingService import MetricMappingService


class MetricMappingUtils:
    _instance_lock = threading.Lock()
    init_first = False

    def __init__(self):
        if MetricMappingUtils.init_first is False:
            MetricMappingUtils.init_first = True
            db = database.SessionLocal()
            so = MetricMappingService(db)
            self.items = so.get_all_mapping("电池")

    def __new__(cls, *args, **kwargs):
        if not hasattr(cls, '_instance'):
            with MetricMappingUtils._instance_lock:
                if not hasattr(cls, '_instance'):
                    MetricMappingUtils._instance = super().__new__(cls)
        return MetricMappingUtils._instance

    def get_own_metrics(self, metrics):
        ret = []
        for metric in metrics:
            if metric is ["ts"]:
                ret.append("ts")
            else:
                ret.append(self.items[metric])
        return ret

    def get_own_metric(self, metric):
        return self.items[metric]
