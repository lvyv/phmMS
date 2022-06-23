"""
=========================
entrypoint of the app
=========================

模型微服务入口.
"""
import threading
import time

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from pydantic import BaseModel

from phmconfig.dataConvertUtil import DataConvertUtil
from phmconfig import constants as bcf
import concurrent.futures
import httpx
import json
import logging
from physics.transport.mqttclient import MqttClient
from fastapi.staticfiles import StaticFiles
from physics.test import mock_zb_router
from physics.vrla import phm
from physics.transport import dataCenter
from services.convert.cluster_display_util import ClusterDisplayUtil
from phmconfig.timeUtils import TimeUtils

logging.basicConfig(format='%(levelname)s:%(message)s', level=logging.INFO)
app = FastAPI()

# 支持跨域
origins = ['*']
app.add_middleware(
    CORSMiddleware,
    allow_origins=origins,
    allow_credentials=True,
    allow_methods=['*'],
    allow_headers=['*']
)

app.mount('/static', StaticFiles(directory='../swagger_ui_dep/static'), name='static')

# 线程池初始化
executor_ = concurrent.futures.ThreadPoolExecutor(max_workers=5)


def startMqtt():
    try:
        MqttClient().start()
    except Exception as e:
        print(e)
    finally:
        pass


threading.Thread(target=startMqtt()).start()


def write_back_history_result(client, reqid):
    # 回写历史状态
    params = {'reqid': reqid, 'res': "settled"}
    client.put(f'{bcf.URL_MD_WRITE_REQ_HISTORY}', params=params)


def publish_data_to_iot(reqid, data):
    # 发布遥测数据到IOT
    try:
        MqttClient().publish(json.dumps({"reqid": reqid, "sohres": data}))
    except Exception as e:
        print(e)
    finally:
        pass


def post_process_vrla_soh(reqid, items):
    with httpx.Client(timeout=None, verify=False) as client:
        write_back_history_result(client, reqid)

        if bcf.CALCULATE_RESULT_BATCH_OPERATOR is False:
            # 写回指标统计数据库表
            for item in items:
                client.post(f'{bcf.URL_MD_WRITE_EVAL}', json=DataConvertUtil.SOH(reqid, item))
        else:
            client.post(f'{bcf.URL_MD_WRITE_EVAL_BATCH}', params={"reqid": reqid},  json={"items": json.dumps(items)})

        publish_data_to_iot(reqid, items)


def post_process_vrla_cluster(reqid, sohres, displayType):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

        # 聚类模型需要数据转换
        items = phm.cluster_convert(sohres)

        # 将数据写入数据库
        if bcf.CALCULATE_RESULT_BATCH_OPERATOR is False:
            for did in items.keys():
                client.post(bcf.URL_MD_WRITE_CLUSTER, json=DataConvertUtil.cluster(reqid, displayType, did, items))
        else:
            client.post(bcf.URL_MD_WRITE_CLUSTER_BATCH,
                        params={"reqid": reqid, "displayType": displayType},
                        json={"items": json.dumps(items)})
        publish_data_to_iot(reqid, sohres)


def post_process_vrla_relation(reqid, items):
    with httpx.Client(timeout=None, verify=False) as client:

        write_back_history_result(client, reqid)

        if bcf.CALCULATE_RESULT_BATCH_OPERATOR is False:
            # 写回指标统计数据库表
            for did in items.keys():
                eqitem = items[did]
                for index, item in enumerate(eqitem["lag"]):
                    eqi = {
                        "reqId": reqid,
                        "lag": item,
                        "value": eqitem["value"][index],
                        "ts": int(time.time() * 1000),
                    }
                    client.post(f'{bcf.URL_MD_WRITE_SELF_RELATION}', json=eqi)
        else:
            client.post(f'{bcf.URL_MD_WRITE_SELF_RELATION_BATCH}',
                        params={"reqid": reqid},
                        json={"items": json.dumps(items)})

        publish_data_to_iot(reqid, items)


# time intensive tasks
def soh_task(sohin, reqid):
    # 下载装备数据
    dataS = dataCenter.download_zb_data(sohin.devices, sohin.tags, sohin.startts, sohin.endts)

    # logging.info("下载的数据:" + json.dumps(dataS, ensure_ascii=False))
    # 获取测点映射
    devices = json.loads(sohin.devices)

    if len(devices) > 0:
        mappingS = dataCenter.query_metric_mapping(devices[0])
    else:
        mappingS = dataCenter.query_metric_mapping()
    # logging.info("下载测点:" + json.dumps(mappingS, ensure_ascii=False))
    # 测点反转
    convertMapping = {}
    if mappingS is not None:
        for k, v in mappingS.items():
            convertMapping[v] = k

    logging.info("测点映射:" + json.dumps(convertMapping, ensure_ascii=False))

    try:
        # 计算SOH
        res = phm.calculate_soh(dataS, convertMapping)
        # 处理结果
        post_process_vrla_soh(reqid, res)
    except Exception as e:
        print(e)
    logging.info("计算SOH完成")


def cluster_task(clusterin, reqid, displayType):
    dataS = dataCenter.download_zb_data(clusterin.devices, clusterin.tags, clusterin.startts, clusterin.endts)
    # logging.info("下载的数据:" + json.dumps(dataS, ensure_ascii=False))
    try:
        res = phm.calculate_cluster(dataS, displayType)
        post_process_vrla_cluster(reqid, res, displayType)
    except Exception as e:
        print(e)
    logging.info("聚类计算完成: " + displayType)


def relation_task(relationin, reqid, leftTag, rightTag, step, unit):
    logging.info("relation param, startTime: " + TimeUtils.convert_time_str(relationin.startts) +
                 " endTime: " + TimeUtils.convert_time_str(relationin.endts) +
                 " leftTag: " + TimeUtils.convert_time_str(leftTag) +
                 " rightTag: " + TimeUtils.convert_time_str(rightTag) +
                 " step: " + str(step) +
                 " unit: " + str(unit))

    dataS = dataCenter.download_zb_data(relationin.devices, relationin.tags, relationin.startts, relationin.endts)
    # logging.info("下载的数据:" + json.dumps(dataS, ensure_ascii=False))
    try:
        res = phm.calculate_relate(dataS, leftTag, rightTag, step, unit)
        post_process_vrla_relation(reqid, res)
    except Exception as e:
        print(e)
    logging.info("自相关计算完成")


# IF11:REST MODEL 外部接口-phmMD与phmMS之间接口
class SohInputParams(BaseModel):
    devices: str = '[\"B001\", \"B002\"]'  # json string
    tags: str = '[\"soc\",\"soh\"]'  # json string
    startts: int = 1652170492000  # timestamp ms
    endts: int = 1652256892000  # timestamp ms


@app.post("/api/v1/soh")
async def calculate_soh(sohin: SohInputParams, reqid: int):
    """模拟耗时的机器学习任务"""
    executor_.submit(soh_task, sohin, reqid)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/cluster")
async def calculate_cluster(sohin: SohInputParams, reqid: int, displayType: str):
    """模拟耗时的机器学习任务"""
    executor_.submit(cluster_task, sohin, reqid, displayType)
    return {'task': reqid, 'status': 'submitted to work thread.'}


@app.post("/api/v1/relation")
async def calculate_relation(sohin: SohInputParams, reqid: int, leftTag: int, rightTag: int, step: int, unit: int):
    executor_.submit(relation_task, sohin, reqid, leftTag, rightTag, step, unit)
    return {'task': reqid, 'status': 'submitted to work thread.'}


app.include_router(mock_zb_router.router)
