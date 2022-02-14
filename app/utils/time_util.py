import time
import calendar


class TimeUtil:

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13T22:09:59.457Z
        timeStamp = calendar.timegm(
            time.strptime(timeStr, '%Y-%m-%dT%H:%M:%S.%fZ'))
        return timeStamp * 1000
