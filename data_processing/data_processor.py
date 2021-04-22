import pandas as pd
import matplotlib
from date_utils import today_date
from dir_utils import item_selector, date_selector, csv_selector, logistics_path
from csv_utils import write2csv, single_line
from data_aggregation import csv2df
from data_analyzer import month_abbrev2num, month_num2abbrev, analyze_past_data, analyze_current_data



#first decide which csv's data to process
item_name, item_dir = item_selector()
date_dir = date_selector(item_dir)
fname, csv_dir = csv_selector(date_dir)


#labels for the eBay item data (columns in the csv)
labels = ["title", "date", "month", "day", "price", "shipping", "total", "link"]

#read from the selected csv and store the data into a Pandas dataframe
csv_df = csv2df(csv_dir, labels)
#pd.to_numeric(csv_df["price"])


#build the path to save the csv of the logistics data
log_dir = logistics_path(date_dir, fname)


#COMPUTING THE LOGISTICS

#first determine if dealing with current or past listings
if('past' in fname):

    #for past listings
    #first determine today's date
    today = today_date()
    month_num = month_abbrev2num[today[0]]

    #then determine what month it was three months ago (remember base 12) since eBay listings are archived for 90 days only
    three_months_ago = month_num + 9
    month_num = month_num + 12

    analyze_past_data(item_name, csv_df, three_months_ago, month_num, labels, log_dir)

elif('active' in fname):
    
    #for current listings
    analyze_current_data(item_name, csv_df, labels, log_dir)
