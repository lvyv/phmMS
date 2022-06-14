import json
import time

from services.convert.cluster_display_util import ClusterDisplayUtil


class DataConvertUtil:
    @staticmethod
    def SOH(reqid, item):
        keys = item.keys()
        eqi = {
            "did": item['did'] if 'did' in keys else "unknown",
            "dclz": "battery",
            "reqId": reqid,
            "remainLife": item['remainLife'] if "remainLife" in keys else 0,
            "voc": item['voc'] if "voc" in keys else 0,
            "workVoc": item['workVoc'] if "workVoc" in keys else 0,
            "current": item['current'] if "current" in keys else 0,
            "minTemp": item['minTemp'] if "minTemp" in keys else 0,
            "maxTemp": item['maxTemp'] if "maxTemp" in keys else 0,
            "cellMaxVoc": item['cellMaxVoc'] if "cellMaxVoc" in keys else 0,
            "cellMinVoc": item['cellMinVoc'] if "cellMinVoc" in keys else 0,
            "cellMaxVol": item['cellMaxVol'] if "cellMaxVol" in keys else 0,
            "cellMinVol": item['cellMinVol'] if "cellMinVol" in keys else 0,
            "cellAvgVol": item['cellAvgVol'] if "cellAvgVol" in keys else 0,
            "envTemp": json.dumps([item['envTemp']]) if "envTemp" in keys else "[0, 0]",
            "cellVol": json.dumps([item['cellVol']]) if "cellVol" in keys else "[0, 0, 0, 0, 0, 0]",
            "cellSoc": json.dumps([item['cellSoc']]) if "cellSoc" in keys else "[0, 0, 0, 0, 0, 0]",
            "soh": item['soh'] if "soh" in keys else 0,
            "soc": item['soc'] if 'soc' in keys else 0,
            "imbalance": item['imbalance'] if 'imbalance' in keys else 0,
            "ts": item['ts'] if 'ts' in keys else 0,
            "state": item['state'] if 'state' in keys else 0,
            "M1": item['M1'] if 'M1' in keys else 0,
            "M2": item['M2'] if 'M2' in keys else 0,
            "M3": item['M3'] if 'M3' in keys else 0,
            "M4": item['M4'] if 'M4' in keys else 0,
            "M5": item['M5'] if 'M5' in keys else 0,
            "M6": item['M6'] if 'M6' in keys else 0,
            "M7": item['M7'] if 'M7' in keys else 0,
            "M8": item['M8'] if 'M8' in keys else 0
        }
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


