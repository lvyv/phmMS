import json

import constants
from models.dao_cellpack import CellPackCRUD
from services.convert.cluster_display_util import ClusterDisplayUtil
from services.convert.convertor_factory import ConvertorFactory
from services.main import AppService
from models.dao_cluster_display import ClusterCRUD
from models.dao_reqhistory import RequestHistoryCRUD
from utils.payload_util import PayloadUtil
from utils.service_result import ServiceResult


class ClusterDisplayService(AppService):

    def create_item(self, pi) -> ServiceResult:
        item = ClusterCRUD(self.db).create_record(pi)
        return ServiceResult(item)

    def clusterDisplay(self, clz, code, metrics, displayType, payload) -> ServiceResult:

        start = PayloadUtil.get_start_time(payload)
        end = PayloadUtil.get_end_time(payload)

        devs = code.split(",")
        devs.sort()
        tags = metrics.split(",")
        tags.sort()

        hisRecordId = []
        hisRecords = RequestHistoryCRUD(self.db).get_records(json.dumps(devs, ensure_ascii=False),
                                                             json.dumps(tags, ensure_ascii=False),
                                                             displayType, start, end)
        for his in hisRecords:
            hisRecordId.append(his.id)

        if displayType == ClusterDisplayUtil.DISPLAY_SCATTER:
            if len(hisRecordId) == 0:
                items = None
            else:
                items = CellPackCRUD(self.db).get_records_latest_by_reqIds(devs, hisRecordId)
        elif displayType == ClusterDisplayUtil.DISPLAY_POLYLINE:
            if len(hisRecordId) == 0:
                items = None
            else:
                items = CellPackCRUD(self.db).get_records_by_reqIds(hisRecordId)
        elif displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                             ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            if len(hisRecordId) == 0:
                items = None
            else:
                items = ClusterCRUD(self.db).get_records(hisRecordId)
        else:
            items = None

        if items is None:
            return ServiceResult(None)
        convertor = ConvertorFactory.get_convertor(clz)
        if convertor is None:
            return ServiceResult(None)
        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            # 2D 3D AGG2D AGG3D
            convertItems = convertor.convertClusterDisplay(displayType, items)
        elif displayType in [ClusterDisplayUtil.DISPLAY_SCATTER]:
            convertItems = convertor.convertClusterDisplayScatter(items, code, metrics)
        elif displayType in [ClusterDisplayUtil.DISPLAY_POLYLINE]:
            convertItems = convertor.convertClusterDisplayPolyline(items, code, metrics)
        else:
            return ServiceResult(None)
        return ServiceResult(convertItems)
