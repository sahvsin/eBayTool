from date_utils import today_date
import requests
from config import *
from csv_utils import csv_printer


def req_URL(url=None):
    '''
    requests data from server accessed by a provided eBay URL or if no or incorrect url is provided, the
    user is asked a series of questions to build the eBay URL which is then used to build a CSV of 
    all of the listings pulled from the item(s) searched by the URL 

    Inputs:
    url -- a possibly passed URL string (input by the user)

    Outputs:
    if the url is valid:
      req -- the requested data if the url exists
    otherwise:
      req -- the data requested from the finally valid url
      history_flag -- integer determining whether to process [1] current or [2] past listings
      csv_file -- CSV of listings data
      url -- a new URL of the specific listing with added parameters
    '''

    #user passed in URL already, check if it is valid and actually eBay search query
    if(url != None and url[:25] == "https://www.ebay.com/sch/"):
        
        #try to see if it's valid (not 404 or nonexistent)
        try:

            #request data from the server at the provided URL
            req = requests.get(url)

            #check the status of the request (200 - success, otherwise - error/fail)
            req.raise_for_status()  #returns None if success, otherwise raises Exception

        #if any exceptions occur (404 error or nonexistent page or "get" times out)
        except Exception:
            print("Nonexistent Page!\n")
        
        #if no exception occured, then done, simply return the data requested
        else:
            return req

    #if no url provided, ask the user to provide one (keep asking until valid))
    def get_URL():
        '''
        requests user to input item to search for on eBay and other parameters then builds the appropriate URL

        Outputs:
        ebay_url -- the (valid) eBay URL built from the user responses
        history_flag -- integer determining whether to process [1] current or [2] past listings
        csv_file -- CSV of listings data
        '''

        #first ask for what to search for on ebay
        search_key = input("Enter item to search for in eBay.\nAdd \"-\" before the keyword to avoid it when searching for listings.\n\n")
        split_search = search_key.split()
        formatted_search = "+".join(split_search) 


        #request category
        print("\nPlease choose one of the following categories that best associates with your item (enter the associated number in the square brackets)")        
        category = input(csv_printer(ebay_cat_csv))
        category = category + '/'


        #request other parameters
        history_param = input("\nCurrent or Past Listings?\n  [1] Current\n  [2] Past\n")
        if(history_param == '1' or history_param == '[1]' or history_param == 'Current'):
            history_param = ""
            history_flag = 1
            listings = "active_"
        elif(history_param == '2' or history_param == '[2]' or history_param == 'Auction'):
            history_param = "&LH_Sold=1&LH_Complete=1"
            history_flag = 2
            listings = "past_"
        #either try again or go with a default
        else:
            history_param = ""
            history_flag = 1
            listings = "active_"

        #if processing current listings, ask the user to choose between only BIN or only auctions (not both)
        #if processing past listings, do all of them
        if(history_flag == 1):
            buying_format = input("\nBuying Format:\n  [1] Buy it now\n  [2] Auction\n")
            if(buying_format == '1' or buying_format == '[1]' or buying_format == 'Buy it now'):
                buying_format = "&LH_BIN=1"
                buy_form = "BIN_" + listings + "listings"
            elif(buying_format == '2' or buying_format == '[2]' or buying_format == 'Auction'):
                buying_format = "&LH_Auction=1"
                buy_form =  "auction_" + listings + "listings"
            else:
                buying_format = "&LH_BIN=1"
                buy_form = "BIN_" + listings + "listings"
        elif(history_flag == 2):
            buying_format = "&LH_ALL=1"
            buy_form = "all_" + listings + "listings"

        params = buying_format + history_param


        '''
        sort_param = input("\nSort by:\n  [1] Price+Shipping Lowest\n  [2] Price+Shipping Highest\n  [3] Most Recent (Newly Listed)\n")
        if(sort_param == '1' or sort_param == '[1]' or sort_param == 'Lowest' or sort_param == 'Price+Shipping Lowest'):
            sort_param = "15"
        elif(sort_param == '2' or sort_param == '[2]' or sort_param == 'Highest' or sort_param == 'Price+Shipping Highest'):
            sort_param = "16"
        elif(sort_param == '3' or sort_param == '[3]' or sort_param == 'Most Recent' or sort_param == 'Newly Listed'):
            sort_param = "10"
        #either try again or go with a default (Most Recent)
        else:
            buying_format = "10"
        '''

        if(history_flag == 1):
            sort_param = "15"
        elif(history_flag == 2):
            sort_param = "10"
        ebay_url = "https://www.ebay.com/sch/{cat}/i.html?_from=R40&_nkw={searchkey}&_sop={sort_by}&_ipg=200&rt=nc{last_params}&LH_ItemCondition=1000|1500|2000|2500|2750|3000|4000|5000|6000".format(cat = category, searchkey = formatted_search, sort_by = sort_param, last_params = params)
        print(ebay_url)


        #get today's date as part of the save name for the csv for today's search
        today = "-".join(today_date())

        outer_dir = os.path.join(ebay_item_dir, "eBay_" + formatted_search)

        #create the destination path for the csv (make the directory if necessary)
        try:
            os.mkdir(outer_dir)
        except OSError as error:
            #print("Error")
            pass

        inner_dir = os.path.join(outer_dir, today)

        try:
            os.mkdir(inner_dir)
        except OSError as error:
            #print("Error")
            pass

        csv_file = os.path.join(inner_dir, buy_form + ".csv")
        

        return ebay_url, history_flag, csv_file


    #psuedo Do-while loop (input validation)
    while True:
        try:
            url, history_flag, csv_file = get_URL()

            #make the data request from the server at the URL
            req = requests.get(url)

            #check the status of the request (200 - success, otherwise - fail)
            req.raise_for_status()    #returns None if success, otherwise Exception

        except Exception:
            #raise_for_status was raised, try another URL (continue to next loop, DO NOT execute RETURN)
            print(url)
            print("Nonexistent Page!\n")
            continue
        
        #no exceptions raised, return the data requested
        return req, history_flag, csv_file, url
