import pymongo
import requests
from urllib.parse import urlencode
from lxml import etree
import json
from urllib.request import urlretrieve


def getPage(page):
	parameters = {
			"key":"python",
			"act":"input",
			"page_index":page,	
	}
	headers = {
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1'
	}
	url = "http://search.dangdang.com/?"+ urlencode(parameters)
	res = requests.get(url,headers=headers)
	# return res.text
	with open("./dangdang.txt","w") as fp:
		fp.write(res.text)
		

def parsePage(content):
	html = etree.HTML(content)
	items = html.xpath('//li[@ddt-pit and @id]')
	x = 1
	data = {}
	for item in items:
		data[str(x)] = {
			'no' : str(x),
			'title' : item.xpath('.//a/attribute::title')[0],
			'image' : item.xpath('.//a/img/attribute::data-original')[0] if "http" not in item.xpath('.//a/img/attribute::src')[0] else item.xpath('.//a/img/attribute::src')[0],
			'desc' : item.xpath('.//p[@class="detail"]/text()').pop() if item.xpath('.//p[@class="detail"]/text()') else "No description"
					}
		x += 1
	return data

def saveToMongo(collection,data):
	
	# 將字典循環寫入, 
	for dd in data.items():
		collection.insert_one(dd[1])

def saveImage(collection):
	num = 1
	for i in collection.find({},{"_id":"0","image":"1"}):
		urlretrieve(i['image'].replace("_b_","_u_"),"./mybooks/"+str(num)+".jpg") #replace的目的是從封面圖換成大圖的規則套用
		num += 1
		
def main():
	# 連接本地mongodb
	connection = pymongo.MongoClient("localhost", 27017)
	# 創建db dangdang
	database = connection.dangdang
	# 創建集合 col_books
	col_books = database.col_books
	# 讀入已儲存的網頁文本
	with open("./dangdang.txt","r") as fp:
		content = fp.read()
	# 爬取網頁第6頁
	# html = getPage(6)
	# 解析網頁，返回解析後數據
	result = parsePage(content)
	# print(json.dumps(result,indent=1,ensure_ascii=False)) # 將數據轉成json輸出，比較漂亮。
	# saveToMongo(col_books,result) #儲存文本到Mongodb
	saveImage(col_books)  # 將db內的image提取出，並下載儲存圖片到設定好的資料夾內

if __name__ == "__main__":
	main()








'''
	本案例是到噹噹網收集關於python書籍的資料，包含書本抬頭，內容描述及圖片，
	爬取資料的工具使用requests.get()，其中組合url與其parameter的工具使用urlencode(),
	爬取下來資料採用儲存文本於本地分析，避免過多的訪問噹噹網，(因本次過程有因為訪問次數過多被禁止過)，
	解析工具使用xpath，注意的是在網頁上F12裡的內容，很可能跟實際獲取到的不同，請以實際獲取到的為搜尋依據，
	採取將蒐集到的資料先儲存在一部字典，之後返回值。資料分為兩部分使用，先是存放入mongodb，
	將字典存入db時，是由原本的字典方式，先用items()轉為tuple，再for in 以insert_one()逐一存入，方便查詢。
	儲存圖片的網址來源是由db中提取，提取方式利用for in collection.find({},{"字段":"0或1"})  
	0表示不提取(通常用在_id關閉自動顯示)，1表示顯示，注意其回傳的結果會是dict字典格式
	之後用urlretrieve()來將圖片下載儲存，在這中間需觀察網站中大小圖之間的關聯，便能修改地址獲取大圖。
	
	字典的type() # dict
		dict.items()可將字典變成字典元組 tpye() # dict_items，可供遍歷使用
	JSON的type() # str
		幾乎任何類型的資料都能轉成json json.dumps() ，經測試str,list,tuple,dict都能轉成json
		若要轉回原本類型 json.loads()即可回到原本類型
		*load和dump是針對文件使用。
	在使用xpath解析時，除了注意以實際獲取為依據，也要注意一致性，比如圖片若用延遲加載或有其他設計因素，
	其屬性可能不是src，本案例中就使用了src以及data-original兩種屬性穿插，需加判斷式。


'''