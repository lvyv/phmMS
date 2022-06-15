import logging
from datetime import datetime
from phmconfig import constants


class TimeGrapUtil:
    last_time = 0

    def canClick(self):
        now_time = int(datetime.now().timestamp())
        if self.last_time == 0 or now_time - self.last_time > constants.CLICK_GRAP:
            self.last_time = now_time
            logging.info("time grap is arrived, can click...")
            return True
        return False
