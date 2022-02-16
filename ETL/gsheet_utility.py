# from Email_Code import send_mail
import pygsheets
import pandas as pd
from datetime import datetime
#from Email_code import * 


def get_gsheet_data(gsheetUrl, datasclearcell, ghseetdatalocation, asset, sheetnumber):
    gc = pygsheets.authorize(service_file='/Users/a/Documents/GitHub/exception_visibility/ETL/Client_Secret.json')
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' Starting Fetching Gsheet Data')
    sh = gc.open_by_url(gsheetUrl)
    ws = sh[sheetnumber] #Selecting the sheet
    gsheetDF = pd.DataFrame(pd.DataFrame(ws.get_all_values(include_tailing_empty=False, include_tailing_empty_rows=False)))
    print(datetime.now().strftime("%m/%d/%Y, %H:%M:%S") + ' Fetching Gsheet Completed')
    print(asset)
    if asset=='RC':
        # print('inside RC')
        gsheetcolumn = gsheetDF.iloc[1:2]
        gsheetDF.columns = gsheetcolumn.values.tolist()[0]
        gsheetDF = gsheetDF.iloc[2:,:]
    else:
        # print('else')
        gsheetcolumn = gsheetDF.iloc[:1]
        # print(gsheetcolumn)
        gsheetDF.columns = gsheetcolumn.values.tolist()[0]
        gsheetDF = gsheetDF.iloc[1:,:]

    gsheetDF.to_csv(ghseetdatalocation, index=False)
    print(datasclearcell)
    # ws.clear(start=datasclearcell)
    return gsheetDF

def assignDBColumns(gsheetDF, gsheet_asset, dbColumns=[]):
    # columnMap = {}
    # for index in range(0,len(dbColumns)-1):
    #     columnMap[gsheetColumns[index]]=dbColumns[index]
    #     print(columnMap)
    # gsheetDF.rename(columns=columnMap, inplace=True)
    gsheetDF.columns=dbColumns
    gsheetDF['asset'] = gsheet_asset
    return gsheetDF


# if __name__ == '__main__':
