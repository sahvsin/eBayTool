import pandas as pd



labels = ["title", "date", "formatted_date", "price", "link"]



def csv2df(csv_file, labels):
    '''
    Inputs:
    csv_file - csv file to get the data from
    labels - list of the column labels

    Outputs:
    pandas dataframe containing the data in the csv
    '''

    #use pandas "read_csv" function
    return pd.read_csv(csv_file, names=labels)




