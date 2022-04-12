class SelfRelationUtil:
    DISPLAY_SELF_RELATION = "SELF_RELATION"

    @staticmethod
    def get_use_metrics(displayType):
        values = {
            "SELF_RELATION": ["lag", "value"]
        }
        return values.get(displayType, None)

    @staticmethod
    def get_metric_value(item, metric):
        values = {
            "lag": item.lag,
            "value": item.value,
        }
        return values.get(metric, None)

    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        return "number"
