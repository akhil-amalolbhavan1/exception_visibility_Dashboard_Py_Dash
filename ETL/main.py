# Owner : Akhil A
# Version V1
# Created on :
from logging import error, exception
# from httplib2.error import FailedToDecompressContent
import pandas as pd
import pygsheets
import os
from datetime import datetime, date
import sys

import gsheet_utility as gsheetUtility
import Email_Code as fkEmail
import data_processing as data_processing
import numpy as np

if __name__ == '__main__':
    basePath = '/Users/a/Documents/GitHub/exception_visibility/'
    ################################################################################################
    ####################################### Asset Data Processing #####################################
    ################################################################################################
    
    ################################################################################################
    ####################################### RC Data Processing #####################################
    ################################################################################################
    emailUserName = 'akhil.a@flipkart.com'
    emailPassword = 'prieuyhpifoqyefr'
    rcSPOCS = "akhil.a@flipkart.com"
    
    date_master_file = pd.read_csv( '/Users/a/Documents/GitHub/exception_visibility/Dashboard/data/week_details.csv')
    date_master_file['weekday'] = pd.to_datetime(date_master_file["weekday"],format = '%d/%m/%Y').dt.date
    date_master_file['month_year'] = pd.to_datetime(date_master_file["month_year"],format = '%d/%m/%Y').dt.date
    
    rc_raw_data_location = basePath + 'ETL/RC_Raw_Data/'
    mh_raw_data_location = basePath + 'ETL/MH_Raw_Data/'
    orphan_raw_data_location = basePath + 'ETL/Orphan_Raw_Data/'
    hv_orphan_raw_data_location = basePath + 'ETL/HV_Orphan_Raw_Data/'
    logistics_raw_data_location = basePath + 'ETL/Logistics_Raw_Data/'

    today = date.today()
    today = str(today.year) + "-" + str('{:02d}'.format(today.month)) + "-" + str('{:02d}'.format(today.day))
    
    rcgsheetdatapath = basePath + 'ETL/gsheet_data/rc_data/' + today + '.csv'
    mhgsheetdatapath = basePath + 'ETL/gsheet_data/mh_data/' + today + '.csv'
    orphangsheetdatapath = basePath + 'ETL/gsheet_data/orphan_data/' + today + '.csv'
    hv_orphangsheetdatapath = basePath + 'ETL/gsheet_data/hv_orphan_data/' + today + '.csv'
    logisticsgsheetdatapath = basePath + 'ETL/gsheet_data/logistics_data/' + today + '.csv'

    error_message = ''
    html_message = ''
    html_header = """<html>
                <head>
                </head>
                <body><h2>Data ingestion Summary fo RC</h2>"""
    html_message = html_message + html_header
    html_message = html_message + "Data Ingestion Job started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
    run_rc = 0
    run_mh = 0
    run_orphan = 0
    run_high_value = 0
    run_logistics = 1
    #######################################################################################################################################################################
    ###############################################################Starting with RC Exception ####Data Capturing###########################################################
    #######################################################################################################################################################################
    if run_rc==1:
        try:    
            html_message = html_message + "Data Ingestion Job for RC started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting RC data process')
            rcData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1kCMwH7tq2RoiugdoDKe3xFYMgp_P4WvidwMtG3tNAUo/edit?usp=sharing', 'A3', rcgsheetdatapath,'RC')
            rcGsheetData = rcData.iloc[0:,0:19].copy()
            rcDBColumns = ['rc_received_timestamp','received_by','rc_name','orphan_id','orphan_id_condition','fsn_identified_warehouse','wsn_id','final_area_rc','business_unit',
                            'supercategory','expiry_date','product_title','packaging_condition','damaged_physical_segregation','damaged_quantity','damaged_scan_box_id',
                            'non_damaged_physical_segregation','non_damaged_quantity','non_damaged_scan_box_id']
            rcColumns= rcGsheetData.columns
            rcGsheetData = gsheetUtility.assignDBColumns(rcGsheetData, gsheet_asset='Retrun Center', dbColumns=rcDBColumns)
            rcGsheetData = rcGsheetData.fillna('NA')
            rcGsheetData.orphan_id = rcGsheetData.orphan_id.str.upper()
            rcGsheetData.orphan_id = rcGsheetData.orphan_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)
            html_message = html_message + "Fetching Data for RC completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")+ '<br>'
            rcGsheetData = data_processing.fun_replace_empty_data(rcGsheetData)
            
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Finishing fetching RC process Completed')
            rcGsheetData = data_processing.datatype_conversion(rcGsheetData, 'rc_received_timestamp', 'datetime')
            scanned_dates = rcGsheetData.rc_received_timestamp.unique()
            
            print('coalesce columns')
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['non_damaged_physical_segregation','damaged_physical_segregation'], 'physical_segregation')
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['damaged_quantity','non_damaged_quantity'], 'quantity')
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['damaged_scan_box_id','non_damaged_scan_box_id'], 'scan_box_id')
            rcGsheetData['scanned_date'] = pd.to_datetime(rcGsheetData['rc_received_timestamp']).dt.date
            rcGsheetData = data_processing.fetch_date_details(rcGsheetData, 'rc_received_timestamp', date_master_file)
            print(rcGsheetData[['scanned_date','weekend','month_year','weeknum']])
            created_raw_files = data_processing.fetch_created_files(rc_raw_data_location)
            filenames = []
            
            print('creating raw files started')
            filenames = data_processing.create_raw_files(rcGsheetData,'scanned_date',created_raw_files, rc_raw_data_location )
            html_message = html_message + "<p> Raw files created for RC at : " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</p>" 
            html_message = html_message + "<p> Total files created for RC : " + str(len(filenames)) + '<br>'
            print('creating raw files completed')
            
            created_raw_files = data_processing.fetch_created_files(rc_raw_data_location)
            # print('Successfuly Completed')

            rc_final_columns = ['rc_received_timestamp','received_by', 'rc_name', 'orphan_id', 'orphan_id_condition',
                                'fsn_identified_warehouse', 'wsn_id', 'final_area_rc', 'business_unit', 'supercategory', 'expiry_date', 
                                'product_title', 'packaging_condition', 'asset', 'physical_segregation', 'quantity', 'scan_box_id', 'scanned_date', 
                                'weekend', 'month', 'year','month_year','weeknum']
            rc_dashboard_data = data_processing.collate_data_for_dashboard(datetime.now().date(), 180, created_raw_files, rc_raw_data_location, rc_final_columns)
            rc_dashboard_data.to_csv(basePath + 'Dashboard/data/rc_full_data.csv', index=False)

        except Exception as ex:
            error_message = datetime.now().strftime("%d-%m-%Y %H:%M:%S") +" "+ str(ex.__class__).replace('<','').replace('>','') + datetime.now().strftime("%d/%m/%Y %H:%M:%S") +' ' + str(ex).replace('<','').replace('>','')
            print(error_message)
        if len(error_message)>0:
            html_message = html_message + "Error Occured - Data Ingestion Failed for RC <p> Error Message : " + error_message + '<br>'
        else:
            html_message = html_message + "Data Ingestion Successfull for RC Exception completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'

        error_message=''
    #######################################################################################################################################################################
    ###############################################################Starting with MH Exception Log Data Capturing###########################################################
    #######################################################################################################################################################################
    if run_mh==1:
        html_message = html_message + "<h2>Data Ingestion Summary for MH Exception Log Form </h2>"
        try:
            html_message = html_message + "Data Ingestion Job for MH Exception Log form started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting MH data process')
            mhGsheetData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1aeODc4c7bxvYs0iI1eJ2nbHTExLCEkA77D5C9X3sxQg/edit?resourcekey#gid=793332736', 'A2', mhgsheetdatapath, 'MH')
            # rcData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1g4n416j5xGvgwV7KnDHpEPyN1mrsGgH5durMXT2hxHU/edit?usp=sharing','A3')
            # mhGsheetData = mhData.copy()
            mhDBColumns = ['exception_log_timestamp', 'scanned_by',	'asset_type', 'exception_type',	'dg_offload_tracking_id', 'dg_offload_is_rto', 'suspected_malicious_tracking_id',
                            'content_missing_tracking_id', 'closed_vendor_orphan_id', 'closed_vendor_scan_tracking_id',	'damaged_shipment_type', 'damaged_shipment_tracking_id', 'damaged_shipment_image_url',
                            'duplicate_shipment_orphan_id',	'duplicate_shipment_type', 'duplicate_shipment_tracking_id', 'orphan_orphan_id', 'orphan_shipment_category', 'orphan_reason', 
                            'orphan_is_invoice_available',	 'orphans_shipment_type',	 'orphans_super_category',	 'scanned_asset',	'is_marketplace', 'orphan_shipment_image_url']
            mhColumns= mhGsheetData.columns
            mhGsheetData = gsheetUtility.assignDBColumns(mhGsheetData, gsheet_asset='Hub', dbColumns=mhDBColumns)
            mhGsheetData = mhGsheetData.fillna('NA')
            html_message = html_message + "Fetching Data for MH Exception log form completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")+ '<br>'

            print('coalesce columns')
            # print(rcGsheetData.columns)
            tracking_id_coalesce_list = ['dg_offload_tracking_id','suspected_malicious_tracking_id','content_missing_tracking_id','closed_vendor_scan_tracking_id','damaged_shipment_tracking_id','duplicate_shipment_tracking_id']
            mhGsheetData = data_processing.coalesce_columns(mhGsheetData, tracking_id_coalesce_list, 'tracking_id')
            
            orphan_id_coalesce_list = ['closed_vendor_orphan_id','duplicate_shipment_orphan_id','orphan_orphan_id']
            mhGsheetData = data_processing.coalesce_columns(mhGsheetData, orphan_id_coalesce_list, 'orphan_id')
            mhGsheetData = data_processing.coalesce_columns(mhGsheetData, ['duplicate_shipment_type','orphans_shipment_type'], 'shipment_type')
            mhGsheetData = data_processing.coalesce_columns(mhGsheetData, ['damaged_shipment_image_url','orphan_shipment_image_url'], 'image_url')

            mhGsheetData.orphan_id = mhGsheetData.orphan_id.str.upper()
            mhGsheetData.orphan_id = mhGsheetData.orphan_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)
            mhGsheetData.tracking_id = mhGsheetData.tracking_id.str.upper()
            mhGsheetData.tracking_id = mhGsheetData.tracking_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)
            # rcGsheetData = data_processing.func_column_strip(rcGsheetData)
            mhGsheetData = data_processing.fun_replace_empty_data(mhGsheetData)
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Finishing fetching MH process Completed')
            
            mhGsheetData['scanned_date'] = pd.to_datetime(mhGsheetData['exception_log_timestamp']).dt.date
            mhGsheetData = data_processing.datatype_conversion(mhGsheetData, 'exception_log_timestamp', 'datetime')
            mhGsheetData = data_processing.fetch_date_details(mhGsheetData, 'exception_log_timestamp', date_master_file)
            # print(mhGsheetData[['scanned_date','weekend','month_year','weeknum']])
            scanned_dates = mhGsheetData.exception_log_timestamp.unique()
            created_raw_files = data_processing.fetch_created_files(mh_raw_data_location)
            filenames = []
            mhzonedata = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/187u3lIk3GSDiHuUm-ZLno_keTe-jCAu1bqiTon7ExgU/edit?usp=sharing', 'A2', mhgsheetdatapath, 'MH')
            mhGsheetData = pd.merge(mhGsheetData, mhzonedata, left_on='scanned_asset', right_on='Asset_Name', how='left')
            print('Starting creating MH Exception Log form raw files')
            filenames = data_processing.create_raw_files(mhGsheetData,'scanned_date',created_raw_files, mh_raw_data_location )
            html_message = html_message + "<p> Raw files created for RC at : " + datetime.now().strftime("%d-%m-%Y %H:%M:%S") + "</p>" 
            html_message = html_message + "<p> Total files created for RC : " + str(len(filenames)) + '<br>'
            print('Completed creating MH Exception Log form raw files')

            created_raw_files = data_processing.fetch_created_files(mh_raw_data_location)
            mh_final_columns = ['exception_log_timestamp', 'scanned_by', 'hub_name', 'asset_type', 'exception_type', 'tracking_id', 'dg_offload_is_rto',
                                'orphan_id', 'shipment_type', 'shipment_image_url', 'orphan_shipment_category', 'orphan_reason', 'orphan_is_invoice_available',
                                'orphans_super_category', 'zone','is_marketplace', 'orphan_shipment_image_url', 'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum']

            mh_dashboard_data = data_processing.collate_data_for_dashboard(datetime.now().date(), 180, created_raw_files, mh_raw_data_location, mh_final_columns)
            mh_dashboard_data.to_csv(basePath + 'Dashboard/data/mh_full_data.csv', index=False)

        except Exception as ex:
            error_message = datetime.now().strftime("%d-%m-%Y %H:%M:%S") + str(ex.__class__).replace('<','').replace('>','') + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + str(ex).replace('<','').replace('>','')
            print(error_message)
        if len(error_message)>0:
            html_message = error_message
        else:
            html_message = html_message + "Data Ingestion Successfull for MH Exception Log form completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
#######################################################################################################################################################################
###############################################################Starting with Orphan Data Capturing###########################################################
#######################################################################################################################################################################
    if run_orphan ==1:
        html_message = html_message + "<h2>Data Ingestion Summary for Orphan Form </h2>"
        try:
            html_message = html_message + "Data Ingestion Job for Orphan form started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting MH data process')
            html_message = html_message + "Starting to fetch orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting orphan data process')
            orphanData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1QrfuwxkbDHSrMDREnhicUcA2dPqpZgJqvFQ7f9FHRvU/edit?usp=sharing', 'A3', orphangsheetdatapath,'Orphan')
            orphandbcolumns = ['shipment_value', 'weeknum', 'cleared_shipment_tracking_id', 'month', 'date', 'scanned_timestamp', 'motherhub_name',	'shipment_category', 'orphan_reason', 
                                'is_invoice_available', 'shipment_type', 'content_details', 'lane_details_semi_large', 'consignment_id_semi_large', 'bag_id',	'orphan_idnetified_mh_area', 'image_url', 
                                'orphan_id', 'bag_seal_id', 'seller_name', 'seller_id', 'seller_type']
            # orphanGsheetColumns = orphanData.columns
            html_message = html_message + "completed fetching orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Fetching orphan data process Completed')
            orphanData = gsheetUtility.assignDBColumns(orphanData, gsheet_asset='Orphan Data', dbColumns=orphandbcolumns)
            orphanData = orphanData.drop(columns=['weeknum','month','date'])
            orphanData = data_processing.datatype_conversion(orphanData, 'scanned_timestamp', 'datetime')
            orphanData['scanned_date'] = orphanData['scanned_timestamp'].dt.date
            orphanData = data_processing.fetch_date_details(orphanData, 'exception_log_timestamp', date_master_file)

            orphanData.cleared_shipment_tracking_id = orphanData.cleared_shipment_tracking_id.replace(r'^\s*$', np.NaN, regex=True)
            orphanData['is_tracking_id_available'] = ''
            orphanData.loc[orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']]='No'
            orphanData.loc[~orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']] = 'Yes'

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to create orphan raw data files')
            html_message = html_message + "Starting to create orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            orphanData['shipment_value'] = orphanData['shipment_value'].str.replace(',', '')
            orphanData['shipment_value'] = orphanData['shipment_value'].str.replace('.0', '')
            orphanData.shipment_value = orphanData.shipment_value.str.replace(' ', '')
            orphanData.shipment_value = orphanData.shipment_value.fillna(0)
            orphanData.shipment_value =pd.to_numeric(orphanData.shipment_value)
            orphanData.orphan_id = orphanData.orphan_id.str.upper()
            filenames = []
            created_raw_files = data_processing.fetch_created_files(orphan_raw_data_location)
            filenames = data_processing.create_rewrite_raw_files(orphanData,'scanned_date', created_raw_files, orphan_raw_data_location )
            html_message = html_message + "Completed creating orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Completed creating orphan raw data files')

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to collate data for dashboard')
            html_message = html_message + "Starting to create orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            orphan_final_columns = ['shipment_value', 'cleared_shipment_tracking_id', 'scanned_timestamp', 'motherhub_name',	'shipment_category', 'orphan_reason', 
                        'is_invoice_available', 'shipment_type', 'orphan_idnetified_area', 'image_url', 
                        'orphan_id', 'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum','is_tracking_id_available']
            created_raw_files = data_processing.fetch_created_files(orphan_raw_data_location)
            orphan_dashboard_data = data_processing.collate_data_for_dashboard(datetime.now().date(), 180, created_raw_files, orphan_raw_data_location, orphan_final_columns)
            orphan_dashboard_data.to_csv(basePath + 'Dashboard/data/orphan_full_data.csv', index=False)


        except Exception as ex:
            error_message = datetime.now().strftime("%d-%m-%Y %H:%M:%S") + str(ex.__class__).replace('<','').replace('>','') + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + str(ex).replace('<','').replace('>','')
            print(error_message)
        if len(error_message)>0:
            html_message = error_message
        else:
            html_message = html_message + "Data Ingestion Successfull for Orphan form completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'

#######################################################################################################################################################################
###############################################################Starting with High Value Data Capturing###########################################################
#######################################################################################################################################################################
    if run_high_value ==1:
        html_message = html_message + "<h2>Data Ingestion Summary for High Value Orphan Form </h2>"
        try:
            html_message = html_message + "Data Ingestion Job for High Value Orphan form started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting High Value data process')
            html_message = html_message + "Starting to fetch High Value orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting High Value orphan data process')
            hv_orphanData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1_lqYbhqhqSuGSxgJoAPYBcBnRtmly91rIznQDqhKKzE/edit?usp=sharing', 'A3', hv_orphangsheetdatapath,'MH High Value Orphans')
            hv_orphandbcolumns = ['pv_status','destination_area','cleared_shipment_tracking_id','shipment_value','weeknum','month','date','scanned_timestamp',
                                'zone','motherhub_name','shift_name','shipment_category','no_of_units','orphan_reason','is_invoice_found','received_time','tracking_id','shipment_type','content_details',
                                'lane_details','trip_id','bag_id','orphan_identified_area','orphan_photograph_link','orphan_id','bag_seal_id','brand_name','product_id','price','model',
                                'color','imei1','imei2','serial_number','ram_rom']
            # orphanGsheetColumns = orphanData.columns
            html_message = html_message + "completed fetching High Value orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Fetching High Value orphan data process Completed')
            hv_orphanData = gsheetUtility.assignDBColumns(hv_orphanData, gsheet_asset='Orphan Data', dbColumns=hv_orphandbcolumns)
            hv_orphanData = hv_orphanData.drop(columns=['weeknum','month','date'])
            hv_orphanData = data_processing.datatype_conversion(hv_orphanData, 'scanned_timestamp', 'datetime')
            hv_orphanData['scanned_date'] = hv_orphanData['scanned_timestamp'].dt.date
            hv_orphanData = data_processing.fetch_date_details(hv_orphanData, 'exception_log_timestamp', date_master_file)

            hv_orphanData.cleared_shipment_tracking_id = hv_orphanData.cleared_shipment_tracking_id.replace(r'^\s*$', np.NaN, regex=True)
            hv_orphanData['is_tracking_id_available'] = ''
            hv_orphanData.loc[hv_orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']]='No'
            hv_orphanData.loc[~hv_orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']] = 'Yes'

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to create orphan raw data files')
            html_message = html_message + "Starting to create High Value orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            hv_orphanData['shipment_value'] = hv_orphanData['shipment_value'].str.replace(',', '')
            hv_orphanData['shipment_value'] = hv_orphanData['shipment_value'].str.replace('.0', '')
            hv_orphanData.shipment_value = hv_orphanData.shipment_value.str.replace(' ', '')
            hv_orphanData.shipment_value = hv_orphanData.shipment_value.fillna(0)
            hv_orphanData.shipment_value =pd.to_numeric(hv_orphanData.shipment_value)
            hv_orphanData.orphan_id = hv_orphanData.orphan_id.str.upper()
            filenames = []
            created_raw_files = data_processing.fetch_created_files(hv_orphan_raw_data_location)
            filenames = data_processing.create_rewrite_raw_files(hv_orphanData,'scanned_date', created_raw_files, hv_orphan_raw_data_location )
            html_message = html_message + "Completed creating High Value orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Completed creating High Value orphan raw data files')

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to collate data for High Value dashboard')
            html_message = html_message + "Starting to create High Value orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            orphan_final_columns = ['shipment_value', 'cleared_shipment_tracking_id', 'scanned_timestamp', 'motherhub_name','zone','motherhub_name','shipment_category',
                        'orphan_reason','is_invoice_found','received_time','tracking_id','shipment_type','orphan_identified_area',
                        'orphan_id', 'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum','is_tracking_id_available']
            created_raw_files = data_processing.fetch_created_files(hv_orphan_raw_data_location)
            orphan_dashboard_data = data_processing.collate_data_for_dashboard(datetime.now().date(), 180, created_raw_files, hv_orphan_raw_data_location, orphan_final_columns)
            orphan_dashboard_data.to_csv(basePath + 'Dashboard/data/hv_orphan_full_data.csv', index=False)

        except Exception as ex:
            error_message = datetime.now().strftime("%d-%m-%Y %H:%M:%S") + str(ex.__class__).replace('<','').replace('>','') + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + str(ex).replace('<','').replace('>','')
            print(error_message)
        if len(error_message)>0:
            html_message = error_message
        else:
            html_message = html_message + "Data Ingestion Successfull for High Value Orphan form completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'

#######################################################################################################################################################################
###############################################################Starting with Logistics Data Capturing###########################################################
#######################################################################################################################################################################
    if run_logistics ==1:
        html_message = html_message + "<h2>Data Ingestion Summary for Logistics Orphan Form </h2>"
        try:
            html_message = html_message + "Data Ingestion Job for Logistics started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting Logistics data process')
            logisticsData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1beqaUyvM7gb8qVnl9sQdQokzKtuftfulAmqmr72IxI0/edit?usp=sharing', 'A2', logisticsgsheetdatapath,'logistics')

            logisticsdbcolumns = ['scanned_timestamp','email_address','zone','asset','hub_name','orphan_type','orphan_id','super_category','product_title','product_value','motherhub_name']
            html_message = html_message + "completed fetching Logistics orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Fetching Logistics orphan data process Completed')
            logisticsData.columns=logisticsdbcolumns
            # logisticsData = gsheetUtility.assignDBColumns(logisticsData, gsheet_asset=logisticsData['asset'], dbColumns=logisticsdbcolumns)
            logisticsData = data_processing.datatype_conversion(logisticsData, 'scanned_timestamp', 'datetime')
            logisticsData['scanned_date'] = logisticsData['scanned_timestamp'].dt.date
            logisticsData = logisticsData[logisticsData.scanned_date >= pd.to_datetime('2021-10-01')]
            logisticsData = logisticsData[logisticsData.asset.isin(['Last Mile','First Mile'])]
            logisticsData = data_processing.fetch_date_details(logisticsData, 'exception_log_timestamp', date_master_file)

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to create Logistics orphan raw data files')
            html_message = html_message + "Starting to create Logistics orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'

            logisticsData.orphan_id = logisticsData.orphan_id.str.upper()
            filenames = []
            created_raw_files = data_processing.fetch_created_files(logistics_raw_data_location)
            filenames = data_processing.create_rewrite_raw_files(logisticsData,'scanned_date', created_raw_files, logistics_raw_data_location )
            html_message = html_message + "Completed creating Logistics orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Completed creating Logistics orphan raw data files')

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to collate data for Logistics dashboard')
            html_message = html_message + "Starting to collate Logistics orphan raw data files for dashboard at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            logistics_final_columns = ['scanned_timestamp','email_address','zone','asset','hub_name','orphan_type','orphan_id','super_category','product_title','product_value', 
                                    'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum']
            created_raw_files = data_processing.fetch_created_files(logistics_raw_data_location)
            logistics_dashboard_data = data_processing.collate_data_for_dashboard(datetime.now().date(), 180, created_raw_files, logistics_raw_data_location, logistics_final_columns)
            logistics_dashboard_data.to_csv(basePath + 'Dashboard/data/logistcs_orphan_full_data.csv', index=False)
            html_message = html_message + "Completed collating Logistics orphan raw data files for dashboard at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
        except Exception as ex:
            error_message = datetime.now().strftime("%d-%m-%Y %H:%M:%S") + str(ex.__class__).replace('<','').replace('>','') + datetime.now().strftime("%d/%m/%Y %H:%M:%S") + str(ex).replace('<','').replace('>','')
            print(error_message)
    print('sending email')
    # fkEmail.send_mail(rcSPOCS, emailUserName, emailPassword, "Data Ingestion Successfull for RC Input on " + str(date.today().strftime("%d-%m-%Y")), "Data Ingestion Successfully completed at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"),filenames)
    fkEmail.send_mail(rcSPOCS, emailUserName, emailPassword, "Data Ingestion summary for :" + datetime.now().strftime("%d/%m/%Y"), html_message)
    print('Email sent successfuly')

