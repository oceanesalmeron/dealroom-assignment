#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Fri Dec 11 02:49:46 2020

@author: oceanesalmeron
"""

import pandas as pd
import numpy as np
import xlsxwriter

#Stopwords list from https://github.com/Yoast/YoastSEO.js/blob/develop/src/config/stopwords.js
stopwords = [ "a", "about", "above", "after", "again", "against", "all", "am", "an", "and", "any", "are", "as", "at", "be", "because", "been", "before", "being", "below", "between", "both", "but", "by", "could", "did", "do", "does", "doing", "down", "during", "each", "few", "for", "from", "further", "had", "has", "have", "having", "he", "he'd", "he'll", "he's", "her", "here", "here's", "hers", "herself", "him", "himself", "his", "how", "how's", "i", "i'd", "i'll", "i'm", "i've", "if", "in", "into", "is", "it", "it's", "its", "itself", "let's", "me", "more", "most", "my", "myself", "nor", "of", "on", "once", "only", "or", "other", "ought", "our", "ours", "ourselves", "out", "over", "own", "same", "she", "she'd", "she'll", "she's", "should", "so", "some", "such", "than", "that", "that's", "the", "their", "theirs", "them", "themselves", "then", "there", "there's", "these", "they", "they'd", "they'll", "they're", "they've", "this", "those", "through", "to", "too", "under", "until", "up", "very", "was", "we", "we'd", "we'll", "we're", "we've", "were", "what", "what's", "when", "when's", "where", "where's", "which", "while", "who", "who's", "whom", "why", "why's", "with", "would", "you", "you'd", "you'll", "you're", "you've", "your", "yours", "yourself", "yourselves" ]

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
    data['TAGLINE'] = data['TAGLINE'].apply(lambda x: [item for item in x.split() if item not in stopwords] if(np.all(pd.notnull(x))) else x)
    data.loc[df['TAGLINE'].isnull(), 'TAGLINE'] = data.loc[df['TAGLINE'].isnull(), 'TAGLINE'].apply(lambda x: [])

    return data



def classify(x, tech, education, government):
    
    dic = {'Startup' : len(set(x['ALL'])&set(tech)),
            'Universities/Schools' : len(set(x['ALL'])&set(education)),
            'Government/Non-profit' : len(set(x['ALL'])&set(government))
           }
    
    maximum = max(dic, key=dic.get)
    entity = str(maximum)
    
    if(dic[maximum] == 0):
        if (x['LAUNCH DATE']<1990):
            entity = 'Mature company'
        else :
            entity = 'Unclassified'
    elif (maximum == 'Startup'):
        if (x['LAUNCH DATE']<1990):
            entity = 'Mature company'
            
    return entity


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

    file = 'Data/Data_Science_Internship_Assignment.xlsx'
    data = pd.ExcelFile(file)
    data = data.parse('Data')
    
    df = data.drop(['WEBSITE', 'HQ REGION', 'HQ COUNTRY', 'HQ CITY', 'GROWTH STAGE', 'LINKEDIN'], axis=1)
    df = clean_data(df)
    df['ALL']=df['TAGS']+df['TAGLINE']
    
    
    tech=['software', 'mobile', 'design', 'data', 'deep tech', 'search engine', 'cloud technology', 'saas', 'video',
         'adtech', 'app', 'cleantech', 'e-commerce', 'fintech', 'regtech compliance', 'consulting services', 'hardware',
         'online', 'monitoring', 'social media', 'analytics', 'game', 'technology', 'enterprise software', 'big data',
         'tech', 'it', 'wireless technology', 'developer tools', 'seo', 'data analytics', 'imaging technology']
    
    education=['research','educational','student', 'university', 'school', 'certification', 
               'e-learnin', 'study', 'studies', 'tutorials', 'academic','assesment','academic','academics', 'learning',
              'skills', 'teach', 'teacher']
    
    government=['charity','medical', 'healthcare']
    
    df['TYPE']=df.apply(classify, args=(tech, education, government), axis=1)
    
    print(df['TYPE'].value_counts())
    
    filename = 'Data/test.xlsx'
    
    count = df['TYPE'].value_counts().rename_axis('Type').to_frame('Count')
    
    data['TYPE']=df['TYPE']
    
    print('Starting writing to excel...')
    export_excel(filename,'Count', count, True)
    export_excel(filename,'Data', data, False)
    print('Writing to excel done')















 