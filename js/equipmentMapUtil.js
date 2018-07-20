var queryHouseOutline = function(hid, callback){
	var baseURL = 'http://map.baidu.com/?reqflag=pcmap&coord_type=3&from=webmap&qt=ext&ext_ver=new&l=18';
	var url = baseURL + "&uid=" + hid;
	callback && (window.queryHouseOutlineCallback = callback);
	$.ajax({
		type: "get",
		async: false,
		url: url,
		dataType: "jsonp",
		jsonpCallback: "queryHouseOutlineCallback",
		success: function(datas) {
		}
	});
};

/**
 * 模糊查询小区信息, 无返回值
 * @param {} house	小区名称
 * @param {} city	所属城市名称
 * @param {} ak		百度地图AK
 * @param {} callback	回调函数，该函数可以接收到请求的返回值
 */
var queryHouse = function(house, city, ak, callback){
	var baseURL = 'http://api.map.baidu.com/place/v2/search?output=json&scope=2';
	var url = baseURL + "&q=" + house + "&region=" + city + "&ak=" + ak;
	callback && (window.queryHouseCallback = callback);
	$.ajax({
		type: "get",
		async: false,
		url: url,
		dataType: "jsonp",
		jsonpCallback: "queryHouseCallback",
		success: function(datas) {
		}
	});
};

/**
 * 墨卡托坐标转百度坐标
 * @param {} coordinate
 * @return {}
 */
var coordinateToPoints = function(map, coordinate) {
	var points = [];
	if (coordinate) {
		var arr = coordinate.split(";");
		if(arr){
			for(var i = 0; i < arr.length; i++){
				var coord = arr[i].split(",");
				if(coord && coord.length == 2){
					var mctXY = new BMap.Pixel(coord[0], coord[1]);    
					var project = map.getMapType().getProjection();
					var point = project.pointToLngLat(mctXY);   
					points.push(new BMap.Point(point.lng, point.lat));
				}
			}
		}
	}
	return points;
};

/**
 * 墨卡托坐标解析
 * @param {} mocator
 * @return {}
 */
var parseGeo = function(mocator){
	if(typeof mocator != 'string'){
		return {};
	}
	var t = mocator.split("|");
	var n = parseInt(t[0]);
	var i = t[1];
	var r = t[2];
	var o = r.split(";");
	if(n === 4){
		for (var a = [], s = 0; s < o.length - 1; s++){
			"1" === o[s].split("-")[0] && a.push(o[s].split("-")[1]);
		}
		o = a;
		o.push("");
	}
	var u = [];
	switch(n){
		case 1:
			u.push(o[0]);
			break;
		case 2:
		case 3:
		case 4:
			for (var s = 0; s < o.length - 1; s++) {
				var l = o[s];
				if (l.length > 100){
					l = l.replace(/(-?[1-9]\d*\.\d*|-?0\.\d*[1-9]\d*|-?0?\.0+|0|-?[1-9]\d*),(-?[1-9]\d*\.\d*|-?0\.\d*[1-9]\d*|-?0?\.0+|0|-?[1-9]\d*)(,)/g,
									"$1,$2;");
					u.push(l);
				} else {
					for (var c = [], d = l.split(","), f = 0; f < d.length; f += 2) {
						var p = d[f];
						var h = d[f + 1];
						c.push(p + "," + h);
					}
					u.push(c.join(";"))
				}
			}
			break;
		default:
			break;
	}
	
	if(u.length <= 1){
		u = u.toString();
	}
	
	var result = {
		type : n,
		bound : i,
		points : u
	};
	return result;
};

