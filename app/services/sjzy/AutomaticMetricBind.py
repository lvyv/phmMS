import json
import logging


class AutomaticMetricBind:
    ownMetrics = ["M1", "M2", "M3", "M4", "M5", "M6", "M7", "M8", "M9", "M10",
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
