from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.self_relation_util import SelfRelationUtil


class IConvertor:
    def __init__(self):
        self.tmpDict = {}

    # 获取测点值
    def get_metric_value(self, item, metric):
        pass

    # 获取测点数据类型
    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        return "number"

    def get_own_metrics(self):
        pass

    # 判断测点是否合法
    def check_metric_valid(self, metric):
        if metric in self.get_own_metrics():
            return True
        return False

    # 获取正确的测点
    def get_right_metrics(self, metrics):
        retMetrics = []
        for metric in metrics:
            if metric in self.get_own_metrics():
                retMetrics.append(metric)
        return retMetrics

    # 进行数据转化
    def convert(self, items, metrics):
        useMetrics = metrics.split(",")
        useMetrics = self.get_right_metrics(useMetrics)
        useMetrics.insert(0, "ts")
        # print(useMetrics)
        self.tmpDict.clear()
        for item in items:
            for m in useMetrics:
                # if self.check_metric_valid(m) is True:
                if m in self.tmpDict.keys():
                    self.tmpDict[m].append(self.get_metric_value(item, m))
                else:
                    self.tmpDict[m] = [self.get_metric_value(item, m)]

    # 将数据转化为健康指标数据协议格式
    @staticmethod
    def convertHealthIndicator(items):
        rets = []
        tmpDict = {}
        for item in items:
            for i in item:
                if i.did in tmpDict.keys():
                    tmpDict[i.did]["soh"].append(i.FM1)
                else:
                    ret = {
                        "state": i.IM1,
                        "soh": [i.FM1],
                        "equipCode": i.did
                    }
                    tmpDict[i.did] = ret
        for m in tmpDict.keys():
            rets.append(tmpDict[m])
        return rets

    @staticmethod
    def convertClusterDisplay(displayType, items):
        rets = []
        tmpDict = {}
        useMetrics = ClusterDisplayUtil.get_use_metrics(displayType)
        for item in items:
            for m in useMetrics:
                if m in tmpDict.keys():
                    tmpDict[m].append(ClusterDisplayUtil.get_metric_value(item, m))
                else:
                    tmpDict[m] = [ClusterDisplayUtil.get_metric_value(item, m)]
        for key in tmpDict.keys():
            rets.append({"name": key, "type": ClusterDisplayUtil.get_metric_type(key), "values": tmpDict[key]})
        return rets

    def convertClusterDisplayPolyline(self, items, codes, metrics):
        devs = codes.split(",")
        tags = metrics.split(",")
        # TODO fix 含特殊测点
        userMetrics = ClusterDisplayUtil.get_use_metrics(ClusterDisplayUtil.DISPLAY_POLYLINE)
        for dev in devs:
            for tag in tags:
                userMetrics.append(dev + "^" + tag)
        rets = []
        tmpDict = {}
        # TODO fix 时间选择
        initTs = False
        ownTs = False
        for dev in devs:
            for item in items:
                if item.did == dev:
                    for m in userMetrics:
                        mtr = m.split("^")
                        if len(mtr) == 2:
                            if mtr[0] == dev:
                                if m in tmpDict.keys():
                                    tmpDict[m].append(self.get_metric_value(item, mtr[1]))
                                else:
                                    tmpDict[m] = [self.get_metric_value(item, mtr[1])]
                        else:
                            if initTs is False:
                                ownTs = True
                                if m in tmpDict.keys():
                                    tmpDict[m].append(self.get_metric_value(item, m))
                                else:
                                    tmpDict[m] = [self.get_metric_value(item, m)]
            if ownTs is True:
                initTs = True
        for key in tmpDict.keys():
            rets.append({"name": key, "type": ClusterDisplayUtil.get_metric_type(key), "values": tmpDict[key]})
        return rets

    # TODO 散点图支持一个测点
    def convertClusterDisplayScatter(self, items, codes, metrics):
        devs = codes.split(",")
        tags = metrics.split(",")
        userMetrics = ClusterDisplayUtil.get_use_metrics(ClusterDisplayUtil.DISPLAY_SCATTER)
        # userMetrics.append(tags[0])
        for tag in tags:
            userMetrics.append(tag)
        rets = []
        tmpDict = {}
        for item in items:
            for m in userMetrics:
                if m in tmpDict.keys():
                    if m == "did":
                        tmpDict[m].append(item.did)
                    else:
                        tmpDict[m].append(self.get_metric_value(item, m))
                else:
                    if m == "did":
                        tmpDict[m] = [item.did]
                    else:
                        tmpDict[m] = [self.get_metric_value(item, m)]
        for key in tmpDict.keys():
            rets.append({"name": key, "type": ClusterDisplayUtil.get_metric_type(key), "values": tmpDict[key]})
        return rets

    @staticmethod
    def convertSelfRelation(items):
        rets = []
        tmpDict = {}
        useMetrics = SelfRelationUtil.get_use_metrics(SelfRelationUtil.DISPLAY_SELF_RELATION)
        for item in items:
            for m in useMetrics:
                if m in tmpDict.keys():
                    tmpDict[m].append(SelfRelationUtil.get_metric_value(item, m))
                else:
                    tmpDict[m] = [SelfRelationUtil.get_metric_value(item, m)]
        for key in tmpDict.keys():
            rets.append({"name": key, "type": SelfRelationUtil.get_metric_type(key), "values": tmpDict[key]})
        return rets

    @staticmethod
    def convertSelfRelationMulti(items):
        rets = []
        tmpDict = {}
        useMetrics = SelfRelationUtil.get_use_metrics(SelfRelationUtil.DISPLAY_SELF_RELATION)
        for item in items:
            for m in useMetrics:
                key = item.own_key + "^" + m
                if key in tmpDict.keys():
                    tmpDict[key].append(SelfRelationUtil.get_metric_value(item, m))
                else:
                    tmpDict[key] = [SelfRelationUtil.get_metric_value(item, m)]
        for key in tmpDict.keys():
            rets.append({"name": key, "type": SelfRelationUtil.get_metric_type(key.split("^")[1]), "values": tmpDict[key]})
        return rets
