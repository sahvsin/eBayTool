import csv


def csv_printer(filename):
    '''
    prints data from a 3-column csv file row by row

    Inputs:
    filename -- string name of the CSV file to process

    Output:
    formatted string to print
    '''

    fin_string = "\n"

    #start by opening the csv file to read ('r')
    with open(filename, "r") as f:

        #create csv reader object
        reader = csv.reader(f)

        #skip the header
        header = next(reader)

        #assuming subsequent rows is data
        for row in reader:
            fin_string = fin_string + "{:<40}{:<40}{:<40}\n".format(*row) 

    return fin_string



def write2csv(vec, filename): 
    '''
    saves Python vector (list) to csv file (overwrites)

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('w') data write (or overwrite) data into
    with open(filename, "w") as f:

        #create csv writer object
        writer = csv.writer(f)

        #writing the list to csv as a row of data
        writer.writerow(vec)


def append2csv(vec, filename):
    '''
    appends Python vector (list) to csv file (does not overwrite)

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('a') data to pre-existing data
    with open(filename, "a") as f:

        #create csv writer object
        writer = csv.writer(f)

        #append the list to csv as a row of data
        writer.writerow(vec)


