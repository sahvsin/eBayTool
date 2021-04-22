import bs4
import re
from sys import exit
from requests import get
from requestor import req_URL
from scraper import BIN_scrape, past_scrape
from config import *


"""
4 step process 
1) Provide a URL to request data from the server accessed by it (use "requests" library)
2) Identify the data of interest in the source code of the target webpage (HTML, "inspect element")
3) Extract HTML element containing data of interest (use "bs4", BeautifulSoup library)
4) Aggregate and organize the data in a more digestable form (Table, Spreadsheet, Text, etc)
"""

'''
Step 1
'''
days = 1
r, history_flag, out_file, url = req_URL()


'''
Step 2
'''
#make BeautifulSoup object so I can use its methods to extract data I want
soup = bs4.BeautifulSoup(r.text, 'lxml') 

#first check how many results we got from our eBay search
#two layer tag
#<h1 class="srp-controls__count-heading" ...> for the entire count heading ("X results for Y")
#the first <span class="BOLD" ...> for just the number
count_subsoup = soup.find(name='h1', attrs={'class': 'srp-controls__count-heading'})
search_res = count_subsoup.find(name='span', attrs={'class': 'BOLD'}).get_text()


#if no results then notify user and exit (do nothing, nothing to scrape)

#compute number of pages for the searched item (given 200 listings per page)
#string includes ',' so cannot directly translate to an int (must remove all ',')
#offset number of pages by 1 since indexing starts at 1
num_results = int("".join(search_res.split(',')))
num_pages = (num_results // 201) + 1
#print(num_results)
#print(num_pages)

#parse the data to just the data of every listing of the item of interest 
#each lisitng comprises of data such as the listing title, price, shipping, purchase options ("Buy it now" or "bids"), etc.
#these lisitngs are tagged by <li class=s-item " ....> so the tag name is "li" and the CSS class attribute is "s-item"
#so find each body of data corresponding to these tag parameters to find every relevant listing
all_listings = soup.find_all(name='li', attrs={'class': 's-item'})



'''
Step 3
'''
#if there are less than 200 listings, only look at the listings (avoid stuff like "results with fewer keywords")
if(num_results < 201):
    if(history_flag == 1):
        BIN_scrape(all_listings, out_file, num_res=num_results)
    elif(history_flag == 2):
        past_scrape(all_listings, out_file, num_res=num_results)
else:
    if(history_flag == 1):
        BIN_scrape(all_listings, out_file)
    elif(history_flag == 2):
        past_scrape(all_listings, out_file)


'''
Step 4
'''
#if there is more than 1 page (over 200 listings), go through each one and scrape their listings in batches of 200
if(num_pages > 1):

    for i in range(2, num_pages+1):

        #build new URL for subsequent pages (append page number parameter to original URL) 
        new_url = url+"&_pgn={}".format(i)
        #print(new_url)

        #make the data request from the server at the URL and build the soup object to find all the listings
        req = get(new_url)
        soup = bs4.BeautifulSoup(req.text, 'lxml')
        all_listings = soup.find_all(name='li', attrs={'class': 's-item'})

        if(history_flag == 1):
            BIN_scrape(all_listings, out_file, i)
        elif(history_flag == 2):
            past_scrape(all_listings, out_file, i)
