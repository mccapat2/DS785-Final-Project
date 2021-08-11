#!usr/bin/env python3
from bs4 import BeautifulSoup
import requests
import pandas as pd
import time

startTime = time.time()

# Setting up URL base parts for loop
url_pre_stat = 'https://www.pgatour.com/stats/stat.' # first part of url
url_pre_year = '.y' # stat year follows
url_end = '.html'

# inititialized empty lists
year = []
stat_list = []

# for loop to iterate and fill empty lists
for i in range(1980, 2021):
    year.append(str(i))

for i in range(101, 500):
    stat_list.append(str(i))

# counters for troubleshooting
counter = 0
bad_counter = 0
bad_stat_counter = 0
good_stat_counter = 0

# main loop that calls the iterative URL and scrapes data table and data labels
# each completed year of X stat is appened to that parent stat df until no more years are left
# non existent URLs are skipped
for x in stat_list:
    try:
        # url check for stat webpage
        check_url = str(url_pre_stat + x + url_end)
        check_source = requests.get(check_url).text
        df_check = []
        df_check = pd.read_html(check_url)

        stat_full = pd.DataFrame()
        for i in year:
            try:
                new_url = str(url_pre_stat + x + url_pre_year + i + url_end)
                source = requests.get(new_url).text #new
                soup = BeautifulSoup(source, 'html5lib') #new
                df_list = []
                df_list = pd.read_html(new_url)
                stat_df = df_list[1]

                # beautifulsoup for stat title
                for div in soup.find_all('div', class_="main-content-off-the-tee-details"):
                    for body in div.find_all('section', class_='statistics-details-content'):
                        stat_header = body.find('div', class_="header").h1.text

                stat_df['year'] = i
                stat_df['stat_type'] = stat_header
                temp_df = stat_df

                stat_full = stat_full.append(temp_df, ignore_index = True)
 
                counter += 1
                print('succesful ' + str(stat_header) + ' ' + str(i) + ' year export')
                time.sleep(3)
            except:
                bad_counter += 1
                print("web page error - no year " + str(i))
                time.sleep(3)
                pass
        good_stat_counter += 1
        csv_string = str('/Users/pat/hello/data_tables/' + x + stat_header + '.csv')
        stat_full.to_csv(csv_string)
        print('succesful stat completion ' + str(x) + str(stat_header))
        update_time = (time.time() - startTime)
        print('duration: ' + str(update_time) + ' seconds')
        time.sleep(3)
    except:
        bad_stat_counter += 1
        print('web page error - no stat' + str(x))
        time.sleep(3)
        pass

# final printout/troubleshooting
print('Sucessful exports =' + str(counter))
print('Unsucessful exports =' + str(bad_counter))
print('Sucessful stat urls =' + str(good_stat_counter))
print('Unsucessful stat urls =' + str(bad_stat_counter))

executionTime = (time.time() - startTime)
print('Total Execution time in seconds: ' + str(executionTime))
print('Total Execution time in minutes: ' + str(executionTime/60))