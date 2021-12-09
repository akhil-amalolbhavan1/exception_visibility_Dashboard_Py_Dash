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
    
    rc_raw_data_location = 'ETL/RC_Raw_Data/'
    mh_raw_data_location = 'ETL/MH_Raw_Data/'
    orphan_raw_data_location = 'ETL/Orphan_Raw_Data/'

    today = date.today()
    today = str(today.year) + "-" + str('{:02d}'.format(today.month)) + "-" + str('{:02d}'.format(today.day))
    
    rcgsheetdatapath = 'ETL/gsheet_data/rc_data/' + today + '.csv'
    mhgsheetdatapath = 'ETL/gsheet_data/mh_data/' + today + '.csv'
    orphangsheetdatapath = 'ETL/gsheet_data/orphan_data/' + today + '.csv'

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
    run_orphan = 1
    run_high_value = 0
    #######################################################################################################################################################################
    ###############################################################Starting with RC Exception ####Data Capturing###########################################################
    #######################################################################################################################################################################
    if run_rc==1:
        try:    
            html_message = html_message + "Data Ingestion Job for RC started at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting RC data process')
            rcData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1kCMwH7tq2RoiugdoDKe3xFYMgp_P4WvidwMtG3tNAUo/edit?usp=sharing', 'A3', rcgsheetdatapath,'RC')
            # rcData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1g4n416j5xGvgwV7KnDHpEPyN1mrsGgH5durMXT2hxHU/edit?usp=sharing','A3')
            rcGsheetData = rcData.iloc[0:,0:19].copy()
            rcDBColumns = ['rc_received_timestamp','received_by','rc_name','orphan_id','orphan_id_condition','fsn_identified_warehouse','wsn_id','final_area_rc','business_unit','supercategory','expiry_date','product_title','packaging_condition','damaged_physical_segregation','damaged_quantity','damaged_scan_box_id','non_damaged_physical_segregation','non_damaged_quantity','non_damaged_scan_box_id']
            rcColumns= rcGsheetData.columns
            rcGsheetData = gsheetUtility.assignDBColumns(rcGsheetData, gsheet_asset='Retrun Center', dbColumns=rcDBColumns)
            rcGsheetData = rcGsheetData.fillna('NA')
            rcGsheetData.orphan_id = rcGsheetData.orphan_id.str.upper()
            rcGsheetData.orphan_id = rcGsheetData.orphan_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)

            html_message = html_message + "Fetching Data for RC completed at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S")+ '<br>'
            # rcGsheetData = data_processing.func_column_strip(rcGsheetData)
            rcGsheetData = data_processing.fun_replace_empty_data(rcGsheetData)
            
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Finishing fetching RC process Completed')
            rcGsheetData = data_processing.datatype_conversion(rcGsheetData, 'rc_received_timestamp', 'datetime')
            scanned_dates = rcGsheetData.rc_received_timestamp.unique()
            
            print('coalesce columns')
            
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['non_damaged_physical_segregation','damaged_physical_segregation'], 'physical_segregation')
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['damaged_quantity','non_damaged_quantity'], 'quantity')
            rcGsheetData = data_processing.coalesce_columns(rcGsheetData, ['damaged_scan_box_id','non_damaged_scan_box_id'], 'scan_box_id')
            # print('droping unused columns')
            # rcGsheetData.drop(columns=['non_damaged_physical_segregation','damaged_physical_segregation','damaged_quantity','non_damaged_quantity','damaged_scan_box_id','non_damaged_scan_box_id'], inplace=True)
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
            
            created_raw_files = data_processing.fetch_created_files(mh_raw_data_location)
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
            mhData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1aeODc4c7bxvYs0iI1eJ2nbHTExLCEkA77D5C9X3sxQg/edit?resourcekey#gid=793332736', 'A2', mhgsheetdatapath, 'MH')
            # rcData = gsheetUtility.get_gsheet_data('https://docs.google.com/spreadsheets/d/1g4n416j5xGvgwV7KnDHpEPyN1mrsGgH5durMXT2hxHU/edit?usp=sharing','A3')
            mhGsheetData = mhData.copy()

            # mhDBColumns = ['exception_log_timestamp', 'scanned_by', 'scanned_asset', 'asset_type', 'exception_type', 'dg_offload_tracking_id', 'dg_offload_is_rto', 'suspected_malicious_tracking_id', 'content_missing_tracking_id', 'closed_vendor_orphan_id',
            #                 'closed_vendor_scan_tracking_id', 'damaged_shipment_type', 'damaged_shipment_tracking_id', 'damaged_shipment_image_url', 'duplicate_shipment_orphan_id', 'duplicate_shipment_type', 'duplicate_shipment_tracking_id',
            #                 'orphan_orphan_id', 'orphan_shipment_category', 'orphan_reason', 'orphan_is_invoice_available', 'orphans_shipment_type', 'orphans_super_category', 'orphan_shipment_image_url']
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
            print('check1')
            # mhGsheetData = data_processing.coalesce_columns(mhGsheetData, 'dg_offload_tracking_id','damaged_physical_segregation','physical_segregation')
            # mhGsheetData = data_processing.coalesce_columns(mhGsheetData, 'damaged_quantity','non_damaged_quantity','quantity')
            # mhGsheetData = data_processing.coalesce_columns(mhGsheetData, 'damaged_scan_box_id','non_damaged_scan_box_id','scan_box_id')

            mhGsheetData.orphan_id = mhGsheetData.orphan_id.str.upper()
            mhGsheetData.orphan_id = mhGsheetData.orphan_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)
            mhGsheetData.tracking_id = mhGsheetData.tracking_id.str.upper()
            mhGsheetData.tracking_id = mhGsheetData.tracking_id.apply(lambda x: 'NA' if ((x =='N/A') | (x == 'N\A')) else x)
            # rcGsheetData = data_processing.func_column_strip(rcGsheetData)
            mhGsheetData = data_processing.fun_replace_empty_data(mhGsheetData)
            print('check2')
            # print(rcData.head(5))
            # print(rcGsheetData)
            print(datetime.now().strftime("%d/%m/%Y %H:%M:%S") + ' Finishing fetching MH process Completed')
            # mhGsheetData['scanned_date'] = pd.to_datetime(mhGsheetData['exception_log_timestamp']).dt.date.astype(str)
            # print(mhGsheetData['exception_log_timestamp'])
            print('check3')
            # mhGsheetData['scanned_date'] = pd.to_datetime(mhGsheetData['exception_log_timestamp'],'%m/%d/%y %H:%M:%S').dt.date
            mhGsheetData['scanned_date'] = pd.to_datetime(mhGsheetData['exception_log_timestamp']).dt.date
            # print(mhGsheetData['scanned_date'])
            # data_processing.datatype_conversion(mhGsheetData, 'exception_log_timestamp', 'datetime')
            # mhGsheetData['month'] = pd.to_datetime(mhGsheetData['scanned_date']).dt.month_name().str.slice(stop=3)
            # mhGsheetData['year'] = pd.to_datetime(mhGsheetData['scanned_date']).dt.year
            mhGsheetData = data_processing.datatype_conversion(mhGsheetData, 'exception_log_timestamp', 'datetime')
            mhGsheetData = data_processing.fetch_date_details(mhGsheetData, 'exception_log_timestamp', date_master_file)
            print(mhGsheetData[['scanned_date','weekend','month_year','weeknum']])
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

            # print('Successfuly Completed')

            created_raw_files = data_processing.fetch_created_files(mh_raw_data_location)

            mh_final_columns = ['exception_log_timestamp', 'scanned_by', 'hub_name', 'asset_type', 'exception_type', 'tracking_id', 'dg_offload_is_rto',
                                'orphan_id', 'shipment_type', 'shipment_image_url', 'orphan_shipment_category', 'orphan_reason', 'orphan_is_invoice_available',
                                'orphans_super_category', 'zone','is_marketplace', 'orphan_shipment_image_url', 'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum']
            # mh_final_columns = ['exception_log_timestamp', 'scanned_by', 'hub_name', 'asset_type', 'exception_type', 'tracking_id', 'dg_offload_is_rto',
            #                     'orphan_id', 'shipment_type', 'shipment_image_url', 'orphan_shipment_category', 'orphan_reason', 'orphan_is_invoice_available',
            #                     'orphans_super_category', 'zone', 'scanned_date','month', 'year']
            
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
            orphandbcolumns = ['shipment_value', 'weeknum', 'cleared_shipment_tracking_id', 'month', 'date', 'orphan_scanned_timestamp', 'motherhub_name',	'shipment_category', 'orphan_reason', 
                                'is_invoice_available', 'shipment_type', 'content_details', 'lane_details_semi_large', 'consignment_id_semi_large', 'bag_id',	'orphan_idnetified_mh_area', 'image_url', 
                                'orphan_unique_id', 'bag_seal_id', 'seller_name', 'seller_id', 'seller_type']
            # orphanGsheetColumns = orphanData.columns
            html_message = html_message + "completed fetching orphan raw data from google sheet : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Fetching orphan data process Completed')
            orphanData = gsheetUtility.assignDBColumns(orphanData, gsheet_asset='Orphan Data', dbColumns=orphandbcolumns)
            orphanData = orphanData.drop(columns=['weeknum','month','date'])
            orphanData = data_processing.datatype_conversion(orphanData, 'orphan_scanned_timestamp', 'datetime')
            orphanData['scanned_date'] = orphanData['orphan_scanned_timestamp'].dt.date
            orphanData = data_processing.fetch_date_details(orphanData, 'exception_log_timestamp', date_master_file)

            orphanData.cleared_shipment_tracking_id = orphanData.cleared_shipment_tracking_id.replace(r'^\s*$', np.NaN, regex=True)
            orphanData['is_tracking_id_available'] = ''
            orphanData.loc[orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']]='No'
            orphanData.loc[~orphanData.cleared_shipment_tracking_id.isna(), ['is_tracking_id_available']] = 'Yes'
            # print(df['is_tracking_id_available'])
            # orphanData['age']=0
            # orphanData['age'] = (datetime.today().date() - pd.to_datetime(orphanData['scanned_date']).dt.date)/np.timedelta64(1, 'D')
            # # print(orphanData['age'])
            # orphanData['ageing_category'] = orphanData['age'].apply(lambda x: '1st week' if x <= 7 else ('2nd week' if ((x >7) & (x <= 14) ) else ('3rd week') if ((x >14) & (x <= 21) ) else ('4th week' if ((x >21) & (x <= 27) ) else 'Older than 4 weeks')))
            # print(orphanData['ageing_category'])

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to create orphan raw data files')
            html_message = html_message + "Starting to create orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            orphanData['shipment_value'] = orphanData['shipment_value'].str.replace(',', '')
            orphanData['shipment_value'] = orphanData['shipment_value'].str.replace('.0', '')
            orphanData.shipment_value = orphanData.shipment_value.fillna(0)
            orphanData.shipment_value =pd.to_numeric(orphanData.shipment_value)
            orphanData.orphan_unique_id = orphanData.orphan_unique_id.str.upper()
            filenames = []
            created_raw_files = data_processing.fetch_created_files(orphan_raw_data_location)
            filenames = data_processing.create_raw_files(orphanData,'scanned_date', created_raw_files, orphan_raw_data_location )
            html_message = html_message + "Completed creating orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Completed creating orphan raw data files')

            print(datetime.now().strftime("%m/%d/%Y %H:%M:%S") + ' Starting to collate data for dashboard')
            html_message = html_message + "Starting to create orphan raw data files at : " + datetime.now().strftime("%m/%d/%Y %H:%M:%S") + '<br>'
            orphan_final_columns = ['shipment_value', 'cleared_shipment_tracking_id', 'orphan_scanned_timestamp', 'motherhub_name',	'shipment_category', 'orphan_reason', 
                        'is_invoice_available', 'shipment_type', 'content_details', 'lane_details_semi_large', 'consignment_id_semi_large', 'bag_id',	'orphan_idnetified_mh_area', 'image_url', 
                        'orphan_unique_id', 'bag_seal_id', 'seller_name', 'seller_id', 'seller_type', 'scanned_date', 'weekend', 'month', 'year', 'month_year','weeknum','is_tracking_id_available']
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


    print('sending email')
    # fkEmail.send_mail(rcSPOCS, emailUserName, emailPassword, "Data Ingestion Successfull for RC Input on " + str(date.today().strftime("%d-%m-%Y")), "Data Ingestion Successfully completed at " + datetime.now().strftime("%d/%m/%Y %H:%M:%S"),filenames)
    fkEmail.send_mail(rcSPOCS, emailUserName, emailPassword, "Data Ingestion summary for :" + datetime.now().strftime("%d/%m/%Y"), html_message)
    print('Email sent successfuly')