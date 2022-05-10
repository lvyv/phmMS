import httpx
from phmconfig import constants


class DashboardManagerService:

    @staticmethod
    def getDashboardList(query, filter):

        def fn_query():
            with httpx.Client(timeout=None, verify=False) as client:
                # url = constants.API_QUERY_HISTORY_DATA
                url = constants.URL_MS_GET_DASHBOARD_LIST + "/api/search"
                r = client.get(url, params={"query": query})
                dataS = r.json()
                return dataS

        def fn_filter(items):
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
