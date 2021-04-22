import pandas as pd
import matplotlib
from csv_utils import write2csv, single_line
from data_aggregation import csv2df




#hashmaps mapping: month abbrev. -> month number, month number -> month abbrev.
month_abbrev2num = {'Jan': 1, 'Feb': 2, 'Mar': 3, 'Apr': 4, 'May': 5, 'Jun': 6, 'Jul': 7, 'Aug': 8, 'Sep': 9, 'Oct': 10, 'Nov': 11, 'Dec': 12}
month_num2abbrev = {1: 'Jan', 2: 'Feb', 3: 'Mar', 4: 'Apr', 5: 'May', 6: 'Jun', 7: 'Jul', 8: 'Aug', 9: 'Sep', 10: 'Oct', 11: 'Nov', 12: 'Dec', 13: 'Jan', 14: 'Feb', 15: 'Mar', 16: 'Apr', 17: 'May', 18: 'Jun', 19: 'Jul', 20: 'Aug', 21: 'Sep', 22: 'Oct', 23: 'Nov', 24: 'Dec'}



def analyze_past_data(item_name, csv_df, three_months_ago, month_num, labels, log_dir):
    '''
    analyzes past listings data stored in its CSV to compute logistics like min, max, and mode prices (overall and monthly)

    Inputs:
    item_name -- Python string of the item to analyze
    csv_df -- Pandas Dataframe of the archived CSV listings data for the specific item to analyze
    three_months_ago -- integer of the month three months ago from the current one
    month_num -- integer of the current month
    labels -- Python list of column labels strings
    log_dir -- Python string of the path to store the analysis CSV
    '''

    #initialize the monthly logistics aggregators
    monthly_data_collected = dict()
    min_df = pd.DataFrame(columns = labels)
    max_df = pd.DataFrame(columns = labels)
    mode_df = pd.DataFrame(columns = labels)

    #loop over the three months and process the data over each individual month
    for i in range(three_months_ago, month_num+1):

        #aggregate the logistics for the month
        month_data = dict()

        #cast the numerical index of the current month to its 3-letter abbreviation using the above map
        cur_month = month_num2abbrev[i]

        #filter the original (all listings) dataframe to select only the listings of the current month
        month_df = csv_df[csv_df["month"] == cur_month]

        #skip dataframe processing if there isn't data for the month
        if(month_df.empty):
            continue

        #compute logistics
        month_data["max price"] = month_df["total"].max()
        month_data["min price"] = month_df["total"].min()
        month_data["avg price"] = month_df["total"].mean()
        month_data["mode price"] = month_df["total"].mode()[0]

        #build the aggragation of each month's logistics
        monthly_data_collected[cur_month] = month_data

        #aggregate each monthly logistic independently as a dataframe for easy display and storage (to csv)
        min_df = min_df.append(month_df[month_df["total"] == month_data["min price"]])
        max_df = max_df.append(month_df[month_df["total"] == month_data["max price"]])
        mode_df = mode_df.append(month_df[month_df["total"] == month_data["mode price"]])

        #initialize the daily and weekly logistics aggregator for the days and weeks in this month
        daily_data_collected = dict()
        #week_df = pd.DataFrame(columns = labels)

        #go through each day in the month and process each day's data
        for j, cur_day in enumerate(range(month_df["day"].min(), month_df["day"].max()+1), 1):

            #one week complete
            #if(j%7 == 6):

                #do stuff for the weekly data
                #print(j)

            #aggregate the logistics for the day
            day_data = dict()

            #filter the listings of the month to select only the listings of the current day
            day_df = month_df[month_df["day"] == cur_day]

            #skip days without any data
            if(day_df.empty):
                continue

            #compute logistics 
            day_data["max price"] = day_df["total"].max()
            day_data["min price"] = day_df["total"].min()
            day_data["avg price"] = day_df["total"].mean()
            #day_data["mode price"] = day_df["total"].mode()

            daily_data_collected[cur_month + " " + str(cur_day)] = day_data

            #print(daily_data_collected)

        #aggregate each daily logistic for the whole month as a dataframe for easy display and storage
        day_logistics_df = pd.DataFrame.from_dict(daily_data_collected, orient='index')
        day_logistics_df.index.name = 'day'
        day_logistics_df.reset_index()
        #print(day_logistics_df)
        #print()

        #aggregate each daily logistic for the whole month as a dataframe for easy display and storage
        day_logistics_df = pd.DataFrame.from_dict(daily_data_collected, orient='index')
        day_logistics_df.index.name = 'day'
        day_logistics_df.reset_index()
        #print(day_logistics_df)
        #print()

        #plot the logistics
        ax = day_logistics_df.plot(kind='line', y='min price', style='.-')
        day_logistics_df.plot(kind='line', y='max price', style='.-', color='red', ax=ax)
        day_logistics_df.plot(kind='line', y='avg price', style='.-', color='green', ax=ax)
        matplotlib.pyplot.xlabel("Dates")
        matplotlib.pyplot.ylabel("Price [$]")
        matplotlib.pyplot.title(item_name + " daily pricing over " + cur_month)

        #show the plots
        matplotlib.pyplot.show()


    #write the monthly data to a csv and save it
    write2csv(monthly_data_collected, monthly_data_collected.keys(), log_dir)
    single_line("", log_dir, 'a')
    single_line("Minimums:", log_dir, 'a')
    min_df.to_csv(log_dir, mode = 'a', index=False)
    single_line("", log_dir, 'a')
    single_line("Maximums:", log_dir, 'a')
    max_df.to_csv(log_dir, mode = 'a', index=False)
    single_line("", log_dir, 'a')
    single_line("Modes:", log_dir, 'a')
    mode_df.to_csv(log_dir, mode = 'a', index=False)


    

def analyze_current_data(item_name, csv_df, labels, log_dir):
    '''
    analyzes current/active listings data stored in its CSV to compute logistics like min, max, mean and mode prices

    Inputs:
    item_name -- Python string of the item to analyze
    csv_df -- Pandas Dataframe of the archived CSV listings data for the specific item to analyze
    labels -- Python list of column labels strings
    log_dir -- Python string of the path to store the analysis CSV
    '''
    
    #aggregating the logistics
    data_collected = dict()

    #compute the logistics
    data_collected["min price"] = csv_df["total"].min()
    data_collected["max price"] = csv_df["total"].max()
    data_collected["avg price"] = csv_df["total"].mean()
    data_collected["mode price"] = csv_df["total"].mode()[0]

    #aggregate each logistic independently as a dataframe for easy display and storae (to csv)
    min_df = csv_df[csv_df["total"] == data_collected["min price"]]
    max_df = csv_df[csv_df["total"] == data_collected["max price"]]
    mode_df = csv_df[csv_df["total"] == data_collected["mode price"]]

    
    #write the monthly data to a csv and save it
    write2csv(data_collected, data_collected.keys(), log_dir)
    single_line("", log_dir, 'a')
    single_line("Minimums:", log_dir, 'a')
    min_df.to_csv(log_dir, mode = 'a', index=False)
    single_line("", log_dir, 'a')
    single_line("Maximums:", log_dir, 'a')
    max_df.to_csv(log_dir, mode = 'a', index=False)
    single_line("", log_dir, 'a')
    single_line("Modes:", log_dir, 'a')
    mode_df.to_csv(log_dir, mode = 'a', index=False)


