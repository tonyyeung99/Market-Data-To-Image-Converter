############################################
# Main program - Transform the market data to scaled images and label the data:
# 1. Read the market data file
# 2. Parsing the raw data
# 3. Scaling the raw data and fit it in the size of one image
# 4. Export the image data
# 5. Also calculate the label file - label whether the trading day rise/drop in the last 30 minutes
############################################

import numpy as np
import math
import cv2
import source.app_constants as const
import source.data.market_data_2_image.HSI_data_extractor as extractor
import source.data.market_data_2_image.data_input_output_splitter as pk_split
import source.data.market_data_2_image.data_scaler as pk_scale
import source.data.market_data_2_image.data_transformer as transform
import source.data.market_data_2_image.y_labeler as pk_y_label
import os

def drawDayGraph(y_values):
    for i in range(1 , len(y_values)):
        drawLine([i-1,y_values[i-1]], [i,y_values[i]])

def drawLine(point1, point2):
    ptX1 = point1[0]
    ptY1 = int(math.floor(point1[1]))
    ptX2 = point2[0]
    ptY2 = int(math.floor(point2[1]))
    cv2.line(img, (ptX1, ptY1), (ptX2, ptY2), (255, 0, 0), 1)

def isEmptyDataPopulated(one_day_extracts):
    return len(one_day_extracts.md_date) <= 0

#initialize the path variables
current_dir = os.getcwd()
import_path = os.path.join(current_dir, "../../../data/import"+ const.HSI_DATA_FILE)

#extract the raw data from the market data files
extracts_obj = extractor.extract_file(import_path)
#Prepare the market data populator
poper = transform.MarketDataPoper(extracts_obj)

currentIndex = 0
label_file_buffers = []
label_file_buffers.append('index, date, isRise20Pct, isRise40Pct, refMax, refMin, v_scale\n')
while True :
    one_day_extracts = poper.popOneDayData()

    #if(len(one_day_extracts.md_date)<=0):
    if(isEmptyDataPopulated(one_day_extracts)):
        break
    else:
        img = np.zeros((const.HSI_IMAGE_HEIGHT, const.HSI_IMAGE_WIDTH, 3), np.uint8)
        #Split the one day into two parts: first 300 mintues as input, the remaining data as output
        spliter = pk_split.input_output_splitter(one_day_extracts,const.HSI_IMAGE_WIDTH)
        split_flag, input_obj, outputobj = spliter.split()
        if(split_flag == False) :
            continue
        #Scale the input data to fit into the size of one image
        scaler = pk_scale.md_data_scaler(input_obj)
        input_obj, max, min, v_scale = scaler.scale(const.HSI_IMAGE_HEIGHT)
        #Plot the price graph by using the scaled input data
        drawDayGraph(input_obj.md_close)
        currentIndex = currentIndex + 1

        #Export the plotted images
        export_prefix = os.path.join(current_dir, "../../../data/export/" + const.HSI_DATA_EXPORT_PREFIX)
        cv2.imwrite(export_prefix + str(currentIndex) + '.png', img)

        #Calculate the label value(label the movement percentage input/output)
        labeler = pk_y_label.y_labeler(outputobj, max, min, v_scale, const.HSI_IMAGE_HEIGHT)
        isOver20Pct = int(labeler.isLabelPositive(1, 0.2))
        isOver40Pct = int(labeler.isLabelPositive(1, 0.4))

        temp_str = str(currentIndex) + ', ' + input_obj.md_date[0] + ', ' + str(isOver20Pct) + ', ' + str(isOver40Pct) + ', ' + str(max) + ', ' + str(min) + ', ' + str(v_scale) + '\n'
        label_file_buffers.append(temp_str)


#Write the label files buffer to lable files
label_file = os.path.join(current_dir, "../../../data/export/"+const.HSI_LABEL_FILE);
f = open(label_file, 'w')
for line in label_file_buffers:
    f.write(line)



