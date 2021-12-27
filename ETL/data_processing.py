import csv
from datetime import date, datetime, timedelta
from numpy.lib import index_tricks
import pandas as pd
import os
import numpy as np

def datatype_conversion(df, columnName, datatype):
    if datatype=='datetime':
        print('Converting '+columnName + ' to ' + datatype)
        df[columnName] = pd.to_datetime(df[columnName])
        print('Converted '+columnName + ' to ' + datatype)
    return df

def fetch_created_files(location):
    print('fetching names of already created raw files')
    all_files = os.listdir(location)
    csv_files = list(filter(lambda f: f.endswith('.csv'), all_files))
    return csv_files

def check_file_existence(csv_files, filename):
    flag = filename in csv_files
    return flag

def fetch_date_details(df, column_name, date_master_file):
    print('mapping dates and weekend to scanned date')
    # df['scanned_date'] = pd.to_datetime(df[column_name]).dt.date
    # print(date_master_file['weekday'])
    # print(date_master_file['weekday'])
    # print(df['scanned_date'])
    df = pd.merge(df,date_master_file, left_on = 'scanned_date', right_on = 'weekday', how='left')
    df=df.drop(columns=['weekday'])
    return df

def func_column_strip(df):
    for col in df.columns:
        df[col] = df[col].str.strip()
    return df

def fun_replace_empty_data(df):
    for col in df.columns:
        # print(col)
        df[col] = df[col].apply(lambda x: 'NA' if len(x.strip())==0 else x )
    return df

def create_raw_files(df, date_column, csv_files, save_location):
    # print(df)
    print('started creating raw files')
    # from csv import writer
    # df = df [ df.scanned_date == '2021-09-08' ]
    unique_dates = df[date_column].unique()
    # print(unique_dates)
    total_files_to_create = len(unique_dates)
    count = 0
    filenames = []
    
    # .orphan_id = df.orphan_id.fillna('NA')
    # df.loc[df.orphan_id .isnull(),'orphan_id'] = 'NA'
    for scanned_date in unique_dates:
        # print(scanned_date)
        scanned_date = scanned_date.strftime("%Y-%m-%d")
        temp = df[df[date_column]==datetime.strptime(scanned_date,'%Y-%m-%d').date()]
        filename = scanned_date + '.csv'
        #print(filename)
        filenames.append(save_location + filename)
        # print(temp)
        if filename in csv_files:
            # print('file_exists')
            temp.to_csv(save_location + filename, mode='a', header=False, index=False)
            temp1 = pd.read_csv(save_location + filename, encoding='utf-8')
            temp1 = temp1.drop_duplicates()
            temp1.to_csv(save_location + filename, index=False)
            print('raw file appended for ' + filename)
        else:
            
            temp.to_csv(save_location + filename, index=False)
            # filenames
            print('creating raw file for the date ' + filename)
        count = count + 1
    print('copmpleted creating %d files ' %count)
    # print(filenames)
    return filenames

def create_rewrite_raw_files(df, date_column, csv_files, save_location):
    print('started creating raw files')
    unique_dates = df[date_column].unique()
    # print(unique_dates)
    count = 0
    filenames = []
    for scanned_date in unique_dates:
        # print(scanned_date)
        scanned_date = scanned_date.strftime("%Y-%m-%d")
        temp = df[df[date_column]==datetime.strptime(scanned_date,'%Y-%m-%d').date()]
        filename = scanned_date + '.csv'
        filenames.append(save_location + filename)
        temp.to_csv(save_location + filename, index=False)
        # filenames
        print('creating raw file for the date ' + filename)
        count = count + 1
    print('copmpleted creating %d files ' %count)
    # print(filenames)
    return filenames


def coalesce_columns(df, coalesce_column_list, result_column):
    # coalesce_column_list = 
    column_count = len(coalesce_column_list)
    df[coalesce_column_list[0]] = df[coalesce_column_list[0]].replace(r'^\s*$', np.nan , regex=True)
    temp = pd.DataFrame(columns=['result'])
    temp['result'] = df[coalesce_column_list[0]]
    for count in range(1,column_count):
        # print(df[coalesce_column_list[3]])
        df[coalesce_column_list[count]]=df[coalesce_column_list[count]].replace(r'^\s*$', np.nan , regex=True)
        # print(count)
        temp.result = temp['result'].fillna(df[coalesce_column_list[count]])

    df[result_column] = temp.fillna('NA')
    df = df.drop(columns=coalesce_column_list)
    return df


def collate_data_for_dashboard(start_date, no_of_days, csv_files, raw_file_location, dataframe_columns):
    df = pd.DataFrame(columns=dataframe_columns) 
    # df = pd.DataFrame() 
    for i in range(0, no_of_days):
        start_date = start_date - timedelta(1)
        # print(start_date)
        file = start_date.strftime("%Y-%m-%d") + '.csv'
        
        if file in csv_files:
            temp = pd.read_csv(raw_file_location + file)
            temp = temp[dataframe_columns]
            df = df.append(temp)
    return df
