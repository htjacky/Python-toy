# Python-toy
It's a toy project try to crawl school house info data from website.

Input data file is 2016PDXX.xls.
There are several output datafiles:
	1. se.xls # it's a temp file, store all the "good school“ infomation
	2. lianjia_house_info.xls # store all the school districts house info
	3. lianjia_sort.xls # the same as lianjia_house_info.xls, just sorted the data by price.
	4. house_info.json # the house info could be parsed by JS, to show on Baidu map API, function not complete yet.
	5. 上海市XXX.json # the same as house_info.json, function not complete yet.


source file info:
	excel_parser.py: a utility to parse excel file
	view_house.py： a utility to store house info into json files, a confusing name...
	start_up.py: the main function was putting here, just run it is enough.
	view_map.html: you could open this file to show the schoold disticts on BAIDU map, need to install web server first.

