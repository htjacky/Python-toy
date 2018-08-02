# store house info to json file

import urllib
import json

#base_map_url = "http://api.map.baidu.com/place/v2/search?output=json&scope=2"
base_map_url = 'http://api.map.baidu.com/geocoder/v2/'
ak = "zr5YTwdDL2PS7g5N4VckLvtQD22IgoVf"
data_dir = 'database/'
stub_info_file = "house_info"

def get_lng_lat(addr):
    #comm_url = base_map_url + "&q=" + urllib.parse.quote(addr) + "&region=shanghai&ak=" + ak
    comm_url = base_map_url + '?' + 'address=' + urllib.parse.quote(addr)  + '&output=json&ak=' + ak
    print(comm_url)
    print('before loads\n')
    req = urllib.request.urlopen(comm_url)
    #res = req.read().decode()
    json_res = req.read()
    print(json_res)
    temp = json.loads(json_res)
    print('after loads\n')
    print(temp)
    return temp
    
#def store_all_house_info(commu_str, house_num):
def store_all_house_info(comm_str, school_str, house_num):
    #result = get_lng_lat(commu_str.strip())
    #lng = result['result']['location']['lng'] #采用构造的函数来获取经度
    #lat = result['result']['location']['lat'] #获取纬度
    #str_temp = '{"commu":\"' + commu_str + '\","lat":' + str(lat) + ',"lng":' + str(lng) + \
    #        ',"count":' + str(house_num) +'},\n'
    #str_temp = '{"commu":\"' + comm_str + '\",count":' + str(house_num) +'},\n'
    str_temp = '{"commu":\"' + comm_str + '\","school":"' + school_str + '\","count":' + str(house_num) +'},\n'
    json_file = open(data_dir + stub_info_file + '.json', 'a')
    json_file.write(str_temp)
    json_file.close()

def store_house_info(commu_str, school_str, house_num):
    result = get_lng_lat(commu_str.strip())
    lng = result['result']['location']['lng'] #采用构造的函数来获取经度
    lat = result['result']['location']['lat'] #获取纬度
    #lng = get_lng_lat(commu_str.strip())[2]['location']['lng'] #采用构造的函数来获取经度
    #lat = get_lng_lat(commu_str.strip())[2]['location']['lat'] #获取纬度
    str_temp = '{"commu":' + commu_str + ',"lat":' + str(lat) + ',"lng":' + str(lng) + \
            ',"count":' + str(house_num) +'},\n'
    #house_file = open(r'house_info.json','a')
    file_name = data_dir + school_str + '.json'
    json_file = open(file_name,'a')
    json_file.write(str_temp)
    json_file.close()

def format_json_files(file_name):
    json_file = open(data_dir + file_name+'.json','r+')
    content = json_file.read()
    json_file.seek(0,0)
    json_file.write('[' + content + ']')
    json_file.close()

def reset_json_files(file_name):
    json_file = open(data_dir + file_name+'.json','w')
    json_file.write('')
    json_file.close()
