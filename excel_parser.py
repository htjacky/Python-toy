# This file is mainly used for parsing school estate excel
import csv
import pandas as pd
import numpy as np

# stub for file and schools
data_dir = 'database/'
pd_in_file = data_dir + "2016PDXX.xls"
se_file = data_dir + "se.xls"
list0 = []
list1 = ["明珠小学", "福山外国语","上海实验学校", "第六师范附属"]
list2 = ["第二中心小学","新世界","海桐小学"]
list3 = ["浦明师范学校", "建平实验小学",
        "竹园小学","进才实验","菊园"]
list4 = ["浦东南路","洋泾实验","昌邑小学"]
school_list = list1 + list2 + list3
# endstub

def get_cols(file_name, cols, sheet_name = 'Sheet1'):
    df = pd.read_excel(file_name, sheet_name, usecols=cols)
    df = df.drop_duplicates()
    np_data = np.array(df)
    col_list = np_data.tolist()
    print(col_list)
    return col_list


def get_all_community_list(house_file):
    return get_cols(house_file, [3,6])


def get_all_school_list(house_file):
    return get_cols(house_file, [3])


def school_estate_parser(file_name, schools =[], sheet_name = 'Sheet1'):
    df = pd.read_excel(file_name, sheet_name)
    df2 = pd.DataFrame()
    print(df2)
    for i in range(1, len(schools)):
        df1 = df
        df2 = df2.append(df1[df1["学校名称"].str.contains(schools[i])])
    print(df2)
    df2.to_excel(se_file, index = False)

