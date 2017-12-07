############################################
# Main program - Transform the market data to scaled images and label the data:
# 1. Read the market data file
# 2. Parsing the raw data to market data
# 3. Scaling the market data and fit it in the size of one image
# 4. Export the image data
# 5. Also calculate the label file - label whether the trading day rise/drop in the last 60 minutes
############################################

import math
import os
import cv2
import numpy as np
# import source.market_data_2_image.MarketDataSplitter as market_data_spliter
from source.market_data_2_image.data_input_output_splitter import MarketDataSplitter as market_data_splitter
# rket_data_2_image.data_scaler as market_data_scaler
from source.market_data_2_image.data_scaler import MarketDataScaler as market_data_scaler
import source.market_data_2_image.data_transformer as market_data_transformer
import source.market_data_2_image.y_labeler as market_data_labeler
import source.market_data_2_image.HSI_data_extractor as market_data_extractor
import source.market_data_2_image.app_constants as const


def draw_day_chart(price_data, img):
    for i in range(1, len(price_data)):
        draw_line([i - 1, price_data[i - 1]], [i, price_data[i]], img)


def draw_line(point1, point2, img):
    pt_x1 = point1[0]
    pt_y1 = int(math.floor(point1[1]))
    pt_x2 = point2[0]
    pt_y2 = int(math.floor(point2[1]))
    cv2.line(img, (pt_x1, pt_y1), (pt_x2, pt_y2), (255, 0, 0), 1)


def is_empty_data(one_day_extracts):
    return len(one_day_extracts.md_date) <= 0


def process_one_day_data(one_day_extracts, label_file_buffers, currentIndex):
    img = np.zeros((const.HSI_IMAGE_HEIGHT, const.HSI_IMAGE_WIDTH, 3), np.uint8)

    # Split the one day into two parts: first 300 mintues as input, the remaining data as output
    spliter = market_data_splitter(one_day_extracts, const.HSI_IMAGE_WIDTH)
    split_flag, input_obj, output_obj = spliter.split()

    # unable to split the data
    if (split_flag == False):
        return

    # Scale the input data to fit into the size of one image
    scaler = market_data_scaler(input_obj)
    input_obj, max, min, v_scale = scaler.scale(const.HSI_IMAGE_HEIGHT)

    # Plot the price graph by using the scaled input data
    draw_day_chart(input_obj.md_close, img)

    # Export the plotted images
    save_image_file(currentIndex, img)

    process_label_logic(currentIndex, input_obj, label_file_buffers, max, min, output_obj, v_scale)


def process_label_logic(currentIndex, input_obj, label_file_buffers, max, min, output_obj, v_scale):
    # Calculate the label value(label the movement percentage input/output)
    labeler = market_data_labeler.y_labeler(output_obj, max, min, v_scale, const.HSI_IMAGE_HEIGHT)
    is_over_20_pct = int(labeler.isLabelPositive(1, 0.2))
    is_over_40_pct = int(labeler.isLabelPositive(1, 0.4))
    temp_str = str(currentIndex) + ', ' + input_obj.md_date[0] + ', ' + str(is_over_20_pct) + ', ' + str(
        is_over_40_pct) + ', ' + str(max) + ', ' + str(min) + ', ' + str(v_scale) + '\n'
    label_file_buffers.append(temp_str)


def save_image_file(currentIndex, img):
    export_prefix = os.path.join(current_dir, "../../data/export/" + const.HSI_DATA_EXPORT_PREFIX)
    cv2.imwrite(export_prefix + str(currentIndex) + '.png', img)


def process_data():
    # initial the buffer writing to the label file
    label_file_buffers = []
    label_file_buffers.append('index, date, isRise20Pct, isRise40Pct, refMax, refMin, v_scale\n')

    currentIndex = 1
    one_day_extracts = poper.popOneDayData()
    while not is_empty_data(one_day_extracts):
        process_one_day_data(one_day_extracts, label_file_buffers, currentIndex)
        one_day_extracts = poper.popOneDayData()
        currentIndex = currentIndex + 1

    write_label_file(label_file_buffers)


def write_label_file(label_file_buffers):
    # Write the buffer to label file
    label_file = os.path.join(current_dir, "../../data/export/" + const.HSI_LABEL_FILE)
    f = open(label_file, 'w')
    for line in label_file_buffers:
        f.write(line)


if __name__ == '__main__':
    # initialize the path variables
    current_dir = os.getcwd()
    import_path = os.path.join(current_dir, "../../data/import" + const.HSI_DATA_FILE)

    # extract the raw data from the market data files
    extracts_obj = market_data_extractor.extract_file(import_path)

    # Prepare the market data populator
    poper = market_data_transformer.MarketDataPoper(extracts_obj)

    process_data()
