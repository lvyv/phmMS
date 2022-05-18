from os import listdir
from os.path import isfile, join
from physics.test import utils

from fastapi import APIRouter, Depends
import json

router = APIRouter(
    prefix="/api/v1/mock",
    tags=["数据资源模拟数据"],
    responses={404: {"description": "Not found"}},
)


# {
# 	"dev1": {
# 		"ts": [1, 2, 3, 4],
# 		"metric1": [1, 2, 3, 5],
# 		"metric2": [2, 3, 4, 5]
# 	},
# 	"dev2": {
# 		"ts": [1, 2, 3, 4],
# 		"metric1": [1, 2, 3, 4],
# 		"metric2": [2, 3, 4, 5]
# 	}
# }
@router.post("/zbData2")
async def getZbData2(devs, metrics, start, end):
    dataS = {}
    # json.loads(devs)
    # json.loads(metrics)
    myPath = '../data/'
    files = [f for f in listdir(myPath) if isfile(join(myPath, f))]
    for index, item in enumerate(files):
        (c1, c2, c3, c4, c5, c6, c7, c8) = utils.load_dat(item, myPath)
        key = "dev" + f'{index}'
        dataS[key] = {
            "metric1": list(c1[0:1024]),
            "metric2": list(c2[0:1024]),
            "metric3": list(c3[0:1024]),
            "metric4": list(c4[0:1024]),
            # "metric5": list(c5[0:1024]),
            # "metric6": list(c6[0:1024]),
            # "metric7": list(c7[0:1024]),
            # "metric8": list(c8[0:1024])
        }
    return dataS


@router.post("/zbMetric")
async def getZbMetric(equipTypeCode):
    ret = {
        "result": {
            "equipCode": "B001",
            "equipName": "电池1",
            "equipTypeCode": "N0001",
            "measurePoints": [
                {
                    "pointCode": "M0001",
                    "pointName": "容量"
                },
                {
                    "pointCode": "M0002",
                    "pointName": "健康指标"
                },
                {
                    "pointCode": "M0003",
                    "pointName": "内阻"
                },
                {
                    "pointCode": "M0004",
                    "pointName": "电压"
                }
            ]
        }
    }
    return ret


@router.post("/zbData")
async def getZbData(metricName, startTime, endTime, interval):
    ret = {
        "code": "success",
        "result": [
            {
                "metric_name": "M0001",
                "metric_value": 0.5,
                "timestamp": 1601863976
            },
            {
                "metric_name": "M0002",
                "metric_value": 0.75,
                "timestamp": 1601863976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.85,
                "timestamp": 1601864976
            },
            {
                "metric_name": "M0002",
                "metric_value": 1.5,
                "timestamp": 1601864976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.5,
                "timestamp": 1601873976
            },
            {
                "metric_name": "M0002",
                "metric_value": 0.75,
                "timestamp": 1601873976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.85,
                "timestamp": 1601874976
            },
            {
                "metric_name": "M0002",
                "metric_value": 1.5,
                "timestamp": 1601874976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.52,
                "timestamp": 1601883976
            },
            {
                "metric_name": "M0002",
                "metric_value": 0.85,
                "timestamp": 1601883976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.95,
                "timestamp": 1601884976
            },
            {
                "metric_name": "M0002",
                "metric_value": 1.25,
                "timestamp": 1601884976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.75,
                "timestamp": 1601893976
            },
            {
                "metric_name": "M0002",
                "metric_value": 0.75,
                "timestamp": 1601893976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.85,
                "timestamp": 1601894976
            },
            {
                "metric_name": "M0001",
                "metric_value": 2.5,
                "timestamp": 1601894976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.5,
                "timestamp": 1601903976
            },
            {
                "metric_name": "M0002",
                "metric_value": 0.75,
                "timestamp": 1601903976
            },
            {
                "metric_name": "M0001",
                "metric_value": 0.85,
                "timestamp": 1601904976
            },
            {
                "metric_name": "M0002",
                "metric_value": 1.5,
                "timestamp": 1601904976
            }
        ]
    }
    return ret
