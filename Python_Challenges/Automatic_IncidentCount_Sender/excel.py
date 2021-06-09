import xlrd
import os.path
wb = xlrd.open_workbook('C:/Users/abhr/Desktop/abhi.xlsx')
wb.sheet_names()
sh = wb.sheet_by_index(0)
i = 1
file = open("Output.txt", "w")
while sh.cell(i,1).value != 0:
   Load = sh.cell(i,1).value
   DB1 = str(Load)
   file.write(DB1 + '\n')
   i = i + 1
file.close
