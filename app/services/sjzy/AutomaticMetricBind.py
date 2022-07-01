import json
import logging


class AutomaticMetricBind:
    ownMetrics = ["M01", "M02", "M03", "M04", "M05", "M06", "M07", "M08", "M09", "M10",
                  "M11", "M12", "M13", "M14", "M15", "M16", "M17", "M18", "M19", "M20",
                  "M21", "M22", "M23", "M24", "M25", "M26", "M27", "M28", "M29", "M30",
                  "M31", "M32", "M33", "M34", "M35", "M36", "M37", "M38", "M39"]

    # in : [{"equipTypeCode": equipTypeCode, "metricName": name, "metricUnit": unit}]
    # out: [{"equipTypeCode": equipTypeCode, "metricName": name, "metricUnit": unit, "metricAlias": alias}]
    @staticmethod
    def autoRun(metrics):
        i = 0
        for m in metrics:
            if i < len(AutomaticMetricBind.ownMetrics):
                m.update({"metricAlias": AutomaticMetricBind.ownMetrics[i]})
                i = i + 1
        logging.info("automatic bind ret : " + json.dumps(metrics, ensure_ascii=False))
        return metrics

    @staticmethod
    def autobind(outerMetrics, innerMetrics):
        usingMetrics = []
        # 查找所有的已使用的测点
        for own in innerMetrics:
            found = False
            usingMetrics.append(own.metric_alias)
            for m in outerMetrics:
                if own.metric_name == m["metricName"]:
                    found = True
                    m.update({"metricAlias": own.metric_alias})
            if found is False:
                # TODO 删除无用的测点, 删除测点后，导致历史数据错误，所以不删
                pass
        # 合并未使用的测点
        noUsingMetrics = sorted(list(set(AutomaticMetricBind.ownMetrics).difference(usingMetrics)))

        if noUsingMetrics is None or len(noUsingMetrics) == 0:
            return outerMetrics

        i = 0
        for m in outerMetrics:
            if "metricAlias" not in m.keys():
                if i < len(noUsingMetrics):
                    m.update({"metricAlias": noUsingMetrics[i]})
                    i = i + 1

        return outerMetrics
