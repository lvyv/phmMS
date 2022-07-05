import json
import logging

import httpx
from phmconfig import constants


class GrafanaMangerService:
    modify_dashboard_title = []

    zbjk_preset_template_name_all = ["equipType", "equipCode", "host", "metrics",
                                     "timeSegment", "params", "subFrom", "subTo"]
    zbjk_preset_template_name_intersection = ["equipType", "equipCode", "host"]

    @staticmethod
    def get_host(host):
        if host is None:
            return constants.PHMMS_URL_PREFIX
        if len(constants.PHMMS_CONTAINER_NAME.split(":")) == 2:
            return constants.PHMMS_URL_PREFIX
        else:
            return constants.SCHEMA_HEADER + "://" + host

    @staticmethod
    def found_zbjk_dashboard(items):
        templateName = []
        for item in items:
            templateName.append(item["name"])
        middle = list(set(GrafanaMangerService.zbjk_preset_template_name_all).intersection(set(templateName)))
        end = list(set(middle).intersection(set(GrafanaMangerService.zbjk_preset_template_name_intersection)))
        if len(end) == len(GrafanaMangerService.zbjk_preset_template_name_intersection):
            return True
        return False

    @staticmethod
    def syncHost(host, timeSegmentLabel, username, password):
        result = []
        dashboards = GrafanaMangerService.query_dashboard_list()
        for dash in dashboards:
            if dash["title"] in GrafanaMangerService.modify_dashboard_title or True:
                data = GrafanaMangerService.query_dashboard_by_uid(dash["uid"])
                # TODO 移除meta
                if "meta" in data.keys():
                    data.pop("meta")
                # TODO 新增 message, overwrite
                data.update({"message": "自动更新模板变量【host】值"})
                data.update({"overwrite": False})

                # TODO 新增folderId
                if "folderId" in dash.keys():
                    data.update({"folderId": dash["folderId"]})

                hasModify = False

                # TODO 修改模板变量
                if "dashboard" in data.keys():
                    _dashboard = data["dashboard"]
                    if "templating" in _dashboard.keys():
                        _template = _dashboard["templating"]
                        if "list" in _template.keys():
                            _list = _template["list"]
                            if GrafanaMangerService.found_zbjk_dashboard(_list) is True:
                                for t in _list:
                                    if t["name"] == "host":
                                        if t["query"] != GrafanaMangerService.get_host(host):
                                            t.update({"query": GrafanaMangerService.get_host(host)})
                                            hasModify = True
                                    elif t["name"] == "timeSegment":
                                        if timeSegmentLabel is not None and t["label"] != timeSegmentLabel:
                                            t.update({"label": timeSegmentLabel})
                                            hasModify = True
                if hasModify is True:
                    ret = GrafanaMangerService.save_dashboard(data, username, password)
                    result.append(ret)

        return result

    @staticmethod
    def query_dashboard_list():
        dashboardUid = []
        with httpx.Client(timeout=None, verify=False) as client:
            url = constants.URL_MS_GET_DASHBOARD_LIST + "/api/search"
            r = client.get(url)
            dataS = r.json()

            for index, data in enumerate(dataS):
                dashboardUid.append({"uid": data["uid"],
                                     "title": data["title"]})
                if "folderId" in data.keys():
                    dashboardUid[index].update({"folderId": data["folderId"]})
        return dashboardUid

    @staticmethod
    def query_dashboard_by_uid(uid):
        with httpx.Client(timeout=None, verify=False) as client:
            url = constants.URL_MS_GET_DASHBOARD_LIST + "/api/dashboards/uid/" + uid
            r = client.get(url)
            dataS = r.json()
            return dataS

    @staticmethod
    def url_add_auth(username, password):
        part = constants.URL_MS_GET_DASHBOARD_LIST.split("://")
        return part[0] + "://" + username + ":" + password + "@" + part[1]

    @staticmethod
    def save_dashboard(data, username, password):
        with httpx.Client(timeout=None, verify=False) as client:
            url = GrafanaMangerService.url_add_auth(username, password) + "/api/dashboards/db"
            r = client.post(url, json=data)
            dataS = r.json()
            return dataS
