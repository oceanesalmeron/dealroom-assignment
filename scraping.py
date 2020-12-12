#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 18:46:09 2020

@author: oceanesalmeron
"""

import pandas as pd
import numpy as np
import xlsxwriter
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities

def scroll_to_end(driver):
    while len(driver.find_elements_by_xpath("//a[@class='SharedDirectory-module__company___AVmr6 no-hovercard']"))<1000 :
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")


def get_links(x):
    links = []
    for result in x:
        s=result.get_attribute('href')
        links.append(s.split('/')[-1])
        
    return links

def retrieve_info(driver):
    facts = driver.find_elements_by_css_selector(".facts div span")
    socials = driver.find_elements_by_css_selector(".social")
               
    item = {'name': driver.find_element_by_class_name("heavy").text, 
            'info': driver.find_element_by_css_selector(".main-box h3").text,
            'description': driver.find_element_by_class_name("pre-line").text,
            'website': driver.find_element_by_css_selector(".main-box .links a").get_attribute('href'),
            'launch_year': facts[0].text,
            'team_size': facts[1].text,
            'location': facts[2].text
            }
            
    for social in socials:
        item[social.get_attribute('class').split()[-1]] = social.get_attribute('href')
        
    return item


def export_excel(Filename,Sheetname,df,ind):
    try:
        xlsx_file = pd.ExcelFile(Filename)
    except:
        xlsxwriter.Workbook(Filename)
        xlsx_file = pd.ExcelFile(Filename)

    writer = pd.ExcelWriter(Filename, engine='openpyxl')
    IsSheetThereAlready = False
    for sheet in xlsx_file.sheet_names:
        if sheet == Sheetname:
            df.to_excel(writer,sheet_name= sheet, startrow=0, index=ind)
            IsSheetThereAlready = True

        else:
            df2 = xlsx_file.parse(sheet)
            df2.to_excel(writer,sheet_name= sheet, index=False)


    if IsSheetThereAlready is False:
        df.to_excel(writer,sheet_name = Sheetname, index=False)

    writer.save()

    return
    
    
if __name__ == '__main__':
    
    url = 'https://www.ycombinator.com/companies/'
    
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path='./chromedriver')

    driver.get(url)
    
    scroll_to_end(driver)
    
    results = driver.find_elements_by_xpath("//a[@class='SharedDirectory-module__company___AVmr6 no-hovercard']")
    
    links=get_links(results)
    
    dic = []
    for link in links:
        driver.get(url+link)
        item=retrieve_info(driver)
        dic.append(item)
        
    data = pd.DataFrame.from_dict(dic)
    data.replace(r'^\s*$', np.nan, regex=True, inplace = True)

    print('Starting writing to excel ',len(links),' rows...')
    export_excel('Data/test.xlsx','Scraping', data, False)