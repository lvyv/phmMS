from utils.payload_util import PayloadUtil


class SelfRelationUtil:
    DISPLAY_SELF_RELATION = "SELF_RELATION"
    DISPLAY_SELF_RELATION_POLYLINE = "SELF_POLYLINE"

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

    @staticmethod
    def getTagInfoByPayload(payload):
        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)
        return start, end

    @staticmethod
    def getStepUintByTagAndPayload(start, end, payload):
        _start, _end = SelfRelationUtil.getTagInfoByPayload(payload)
        if start >= _start and end <= _end:
            return 0, 0
        return 0, 0
