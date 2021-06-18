import bs4
import re



def text_scrape(listing, tag, id_type, attr):
    '''
    scrapes for first element tagged by the provided tag with an attribute of the provided identifier type
    assumes the element of interest is text

    Inputs:
    listing - the item/content to scrape
    tag - string type object
    id_type - string type object
    attr - string type object

    Output:
    webscraped text
    '''

    return bs4.BeautifulSoup(str(listing.find(name=tag, attrs={id_type: attr})), 'lxml').get_text()




def datetime_check(today, l_time, t_period):
    '''
    determines whether the listing falls within the chosen period from the current date/time
    '''

    #if current hour is 0
    if(today[2] == 0):
        #if minutes less than the time period, then consider yesterday's lisitngs in the late 23 hour
        if(today[3] < t_period):
            t_diff = today[3] - t_period
            t_cutoff = 60 + t_diff
            if(l_time[2] == 23 and l_time[3] >= t_cutoff):
                #next check the date, is it the first of the month, if so yesterday is a day in last month
                if(today[1] == 1):
                    if(today[0] == month_dig2abbrev[1+month_abbrev2dig[l_time[0]]] and l_time[1] == num_days_in_month[l_time[0]]):
                        return True        
                    else:
                        return False
                else:
                    #not first in the month, so listing month must be same
                    if(today[0] == l_time[0] and l_time[1] == today[1] - 1):
                        return True
                    else:
                        return False
            else:
                return False
        else:
            #chceking today's listings, are they within the period (same month, day, hour)
            if(l_time[0] == today[0] and l_time[1] == today[1] and l_time[2] == today[2]):
                #check if the listing minutes is within the period
                if(l_time[3] >= today[3] - t_period):
                    return True
                else:
                    return False
            else:
                return False
    #hour not 0, no need to worry about rolling back day or month
    else:
        #more general case, check if month and day are the same
        if(today[0] == l_time[0] and today[1] == l_time[1]):
            #check if current time's minutes is less than the time period, then must consider listings of previous hour
            if(today[3] < t_period):
                t_diff = today[3] - t_period
                t_cutoff = 60 + t_diff
                if(l_time[2] == today[2]-1 and l_time[3] >= t_cutoff):
                    return True
                else:
                    #check for listings in same hour but within the time period
                    if(l_time[2] == today[2] and l_time[3] >= today[3] - t_period):
                        return True
                    else:
                        return False
            else:
                #otherwise just check if it's in the same hour and within the period
                if(l_time[2] == today[2] and l_time[3] >= today[3] - t_period):
                    return True
                else:
                    return False
        else:
            return False





def compute_price(listing):
    '''
    compute the current total price (includes shipping) of the listing
    '''

    #listing passes date check, now process the price (less than threshold?)
    listing_price = text_scrape(listing, 'span', 'class', 's-item__price')
    try:
        listing_price = float(listing_price[1:].replace(',', ''))
    except ValueError:
        return None

    listing_shipping = text_scrape(listing, 'span', 'class', 's-item__shipping s-item__logisticsCost')
    if(listing_shipping == "Free shipping"):
        shipping = '0'
    elif(listing_shipping == "None"):
        return None
    else:
        shipping = re.sub('[^0-9.]', '', listing_shipping)

    return listing_price + float(shipping)




def scrape_the_listing(listing, total_price):
    '''
    scrapes the title and link of the passed listing (implies date and price checks passed)
    '''
    
    dat = []

    listing_title = text_scrape(listing, 'h3', 'class', 's-item__title')
    dat.append(listing_title)

    dat.append(str(total_price))
    
    for listing_links in listing.find_all(name='a', attrs={'href': re.compile('^https://www.ebay.com/itm/')}):
        listing_link = listing_links.get('href')
        dat.append(listing_link)
        break

    return dat





def listing_scrape(all_listings, today, t_period, price_thresh):
    '''
    given a collection of souped listings, scrape data from each individual listing within the past time period
    '''



    from date_utils import listing_date_parser

    #mapping month representations (abbrev -> two-digit, vice-versa)
    month_abbrev2dig = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
    month_dig2abbrev = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec', 13: 'Jan', 14: 'Feb', 15: 'Mar', 16: 'Apr', 17: 'May', 18: 'Jun', 19: 'Jul', 20: 'Aug', 21: 'Sep', 22: 'Oct', 23: 'Nov', 24: 'Dec'}
    
    #mapping months to number of days (doesn't count leap years for February)
    num_days_in_month = {'Jan': 31, 'Feb': 28, 'Mar': 31, 'Apr': 30, 'May': 31, 'Jun': 30, 'Jul': 31, 'Aug': 31, 'Sep': 30, 'Oct': 31, 'Nov': 30, 'Dec': 31}

    all_scrapings = []

    for i, listing in enumerate(all_listings):

        #skip first item b/c not actually a listing (Starts at i==1)
        if(i==0):
            continue

        #first check the time of listing (when it started)
        #if over 15 minutes ago, exit the loop, done scraping
        listing_time = text_scrape(listing, 'span', 'class', 's-item__listingDate')
       
        #print(i)
        #print(listing_time)

        #break the date into its components
        l_time = listing_date_parser(listing_time)
        #print(l_time)
            
        #compare with current time
        if(datetime_check(today, l_time, t_period)):

            #print("\nThis is NEW\n")
            total_price = compute_price(listing)
            
            if(total_price is None):
                continue

            if(total_price <= float(price_thresh)):
                #print("\n\nTHIS IS A GOOD DEAL!!!\n\n")
                all_scrapings.append(scrape_the_listing(listing, total_price))

        else:
            break

               
    print("\nFinished\n")
    return all_scrapings



def scrape(query, cur_time, t_period, price_thresh):
    '''
    scrape the listings provided by the url for the past time period
    '''

    from requestor import make_request

    #make the data request first
    req = make_request(query)

    #if failed request, cannot scrape so return (0/nothing?, will see later how to handle this)
    if(req == 0):
        return

    #make the BeautifulSoup object to extract data off the provided URL
    soup = bs4.BeautifulSoup(req.text, 'lxml')

    #first check how many results wre returned from the search
    count_subsoup = soup.find(name='h1', attrs={'class': 'srp-controls__count-heading'})
    search_res = count_subsoup.find(name='span', attrs={'class':'BOLD'}).get_text()
    num_res = int(search_res.replace(',', ''))

    #if no results, nothing to scrape (do nothing and return?)
    if(num_res == 0):
        return

    #compute number of pages for the searched item (given 200 listings per page)
    num_pages = (num_res // 201) + 1

    #parse the data to just the data of every listing of the searched item
    all_listings = soup.find_all(name='li', attrs={'class': 's-item'})

    #break the (mmm-dd HH:MM) date format to individual components to process
    parsed_date = [cur_time[:3], int(cur_time[4:6]), int(cur_time[7:9]), int(cur_time[10:])]
    #print(parsed_date)

    return listing_scrape(all_listings, parsed_date, t_period, price_thresh)
