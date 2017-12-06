import unittest
import source.data.market_data_2_image.HSI_data_extractor as extractor
import source.data.market_data_2_image.market_data_extracts as extracts
import source.app_constants as constants


class TestExtractFile(unittest.TestCase):

    def setUp(self):
        self.extracts_obj = extractor.extract_file(constants.HSI_DATA_DIR ,constants.HSI_DATA_FILE)

    def test_loadNumber(self):
        self.assertEqual(self.extracts_obj.md_date.shape[0], 445874)

    def test_firstLine(self):
        self.assertEqual(self.extracts_obj.md_date[0], '03/06/2012')
        self.assertEqual(self.extracts_obj.md_time[0], '09:15:00 AM')
        self.assertEqual(self.extracts_obj.md_open[0], '21119')
        self.assertEqual(self.extracts_obj.md_close[0], '21130')
        self.assertEqual(self.extracts_obj.md_high[0], '21101')
        self.assertEqual(self.extracts_obj.md_low[0], '21115')
        self.assertEqual(self.extracts_obj.md_volume[0], '662')

if __name__ == '__main__':
    unittest.main()