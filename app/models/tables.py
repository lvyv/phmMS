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
    reqId = Column(Integer)  # 执行请求ID 关联历史记录表
    ts = Column(BigInteger)  # 时间
    did = Column(TEXT)  # 装备ID
    dclz = Column(TEXT)  # 装备类型

    # 普通测点   可采集的测点
    M01 = Column(FLOAT)
    M02 = Column(FLOAT)
    M03 = Column(FLOAT)
    M04 = Column(FLOAT)
    M05 = Column(FLOAT)
    M06 = Column(FLOAT)
    M07 = Column(FLOAT)
    M08 = Column(FLOAT)
    M09 = Column(FLOAT)
    M10 = Column(FLOAT)
    M11 = Column(FLOAT)
    M12 = Column(FLOAT)
    M13 = Column(FLOAT)
    M14 = Column(FLOAT)
    M15 = Column(FLOAT)
    M16 = Column(FLOAT)
    M17 = Column(FLOAT)
    M18 = Column(FLOAT)
    M19 = Column(FLOAT)
    M20 = Column(FLOAT)
    M21 = Column(FLOAT)
    M22 = Column(FLOAT)
    M23 = Column(FLOAT)
    M24 = Column(FLOAT)
    M25 = Column(FLOAT)
    M26 = Column(FLOAT)
    M27 = Column(FLOAT)
    M28 = Column(FLOAT)
    M29 = Column(FLOAT)
    M30 = Column(FLOAT)
    M31 = Column(FLOAT)
    M32 = Column(FLOAT)
    M33 = Column(FLOAT)
    M34 = Column(FLOAT)
    M35 = Column(FLOAT)
    M36 = Column(FLOAT)
    M37 = Column(FLOAT)
    M38 = Column(FLOAT)
    M39 = Column(FLOAT)

    # 组测点  eg: # 电池组的环境温度集合,  # 电池单元端电压集合 , # 电池单元容量集合
    AM1 = Column(TEXT)
    AM2 = Column(TEXT)
    AM3 = Column(TEXT)
    AM4 = Column(TEXT)
    AM5 = Column(TEXT)

    # 整型测点 eg: # 健康状态
    IM1 = Column(Integer)

    # 用于计算模型结果存放字段
    FM1 = Column(FLOAT)
    FM2 = Column(FLOAT)
    FM3 = Column(FLOAT)
    FM4 = Column(FLOAT)
    FM5 = Column(FLOAT)


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
    metric_code = Column(TEXT)     # 测点编码      ignore
    metric_name = Column(TEXT)     # 测点名称
    metric_alias = Column(TEXT)    # 测点别名
    equip_code = Column(TEXT)      # 装备编码      ignore
    equip_name = Column(TEXT)      # 装备名称      ignore
    equip_type = Column(TEXT)      # 装备类型
    equip_type_code = Column(TEXT)  # 装备类型编码
    metric_describe = Column(TEXT)        # 描述   ignore
    metric_unit = Column(TEXT)     # 测点类型


class TEquipTypeMapping(Base):
    __tablename__ = "xc_equip_type_mapping"
    id = Column(Integer, primary_key=True, index=True)
    equip_type_code = Column(TEXT)  # 装备类型编码
    equip_type = Column(TEXT)  # 装备类型


# create all tables
TABLES = create_tables()
