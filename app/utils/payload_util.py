from utils.time_util import TimeUtil


class PayloadUtil:
    @staticmethod
    def get_start_time(payload):
        start = TimeUtil.convert_time_stamp(payload["range"]["from"])
        return start

    @staticmethod
    def get_end_time(payload):
        end = TimeUtil.convert_time_stamp(payload["range"]["to"])
        return end

    @staticmethod
    def get_interval_ms(payload):
        return payload["intervalMs"]

    @staticmethod
    def get_limit(payload):
        return payload["maxDataPoints"]

    @staticmethod
    def get_time_zone(payload):
        return payload["timezone"]
