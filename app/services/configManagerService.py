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
