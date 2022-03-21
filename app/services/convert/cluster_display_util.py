class ClusterDisplayUtil:
    DISPLAY_SCATTER = "SCATTER"
    DISPLAY_POLYLINE = "POLYLINE"
    DISPLAY_2D = "2D"
    DISPLAY_3D = "3D"
    DISPLAY_AGG2D = "AGG2D"
    DISPLAY_AGG3D = "AGG3D"

    @staticmethod
    def get_use_metrics(displayType):
        values = {
            # "SCATTER": ["ts", "did"],
            "2D": ["x", "y", "color", "size", "shape", "name"],
            "3D": ["x", "y", "z", "color", "size", "shape", "name"],
            "POLYLINE": ["ts"],
            "AGG2D": ["x", "y", "color", "shape", "name"],
            "AGG3D": ["x", "y", "z", "color", "shape", "name"]
        }
        return values.get(displayType, None)

    @staticmethod
    def get_metric_value(item, metric):
        values = {
            "x": item.x,
            "y": item.y,
            "color": item.color,
            "shape": item.shape,
            "name": item.name
        }
        if hasattr(item, "z") is True:
            values["z"] = item.z
        if hasattr(item, "size") is True:
            values["size"] = item.size

        return values.get(metric, None)

    @staticmethod
    def get_metric_type(key):
        if key in ["ts"]:
            return "time"
        if key in ["color", "shape", "name"]:
            return "string"
        return "number"
