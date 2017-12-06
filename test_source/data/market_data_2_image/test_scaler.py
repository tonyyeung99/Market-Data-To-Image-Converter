import numpy as np
import source.data.market_data_2_image.data_scaler as scale_pkg
import source.data.market_data_2_image.market_data_extracts as extracts
import source.app_constants as const
import unittest
import numpy.testing as nptest

class TestScaler(unittest.TestCase):

    def setUp(self):
        self.md_date = np.array(['03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012'])
        self.md_time = np.array(['09:15:00 AM', '09:16:00 AM', '09:17:00 AM', '09:18:00 AM', '09:19:00 AM', '09:20:00 AM'])
        self.md_open = np.array(['21119', '21119', '21126', '22119', '22119', '22126'])
        self.md_high = np.array(['21130', '21127', '21126', '22130', '22127', '22126'])
        self.md_low = np.array(['21101', '21111', '21105', '22101', '22111', '22105'])
        self.md_close = np.array(['21115', '21125', '21108', '22115', '22125', '22108'])
        self.md_volume = np.array(['662', '243', '392', '2662', '2243', '2392'])
        self.extract_obj = extracts.md_extracts(self.md_date, self.md_time, self.md_open, self.md_close, self.md_high, self.md_low, self.md_volume)

    def testScaleClose(self):
        scaler = scale_pkg.md_data_scaler(self.extract_obj)
        scaled_obj, max, min , v_scale = scaler.scale(const.HSI_IMAGE_HEIGHT);
        nptest.assert_equal(max, 22125)
        nptest.assert_equal(min, 21108)
        nptest.assert_equal(v_scale, 5.65)
        nptest.assert_array_equal(scaled_obj.md_close, np.array([1, 3, 0, 178, 180, 177]))