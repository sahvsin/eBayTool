from datetime import datetime


def current_date():
    '''
    determine today's date and time (of program runtime) and reformat it to a string similar to eBay's current (newly) listing format (mmm-dd hh:mm)

    Output:
    Pyton string of the current date formatted like in eBay listings
    '''

    #first determine the current time and day
    #then cast it to string of the same format eBay uses (mmm-dd HH:MM)
    now = datetime.now()
    now = now.strftime("%b-%d %H:%M")

    return now




def listing_date_parser(date):
    '''
    separates the month (abbrev), day, hour, and minute from an eBay listing formatted date for further processing

    Input:
    date -- string of complete date

    Output:
    Pyhon list of the substring components (month, day, hour, minute) of the date 
    '''

    #first determine if the day's digit is single or double digit by the size of the string
    #split the date string into a list of its components
    if(len(date) == 11):
        return [date[:3], int(date[4]), int(date[6:8]), int(date[9:])]
    elif(len(date) == 12):
        return [date[:3], int(date[4:6]), int(date[7:9]), int(date[10:])]
    
