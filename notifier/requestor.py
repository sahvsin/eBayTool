def make_request(query):
    '''
    makes the request to access data from the eBay URL built given the search query and search parameters
    '''

    def url_builder(query):
        '''
        builds the eBay URL for the provided search query and associated parameters
        '''

        #transform the search query to its URL encoding
        search_code = '+'.join(query[0].split(' '))

        #write code to encode categories (for now encodings are already written in the csv)
        category = query[1]

        #sorting parameter(10 - "Most Recent", 15 - "Price+Shipping Lowest", 16 - "Price+Shipping Highest")
        sort_param = "10"

        #encoding the buying format to its URL encoding
        if(query[2] == "BIN" or query[2] == "Buy It Now" or query[2] == "bin" or query[2] == "buy it now" or query[2] == "Buy it now"):
            buy_format = "&LH_BIN=1"
        elif(query[2] == "auction" or query[2] == "Auction" or query[2] == "AUCTION"):
            buy_format = "&LH_Auction=1"
        else:
            buy_format = "&LH_ALL=1"

        return "https://www.ebay.com/sch/{cat}/i.html?_from=R40&_nkw={searchkey}&_sop={sort_by}&_ipg=200&rt=nc{last_params}&LH_ItemCondition=1000|1500|2000|2500|2750|3000|4000|5000|6000".format(cat = category, searchkey = search_code, sort_by = sort_param, last_params = buy_format)


    import requests

    try:
        #first build the URL to request
        url = url_builder(query)
        print(url)

        #make the data request
        req = requests.get(url)

        #check the status of the request (200- success, otherwise - fail)
        req.raise_for_status()      #returns None if success, otherwise Exception occurs

    except Exception:
        return 0    #failed request, raise flag to exit

    return req      #successful request, return the requested data

 
