import pandas as pd
import os
import time
import numpy as np
import helper_functions as hf
from datetime import datetime

# directory where deutsche-boerse data is stored
data_dir = 'data/'
start_date = '2018-01-01'
end_date = '2018-03-30'

# because newer data is not working we use this only for naming the file
end_date_2 = datetime.today().strftime('%Y-%m-%d')

# creates list with dates between start and end date
dates = list(pd.date_range(start_date,end_date, freq='D').strftime('%Y-%m-%d'))

isin = input("Please enter a valid ISIN: ")
data_sync = hf.yes_no_input("Do you want to download/synchronize Deutsche-Boerse data?")

# using shell commands since aws cli has better build-in commands for downloading
# and syncing s3 bucket data by date keys than writing in python.
if data_sync:
    download_time_start = time.time()
    for date in dates:
        print("Downloading/Synchronizing Deutsche-Boerse data from {date}".format(date=date))
        os.system("mkdir -p data/{date}".format(date=date))
        os.system("aws s3 sync s3://deutsche-boerse-xetra-pds/{date}/ data/{date} --no-sign-request".format(date=date))
    download_duration = round(time.time() - download_time_start,2)
    print("\nDownload/Sync took {0} seconds.".format(download_duration))

# creating sub directories for every date
data_sub_dirs = map(lambda date: data_dir + date, dates)
# creating list for every csv file in every date sub dir
csv_file_names = hf.create_list_of_files(data_sub_dirs)

print("\nPlease wait while csv files are concatenated. This will take some minutes.")
start_time = time.time()
read_csv_files = map(lambda csv: pd.read_csv(csv,error_bad_lines=False,engine='python'), csv_file_names)
# checking if the entered ISIN is in the csv files
concat_csv_files = pd.concat((file[(file["ISIN"] == isin)] for file in read_csv_files),sort=False)

if not concat_csv_files.empty:
    concat_csv_files["DateTime"] = pd.to_datetime(concat_csv_files["Date"] + " " + concat_csv_files["Time"]).copy()

    df2 = concat_csv_files[['ISIN','Date','StartPrice','EndPrice','TradedVolume','DateTime']].copy()
    df2.TradedVolume = pd.to_numeric(df2.TradedVolume, errors='coerce').fillna(0).astype(np.int64)

    # selecting the opening price for ISIN by date
    print("\nAggregating StartPrice by date")
    df3 = df2.groupby(["ISIN","Date"]).apply(lambda x: x.loc[
        x.DateTime.idxmin(),['StartPrice']]).reset_index()

    # selecting the closing price for ISIN by date
    print("\nAggregating EndPrice by date")
    df4 = df2.groupby(["ISIN","Date"]).apply(lambda x: x.loc[
        x.DateTime.idxmax(),['EndPrice']]).reset_index()

    # summing up traded volume for ISIN by date
    print("\nSumming up TradedVolume by date")
    df5 = df2.groupby(["ISIN","Date"]).agg({"TradedVolume": 'sum'})

    # join the results of the previous data frames on ISIN and date
    merge = df3.merge(df4, left_on=['ISIN','Date'],right_on=['ISIN','Date'], how='inner').merge(
        df5, left_on=['ISIN','Date'],right_on=['ISIN','Date'], how='left').reset_index()
    # sort the data frame by date asc to calculate the difference of the closing prices
    merge.sort_values(by=["Date"])
    merge["change"] = round(merge["EndPrice"].pct_change()*100,2)
    # renaming columns
    merge.columns = ["index","ISIN","date","opening_price","closing_price","daily_traded_volume","percent_change_prev_closing"]

    print("\nSaving result.")
    # creating directory for the result file
    os.system("mkdir -p result")
    merge.to_csv("result/{0}_{1}".format(end_date_2,isin), sep=",")

    print("\nTook {0} seconds to concatenate, aggregate and save result.".format(round(time.time()-start_time,2)))
else:
    print("\nISIN not found. No result.")