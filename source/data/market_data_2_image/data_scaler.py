import numpy as np
import math
import source.app_constants as const
############################################
#  Scale the market data and fit it into the size of one image
#############################################
class md_data_scaler:
    def __init__(self, extracts_obj):
        self.extract_obj = extracts_obj

    def scale(self, v_height):
        c_close = np.asfarray(self.extract_obj.md_close)
        max, min, v_scale = self.getScaleParam(c_close, v_height)
        self.extract_obj.md_close = self.toInteger(self.scaleFloatProperty(c_close,  min, v_scale))
        return self.extract_obj, max, min , v_scale

    def getScaleParam(self, f_data, v_height):
        max = np.amax(f_data, axis=0)
        min = np.amin(f_data, axis=0)
        v_scale = (max-min)/ v_height
        return max, min, v_scale

    def toInteger(self, f_data):
        return np.round(f_data, 0).astype(int)

    def scaleFloatProperty(self, f_data, v_min, v_scale):
        return (f_data - v_min) / v_scale