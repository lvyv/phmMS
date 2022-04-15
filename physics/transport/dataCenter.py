import httpx
from phmconfig import basiccfg


# 从数据资源下载下载装备数据
def download_zb_data(devs, metrics, start, end):
    with httpx.Client(timeout=None, verify=False) as client:
        r = client.post(basiccfg.URL_GET_ZB_DATA, params={"devs": devs, "metrics": metrics, "start": start, "end": end})
        dataS = r.json()
        return dataS
    return None
