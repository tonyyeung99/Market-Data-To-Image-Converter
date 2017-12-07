import unittest

import numpy as np
import numpy.testing as nptest
import source.market_data_2_image.data_transformer as transformer
import source.market_data_2_image.market_data_extracts as extracts


class TestPopOneDayData(unittest.TestCase):
    def setUp(self):
        self.md_date = np.array(['03/06/2012', '03/06/2012', '03/06/2012', '03/07/2012', '03/07/2012', '03/07/2012'])
        self.md_time = np.array(
            ['09:15:00 AM', '09:16:00 AM', '09:17:00 AM', '09:15:00 AM', '09:16:00 AM', '09:17:00 AM'])
        self.md_open = np.array(['21119', '21119', '21126', '22119', '22119', '22126'])
        self.md_high = np.array(['21130', '21127', '21126', '22130', '22127', '22126'])
        self.md_low = np.array(['21101', '21111', '21105', '22101', '22111', '22105'])
        self.md_close = np.array(['21115', '21125', '21108', '22115', '22125', '22108'])
        self.md_volume = np.array(['662', '243', '392', '2662', '2243', '2392'])
        self.extract_obj = extracts.md_extracts(self.md_date, self.md_time, self.md_open, self.md_close, self.md_high,
                                                self.md_low, self.md_volume)

    def test_pop_one_day(self):
        poper = transformer.MarketDataPoper(self.extract_obj)
        one_day_extracts = poper.popOneDayData()
        self.assertEqual(one_day_extracts.md_date.shape[0], 3)
        nptest.assert_array_equal(one_day_extracts.md_time, np.array(['09:15:00 AM', '09:16:00 AM', '09:17:00 AM']))
        nptest.assert_array_equal(one_day_extracts.md_open, np.array(['21119', '21119', '21126']))
        nptest.assert_array_equal(one_day_extracts.md_close, np.array(['21115', '21125', '21108']))
        nptest.assert_array_equal(one_day_extracts.md_high, np.array(['21130', '21127', '21126']))
        nptest.assert_array_equal(one_day_extracts.md_low, np.array(['21101', '21111', '21105']))
        nptest.assert_array_equal(one_day_extracts.md_volume, np.array(['662', '243', '392']))

    def test_pop_one_day_two_times(self):
        poper = transformer.MarketDataPoper(self.extract_obj)
        poper.popOneDayData()
        one_day_extracts = poper.popOneDayData()
        nptest.assert_array_equal(one_day_extracts.md_time, np.array(['09:15:00 AM', '09:16:00 AM', '09:17:00 AM']))
        nptest.assert_array_equal(one_day_extracts.md_open, np.array(['22119', '22119', '22126']))
        nptest.assert_array_equal(one_day_extracts.md_close, np.array(['22115', '22125', '22108']))
        nptest.assert_array_equal(one_day_extracts.md_high, np.array(['22130', '22127', '22126']))
        nptest.assert_array_equal(one_day_extracts.md_low, np.array(['22101', '22111', '22105']))
        nptest.assert_array_equal(one_day_extracts.md_volume, np.array(['2662', '2243', '2392']))

    def test_pop_one_day_three_times(self):
        poper = transformer.MarketDataPoper(self.extract_obj)
        poper.popOneDayData()
        poper.popOneDayData()
        one_day_extracts = poper.popOneDayData()
        nptest.assert_array_equal(one_day_extracts.md_time, np.array([]))
