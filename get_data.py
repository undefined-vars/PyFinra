import datetime
import requests
import urllib.request
from bs4 import BeautifulSoup
from bs4.element import Comment
from collections import defaultdict
import matplotlib.pyplot as plt

################################################################
#constants:
#NOTE: Don't edit this section unless you know what you are doing
FINAL_DATA_URL = "http://regsho.finra.org/CNMSshvol{}.txt" #ex: "http://regsho.finra.org/CNMSshvol20210201.txt"
FINRA_DATA_HEADING = ["Date", "Symbol", "ShortVolume", "ShortExemptVolume", "TotalVolume", "Market"]
SYMBOL_POSITION_INDEX = 1
SHORT_VOLUME_POSITION_INDEX = 2
TOTAL_VOLUME_POSITION_INDEX = 4
FINRA_TXT_FILE_DELIMETER = "|"
################################################################

#helper functions:
def get_data_string_for_stock_from_finra_url(finra_url,symbol):
    try:
        file = urllib.request.urlopen(finra_url)
        for line in file:
            data = line.decode("utf-8").strip().split(FINRA_TXT_FILE_DELIMETER)
            if len(data) > SYMBOL_POSITION_INDEX and symbol.strip() == data[SYMBOL_POSITION_INDEX].strip():
                return data
        return []
    except:
        return []

def get_short_interest_percent_from_data(data):
    #Formula: Percent = (ShortVolume/TotalVolume) * 100
    error_occured = False

    if len(data) > max(SHORT_VOLUME_POSITION_INDEX, TOTAL_VOLUME_POSITION_INDEX):
        short_volume_str = data[SHORT_VOLUME_POSITION_INDEX]
        total_volume_str = data[TOTAL_VOLUME_POSITION_INDEX]

        if short_volume_str.isdigit() and total_volume_str.isdigit():
            return (int(short_volume_str)/int(total_volume_str)) * 100
    return -1
    
def generates_dates_in_range_in_last_n_days(n_days):
    base = datetime.datetime.today()
    return [base - datetime.timedelta(days=x) for x in range(n_days)]

def get_date_string_from_datetime_object(datetime_object):
    return "{}{:02d}{:02d}".format(datetime_object.year,datetime_object.month,datetime_object.day)

def get_human_readable_date_string(datetime_object):
    return "{:02d}/{:02d}/{}".format(datetime_object.month,datetime_object.day,datetime_object.year)


#functions:
def print_short_interest_percent_in_human_readable_form_for_last_n_days(n_days, symbol):
    dates = generates_dates_in_range_in_last_n_days(n_days)
    date_and_percents = []

    for each_date in reversed(dates):
        url_date_str = get_date_string_from_datetime_object(each_date)
        url = FINAL_DATA_URL.format(url_date_str)
        data = get_data_string_for_stock_from_finra_url(url,STOCK_SYMBOL)
        if data != []:
            short_interest_percent = get_short_interest_percent_from_data(data)
            if short_interest_percent >= 0:
                date_and_percents.append((get_human_readable_date_string(each_date),short_interest_percent))

 
    if len(date_and_percents) > 0:
        print("{} short interest from all reports (found within the) last {} days".format(symbol, n_days))
        for each_day, each_percent in date_and_percents:
            print(each_day, "{:.2f}%".format(each_percent))
    else:
        print("No data found for {} in last {} days, double check symbol, or try extending date range".format(symbol, n_days))

            
def generate_graph_of_short_nterest_percent_for_last_n_days(n_days, symbol):
    dates = generates_dates_in_range_in_last_n_days(n_days)

    dates_to_plot = []
    percents_to_plot = []

    for each_date in reversed(dates):
        url_date_str = get_date_string_from_datetime_object(each_date)
        url = FINAL_DATA_URL.format(url_date_str)
        data = get_data_string_for_stock_from_finra_url(url,STOCK_SYMBOL)
        if data != []:
            short_interest_percent = get_short_interest_percent_from_data(data)
            if short_interest_percent >= 0:
                dates_to_plot.append(each_date)
                percents_to_plot.append(short_interest_percent)

    #generate figure:
    plt.plot(dates_to_plot,percents_to_plot)
    plt.title("Daily Short Interest Percent Reported to FINRA for {} over part {} days".format(symbol,n_days))
    plt.xlabel("Days")
    plt.ylabel("Short Interest Percent [%] = (ShortVolume/TotalVolume) * 100%")
    
    # beautify the x-labels
    plt.gcf().autofmt_xdate() #source: https://stackoverflow.com/a/16428019/13544635
    plt.show()
    


if __name__ == "__main__":
    #example 1: print daily short interest percent for GME for all reports within last 10 days
    NUMBER_OF_DAYS = 10
    STOCK_SYMBOL = "GME"
    print_short_interest_percent_in_human_readable_form_for_last_n_days(NUMBER_OF_DAYS, STOCK_SYMBOL)

    #example 2: print daily short interest percent for GME for all reports within last 50 days
    NUMBER_OF_DAYS = 50
    STOCK_SYMBOL = "GME"
    generate_graph_of_short_nterest_percent_for_last_n_days(NUMBER_OF_DAYS, STOCK_SYMBOL)
        
        

    
