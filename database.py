#!usr/bin/env python3
from typing import final
import pandas as pd
import os
import time
import gc

startTime = time.time()

directory_in_str = str('/Users/pat/hello/final_tables') # was cleaned_tables
directory = os.fsencode(directory_in_str)

# read in Driving Distance csv as initial data frame to join on
# reason is because this is the most popular stat that should cover all players going back to 1980
final_df = pd.read_csv('/Users/pat/hello/clean_test/Driving Distance.csv')
# changing columns to player and year for easy joining
new_columns = final_df.columns.values
new_columns[0] = 'player'
new_columns[-1] = 'year'
final_df.columns  = new_columns

# loopin over each csv file in folder and joining on player and year
# that df is then joined on the next one in the folder list
for file in os.listdir(directory):
    try:
        filename = os.fsencode(file)
        file_x = os.path.join(directory, filename)
        temp_df = pd.read_csv(file_x.decode('utf-8')) # read in df
        
        # changing column names for merging
        temp_columns = temp_df.columns.values
        temp_columns[0] = 'player'
        temp_columns[-1] = 'year'
        temp_df.columns = temp_columns

        final_df = pd.merge(final_df, temp_df, how='outer', left_on=['player','year'], right_on=['player','year'])
        final_df1 = final_df[final_df['player'] != 'Richard Johnson']
        gc.collect()
    except:
        print('something wrong happened')
        print(str(file))
        gc.collect()

merge_df = final_df1
# write to file
merge_df.to_csv('golf_data.csv')
print(merge_df)

executionTime = (time.time() - startTime)

print('Total Execution time in seconds: ' + str(executionTime))
print('Total Execution time in minutes: ' + str(executionTime/60))