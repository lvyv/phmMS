import logging
import time
from datetime import datetime
from pathlib import Path
import scipy.io


class NasaData:

    @staticmethod
    def convert_to_time(hmm):
        year, month, day, hour, minute, second = int(hmm[0]), int(hmm[1]), int(hmm[2]), int(hmm[3]), int(hmm[4]), int(
            hmm[5])
        return datetime(year=year, month=month, day=day, hour=hour, minute=minute, second=second)

    @staticmethod
    # 提取锂电池容量
    def getBatteryCapacity(Battery):
        cycle, capacity = [], []
        i = 1
        for Bat in Battery:
            if Bat['type'] == 'discharge':
                capacity.append(Bat['data']['Capacity'][0])
                cycle.append(i)
                i += 1
        return [cycle, capacity]

    @staticmethod
    # 获取锂电池充电或放电时的测试数据
    def getBatteryValues(Battery, Type='charge'):
        data = []
        for Bat in Battery:
            if Bat['type'] == Type:
                data.append(Bat['data'])
        return data

    @staticmethod
    def loadMat(matFile):
        data = scipy.io.loadmat(matFile)
        filename = matFile.split('/')[-1].split('.')[0]
        col = data.get(filename, None)
        col = col[0][0][0][0]
        size = col.shape[0]
        data = []
        for i in range(size):
            k = list(col[i][3][0].dtype.fields.keys())
            d1, d2 = {}, {}
            if str(col[i][0][0]) != 'impedance':
                for j in range(len(k)):
                    t = col[i][3][0][0][j][0];
                    l = [t[m] for m in range(len(t))]
                    d2[k[j]] = l
            d1['type'], d1['temp'] = str(col[i][0][0]), int(col[i][1][0])
            d1['time'], d1['data'] = str(NasaData.convert_to_time(col[i][2][0])), d2
            data.append(d1)
        return data


class NasaDataManage:

    mappings = {"Voltage_measured": "测量的电压", "Current_measured": "测量的电流", "Temperature_measured": "工作温度",
                 "Current_charge": "充电器充电电流", "Voltage_charge": "充电器充电电压", "Time": "工作时间"}

    @staticmethod
    def load():
        Battery_list = ['B0005', 'B0006', 'B0007', 'B0018']  # 4 个数据集的名字
        nasaDataPath = Path(Path(__file__).parent).joinpath("nasa_data")
        capacity, charge, discharge = {}, {}, {}
        for name in Battery_list:
            print('Load Dataset ' + name + '.mat ...')
            path = str(nasaDataPath) + "/" + name + '.mat'
            data = NasaData.loadMat(path)
            capacity[name] = NasaData.getBatteryCapacity(data)  # 放电时的容量数据
            charge[name] = NasaData.getBatteryValues(data, 'charge')  # 充电数据
            discharge[name] = NasaData.getBatteryValues(data, 'discharge')  # 放电数据
        logging.info("nasa mat data load compeleted.")
        return capacity, charge, discharge

    @staticmethod
    def convert(equipCode, metricName, startTime, endTime):

        capacity, charge, discharge = NasaDataManage.load()

        deviceIds = equipCode.split(",")
        metricIds = metricName.split(",")

        # 生成模拟数据
        ret = {
            "code": "success",
            "result": []
        }
        tagNumber = 1
        for dev in charge.keys():
            if dev not in deviceIds:
                continue
            genDev = {
                "equipCode": dev,
                "equipName": dev,
                "equipData": []
            }
            tag = charge[dev][0]
            for key in tag.keys():
                if key == "Time":
                    continue
                if NasaDataManage.mappings[key] not in metricIds:
                    continue
                genTag = {
                    "metricName": NasaDataManage.mappings[key],
                    "metricCode": "M00" + str(tagNumber),
                    "metricData": []
                }
                data_len = len(tag[key])
                for index, itval in enumerate(tag[key]):
                    genTag["metricData"].append({
                        "timestamp": NasaDataManage.makeTime(startTime, endTime, data_len, index),
                        "metricValue": itval
                    })
                genDev["equipData"].append(genTag)
                tagNumber = tagNumber + 1
            ret["result"].append(genDev)

        return ret

    @staticmethod
    def makeTime(startTime, endTime, data_len, index):
        start = TimeUtil.convert_time_stamp(startTime)
        end = TimeUtil.convert_time_stamp(endTime)
        # int(down)  ceil(up) round(四舍五入)
        # interval = round((end - start) / 1000 / data_len)
        interval = 5
        return TimeUtil.convert_time_str(start + index * interval * 1000)


class TimeUtil:

    @staticmethod
    def convert_time_stamp(timeStr):
        # 2022-02-13 22:09:59
        timeArray = time.strptime(timeStr, "%Y-%m-%d %H:%M:%S")
        timeStamp = int(time.mktime(timeArray))
        return timeStamp * 1000

    @staticmethod
    def convert_time_str(timestamp):
        time_tuple = time.localtime(timestamp / 1000)
        bj_time = time.strftime("%Y-%m-%d %H:%M:%S", time_tuple)
        # print("北京时间:", bj_time)
        return bj_time


if __name__ == "__main__":
    ret = NasaDataManage.convert("B0005", ",".join(it for it in NasaDataManage.mappings.values()),
                                 "2022-07-25 10:00:00", "2022-07-25 11:00:00")
