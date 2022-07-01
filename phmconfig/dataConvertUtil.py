import json
import time

from services.convert.cluster_display_util import ClusterDisplayUtil


class DataConvertUtil:
    @staticmethod
    def SOH(reqid, item):
        keys = item.keys()

        eqi = {
            "did": item['did'] if 'did' in keys else "unknown",
            "dclz": "N/A",
            "reqId": reqid,
            "ts": item['ts'] if 'ts' in keys else 0,
        }
        for i in range(39):
            if i < 9:
                key = "M0" + str(i + 1)
            else:
                key = "M" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        for i in range(1):
            key = "IM" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        for i in range(5):
            key = "AM" + str(i + 1)
            eqi.update({key: json.dumps(item[key]) if key in keys else "[0]"})
        for i in range(5):
            key = "FM" + str(i + 1)
            eqi.update({key: item[key] if key in keys else 0})
        return eqi

    @staticmethod
    def cluster(reqid, displayType, did,  items):
        eqi = {
            "reqId": reqid,
            "ts": int(time.time() * 1000),
            "name": items[did][0],
            "size": 0,  # items[did][1],
            "color": items[did][2],
            "shape": 0,  # items[did][3],
            "x": items[did][4],
            "y": items[did][5],
            "z": 0  # items[did][6]
        }

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D]:
            eqi["size"] = items[did][1]

        if displayType in [ClusterDisplayUtil.DISPLAY_2D, ClusterDisplayUtil.DISPLAY_3D,
                           ClusterDisplayUtil.DISPLAY_AGG2D]:
            eqi["shape"] = items[did][3]

        if displayType in [ClusterDisplayUtil.DISPLAY_3D, ClusterDisplayUtil.DISPLAY_AGG3D]:
            eqi["z"] = items[did][6]

        return eqi


