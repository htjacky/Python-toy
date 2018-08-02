# craw house data from LianJia/AnJuKe/FangTianXia
# LianJia https://blog.csdn.net/haohaixingyun/article/details/51839956
#         https://www.linchun.com.cn/technic/634.html
# FangTianXia https://blog.csdn.net/yiranhwj/article/details/52680536
#             https://zhuanlan.zhihu.com/p/25713752
# AnJuKe https://segmentfault.com/a/1190000013932818
# 2018.7.25 first implement only with Lianjia data

from bs4 import BeautifulSoup

import re
import urllib
import urllib.request
import math
import codecs
import pandas as pd

import excel_parser
import view_house

lj_domain='http://sh.lianjia.com/'
lj_house_url = lj_domain + 'ershoufang/pudong/'
#se_file='se.xls'
num_per_page = 30.0
down_price = 100
up_price = 450

#def getHouseInfo(house_soup, h_list, comm_name):
#def getHouseInfo(house_soup, comm_name, school_str):
def getHouseInfo(house_soup, comm_name, school_str, h_list):
    for tag in  house_soup.find('ul',class_='sellListContent').find_all('div', class_="info"):
        href        = tag.find('a').get('href')
        title       = tag.find('a').string
        addr_commu  = tag.find('div',class_="houseInfo").a.string
        addr_info   = tag.find('div',class_="houseInfo").a.next_sibling
        floor       = tag.find('div',class_="flood").find('div',class_="positionInfo").span.next_sibling
        area        = tag.find('div',class_="flood").find('div',class_="positionInfo").a.string
        total_price = tag.find('div',class_="totalPrice").span.string + \
                tag.find('div',class_="totalPrice").span.next_sibling
        unit_price  = tag.find('div',class_="unitPrice").span.string
        #house_info  = [href, title, addr_commu, addr_info, total_price, unit_price]
        house_info  = [href, title, addr_commu, addr_info, total_price.strip("万"), unit_price, school_str]
        if addr_commu.find(comm_name) != -1:
            #print('%s is %s, Add:\n%s\n' %(addr_commu, comm_name, house_info))
            h_list.append(house_info)
            #return house_info
        else:
            # here is a bug: 广洋苑  is not 广洋苑二期, just skip
            # 东方城市花园(一期)  is not 东方城市花园一期
            #大华锦绣华城(十一街区)  is not 11街区, just skip:  ['上海市浦东新区昌邑小学(大华校区)'] 
            print('%s is not %s, just skip:\n%s\n' %(addr_commu, comm_name, house_info))


def getHouseInfoForOneCommu(community, house_list):
#def getHouseInfoForOneCommu(community):
    house_num = 0
    #house_list = []
    print(community)
    comm_str = str(community[1]).strip('[]')
    comm_str = comm_str.strip('\'')
    school_str = str(community[0]).strip('[]')
    school_str = school_str.strip('\'')
    #print(comm_str)
    #print(school_str)
    #comm_url=r'http://sh.lianjia.com/ershoufang/lc2lc1bp200ep400rs潍坊二村/'
    comm_url = lj_house_url + 'lc2lc1bp' + str(down_price) + 'ep' + str(up_price) + 'rs' \
        + urllib.parse.quote(comm_str)
    #print(comm_url)
    try:
        xiao_html_doc = urllib.request.urlopen(comm_url).read()
        xiaoqu_soup = BeautifulSoup(xiao_html_doc, 'html.parser')
        house_num=int(xiaoqu_soup.find("h2",class_="total fl").find('span').string)
    except:
        print("search %s failed!\n" %comm_str)
        return house_list

    #print(house_num)

    if house_num == 0:
        print('no house found')
        return house_list

    if house_num > 300:
        print('300+ house in %s found, maybe the address is wrong!!!\n' %comm_str)
        return house_list
   
    try:
        #view_house.store_house_info(comm_str, school_str, house_num)
        # store all the house info with the same school in a data file
        # a stub to store in house_info.json
        #view_house.store_all_house_info(comm_str, house_num)
        view_house.store_all_house_info(comm_str, school_str, house_num)
   
        #getHouseInfo(xiaoqu_soup,house_list,comm_str)
        getHouseInfo(xiaoqu_soup, comm_str, school_str, house_list)
        #house_list.append(getHouseInfo(xiaoqu_soup,comm_str))
        #house_list.append(getHouseInfo(xiaoqu_soup,comm_str, school_str))
    except:
        print("store %s failed!\n" %comm_str)
        return house_list 

    total_page = math.ceil(house_num / num_per_page)
    for page_index in range(2, int(total_page)+1):
        page_url = lj_house_url + 'pg' + str(page_index) + 'lc2lc1bp' + str(down_price) \
            + 'ep' + str(up_price) + 'rs' + urllib.parse.quote(comm_str)
        page_html_doc= urllib.request.urlopen(page_url).read()
        page_soup = BeautifulSoup(page_html_doc, 'html.parser')
        #getHouseInfo(page_soup,house_list,comm_str)
        getHouseInfo(page_soup, comm_str, school_str, house_list)
        #house_list.append(getHouseInfo(page_soup,comm_str, school_str))
    return house_list




# Start from here

# 1. extract the best schools' info into se.xls
excel_parser.school_estate_parser(excel_parser.pd_in_file, excel_parser.school_list, '浦东新区')

# 2. get all the school names, to create files by school name
school_list = excel_parser.get_all_school_list(excel_parser.se_file)
for school in school_list:
    school_name = str(school).strip('[]').strip('\'')
    view_house.reset_json_files(school_name)

# 3. it's a stub to store in house_info.json
view_house.reset_json_files(view_house.stub_info_file)

# 4. store all the data into database by school name, not finished yet;
# still store the data in house_info.json temparily
community_list = excel_parser.get_all_community_list(excel_parser.se_file)
all_house_data = []
for community in community_list:
    getHouseInfoForOneCommu(community, all_house_data)
    #all_house_data.append(getHouseInfoForOneCommu(community))

# 5. format school info files into a valid json format
for school in school_list:
    school_name = str(school).strip('[]').strip('\'')
    view_house.format_json_files(school_name)

# 6. store all the data into excel to check
house_df = pd.DataFrame(all_house_data)
house_df.to_excel(view_house.data_dir + 'lianjia_house_info.xls')

# 7. sorted by price
house_df = house_df.sort_values(by=4)
house_df.to_excel(view_house.data_dir + 'lianjia_house_sorted.xls')

