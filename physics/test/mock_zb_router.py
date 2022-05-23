from fastapi import APIRouter
from typing import Optional

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
            "measurePoints": [{"pointCode": "M0001", "pointName": "容量"},
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
                              {"pointCode": "M0014", "pointName": "未知"}]
        },
            {
                "equipCode": "B002", "equipName": "电池2", "equipTypeCode": "N0001",
                "measurePoints": [{"pointCode": "M0015", "pointName": "容量"},
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
    ret = {
        "code": "success",
        "result": [{
            "equipCode": "B001",
            "equipName": "电池A",
            "equipData": [{
                "metricName": "容量",
                "metricCode": "M001",
                "metricData": [{
                    "timestamp": "2022-05-18 00:00:00",
                    "metricValue": 0.5
                },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    },
                    {
                        "timestamp": "2022-05-18 01:00:00",
                        "metricValue": 0.6
                    },
                    {
                        "timestamp": "2022-05-18 02:00:00",
                        "metricValue": 0.7
                    }
                ]
            },
                {
                    "metricName": "健康指标",
                    "metricCode": "M002",
                    "metricData": [{
                        "timestamp": "2022-05-18 00:00:00",
                        "metricValue": 0.5
                    },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        }
                    ]
                }
            ]
        },
            {
                "equipCode": "B002",
                "equipName": "电池B",
                "equipData": [{
                    "metricName": "容量",
                    "metricCode": "M003",
                    "metricData": [{
                        "timestamp": "2022-05-18 00:00:00",
                        "metricValue": 0.5
                    },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        },
                        {
                            "timestamp": "2022-05-18 01:00:00",
                            "metricValue": 0.6
                        },
                        {
                            "timestamp": "2022-05-18 02:00:00",
                            "metricValue": 0.7
                        }
                    ]
                },
                    {
                        "metricName": "健康指标",
                        "metricCode": "M004",
                        "metricData": [{
                            "timestamp": "2022-05-18 00:00:00",
                            "metricValue": 0.5
                        },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            },
                            {
                                "timestamp": "2022-05-18 01:00:00",
                                "metricValue": 0.6
                            },
                            {
                                "timestamp": "2022-05-18 02:00:00",
                                "metricValue": 0.7
                            }
                        ]
                    }
                ]
            }
        ]
    }
    return ret
