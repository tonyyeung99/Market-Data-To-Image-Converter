import numpy as np

############################################
#  Class y_labeler: Calculate and label the market data file
#############################################

class y_labeler:
    def __init__(self, extract_obj, ref_max, ref_min, ref_v_scale, ref_v_height):
        self.extract_obj = extract_obj
        self.ref_max = ref_max
        self.ref_min = ref_min
        self.ref_v_scale = ref_v_scale
        self.ref_v_height = ref_v_height

    ############################################
    #  Should this data labelled positive? check whether it rise/drop over the percentage
    #############################################
    def isLabelPositive(self, rise_or_drop, percentage):
        scaled_data = (self.extract_obj.md_close.astype(float) - self.ref_min) / self.ref_v_scale
        scaled_data = np.round(scaled_data, 0)
        len_data = len(self.extract_obj.md_close)
        delta = scaled_data[len_data -1] - scaled_data[0]
        pct_delta = delta/self.ref_v_height
        if((delta * rise_or_drop)>0 and abs(pct_delta) > percentage ) :
            return True
        else:
            return False
