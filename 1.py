import requests
from lxml import etree
import json

def getPage():
	''' # 將購物車內頁寫入本地
	try:
		headers = {
			        'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/535.1 (KHTML, like Gecko) Chrome/14.0.835.163 Safari/535.1',
			    	#'Cookie' : '用來download本帳號內的html頁面,已完成購物車頁面下載'

			    }
		url = "https://cart.jd.com/cart.action"
		res = requests.get(url,headers=headers)
		html = res.content.decode("utf-8")

		with open("jdcart.html","w") as fp:
			fp.write(html)
		return html

	except:
		return None
	'''
	with open("jdcart.html","r") as fp:
		content = fp.read()
		return content

def parsePage(html):
	html = etree.HTML(html)
	items = html.xpath('//*[@cid]')
	x = 1
	data = {}
	for item in items:
		data[str(x)] = {
			'title' : item.xpath('.//img/attribute::alt')[0],
			'image' : "https:"+ item.xpath('.//img/attribute::src')[0],
			'amount' : item.xpath('.//div[1]/div[4]/p[1]/strong/text()')[0],
			'quantity' : item.xpath('.//div[@class="quantity-form"]/input/attribute::value')[0],
			'sum' : item.xpath('.//div[1]/div[6]/strong/text()')[0],
		}
		x += 1
	return data

def main():
	html = getPage()
	result = parsePage(html)
	print(json.dumps(result,indent=1,ensure_ascii=False)) #encure_ascii默認為True,需調整回False(原本是UTF8)
	#for item in parsePage(html):
	#	pass

if __name__ == "__main__":

	main()




'''
學習點:
:47 print(json.dumps(result,indent=1,ensure_ascii=False)) #encure_ascii默認為True,需調整回False(原本是UTF8)
:36 'image' : "https:"+ item.xpath('.//img/attribute::src')[0], #attribute::src
:10 cookie 的放入可幫助爬蟲通過session進入購物車
'''
