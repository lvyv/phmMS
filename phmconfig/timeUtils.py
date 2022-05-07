import time


class TimeUtils:
    @staticmethod
    def convert_time_str(timestamp):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        print("北京时间:", bj_time)
        return bj_time

    @staticmethod
    def get_time_interval(start, end):
        diff = int(end / 1000 - start / 1000)
        maxPoints = 1000
        interval = int(diff / maxPoints)
        if interval > 24 * 60 * 60:
            gap = int(interval / (24 * 60 * 60))
            gap = str(gap) + "D"
        elif interval > 60 * 60:
            gap = int(interval / (60 * 60))
            gap = str(gap) + "H"
        elif interval > 60:
            gap = int(interval / 60)
            gap = str(gap) + "M"
        else:
            gap = str(0.1) + "M"
        return gap
