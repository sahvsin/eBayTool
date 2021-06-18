import csv



def csv_reader(filename="items.csv"):
    '''
    read csv file provided its path and create a list off of its every row (end up with list of rows/lists)

    Inputs:
    filename -- the string of the filename of the CSV to read

    Output:
    Python list of data in all rows in the CSV file
    '''

    all_rows = []

    #start by opening the csv file to read ('r')
    with open(filename, 'r') as f:
        
        #create csv reader object
        reader = csv.reader(f)

        #skip the header
        header = next(reader)

        #read each row as a list and append to list of rows
        for row in reader:
            all_rows.append(row)

    return all_rows



def write2csv(vec, filename): 
    '''
    saves Python vector (list) to csv file

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('w') data write (or overwrite) data into
    with open(filename, "w") as f:

        #create csv writer object
        writer = csv.writer(f)

        #writing the list to csv as a row of data
        writer.writerows(vec)


def append2csv(vec, filename):
    '''
    appends Python vector (list) to csv file

    Inputs:
    vec -- Python list of data to write
    filename -- string name of the CSV file to write to
    '''

    #start by opening the csv file to append ('a') data to pre-existing data
    with open(filename, "a") as f:

        #create csv writer object
        writer = csv.writer(f)

        #append the list to csv as a row of data
        writer.writerows(vec)


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



def delete_csv(filename):
    '''
    deletes the passed in file

    Inputs:
    filename -- string name of the CSV file to write to
    '''
    import os

    os.remove(filename)
	
