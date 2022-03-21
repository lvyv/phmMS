import json

from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.convertor_factory import ConvertorFactory
from services.main import AppService
from models.dao_cluster_display import Cluster2DCRUD
from models.dao_reqhistory import RequestHistoryCRUD
from utils.payload_util import PayloadUtil
from utils.service_result import ServiceResult


class ClusterDisplayService(AppService):
    def create_item_2D(self, pi) -> ServiceResult:
        item = Cluster2DCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def clusterDisplay(self, clz, code, metrics, displayType, payload) -> ServiceResult:

        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        if displayType == ClusterDisplayUtil.DISPLAY_SCATTER:
            # CellPackCRUD(self.db).get_records(code, start, end)
            pass
        elif displayType == ClusterDisplayUtil.DISPLAY_POLYLINE:
            pass
        elif displayType == ClusterDisplayUtil.DISPLAY_2D:
            devs = code.split(",")
            tags = metrics.split(",")
            hisRecord = RequestHistoryCRUD(self.db).get_record_by_condition(json.dumps(devs),
                                                                            json.dumps(tags), displayType)
            if hisRecord is None:
                pass
            else:
                items = Cluster2DCRUD(self.db).get_records(hisRecord.id, start, end)
        elif displayType == ClusterDisplayUtil.DISPLAY_3D:
            pass
        elif displayType == ClusterDisplayUtil.DISPLAY_AGG2D:
            pass
        elif displayType == ClusterDisplayUtil.DISPLAY_AGG3D:
            pass
        else:
            items = None
        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)

        # 2D 3D AGG2D AGG3D
        convertItems = convertor.convertClusterDisplay(displayType, items)
        return ServiceResult(convertItems)
