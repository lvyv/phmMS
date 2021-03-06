from phmconfig import constants
from phmconfig.config import ConfigSet


class ConfigManagerService:

    @staticmethod
    def update(msHost, mdHost, dbHost, dbUser, dbPw, dbName,
               grafanaHost, sjzyHost, schema, sample, multiSelf, clickGap):

        hasModify = False

        if msHost is not None:
            constants.cfg.update({"phmms_container_name": msHost})
            hasModify = True

        if mdHost is not None:
            constants.cfg.update({"phmmd_container_name": mdHost})
            hasModify = True

        if dbHost is not None and dbUser is not None and dbPw is not None and dbName is not None:
            dbPrefix = constants.PHM_DATABASE_URL.split("://")[0]
            dbUrl = dbPrefix + "://" + dbUser + ":" + dbPw + "@" + dbHost + "/" + dbName
            constants.cfg.update({"datasource_url": dbUrl})
            hasModify = True

        if grafanaHost is not None:
            constants.cfg.update({"url_ms_get_dashboard_list": grafanaHost})
            hasModify = True

        if sjzyHost is not None:
            constants.cfg.update({"url_sjzy_host": sjzyHost})
            hasModify = True

        if schema is not None:
            constants.cfg.update({"schema_https": schema})
            hasModify = True

        if sample is not None:
            constants.cfg.update({"max_point": sample})
            hasModify = True

        if multiSelf is not None:
            constants.cfg.update({"support_mutil_relation": multiSelf})
            hasModify = True

        if clickGap is not None:
            constants.cfg.update({"click_gap": clickGap})
            hasModify = True

        if hasModify is True:
            ConfigSet.save_json()

        return True

    @staticmethod
    def query():
        conf = {}

        if "phmms_container_name" in constants.cfg_keys:
            conf.update({"msHost": constants.cfg["phmms_container_name"]})

        if "phmmd_container_name" in constants.cfg_keys:
            conf.update({"mdHost": constants.cfg["phmmd_container_name"]})

        if "datasource_url" in constants.cfg_keys:
            dbInfo = constants.cfg["datasource_url"].split("://")[1]
            userNameAndPassword = dbInfo.split("@")[0]
            hostAndName = dbInfo.split("@")[1]
            conf.update({"dbHost": hostAndName.split("/")[0]})
            conf.update({"dbUser": userNameAndPassword.split(":")[0]})
            conf.update({"dbPw": userNameAndPassword.split(":")[0]})
            conf.update({"dbName": hostAndName.split("/")[1]})

        if "url_ms_get_dashboard_list" in constants.cfg_keys:
            conf.update({"grafanaHost": constants.cfg["url_ms_get_dashboard_list"]})
        if "url_sjzy_host" in constants.cfg_keys:
            conf.update({"sjzyHost": constants.cfg["url_sjzy_host"]})
        if "schema_https" in constants.cfg_keys:
            conf.update({"schema": constants.cfg["schema_https"]})
        if "max_point" in constants.cfg_keys:
            conf.update({"sample": constants.cfg["max_point"]})
        if "support_mutil_relation" in constants.cfg_keys:
            conf.update({"multiSelf": constants.cfg["support_mutil_relation"]})
        if "click_gap" in constants.cfg_keys:
            conf.update({"clickGap": constants.cfg["click_gap"]})

        return conf
