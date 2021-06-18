#import emailing stuff
import pandas as pd
from date_utils import current_date
from csv_utils import csv_reader, write2csv, append2csv, single_line, delete_csv
from scraper import scrape
from emailer import send_email


#ebay items categorized as NEWLY LISTED are listed within 24 hours of current date/time
#use Linux cron to run this script at some time interval (every 30 minutes, every hour, etc.)

all_scrapings = []
csv_in = "items.csv"
csv_out = "cheap_eBay_listings.csv"
time_period = 45    #minutes (must be less than 60)

#ENTER EMAIL ADDRESSES HERE
sender = "sender@domain.com"
destination = "destination@domain.com"

#determine today's date and time
now = current_date()


#read the local "items.csv" file to get the search parameters to build each URL to poll
all_queries = csv_reader(csv_in)

#print(all_queries)

#go through each search query and scrape the appropriate listings
for query in all_queries:

    all_scrapings.append(scrape(query, now, time_period, query[3]))


#go through all the scrapings and store them in a local csv
for i, scrapings in enumerate(all_scrapings):

    if(i==0):
        single_line(all_queries[i][0], csv_out, 'w')
    else:
        single_line(all_queries[i][0], csv_out, 'a')
    
    append2csv(scrapings, csv_out)
    single_line("", csv_out, 'a')

    
#now email the csv to the person
send_email(sender, destination, "", csv_out)

#destroy the csv (meant to only be temporary)
delete_csv(csv_out)
