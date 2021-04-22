import os



def item_selector():
    '''
    asks the user to choose which csv file (pertaining to a searched item on eBay) to process among a list of avialable csv files in a separate directory

    Output:
    the absolute path to the chosen csv file
    '''
    #go to directory with all of the saved items which should be in directory one level higher than the current working dir 
    dir_up_one_lvl = os.path.dirname(os.getcwd())
    items_dir = os.path.join(dir_up_one_lvl, "item_csv")

    #store all of the csv's in a list
    #NOTE: os.listdir lists EVERYTHING in the directory (files+subdirs), use os.walk to split files and subdirs
    item_list = os.listdir(items_dir)
    #print(item_list)

    #go through the list of item dirs and print each one, asking the user to choose which to operate on
    #start by making the string to print
    request_string = "\nPlease select one of the following:\n"

    for i, item_dir in enumerate(item_list):
    
        #extract the searched item name (with spaces) 
        #first splice the middle of the dir name (without the "ebay_" prefix)
        #then split the string to remove all "+"
        #lastly rejoin the split parts with a " " (space) in between each part
        item_name = " ".join(item_dir[5:].split('+'))

        #display the options in such a way that expects the user to respond with the csv's index in the list
        #i.e. [0] item A\n  [1] item B\n ... 
        request_string = request_string + "  [{}] {}\n".format(i, item_name)


    #then use "input()" using the built request string to display it and get the user's response
    chosen_item = input(request_string)

    return " ".join(item_list[int(chosen_item)][5:].split('+')), os.path.join(items_dir, item_list[int(chosen_item)])



def date_selector(item_path):
    '''
    asks the user to choose the date (pertaining to a searched item on eBay) to process among a list of dates of when the item was scraped

    Input:
    item_path -- string of the path to the directory of the item CSVs 

    Output:
    the absolute path to the chosen scrape date
    '''
    #store all of the csv's in a list
    #NOTE: os.listdir lists EVERYTHING in the directory (files+subdirs), use os.walk to split files and subdirs
    date_list = os.listdir(item_path)
    #print(csv_list)

    #go through the list of item dirs and print each one, asking the user to choose which to operate on
    #start by making the string to print
    request_string = "\nPlease select one of the following scrape dates:\n"

    for i, date_dir in enumerate(date_list):

        #extract the searched item name 
        date_name = date_dir

        #display the options in such a way that expects the user to respond with the date's index shown in the list
        #i.e. [0] item A\n  [1] item B\n ... 
        request_string = request_string + "  [{}] {}\n".format(i, date_name)


    #then use "input()" using the built request string to display it and get the user's response
    chosen_date = input(request_string)

    return os.path.join(item_path, date_list[int(chosen_date)])




def csv_selector(item_path):
    '''
    asks the user to choose which csv file (pertaining to a searched item on eBay) to process among a list of avialable csv files in a separate directory

    Input:
    item_path -- string of the path to the directory of the item CSVs 

    Output:
    the absolute path to the chosen csv file
    '''
    #store all of the csv's in a list
    #NOTE: os.listdir lists EVERYTHING in the directory (files+subdirs), use os.walk to split files and subdirs
    csv_list = os.listdir(item_path)
    #print(csv_list)

    #go through the list of item dirs and print each one, asking the user to choose which to operate on
    #start by making the string to print
    request_string = "\nPlease select one of the following to process:\n"

    for i, csv_dir in enumerate(csv_list):

        #only process ".csv" files and not "logistics" files
        if(csv_dir[-4:] == ".csv" and 'logistics' not in csv_dir):
    
            #extract the searched item name (with spaces) 
            #first splice the middle of the dir name (without the ".csv" prefix)
            csv_name = csv_dir[:-4]

            #display the options in such a way that expects the user to respond with the csv's index in the list
            #i.e. [0] item A\n  [1] item B\n ... 
            request_string = request_string + "  [{}] {}\n".format(i, csv_name)

        else:
            continue


    #then use "input()" using the built request string to display it and get the user's response
    chosen_csv = input(request_string)

    return csv_list[int(chosen_csv)][:-4], os.path.join(item_path, csv_list[int(chosen_csv)])


#TEST
#print(csv_selector())


def logistics_path(item_dir, scraped_date):
    '''
    builds the path to save the csv's with the logistics of the scraped item (for the 90 day window)

    Input:
    item_dir -- string of the path to the directory of the item CSVs
    scraped_date -- the specific date/time of when the item was scraped (part of the CSV's filename) 

    Output:
    the string of the path to save the CSVs of data
    '''

    return os.path.join(item_dir, "logistics_" + scraped_date + ".csv") 

