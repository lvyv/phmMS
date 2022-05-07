import json
import time
from schemas.vrla.health_indicator_model import HealthIndicatorModel
import httpx
import constants


# {
# 	"alarmInfo": [{
# 		"deviceId": "B001",
# 		"variables": [{
# 			"variable": "soh",
# 			"data": 20
# 		}, {
# 			"variable": "state",
# 			"data": 1
# 		}]
# 	}, {
# 		"deviceId": "B001",
# 		"variables": [{
# 			"variable": "soh",
# 			"data": 20
# 		}, {
# 			"variable": "state",
# 			"data": 1
# 		}]
# 	}]
# }
class PayloadProcess:

    @staticmethod
    def process(msg):
        # TODO 解析数据，并将数据写入数据库
        data = json.loads(msg)
        # data["alarmId"]
        # data["ruleId"]
        alarmInfo = data["alarmInfo"]
        tmpDic = {}
        for ai in alarmInfo:
            deviceId = ai["deviceId"]
            variables = ai["variables"]
            for v in variables:
                variable = v["variable"]
                value = v["data"]
                if deviceId in tmpDic.keys():
                    tmpDic[deviceId][variable] = value
                else:
                    tmpDic[deviceId] = {
                        "ts": time.time() * 1000,
                        "did": deviceId
                    }
                    tmpDic[deviceId][variable] = value

        for key in tmpDic.keys():
            item = tmpDic[key]
            if "soh" in item.keys() and "state" in item.keys():
                with httpx.Client(timeout=None, verify=False) as client:
                    model = HealthIndicatorModel(soh=item["soh"],
                                                 ts=item["ts"],
                                                 did=item["did"],
                                                 dclz='',
                                                 state=item["state"]
                                                 )
                    data = json.loads(json.dumps(model.__dict__))
                    r = client.post(constants.URL_MS_WRITE_HEALTH_INDICATOR, json=data)
                    print(r)

    @staticmethod
    def getEquipCode(topic):
        topics = topic.split("/")
        if len(topics) == 3:
            return topics[1]
        return None

    @staticmethod
    def topicIsEqual(topic1, topic2):
        if topic1 == topic2:
            return True
        equipCode = PayloadProcess.getEquipCode(topic1)
        if equipCode is None:
            return False
        generalTopic = topic1.replace(equipCode, "+")
        if generalTopic == topic2:
            return True
        return False
