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


def clean_text(x):
    x = x.astype(str)
    x = x.str.replace(r'[^\w\s]','')
    x = x.str.replace('\d+', '')
    x = x.str.lower() 
    return x



def clean_data(data):
    data['LAUNCH DATE'] = pd.to_datetime(data['LAUNCH DATE'].astype(str), errors="coerce").dt.year

    data['TAGS'] = data['TAGS'].str.split(pat=';')
    data.loc[data['TAGS'].isnull(), 'TAGS'] = data.loc[df['TAGS'].isnull(), 'TAGS'].apply(lambda x: [])
    
    data['TAGLINE']= clean_text(df['TAGLINE'])
    data['TAGLINE'] = data['TAGLINE'].str.strip()
    data['TAGLINE'] = data['TAGLINE'].apply(lambda x: [item for item in x.split() if item not in stopwords.words('english')] if(np.all(pd.notnull(x))) else x)
    data.loc[df['TAGLINE'].isnull(), 'TAGLINE'] = data.loc[df['TAGLINE'].isnull(), 'TAGLINE'].apply(lambda x: [])

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
        if (x['LAUNCH DATE']<1990):
            entity = 'Mature company'
            
    return entity


if __name__ == '__main__':


    # Load dataframe
    file = '../Data/Data_Science_Internship_Assignment.xlsx'
    data = pd.ExcelFile(file)
    data = data.parse('Data')
    
    df = data.drop(['WEBSITE', 'HQ REGION', 'HQ COUNTRY', 'HQ CITY', 'GROWTH STAGE', 'LINKEDIN'], axis=1)
    df = clean_data(df)
    df['ALL']=df['TAGS']+df['TAGLINE']
    
    
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
                'governmental','organisation']
    
    mature = ['mature', 'mutlinational', 'established', 'leader', 'leading']
    
    # Classify entities
    df['TYPE']=df.apply(classify, args=(startup, education, government, mature), axis=1)
    
    # Print entites count
    print(df['TYPE'].value_counts())
    
    # Create dataframe for export
    count = df['TYPE'].value_counts().rename_axis('Type').to_frame('Count')
    data['TYPE']=df['TYPE']
    
    # Excel export
    filename = '../Data/Results.xlsx'
    print('Writing to excel...')
    export_excel(filename,'Count', count, True)
    export_excel(filename,'Data', data, False)
    print('Writing to excel done')