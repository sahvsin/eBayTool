import datetime


def today_date():
    '''
    determine today's date (date of program runtime) and reformat it to a string similar to eBay's format

    Output:
    Pyton string of the current date formatted like in eBay listings
    '''

    #first determine today's date and cast it to string of the same format eBay uses (mmm-dd, mmm is abbrev.)
    today = datetime.date.today()
    today = today.strftime("%b-%d-%Y")
    
    #extract the month (abbrev.) and day (number)
    today_month = today[:3]
    today_day = today[4:6]

    return [today_month, today_day]
    
