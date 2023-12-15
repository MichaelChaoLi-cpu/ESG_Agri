#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Tue Dec 12 10:55:33 2023

@author: lichao
"""

import pandas as pd
import regex as re
from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
import time

with open('Key/EikonKey.txt', 'r') as file:
    file_content = file.read()

print(file_content)

driver = webdriver.Chrome()

eikon = 'https://apac1-apps.platform.refinitiv.com/web/Apps/IndustryApp#/filings'
driver.get(eikon)

#driver.switch_to.frame(driver.find_element(By.TAG_NAME, 'iframe'))

iframe_xpath = '//*[@id="AppFrame"]'
iframe_element = driver.find_element(By.XPATH, iframe_xpath)
driver.switch_to.frame(iframe_element)

iframe_xpath = '//*[@id="contentframe"]'
iframe_element = driver.find_element(By.XPATH, iframe_xpath)
driver.switch_to.frame(iframe_element)

iframe_xpath = '//*[@id="AppFrame"]'
iframe_element = driver.find_element(By.XPATH, iframe_xpath)
driver.switch_to.frame(iframe_element)

iframe_xpath = '/html/body/ui-view/div/ui-view/div/div[2]/iframe'
iframe_element = driver.find_element(By.XPATH, iframe_xpath)
driver.switch_to.frame(iframe_element)

data_info = []
fail_array = []

for page in list(range(13)):
    for batch in list(range(10)):
        for row_number in list(range(1,21)):
            try:
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_xpath = f'#section0 > div.tr-lg > div.grid-pane.columns > div > div:nth-child(4) > div:nth-child({row_number}) > button > div > app-icon:nth-child(2) > coral-icon'
                WebDriverWait(shadow_root, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_within_shadow_xpath))).click()
                time.sleep(80)
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div.tr-lg > div.grid-pane.columns > div > div:nth-child(3) > div:nth-child({row_number}) > button > span > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_company_name = element_within_shadow.text
                stock_name = element_within_shadow.get_attribute("title")
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div.tr-lg > div.grid-pane.columns > div > div:nth-child(6) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_filing_date = element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div.tr-lg > div.grid-pane.columns > div > div:nth-child(7) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_doc_date = element_within_shadow.text
                
                shadow_host_xpath_download = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[2]/app-sidebar/div/app-doc-viewer/carbon-sidebar-layout/div/lib-document-viewer/lib-pdf-viewer-wrapper/div/coral-panel[1]/coral-button[1]"
                shadow_root_download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath_download))).shadow_root
                element_within_shadow_xpath_download = '#icon'
                WebDriverWait(shadow_root_download, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_within_shadow_xpath_download))).click()
                time.sleep(10)
                
                #print(element_text_company_name)
                #print(element_text_filing_date)
                #print(stock_name)
                
                info = [element_text_company_name, element_text_filing_date, element_text_doc_date, stock_name]
                data_info.append(info)
                print(info)
                
                df = pd.DataFrame(data_info)
                df.to_csv("Data/DownloadedReport.csv")
            except:
                print(page, batch, row_number)
                fail_array.append([page, batch, row_number])
                fail_df = pd.DataFrame(fail_array)
                fail_df.to_csv("Data/FailToDownload.csv")
        
        shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
        shadow_host = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath)))
        shadow_root = driver.execute_script('return arguments[0].shadowRoot', shadow_host)
        scrollable_element_selector = 'div.grid-scrollbar.grid-vscroll.grid-scroll-fadeout'
        scrollable_element = shadow_root.find_element(By.CSS_SELECTOR, scrollable_element_selector)
        driver.execute_script("arguments[0].scrollTop += 650;", scrollable_element)
    
    shadow_host_xpath_download = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/div/span/emerald-pagination"
    shadow_root_download = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath_download))).shadow_root
    element_within_shadow_xpath_download = '#next'
    WebDriverWait(shadow_root_download, 10).until(EC.element_to_be_clickable((By.CSS_SELECTOR, element_within_shadow_xpath_download))).click()
    
    print(f"****{page+1}****")





