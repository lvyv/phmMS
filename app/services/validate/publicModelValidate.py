class PublicModelValidate:
    @staticmethod
    def support(equipCode: str, metrics: str):
        if equipCode is '' or metrics is '':
            return False, '', ''
        devs = list(set(filter(None, equipCode.split(","))))
        metrics = list(set(filter(None, metrics.split(","))))
        return True, ",".join(dev for dev in devs), ",".join(metric for metric in metrics)
