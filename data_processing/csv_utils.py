import csv


def csv_printer(filename):
    '''
    prints data from a 3-column csv file row by row

    Inputs:
    filename -- the string of the filename of the CSV to read

    Output:
    Python list of data in all rows in the CSV file
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



def write2csv(hashmap, columns, filename): 
    '''
    saves Python dict (hashmap) to csv file

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('w') data write (or overwrite) data into
    with open(filename, "w") as f:
	
        #create csv writer object
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        #writing the list to csv as a row of data
        writer.writerow(hashmap)


def append2csv(hashmap, columns, filename):
    '''
    appends Python dict (hashmap) to csv file

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('a') data to pre-existing data
    with open(filename, "a") as f:

        #create csv writer object
        writer = csv.DictWriter(f, fieldnames=columns)
        writer.writeheader()
        #writing the list to csv as a row of data
        writer.writerow(hashmap)


def single_line(string, filename, mode):
    '''
    either writes or appends a single-cell row of text to a csv file

    Inputs:
    string -- Python string to append to the next row in the file
    filename -- string name of the CSV file to write to 
    mode -- CSV modifier mode, expects either 'a' to append or 'w' to write
    '''

    #start by opening the csv file to either write or append (depending on passed mode)
    with open(filename, mode) as f:

        #create csv writer object
        writer = csv.writer(f)

        #write/append the string (wrapped as a sequence) to next open row
        writer.writerow([string])
