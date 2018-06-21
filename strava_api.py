import os
import requests
import csv
import pymongo
from datetime import timedelta, date


def make_request(endpoint, api_key, yyymmdd, STATE, location):
    url = ''.join([endpoint, api_key, '/history_', str(yyyymmdd), '/q/', STATE, '/', location, '.json'])
    response = requests.get(url)
    response = response.json()
    return response

def write_to_file(response, fname='weatherdata.csv'):
    if len(response) > 0:
        # unpack response dictionary
        metadata = list(response.values())[0]
        results = list(response.values())[1]

        # print column names to see what they are
        #print(results.keys())

        # extract daily summary
        daily_summary = results['dailysummary'][0]

        # write to csv
        csv_columns = list(daily_summary.keys())
        # datetime dict --> string
        date_dict = daily_summary['date']
        date_string = "{y}{m}{d}".format(y=date_dict['year'], m=date_dict['mon'], d=date_dict['mday'])
        # cols and values
        datacols = ['minwspdm','maxwspdm','meanwindspdm','precipm']
        colnames = ['date','min_wspd','max_wspd','mean_wspd','precip']
        data = [date_string, daily_summary[datacols[0]], daily_summary[datacols[1]]]
        data = [daily_summary[datacols[x]] for x in range(len(datacols))]
        data.insert(0, date_string)

        with open(fname, 'a') as csvfile: # 'w for write, a for append'
                    #writer = csv.DictWriter(csvfile, fieldnames=colnames)
                    txtwriter = csv.writer(csvfile, delimiter=',')
                    #txtwriter.writeheader()
                    #txtwriter.writerow(colnames) # only if first time
                    txtwriter.writerow(data)
    else:
        print('response object = empty')

def daterange(start_date, end_date):
    for n in range(int ((end_date - start_date).days)):
        yield start_date + timedelta(n)

if __name__=='__main__':
    # API key
    api_key = os.environ['WUnderground_API_KEY']

    # loop over time:
    start_date = date(2013, 1, 1)
    end_date = date(2015, 6, 2)
    for single_date in daterange(start_date, end_date):
        timestamp = single_date.strftime("%Y%m%d")

        # request params
        endpoint = "http://api.wunderground.com/api/"
        yyyymmdd = timestamp
        STATE = 'CO'
        location = 'Aspen'

        response = make_request(endpoint, api_key, yyyymmdd, STATE, location)
        #print('response code = {}'.format(response.status_code))
        fname = 'Aspen.csv'
        write_to_file(response, fname)
