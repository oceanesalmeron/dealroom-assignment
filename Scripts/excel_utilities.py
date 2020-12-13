#!/usr/bin/env python3
# -*- coding: utf-8 -*-
"""
Created on Sun Dec 13 16:25:23 2020

@author: oceanesalmeron
"""
import pandas as pd
import xlsxwriter

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