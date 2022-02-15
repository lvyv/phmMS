class IConvertor:
    def __init__(self):
        self.tmpDict = {}

    def get_metric_value(self, item, metric):
        pass

    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        return "number"

    def get_own_metrics(self):
        pass

    def check_metric_valid(self, metric):
        if metric in self.get_own_metrics():
            return True
        return False

    def get_right_metrics(self, metrics):
        retMetrics = []
        for metric in metrics:
            if metric in self.get_own_metrics():
                retMetrics.append(metric)
        return retMetrics

    def convert(self, items, metrics):
        useMetrics = metrics.split(",")
        useMetrics = self.get_right_metrics(useMetrics)
        useMetrics.insert(0, "ts")
        print(useMetrics)
        self.tmpDict.clear()
        for item in items:
            for m in useMetrics:
                # if self.check_metric_valid(m) is True:
                if m in self.tmpDict.keys():
                    self.tmpDict[m].append(self.get_metric_value(item, m))
                else:
                    self.tmpDict[m] = [self.get_metric_value(item, m)]
