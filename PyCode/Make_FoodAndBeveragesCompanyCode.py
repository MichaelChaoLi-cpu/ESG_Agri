# -*- coding: utf-8 -*-
"""
Created on Mon Feb  5 12:16:11 2024

@author: Li Chao
"""

import pandas as pd

report_list_1 = pd.read_csv("Data/Agri_DownloadedReport_FoodandBeverages_firstPage.csv",
                            index_col=0)
report_list_1.columns = ['Code', 'Document_Date', 'Country',
                         'Industry', 'DCN']
report_list_1['Document_Date'] = pd.to_datetime(report_list_1['Document_Date'], 
                                                format='%d-%b-%Y')

report_list_all = pd.read_csv("Data/Agri_DownloadedReport_FoodandBeverages.csv",
                            index_col=0)
report_list_all.columns = ['Code', 'Document_Date', 'Country',
                           'Industry', 'DCN']
report_list_all['Document_Date'] = pd.to_datetime(report_list_all['Document_Date'], 
                                                  format='%d-%b-%Y')

report_list_add = pd.read_excel("Data/Agri_DownloadedReport_FoodandBeverages_add.xlsx",
                                index_col=0)
report_list_add.columns = ['Code', 'Document_Date', 'Country',
                           'Industry', 'DCN']

report_list_addRow = pd.read_csv("Data/Agri_DownloadedReport_FoodandBeverages_AddRows.csv",
                                 index_col=0)
report_list_addRow.columns = ['Code', 'Document_Date', 'Country',
                              'Industry', 'DCN']
report_list_addRow['Document_Date'] = pd.to_datetime(report_list_addRow['Document_Date'], 
                                                     format='%d-%b-%Y')

report_list_addRow2 = pd.read_csv("Data/Agri_DownloadedReport_FoodandBeverages_AddRows2.csv",
                                  index_col=0)
report_list_addRow2.columns = ['Code', 'Document_Date', 'Country',
                               'Industry', 'DCN']
report_list_addRow2['Document_Date'] = pd.to_datetime(report_list_addRow2['Document_Date'], 
                                                      format='%d-%b-%Y')

report_list_addRow3 = pd.read_csv("Data/Agri_DownloadedReport_FoodandBeverages_AddRows3.csv",
                                  index_col=0)
report_list_addRow3.columns = ['Code', 'Document_Date', 'Country',
                               'Industry', 'DCN']
report_list_addRow3['Document_Date'] = pd.to_datetime(report_list_addRow3['Document_Date'], 
                                                      format='%d-%b-%Y')

report_list = pd.concat([report_list_1, report_list_all,
                         report_list_add, report_list_addRow,
                         report_list_addRow2, report_list_addRow3])

code_df = report_list[['Code']]
code_df['Code'] = code_df['Code'].str.split('^').str[0]
code_df = code_df.drop_duplicates()
#code_df.to_excel("Data/FoodAndBeveragesCompanyCode.xlsx")

report_list.to_csv("Data/FoodAndBeveragesCompanyNameCodeDID.xlsx")


