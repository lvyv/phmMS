import json
import logging


class AutomaticMetricBind:
    ownMetrics = ["remainLife", "voc", "workVoc", "soc",
                  "soh", "imbalance", "current", "minTemp",
                  "maxTemp",
                  "cellMaxVoc", "cellMinVoc", "cellMaxVol",
                  "cellMinVol", "cellAvgVol",
                  "envTemp", "cellVol", "cellSoc", "state",
                  "M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8"]

    # in : [{"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode,
    #                                          "metricCode": code, "metricName": name, "metricUnit": unit}]
    # out: [{"equipCode": equipCode, "equipName": equipName, "equipTypeCode": equipTypeCode,
    #       "metricCode": code, "metricName": name, "metricUnit": unit, "metricAlias": alias}]
    @staticmethod
    def autoRun(metrics):
        tmp = {}
        i = 0
        for m in metrics:
            if m["equipCode"] in tmp.keys():
                found = False
                for kkk in tmp.keys():
                    for jjj in tmp[kkk]:
                        if m["metricName"] == jjj["metricName"]:
                            found = True
                            m.update({"metricAlias": jjj["metricAlias"]})

                if found is False:
                    if i < len(AutomaticMetricBind.ownMetrics):
                        m.update({"metricAlias": AutomaticMetricBind.ownMetrics[i]})
                        i = i + 1
                tmp[m["equipCode"]].append(m)
            else:
                found = False
                for kkk in tmp.keys():
                    for jjj in tmp[kkk]:
                        if m["metricName"] == jjj["metricName"]:
                            found = True
                            m.update({"metricAlias": jjj["metricAlias"]})
                if found is False:
                    if i < len(AutomaticMetricBind.ownMetrics):
                        m.update({"metricAlias": AutomaticMetricBind.ownMetrics[i]})
                        i = i + 1
                tmp[m["equipCode"]] = [m]
        logging.info("automatic bind ret : " + json.dumps(metrics, ensure_ascii=False))
        return metrics
