from phmconfig.config import ConfigSet

cfg = ConfigSet.get_cfg()

cfg_keys = cfg.keys()

# --------------------- MS -------------------------------------
# phmMS启动的地址、端口、证书等
PHMMS_HOST = cfg['phmms_host']
PHMMS_PORT = cfg['phmms_port']
PHMMS_KEY = cfg['phmms_key']
PHMMS_CER = cfg['phmms_cer']

# ------------------------------------ MD -----------------
# phmMD启动的地址、端口、证书等
PHMMD_HOST = cfg['phmmd_host']
PHMMD_PORT = cfg['phmmd_port']
PHMMD_KEY = cfg['phmmd_key']
PHMMD_CER = cfg['phmmd_cer']

# ----------------------------- DB -----------------------
# 数据库地址
PHM_DATABASE_URL = cfg['datasource_url']

DATABASE_TYPE_MYSQL = 'MYSQL'
DATABASE_TYPE_PGSQL = 'PGSQL'


def get_database_type():
    if PHM_DATABASE_URL.startswith("postgresql") is True:
        return DATABASE_TYPE_PGSQL
    elif PHM_DATABASE_URL.startswith("mysql") is True:
        return DATABASE_TYPE_MYSQL
    else:
        return None


USING_DATABASE_TYPE = get_database_type()

#  --------------------------- COMMON -------------------------
# 所有后端的科学计算模型，phmMD类型
DEV_VRLA = 'vrla'
# 各种状态常量
REQ_STATUS_PENDING = 'pending'
REQ_STATUS_SETTLED = 'settled'
# 后台ai模型的地址
REST_REQUEST_TIMEOUT = 10

# 精确查询
PREFECT_MATCH_HISTORY_QUERY_RECORD = cfg[
    "time_segment_prefect_match"] if "time_segment_prefect_match" in cfg_keys else True

EQUIP_DATA_MAX_POINT = cfg["max_point"] if "max_point" in cfg_keys else 1000

# 点击时间间隔
CLICK_GRAP = cfg["click_gap"] if 'click_gap' in cfg_keys else 60

EQUIP_METRIC_SYNC_GAP = cfg["equip_metric_sync_gap"] if 'equip_metric_sync_gap' in cfg_keys else 300

TIME_SEGMENT_SHOW_UTF8 = cfg["time_segment_show_utf_8"] if "time_segment_show_utf_8" in cfg_keys else True

# ------------------------- api ------------------------------

# 配置服务启动模式
SCHEMA_HTTPS = cfg["schema_https"] if "schema_https" in cfg_keys else False

SCHEMA_HEADER = "https" if SCHEMA_HTTPS is True else "http"

# prefix
PHMMS_CONTAINER_NAME = cfg["phmms_container_name"]

if len(PHMMS_CONTAINER_NAME.split(":")) == 2:
    PHMMS_URL_PREFIX = SCHEMA_HEADER + "://" + PHMMS_CONTAINER_NAME
else:
    PHMMS_URL_PREFIX = SCHEMA_HEADER + "://" + PHMMS_CONTAINER_NAME + ":" + str(PHMMS_PORT)
# 写评估数据
URL_MD_WRITE_EVAL = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeEval"
# 写健康指标URL地址
URL_MS_WRITE_HEALTH_INDICATOR = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeHealthIndicator"
# 写聚类数据
URL_MD_WRITE_CLUSTER = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeCluster"
# 写自相关数据
URL_MD_WRITE_SELF_RELATION = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeRelation"
# 写更新历史请求记录
URL_MD_WRITE_REQ_HISTORY = PHMMS_URL_PREFIX + "/api/v1/public/updateHistoryRecord"

# 查询Mapping表
URL_MD_QUERY_METRIC_MAPPING = PHMMS_URL_PREFIX + "/api/v1/public/getMapping"

# prefix
PHMMD_CONTAINER_NAME = cfg["phmmd_container_name"]

if len(PHMMD_CONTAINER_NAME.split(":")) == 2:
    PHMMD_URL_PREFIX = SCHEMA_HEADER + "://" + PHMMD_CONTAINER_NAME
else:
    PHMMD_URL_PREFIX = SCHEMA_HEADER + "://" + PHMMD_CONTAINER_NAME + ":" + str(PHMMD_PORT)
# 调用评估
URL_MS_CALL_SOH = PHMMD_URL_PREFIX + "/api/v1/soh"
# 调用聚类
URL_MS_CALL_CLUSTER = PHMMD_URL_PREFIX + "/api/v1/cluster"
# 调用自相关
URL_MS_CALL_RELATION = PHMMD_URL_PREFIX + "/api/v1/relation"

# 数据资源
URL_SJZY_API_PREFIX = cfg["url_sjzy_host"]
# 从数据资源获取装备所有测点
API_QUERY_EQUIP_INFO_WITH_MEASURE_POINT = URL_SJZY_API_PREFIX + "/api/equip/query_equip_info_with_measure_point"
# 从数据资源获取装备的测点数据
API_QUERY_HISTORY_DATA = URL_SJZY_API_PREFIX + "/api/devices/query_history_data_v2"

# 对接grafana
URL_MS_GET_DASHBOARD_LIST = cfg["url_ms_get_dashboard_list"]

# 模拟装备数据
MOCK_ZB_DATA = cfg["mock_zb_data"] if "mock_zb_data" in cfg_keys else False

# 批量写入
CALCULATE_RESULT_BATCH_OPERATOR = cfg["batch_operator"] if "batch_operator" in cfg_keys else True
URL_MD_WRITE_EVAL_BATCH = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeEvalBatch"
URL_MD_WRITE_CLUSTER_BATCH = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeClusterBatch"
URL_MD_WRITE_SELF_RELATION_BATCH = PHMMS_URL_PREFIX + "/api/v1/cellpack/writeRelationBatch"
