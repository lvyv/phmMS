from datetime import datetime

from services.http.dataCenterService import DataCenterService
from services.metricMappingService import MetricMappingService
import logging


class SjzyManager:
    LastTime = 0

    # 根据装备名称，同步测点数据
    def dataSync(self, equipCode, db):
        # 每隔一小时，同步测点
        now_time = int(datetime.now().timestamp())
        if self.LastTime == 0 or now_time - self.LastTime > 3600:
            self.LastTime = now_time
            logging.info("sync equip metric ...")
        else:
            return None
        # 取一个设备编码
        dev = equipCode.split(",")[0]
        # 通过装备下载测点信息
        data = DataCenterService.download_zb_metric(equipCode=dev)
        if data is None:
            return None
        # 获取装备类型编码
        equipTypeCode = data[0]["equipTypeCode"]
        # 通过测点
        so = MetricMappingService(db)
        metrics = DataCenterService.download_zb_metric(equipTypeCode)
        # 同步电池测点映射数据
        so.update_all_mapping(equipTypeCode, metrics)
