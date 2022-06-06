from random import random

from fastapi import APIRouter
from typing import Optional
from phmconfig.timeUtils import TimeUtils

router = APIRouter(
    prefix="/api/v1/mock",
    tags=["数据资源模拟数据"],
    responses={404: {"description": "Not found"}},
)


@router.post("/zbMetric")
async def getZbMetric(equipTypeCode: Optional[str] = None, equipCode: Optional[str] = None,
                      equipName: Optional[str] = None):
    ret = {
        "result": [{
            "equipCode": "B001", "equipName": "电池1", "equipTypeCode": "N0001",
            "measurePoints": [{"pointCode": "M0001", "pointName": "容量", "pointUnit": "%"},
                              {"pointCode": "M0002", "pointName": "健康指标"},
                              {"pointCode": "M0003", "pointName": "最大温度"},
                              {"pointCode": "M0004", "pointName": "电池单元的最大开路电压"},
                              {"pointCode": "M0005", "pointName": "电池单元的最小开路电压"},
                              {"pointCode": "M0006", "pointName": "电池单元的最大端电压"},
                              {"pointCode": "M0007", "pointName": "电池单元的最小端电压"},
                              {"pointCode": "M0008", "pointName": "电池单元的均值端电压"},
                              {"pointCode": "M0009", "pointName": "电池组的环境温度（存在多个测点）"},
                              {"pointCode": "M0010", "pointName": "电池单元端电压集合"},
                              {"pointCode": "M0011", "pointName": "电池单元容量集合"},
                              {"pointCode": "M0012", "pointName": "健康状态"},
                              {"pointCode": "M0013", "pointName": "电压不平衡度"},
                              {"pointCode": "M0038", "pointName": "abc", "pointUnit": "%"},
                              {"pointCode": "M0014", "pointName": "未知"}]
        },
            {
                "equipCode": "B002", "equipName": "电池2", "equipTypeCode": "N0001",
                "measurePoints": [{"pointCode": "M0015", "pointName": "容量", "pointUnit": "%"},
                                  {"pointCode": "M0016", "pointName": "健康指标"},
                                  {"pointCode": "M0017", "pointName": "剩余寿命"},
                                  {"pointCode": "M0018", "pointName": "开路电压"},
                                  {"pointCode": "M0019", "pointName": "端电压"},
                                  {"pointCode": "M0020", "pointName": "内阻不平衡度"},
                                  {"pointCode": "M0021", "pointName": "冲放电电流"},
                                  {"pointCode": "M0022", "pointName": "最小温度"},
                                  {"pointCode": "M0023", "pointName": "最大温度"},
                                  {"pointCode": "M0024", "pointName": "电池单元的最大开路电压"},
                                  {"pointCode": "M0025", "pointName": "电压不平衡度"},
                                  {"pointCode": "M0026", "pointName": "未知"}]
            }
        ]
    }
    return ret


@router.post("/zbData")
async def getZbData(equipCode, metricName, startTime, endTime, interval: Optional[str] = None):
    # 根据开始数据 与 结束时间生成 时间序列
    skipK = 10
    maxPoints = int(1000 / skipK)
    if interval.endswith("M"):
        if interval.find(".") > 0:
            # 秒
            step = float(interval.replace("M", ""))
            interval = int(step * 60) * skipK
            pass
        else:
            # 分
            step = int(interval.replace("M", ""))
            interval = step * 60 * skipK
            pass
    elif interval.endswith("H"):
        step = int(interval.replace("H", ""))
        interval = step * 3600 * skipK
        pass
    elif interval.endswith("D"):
        step = int(interval.replace("D", ""))
        interval = step * 24 * 3600 * skipK
        pass

    genTime = []
    start = TimeUtils.convert_time_stamp(startTime)
    end = TimeUtils.convert_time_stamp(endTime)

    for inc in range(maxPoints):
        genTime.append(TimeUtils.convert_time_str(start + inc * interval * 1000))

    # 生成模拟数据
    ret = {
        "code": "success",
        "result": []
    }
    # 通过传入的设备编码
    devs = equipCode.split(",")
    tags = metricName.split(",")
    tagNumber = 1
    for dev in devs:
        genDev = {
            "equipCode": dev,
            "equipName": "电池" + dev,
            "equipData": []
        }
        for tag in tags:
            genTag = {
                "metricName": tag,
                "metricCode": "M00" + str(tagNumber),
                "metricData": []
            }

            for inx in range(maxPoints):
                genTag["metricData"].append({
                    "timestamp": genTime[inx],
                    "metricValue": int(random() * 100)
                })

            genDev["equipData"].append(genTag)

            tagNumber = tagNumber + 1
        ret["result"].append(genDev)

    return ret
