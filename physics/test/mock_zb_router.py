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
@router.post("/zbData")
async def getZbData(devs, metrics, start, end):
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
