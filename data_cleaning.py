#!usr/bin/env python3
import pandas as pd
import os
import time

# function to drop the "ranking" columns
# also prefixes the stat from web scraping script to all the headers
# drops the extra stat column
def clean(df):
    try:
        stat_name = df.iloc[1][-1]
        df.drop(df.iloc[:,0:3], inplace=True, axis=1)
        df2 = df.add_prefix(stat_name+'_')
        df3 = df2.iloc[:, :-1]
        # troubleshoot
        print(df3)
        csv_string = str('/Users/pat/hello/cleaned_tables/' + stat_name + '.csv')
        df3.to_csv(csv_string, index=False)
    except:
        print("something went wrong")
        pass

startTime = time.time()
counter = 0
bad_counter = 0

# directory location for looping through csv files
directory_in_str = str('/Users/pat/hello/data_tables')
directory = os.fsencode(directory_in_str)

# loop main function in folder
for file in os.listdir(directory):
    try:
        filename = os.fsencode(file)
        file_x = os.path.join(directory, filename)
        df = pd.read_csv(file_x.decode('utf-8'))
        clean(df)
        counter += 1
    except:
        print(str(file))
        bad_counter += 1


executionTime = (time.time() - startTime)
print('good count: ' + str(counter))
print('bad count: ' + str(bad_counter))
print('Total Execution time in seconds: ' + str(executionTime))
print('Total Execution time in minutes: ' + str(executionTime/60))