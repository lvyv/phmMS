from datetime import datetime

from phmconfig import constants
from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
import logging


class SjzyManager:
    LastTime = 0

    # 根据装备名称，同步测点数据
    def dataSync(self,  equipTypeCode, equipType, db):

        # 每隔5分钟，同步测点
        now_time = int(datetime.now().timestamp())
        if self.LastTime == 0 or now_time - self.LastTime > constants.EQUIP_METRIC_SYNC_GAP:
            self.LastTime = now_time
            logging.info("sync equip metric ...")
        else:
            return None
        # 通过测点
        so = MetricMappingService(db)
        metrics = DataCenterService.download_zb_metric_by_type_code(equipTypeCode)
        # 同步电池测点映射数据
        so.update_all_mapping(equipTypeCode, metrics, equipType)
