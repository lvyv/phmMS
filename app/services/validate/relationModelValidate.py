class RelationModelValidate:

    @staticmethod
    def support(equipCode, metric):
        devs = equipCode.split(",")
        if len(devs) > 1:
            return False
        tags = metric.split(",")
        if len(tags) > 1:
            return False
        return True
