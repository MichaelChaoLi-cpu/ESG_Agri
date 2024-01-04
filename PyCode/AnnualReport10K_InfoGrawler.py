# -*- coding: utf-8 -*-
"""
Created on Tue Dec 19 10:40:49 2023

@author: Li Chao
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

for page in list(range(4)):
    for batch in list(range(10)):
        for row_number in list(range(1,21)):
            try:
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(2) > div:nth-child({row_number}) > button > span > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_company_name = element_within_shadow.text
                stock_name = element_within_shadow.get_attribute("title")
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(4) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_receipt_date = element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(5) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_filing_date = element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(6) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_document_date = element_within_shadow.text                
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(7) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_title= element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(8) > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_country = element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div:nth-child(9) > div:nth-child({row_number}) > button > span > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_industry = element_within_shadow.text
                
                shadow_host_xpath = "/html/body/app-root/app-industry-view/carbon-sidebar-layout/div/carbon-sidebar-layout/div[1]/app-main-grid/coral-panel/app-emerald-grid/emerald-grid"
                shadow_root = WebDriverWait(driver, 10).until(EC.presence_of_element_located((By.XPATH, shadow_host_xpath))).shadow_root
                element_within_shadow_css = f'#section0 > div > div.grid-pane.columns.scroll-disabled > div > div.column.last > div:nth-child({row_number}) > button > span'
                element_within_shadow = WebDriverWait(shadow_root, 10).until(EC.presence_of_element_located((By.CSS_SELECTOR, element_within_shadow_css)))
                element_text_DCN = element_within_shadow.text

                info = [element_text_company_name, stock_name,
                        element_text_receipt_date, element_text_filing_date,
                        element_text_document_date, element_text_title,
                        element_text_country, element_text_industry,
                        element_text_DCN]
                data_info.append(info)
                print(info)
                
                df = pd.DataFrame(data_info)
                df.to_csv("Data/Agri_DownloadedReport_AllInfoTab.csv")
                time.sleep(1)
            except:
                print(page, batch, row_number)
                
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
                
                
                
                
                
                
                
                
                