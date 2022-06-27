import database
from services.metricMappingService import MetricMappingService


class MetricMappingUtils:

    def __init__(self, clz):
        db = database.SessionLocal()
        so = MetricMappingService(db)
        self.items = so.get_all_mapping(clz)

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
