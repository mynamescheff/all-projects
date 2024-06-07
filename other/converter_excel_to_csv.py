import os
import openpyxl

#get absolute directory path

path = os.path.abspath(os.path.dirname(__file__))
print(path)

#load the excel file
wb = openpyxl.load_workbook(os.path.join(path, 'data.xlsx'))
print(wb.sheetnames)

#select sheet named 'Sheet1'
sheet = wb['Sheet1']

#convert the sheet to csv
openpyxl.worksheet.csv.writer(sheet, os.path.join(path, 'data.csv'))

