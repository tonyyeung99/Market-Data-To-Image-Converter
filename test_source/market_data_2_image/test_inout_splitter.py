import unittest

import numpy as np
import numpy.testing as nptest
from source.market_data_2_image.data_input_output_splitter import MarketDataSplitter as market_data_splitter
import source.market_data_2_image.market_data_extracts as extracts


class TestInOutSplitter(unittest.TestCase):
    def setUp(self):
        self.md_date = np.array(['03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012', '03/06/2012'])
        self.md_time = np.array(
            ['09:15:00 AM', '09:16:00 AM', '09:17:00 AM', '09:18:00 AM', '09:19:00 AM', '09:20:00 AM'])
        self.md_open = np.array(['21119', '21119', '21126', '22119', '22119', '22126'])
        self.md_high = np.array(['21130', '21127', '21126', '22130', '22127', '22126'])
        self.md_low = np.array(['21101', '21111', '21105', '22101', '22111', '22105'])
        self.md_close = np.array(['21115', '21125', '21108', '22115', '22125', '22108'])
        self.md_volume = np.array(['662', '243', '392', '2662', '2243', '2392'])
        self.extract_obj = extracts.md_extracts(self.md_date, self.md_time, self.md_open, self.md_close, self.md_high,
                                                self.md_low, self.md_volume)

    def test_split_data_within_thresold(self):
        splitter = market_data_splitter(self.extract_obj, 3)
        split_flag, input_split_obj, output_split_obj = splitter.split()
        self.assertEqual(input_split_obj.md_date.shape[0], 3)
        self.assertEqual(split_flag, True)
        nptest.assert_array_equal(input_split_obj.md_date, np.array(['03/06/2012', '03/06/2012', '03/06/2012']))
        nptest.assert_array_equal(output_split_obj.md_date, np.array(['03/06/2012', '03/06/2012', '03/06/2012']))
        nptest.assert_array_equal(input_split_obj.md_time, np.array(['09:15:00 AM', '09:16:00 AM', '09:17:00 AM']))
        nptest.assert_array_equal(output_split_obj.md_time, np.array(['09:18:00 AM', '09:19:00 AM', '09:20:00 AM']))
        nptest.assert_array_equal(input_split_obj.md_open, np.array(['21119', '21119', '21126']))
        nptest.assert_array_equal(output_split_obj.md_open, np.array(['22119', '22119', '22126']))
        nptest.assert_array_equal(input_split_obj.md_close, np.array(['21115', '21125', '21108']))
        nptest.assert_array_equal(output_split_obj.md_close, np.array(['22115', '22125', '22108']))
        nptest.assert_array_equal(input_split_obj.md_high, np.array(['21130', '21127', '21126']))
        nptest.assert_array_equal(output_split_obj.md_high, np.array(['22130', '22127', '22126']))
        nptest.assert_array_equal(input_split_obj.md_low, np.array(['21101', '21111', '21105']))
        nptest.assert_array_equal(output_split_obj.md_low, np.array(['22101', '22111', '22105']))
        nptest.assert_array_equal(input_split_obj.md_volume, np.array(['662', '243', '392']))
        nptest.assert_array_equal(output_split_obj.md_volume, np.array(['2662', '2243', '2392']))

    def test_split_data_touch_thresold(self):
        splitter = market_data_splitter(self.extract_obj, 6)
        split_flag, input_split_obj, output_split_obj = splitter.split()
        self.assertEqual(split_flag, False)

    def test_split_data_out_thresold(self):
        splitter = market_data_splitter(self.extract_obj, 7)
        split_flag, input_split_obj, output_split_obj = splitter.split()
        self.assertEqual(split_flag, False)
