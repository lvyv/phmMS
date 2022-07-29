import httpx
from phmconfig import constants


class DashboardManagerService:
    """
    grafana 大屏管理服务
    """
    @staticmethod
    def getDashboardList(query, filter):
        """
        获取zbjk大屏列表
        :param query:  查询参数
        :param filter: 过滤参数
        :return:
        """
        def fn_query():
            """
            查询大屏列表
            :return:
            """
            with httpx.Client(timeout=None, verify=False) as client:
                # url = constants.API_QUERY_HISTORY_DATA
                url = constants.URL_MS_GET_DASHBOARD_LIST + "/api/search"
                if query is not None:
                    r = client.get(url, params={"query": query})
                else:
                    r = client.get(url)
                dataS = r.json()
                return dataS

        def fn_filter(items):
            """
            过滤大屏列表
            :param items:
            :return:
            """
            ret = []
            if filter is not None:
                ft = filter.split(",")
                for item in items:
                    hasFilter = False
                    for it in ft:
                        if it is not None and it in item["title"]:
                            hasFilter = True
                            break
                    if hasFilter is False:
                        ret.append(item)
            else:
                return items
            return ret

        def fn_convert(items):
            """
            将数据转换为grafana识别的数据格式
            :param items:
            :return:
            """
            rets = []
            titles = []
            urls = []
            for item in items:

                titles.append(item["title"])
                urls.append(item["url"])
            rets.append({"name": "名称", "type": "String", "values": titles})
            rets.append({"name": "url", "type": "String", "values": urls})
            return rets

        items = fn_query()
        items = fn_filter(items)
        items = fn_convert(items)
        return items
