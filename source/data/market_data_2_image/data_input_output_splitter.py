import source.data.market_data_2_image.market_data_extracts as extracts
import numpy as np
############################################
#  Split the market data into two parts
#  - input: the first X (e.g. 300) minutes of the trading day
#  - output: the last Y (e.g. 30) minutes of the trading day
#############################################
class input_output_splitter:
    def __init__(self, extract_obj, threshold):
        self.extract_obj = extract_obj
        self.threshold = threshold


    def split(self):
        if self.extract_obj.md_date.shape[0] > self.threshold:
            input_date, output_date = np.split(self.extract_obj.md_date, [self.threshold]);
            input_time, output_time = np.split(self.extract_obj.md_time, [self.threshold]);
            input_open, output_open = np.split(self.extract_obj.md_open, [self.threshold]);
            input_close, output_close = np.split(self.extract_obj.md_close, [self.threshold]);
            input_high, output_high = np.split(self.extract_obj.md_high, [self.threshold]);
            input_low, output_low = np.split(self.extract_obj.md_low, [self.threshold]);
            input_volume, output_volume = np.split(self.extract_obj.md_volume, [self.threshold]);
            input_extract_obj = extracts.md_extracts(input_date, input_time, input_open, input_close, input_high, input_low, input_volume)
            output_extract_obj = extracts.md_extracts(output_date, output_time, output_open, output_close, output_high,
                                                     output_low, output_volume)
            return True, input_extract_obj, output_extract_obj
        else :
            input_extract_obj = extracts.md_extracts(np.array([]), np.array([]), np.array([]), np.array([]), np.array([]),
                                        np.array([]), np.array([]))
            output_extract_obj = extracts.md_extracts(np.array([]), np.array([]), np.array([]), np.array([]), np.array([]),
                                        np.array([]), np.array([]))
            return False, input_extract_obj, output_extract_obj