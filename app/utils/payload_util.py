from utils.time_util import TimeUtil


class PayloadUtil:

    @staticmethod
    def check_relative_time_valid(payload):
        try:
            start = payload["rangeRaw"]["from"]
            end = payload["rangeRaw"]["to"]
            if "now" in start or "now" in end:
                return False
        except Exception as e:
            # print(e)
            return True


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
