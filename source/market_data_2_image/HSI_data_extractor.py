import numpy as np

import source.market_data_2_image.market_data_extracts as extracts


############################################
#  Extract the raw data from market data file
#############################################
def extract_file(train_file):

    data_file = open(train_file)
    data_file_header = data_file.readline();

    file_data = []
    for line in data_file:
        if (len(line.strip()) > 0):
            file_data.append(line)

    data_file_header = [x for x in data_file_header.split(',') if len(x) >= 1]
    data_by_field = [[x for x in y.split(',') if len(x) >= 1] for y in file_data if len(y) >= 1]

    md_date = np.array([x[0].strip() for x in data_by_field])
    md_time = np.array([x[1].strip() for x in data_by_field])
    md_open = np.array([x[5].strip() for x in data_by_field])
    md_close = np.array([x[6].strip() for x in data_by_field])
    md_high = np.array([x[7].strip() for x in data_by_field])
    md_low = np.array([x[8].strip() for x in data_by_field])
    md_volume = np.array([x[9].strip() for x in data_by_field])
    extracts_obj = extracts.md_extracts(md_date, md_time, md_open, md_close, md_high, md_low, md_volume)
    data_file.close()

    return extracts_obj
