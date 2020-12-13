#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sat Dec 12 18:46:09 2020

@author: oceanesalmeron
"""

import pandas as pd
import numpy as np
import time
from excel_utilities import export_excel
from selenium import webdriver
from selenium.webdriver.common.desired_capabilities import DesiredCapabilities


def scroll_to_end(driver):
    prev_len = driver.execute_script("return document.body.scrollHeight")
    while True:
        driver.execute_script("window.scrollTo(0, document.body.scrollHeight);")
        time.sleep(0.5)
        new_len = driver.execute_script("return document.body.scrollHeight")
        if new_len == prev_len:
            break
        prev_len = new_len


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
    
    
if __name__ == '__main__':
    
    url = 'https://www.ycombinator.com/companies/'
    
    caps = DesiredCapabilities().CHROME
    caps["pageLoadStrategy"] = "eager"
    driver = webdriver.Chrome(desired_capabilities=caps, executable_path='../chromedriver')

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
    export_excel('../Data/Results.xlsx','Scraping results', data, False)