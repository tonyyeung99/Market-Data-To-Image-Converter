import numpy as np
import source.data.market_data_2_image.market_data_extracts as extracts
############################################
#  Class MarketData: An Object represent 1 minute data
#############################################

class MarketData:
    def __init__(self, _date, md_time, md_open, md_close, md_high, md_low, md_volume):
        self._date = _date
        self.md_time = md_time
        self.md_open = md_open
        self.md_close = md_close
        self.md_high = md_high
        self.md_low = md_low
        self.md_volume = md_volume

############################################
#  Class MarketDataPoper: Populate one day market data
#############################################
class MarketDataPoper:
    def __init__(self, extract_obj):
        self.md_date = extract_obj.md_date
        self.md_time = extract_obj.md_time
        self.md_open = extract_obj.md_open
        self.md_close = extract_obj.md_close
        self.md_high = extract_obj.md_high
        self.md_low = extract_obj.md_low
        self.md_volume = extract_obj.md_volume

    def popOneDayData(self):
        # if self.md_date is None
        #     return extracts.md_extracts(np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]))
        # if self.md_date.shape[0] < 1:
        #     return extracts.md_extracts(np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]), np.array([]))
        if self.md_date is None or self.md_date.shape[0] < 1:
            return extracts.md_extracts(np.array([]), np.array([]), np.array([]), np.array([]), np.array([]),
                                        np.array([]), np.array([]))

        currentDay = self.md_date[0]
        nextDayIndex = 0
        for dayIndex in range(self.md_date.shape[0]):
            if currentDay != self.md_date[dayIndex]:
                nextDayIndex = dayIndex
                break
        if nextDayIndex ==0 :
            nextDayIndex = self.md_date.shape[0]
        oneDayDate, self.md_date = np.split(self.md_date, [nextDayIndex])
        oneDayTime, self.md_time = np.split(self.md_time, [nextDayIndex])
        oneDayOpen, self.md_open = np.split(self.md_open, [nextDayIndex])
        oneDayClose, self.md_close = np.split(self.md_close, [nextDayIndex])
        oneDayHigh, self.md_high = np.split(self.md_high, [nextDayIndex])
        oneDayLow, self.md_low = np.split(self.md_low, [nextDayIndex])
        oneDayVolume, self.md_volume = np.split(self.md_volume, [nextDayIndex])
        extract_obj = extracts.md_extracts(oneDayDate, oneDayTime, oneDayOpen, oneDayClose, oneDayHigh,oneDayLow, oneDayVolume )
        return extract_obj
