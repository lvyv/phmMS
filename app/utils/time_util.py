import time
import calendar


class TimeUtil:

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13T22:09:59.457Z
        timeStamp = calendar.timegm(
            time.strptime(timeStr, '%Y-%m-%dT%H:%M:%S.%fZ'))
        return timeStamp * 1000

    @staticmethod
    def convert_time_utc_str(timeStamp):
        # 将linux时间转化为 2022-02-13T22:09:59.000Z
        time_tuple = time.localtime(int(timeStamp / 1000) - 8 * 3600)
        timeStr = time.strftime("%Y-%m-%dT%H:%M:%S.000Z", time_tuple)
        return timeStr
