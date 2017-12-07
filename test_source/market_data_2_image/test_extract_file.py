import unittest

import source.market_data_2_image.HSI_data_extractor as extractor
import source.market_data_2_image.app_constants as constants
import os

class TestExtractFile(unittest.TestCase):

    def setUp(self):
        current_dir = os.getcwd()
        import_path = os.path.join(current_dir, "../../data/import" + constants.HSI_DATA_FILE)
        self.extracts_obj = extractor.extract_file(import_path)
        #self.extracts_obj = extractor.extract_file(constants.HSI_DATA_DIR ,constants.HSI_DATA_FILE
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