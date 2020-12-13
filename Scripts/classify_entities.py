#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 02:49:46 2020

@author: oceanesalmeron
"""

import pandas as pd
import numpy as np
import nltk
from nltk.corpus import stopwords
#nltk.download('stopwords')
from excel_utilities import export_excel

def load_data(file):
    data = pd.ExcelFile(file)
    data = data.parse('Data')
    return data
    

def clean_text(x):
    x = x.astype(str)
    x = x.str.replace('\d+', '')
    x = x.str.lower() 
    return x


def clean_tag(x):
    x = clean_text(x)
    x = x.str.split(pat=';')
    return x
    

def clean_tagline(x):
    x = clean_text(x)
    x = x.str.replace(r'[^\w\s]','')
    x = x.str.strip()
    x = x.apply(lambda i: [item for item in i.split() if item not in stopwords.words('english')])
    return x


def remove_duplicates(x):
    return list(dict.fromkeys(x))


def clean_data(data):
    
    # Clean date
    data.rename(columns={'LAUNCH DATE':'LAUNCH_DATE'}, inplace=True)
    ## Convert date string to date format and only keep the year
    data['LAUNCH_DATE'] = pd.to_datetime(data['LAUNCH_DATE'].astype(str), errors="coerce").dt.year

    # Clean TAGS column
    data['TAGS'] = clean_tag(data['TAGS'])
    data.loc[data['TAGS']=='nan', 'TAGS'] = data.loc[data['TAGS']=='nan', 'TAGS'].apply(lambda x: [])
    
    # Clean TAGLINE column
    data['TAGLINE']= clean_tagline(df['TAGLINE'])
    data.loc[data['TAGLINE']=='nan', 'TAGLINE'] = data.loc[data['TAGLINE']=='nan', 'TAGLINE'].apply(lambda x: [])
    
    return data


def classify(x, tech, education, government, mature):
    
    dic = {'Startup' : len(set(x['ALL'])&set(tech)),
            'Universities/Schools' : len(set(x['ALL'])&set(education)),
            'Government/Non-profit' : len(set(x['ALL'])&set(government)),
            'Mature company' : len(set(x['ALL'])&set(mature))
            }
    
    maximum = max(dic, key=dic.get)
    entity = str(maximum)
    
    if(dic[maximum] == 0):
        entity = 'Unclassified'
    elif (maximum == 'Startup'):
        if (x['LAUNCH_DATE']<1990):
            entity = 'Mature company'
            
    return entity


if __name__ == '__main__':


    # Load dataframe
    data = load_data('../Data/Data_Science_Internship_Assignment.xlsx')
    
    df = data.drop(['WEBSITE', 'HQ REGION', 'HQ COUNTRY', 'HQ CITY', 'GROWTH STAGE', 'LINKEDIN'], axis=1)
    df = clean_data(df)
    df['ALL']=df['TAGS']+df['TAGLINE']
    df['ALL']=df['ALL'].apply(remove_duplicates)
    
    # Build list of keywords
    startup=['software', 'mobile', 'design', 'data', 'deep tech', 'search engine', 'cloud technology', 'saas', 'video',
          'adtech', 'app', 'cleantech', 'e-commerce', 'fintech', 'regtech compliance', 'consulting services', 'hardware',
          'online', 'monitoring', 'social media', 'analytics', 'game', 'technology', 'enterprise software',
          'tech', 'it', 'wireless technology', 'developer tools', 'seo', 'data analytics', 'imaging technology',
          'machine', 'deep', 'artificial', 'solutions', 'startup','services']
    
    education=['research','educational','student', 'university', 'school', 'certification', 
                'e-learning', 'study', 'studies', 'tutorials', 'academic','assesment','academics', 'learning',
              'skills', 'teach', 'teacher', 'education']
    
    government=['charity','medical', 'healthcare','profit','non-profit','volunteer', 'volunteering', 
                'governmental','governement', 'organisation']
    
    mature = ['mature', 'mutlinational', 'established', 'leader', 'leading']
    
    # Classify entities
    df['TYPE']=df.apply(classify, args=(startup, education, government, mature), axis=1)
    
    # Print entities count
    print(df['TYPE'].value_counts())
    
    data['TYPE']=df['TYPE']
    
    # Excel export
    filename = '../Data/Results.xlsx'
    print('Writing to excel...')
    export_excel(filename,'Count', df['TYPE'].value_counts().rename_axis('Type').to_frame('Count'), True)
    export_excel(filename,'Data', data, False)
    print('Writing to excel done')