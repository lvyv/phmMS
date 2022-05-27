class EvalModelValidate:
    @staticmethod
    def support(equipCode):
        devs = equipCode.split(",")
        if len(devs) > 1:
            return False
        return True
