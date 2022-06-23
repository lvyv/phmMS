from sqlalchemy import Column, Integer, String, FLOAT, INTEGER, BigInteger, Boolean, TEXT
from phmconfig.database import Base, create_tables


# class TApiToken(Base):
#     """
#     令牌表，暂存api访问令牌，便于使用。
#     该表主要字段：
#         id: 记录权限Token；
#         url: api的原型，https://ip:port/api/v1/phm/{soh}；
#         tk: 该api的访问令牌。
#
#     Attributes
#     ----------
#
#     Methods
#     -------
#
#     """
#     __tablename__ = "api_token"
#
#     id = Column(Integer, primary_key=True, index=True)
#     url = Column(String(512))
#     tk = Column(String(512))


class TReqHistory(Base):
    """
    在phmMS收到REST调用时，创建一条记录，保存该异步请求，之后调用phmMD。
    在phmMD被调用启动的工作线程完成耗时计算后，反向回调phmMS，保存原来异步请求的执行结果。
    该表主要字段：
        id: 记录请求号，每次调用都是唯一的；
        model: 记录请求是针对哪个模型；
        status: 该请求的执行状态；
        result: 请求执行的结果。
        requestts: 客户端调用的时间戳。
        settledts: Ai模型执行完成的时间戳。
        memo: 放设备id。
        metrics: 存放设备测点。
    Attributes
    ----------

    Methods
    -------

    """
    __tablename__ = "xc_req_history"

    id = Column(Integer, primary_key=True, index=True)
    model = Column(TEXT)
    status = Column(TEXT)
    result = Column(TEXT)
    requestts = Column(BigInteger)
    settledts = Column(BigInteger)
    memo = Column(TEXT)
    metrics = Column(TEXT)
    displayType = Column(TEXT)
    startTs = Column(BigInteger)
    endTs = Column(BigInteger)


class TCellPack(Base):
    __tablename__ = "xc_cell_pack"
    id = Column(Integer, primary_key=True, index=True)  # 主键
    ts = Column(BigInteger)  # 时间
    did = Column(TEXT)  # 装备ID
    dclz = Column(TEXT)  # 装备类型
    remainLife = Column(FLOAT)  # 剩余寿命
    voc = Column(FLOAT)  # 开路电压 【电池处于断路状态时的电压，即非工作电压】
    workVoc = Column(FLOAT)  # 端电压 【电池处于闭路状态时的电池正负极之间的电压，即工作电压】
    soc = Column(FLOAT)  # 容量 【state of charge】
    soh = Column(FLOAT)  # 健康指标 【state of health】
    imbalance = Column(FLOAT)  # 内阻不平衡度
    current = Column(FLOAT)  # 冲放电电流
    minTemp = Column(FLOAT)  # 最小温度
    maxTemp = Column(FLOAT)  # 最大温度
    cellMaxVoc = Column(FLOAT)  # 电池单元的最大开路电压
    cellMinVoc = Column(FLOAT)  # 电池单元的最小开路电压
    cellMaxVol = Column(FLOAT)  # 电池单元的最大端电压
    cellMinVol = Column(FLOAT)  # 电池单元的最小端电压
    cellAvgVol = Column(FLOAT)  # 电池单元的均值端电压
    envTemp = Column(TEXT)  # 电池组的环境温度（存在多个测点）
    cellVol = Column(TEXT)  # 电池单元端电压集合
    cellSoc = Column(TEXT)  # 电池单元容量集合
    state = Column(Integer)  # 健康状态
    reqId = Column(Integer)  # 执行请求ID 关联历史记录表
    # extend
    M1 = Column(FLOAT)
    M2 = Column(FLOAT)
    M3 = Column(FLOAT)
    M4 = Column(FLOAT)
    M5 = Column(FLOAT)
    M6 = Column(FLOAT)
    M7 = Column(FLOAT)
    M8 = Column(FLOAT)


class TSchedule(Base):  # 装备数据分析调度表
    __tablename__ = "xc_schedule"
    id = Column(Integer, primary_key=True, index=True)  # 主键
    dids = Column(TEXT)  # 设备ID列表
    dtags = Column(TEXT)  # 设备测点列表
    enable = Column(Boolean)  # 启用任务
    initDelay = Column(Integer)  # 初始任务延迟时间
    delay = Column(Integer)  # 定时延迟时间
    execUrl = Column(TEXT)  # 执行调用的 URL
    startTime = Column(BigInteger)  # 调度执行时间


class TCluster(Base):
    __tablename__ = "xc_cluster"
    id = Column(Integer, primary_key=True, index=True)  # 主键
    ts = Column(BigInteger)  # 时间
    reqId = Column(Integer)  # 执行请求ID 关联历史记录表
    x = Column(FLOAT)  # x 轴坐标
    y = Column(FLOAT)  # y 轴坐标
    z = Column(FLOAT)  # z 轴坐标
    color = Column(TEXT)  # 颜色值 eg: "red", "green", "yellow", "blue", "gray","black", "orange"
    size = Column(FLOAT)  # 大小
    shape = Column(TEXT)  # 形状 eg: "circle", "star","square", "cross", "diamond"
    name = Column(TEXT)  # 装备ID


class TSelfRelation(Base):
    __tablename__ = "xc_self_relation"
    id = Column(Integer, primary_key=True, index=True)  # 主键
    ts = Column(BigInteger)
    reqId = Column(Integer)
    lag = Column(Integer)
    value = Column(FLOAT)


class TMetricMapping(Base):
    __tablename__ = "xc_metric_mapping"
    id = Column(Integer, primary_key=True, index=True)
    metric_code = Column(TEXT)     # 测点编码
    metric_name = Column(TEXT)     # 测点名称
    metric_alias = Column(TEXT)    # 测点别名
    equip_code = Column(TEXT)      # 装备编码
    equip_name = Column(TEXT)      # 装备名称
    equip_type = Column(TEXT)      # 装备类型
    equip_type_code = Column(TEXT)  # 装备类型编码
    metric_describe = Column(TEXT)        # 描述
    metric_unit = Column(TEXT)     # 测点类型


class TEquipTypeMapping(Base):
    __tablename__ = "xc_equip_type_mapping"
    id = Column(Integer, primary_key=True, index=True)
    equip_type_code = Column(TEXT)  # 装备类型编码
    equip_type = Column(TEXT)  # 装备类型


# create all tables
TABLES = create_tables()
