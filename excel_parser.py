import csv
import pandas as pd

def school_estate_parser(file_name, schools =[], sheet_name = 'sheet1'):
  df = pd.read_excel(file_name, sheet_name)
  df1 = df
  df2 = df1[df1["学校名称"].str.contains("明珠小学")]
  print(df2)

  for i in range(1, len(schools)):
    df1 = df
    df2 = df2.append(df1[df1["学校名称"].str.contains(schools[i])])
    print(df2)

  print(df2)
  df2.to_excel('se.xls', index = False)
  
  




  # stub for file and schools
pd_file = "2016PDXX.xls"
list0 = []
list1 = ["明珠小学", "福山外国语","上海实验学校", "第六师范附属"]
list2 = ["第二中心小学","新世界","海桐小学"]
list3 = ["浦明师范学校", "建平实验小学","浦东南路","洋泾实验",
        "昌邑小学","第二中心小学","竹园小学","进才实验","菊园"]

school_list = list1 + list2 + list3
school_estate_parser(pd_file, list0, '浦东新区')
  # endstub
