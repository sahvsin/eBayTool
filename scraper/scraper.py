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


def BIN_scrape(all_listings, out_file, res_pg_num=1, num_res=200):
    '''
    scraping data specifically from Buy It Now listings

    Inputs:
    all_listings - collection of all of the listings scraped
    out_file - csv file (string/name) to save/write scraped data into
    res_pg_num - integer of eBay search results page number
    num_res - integer number of search results this page (defaults to 200)

    Outputs:
    data scraped from each listing
    '''

    from csv_utils import write2csv, append2csv

    #go through each listing and extract relevant information
    #NOTE: to extract the meaningful text (using get_text), must re-soup after find/find_all (otherwise error)
    for i, listing in enumerate(all_listings):
        
        #skip first searched/found soup because it's not an actual listing (listings start at i = 1)
        if(i==0):
            continue

        if(i>num_res+1):
            return
    

        #temporary storage
        dat = []

        #get the name/title of the listing
        #tagged by <h3 class="s-item__title" ...>
        listing_title = text_scrape(listing, 'h3', 'class', 's-item__title')
        dat.append(listing_title)

        #start with the end date of the listing
        #tagged by <span class="s-item__ended-date s-item__listingDate" ...>
        listing_date = text_scrape(listing, 'span', 'class', 's-item__listingDate')
        dat.append(listing_date)

        #reformat to (mmm, dd) to store the date for easier processing later
        dat.append(listing_date[:3])
        dat.append(listing_date[4:6])

        #grab its price
        #tagged by <span class="s-item__price" ...>
        listing_price = text_scrape(listing, 'span', 'class', 's-item__price')
        #skip the dollar sign and remove commas (makes later processing easier)
        try: 
            #listing_price = float("".join(listing_price[1:].split(',')))
            listing_price = float(listing_price[1:].replace(',', ''))
        except ValueError:
            continue
        dat.append(str(listing_price))

        #grab its shipping
        #tagged by <span class="s-item__shipping s-item__logisticsCost" ...>
        #NOTE: for tags with multiple CSS classes, better to use CSS selector
        #i.e. select("span.s-item__shipping.s-item__logisticsCost")
        #or just find_all("span", attrs={"class": "s-item__shipping s-item__logisticsCost"})
        #print()
        listing_shipping = text_scrape(listing, 'span', 'class', 's-item__shipping s-item__logisticsCost')
        if(listing_shipping == "Free shipping"):
            shipping = '0'
        #METHOD 1: manually check for empty or "Not specified" shipping, if not, get the middle 4 characters (may miss a digit or two)
        elif(listing_shipping  == "None"):   # or listing_shipping == "Shipping not specified"):
            continue
        else:
            #shipping = listing_shipping[2:6]
            #METHOD 2: use regex to remove all but digits and decimal (.)
            shipping = re.sub('[^0-9.]', '', listing_shipping)
        dat.append(shipping)

        #total price (selling price + shipping)
        total_price = listing_price + float(shipping)
        dat.append(str(total_price))


        #grab its link
        #tag: <a href="https://...">
        #little different to extract since link is the attribute
        #iterate through all 'a' tags with the ebay item URL CSS class attribute
        #use regex to specifically search for ebay item URL strings
        for listing_links in listing.find_all(name='a', attrs={'href': re.compile('^https://www.ebay.com/itm/')}):
            listing_link = listing_links.get('href')
            #print(listing_link)
            dat.append(listing_link)
            #break after getting first appropriate link, rest are redundant
            break

        if(i == 1 and res_pg_num == 1):
            write2csv(dat, out_file)
        else:
            append2csv(dat, out_file)



def past_scrape(all_listings, out_file, res_pg_num=1, num_res=200):
    '''
    scraping data specifically from past (sold/completed) listings

    Inputs:
    all_listings - collection of all of the listings scraped
    out_file - csv file to save/write scraped data into
    res_pg_num - integer of eBay search results page number
    num_res - integer number of search results this page (defaults to 200)

    Outputs:
    data scraped from each listing
    '''

    from csv_utils import write2csv, append2csv

    #go through each listing and extract relevant information
    #NOTE: to extract the meaningful text (using get_text), must re-soup after find/find_all (otherwise error)
    for i, listing in enumerate(all_listings):
       
        #skip first searched/found soup because it's not an actual listing (listings start at i = 1)
        if(i==0):
            continue

        if(i>num_res+1):
            return
    

        #temporary storage
        dat = []

        #index
        #print('[{}]'.format(i))

        #get the name/title of the listing
        #tagged by <h3 class="s-item__title" ...>
        listing_title = text_scrape(listing, 'h3', 'class', 's-item__title')
        #remove the "NEW LISTING" tag from the title
        if(listing_title[:11] == "New Listing"):
            listing_title = listing_title[11:]
        #semicolons mess with csv structure
        listing_title = listing_title.replace(';', '.')
        dat.append(listing_title)

        #start with the end date of the listing
        #tagged by <span class="s-item__ended-date s-item__endedDate" ...>
        listing_date = text_scrape(listing, 'span', 'class', 's-item__endedDate')
        dat.append(listing_date)

        #reformat (mmm, dd) and store the date
        dat.append(listing_date[:3])
        dat.append(listing_date[4:6])

        #grab its price
        #tagged by <span class="s-item__price" ...>
        listing_price = text_scrape(listing, 'span', 'class', 's-item__price')
        #skip the dollar sign and comma (makes later processing easier)
        try: 
            #listing_price = float("".join(listing_price[1:].split(',')))
            listing_price = float(listing_price[1:].replace(',', ''))
        except ValueError:
            continue
        dat.append(str(listing_price))

        #grab its shipping
        #tagged by <span class="s-item__shipping s-item__logisticsCost" ...>
        #NOTE: for tags with multiple CSS classes, better to use CSS selector
        #i.e. select("span.s-item__shipping.s-item__logisticsCost")
        #or just find_all("span", attrs={"class": "s-item__shipping s-item__logisticsCost"})
        listing_shipping = text_scrape(listing, 'span', 'class', 's-item__shipping s-item__logisticsCost')
        if(listing_shipping == "Free shipping"):
            shipping = '0'
        #METHOD 1: manually check for empty or "Not specified" shipping, if not, get the middle 4 characters (may miss a digit or two)
        elif(listing_shipping  == "None"):   # or listing_shipping == "Shipping not specified"):
            continue
        else:
            #shipping = listing_shipping[2:6]
            #METHOD 2: use regex to remove all characters except digits and decimals
            shipping = re.sub('[^0-9.]', '', listing_shipping)
            if(shipping == ''):
                continue
        dat.append(shipping)

        #total price (selling price + shipping)
        total_price = listing_price + float(shipping)
        dat.append(str(total_price))


        #grab its link
        #tag: <a href="https://...">
        #little different to extract since link is the attribute
        #iterate through all 'a' tags with the ebay item URL CSS class attribute
        #use regex to specifically search for ebay item URL strings
        for listing_links in listing.find_all(name='a', attrs={'href': re.compile('^https://www.ebay.com/itm/')}):
            listing_link = listing_links.get('href')
            #print(listing_link)
            dat.append(listing_link)
            #break after getting first appropriate link, rest are redundant
            break

        if(i == 1 and res_pg_num == 1):
            write2csv(dat, out_file)
        else:
            append2csv(dat, out_file)

