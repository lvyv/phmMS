from fastapi import APIRouter


router = APIRouter(
    prefix="/api/v1/mock",
    tags=["数据资源模拟数据"],
    responses={404: {"description": "Not found"}},
)


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
async def getZbData(equipCode, metricName, startTime, endTime, interval):
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
