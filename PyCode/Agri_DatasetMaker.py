
from google.cloud import bigquery
import os
import pandas as pd
import re

def BqDatasetGetter(Table_Name=''):
    
    key_path = 'Key/key.json'
    client = bigquery.Client.from_service_account_json(key_path)
    
    table = client.get_table(Table_Name)
    df = client.list_rows(table).to_dataframe()
    return df

def GetRID(text):
    match = re.search(r'\d+(?=\.pdf)', text)
    if match:
        number = match.group()
        return number
    else:
        number = ''
        return number
        
    
if __name__ == '__main__':
    Table_Name = 'quixotic-sol-387506.CPT_results.CPT_esg_trendency_agri_ESG06'
    DatasetFromBq = BqDatasetGetter(Table_Name)
    
    ReportInfoTable = pd.read_csv('Data/Agri_DownloadedReport_AllInfoTab.csv', 
                                  index_col=0)
    ReportInfoTable.columns = ['company_name', 'stock_name',
                               'receipt_date', 'filing_date',
                               'document_date', 'doc_title',
                               'country', 'industry',
                               'RID']
    ReportInfoTable = ReportInfoTable.dropna()
    ReportInfoTable['RID'] = ReportInfoTable['RID'].apply(int)
    ReportInfoTable['RID'] = ReportInfoTable['RID'].apply(str)
    ReportInfoTable = ReportInfoTable.drop_duplicates()
    
    DataPreProcess = DatasetFromBq.dropna()
    DataPreProcess['RID'] = DataPreProcess['nake_name'].apply(GetRID)
    DataPreProcess['RID'] = DataPreProcess['RID'].apply(int)
    DataPreProcess['RID'] = DataPreProcess['RID'].apply(str)
    
    merged_df = pd.merge(DataPreProcess, ReportInfoTable, on='RID', how='inner')
    
    AimComp = merged_df[['company_name']].drop_duplicates()
    AimComp.to_csv('Data/AimCompanyName.csv')
