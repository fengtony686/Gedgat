#!/usr/bin/python
# -- coding: utf-8 --
# 这个程序可以将所在文件夹中所有文件的名称、大小以及类型制成表格
import os
import os.path
import sys
from openpyxl import Workbook


TITLE = r'文件表'


list1 = []
list2 = []
list3 = []


def get(path):
    fileList = os.listdir(path)
    for filename in fileList:
        pathTmp = os.path.join(path,filename)
        if os.path.isdir(pathTmp):
            get(pathTmp)
        elif os.path.isfile(pathTmp):
            filesize = os.path.getsize(pathTmp)
            prefix,suffix = os.path.splitext(filename)
            list1.append(prefix)
            if filesize/1073741824 >= 1:
                list2.append(str(round(filesize/1073741824,3))+"GB")
            elif filesize/1048576 >= 1:
                list2.append(str(round(filesize/1048576,3))+"MB")
            elif filesize/1024 >= 1:
                list2.append(str(round(filesize/1024,3))+"KB")
            else:
                list2.append(str(filesize)+"B")
            list3.append(suffix)


wb=Workbook()
sheet=wb.active
sheet.title = TITLE
path = sys.path[0]
get(path)
sheet["A1"] = '文件名'
sheet['B1'] = '文件大小'
sheet['C1'] = '文件类型'
sheet['D1'] = '文件名'
sheet['E1'] = '文件大小'
sheet['F1'] = '文件类型'


for i in range(int(len(list1)/2)):
  tem=int(len(list1)/2)
  sheet["A%d" % (i+2)] = list1[i+1]
  sheet["B%d" % (i+2)] = list2[i+1]
  sheet["C%d" % (i+2)] = list3[i+1]
  try:
      sheet["D%d" % (i+2)] = list1[i+tem+1]
      sheet["E%d" % (i+2)] = list2[i+tem+1]
      sheet["F%d" % (i+2)] = list3[i+tem+1]
  except:
      break


wb.save(TITLE+'.xlsx')
