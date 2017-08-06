#encoding=utf-8
import scrapy
from news_spider.items import NewsSpiderItem
import json
import time 
import re
import datetime
import json
from pip._vendor.requests.packages.urllib3.util import url
from __builtin__ import str
import sys

class TencentSpider(scrapy.Spider):

# 	start_urls = ['http://news.qq.com']
	start_urls = ['http://sports.qq.com/']
	name='tencent'
# 	allowed_domains=['news.qq.com']
	allowed_domains=['sports.qq.com']

# 	base_url = 'http://news.qq.com/b/history/index'
# 	base_url = 'http://news.qq.com'
	base_url = 'http://sports.qq.com'
#	year = ['2016','2015','2014']
#	month = ['12','11','10','09','08','07','06','05','04','03','02','01']
#	day = ['31','30','29','28','27','26','25','24','23','22','21',
#		   '20','19','18','17','16','15','14','13','12','11','10',
#		   '09','08','07','06','05','04','03','02','01']
	tp = ['am','pm']

	#===========================================================================
	# day = ['31']
	# year = ['2016']
	# month = ['03']
	#===========================================================================
	
	day = ['02']
	year = ['2017']
	month = ['08']

	#===========================================================================
	# def parse(self,response):
	# 	for y in self.year:
	# 		for m in self.month:
	# 			for d in self.day:
	# 				for t in self.tp:
	# 					url = self.base_url+y+m+d+t+'.shtml?'
	# 					yield scrapy.Request(url,self.parseList)
	#===========================================================================
	def generateSubPath(self):
		currentTime = datetime.datetime.now()
		year = str(currentTime.year)
		month = str(currentTime.month)
		day = str(currentTime.day)
		if len(month) < 2:
			month = '0'+month
		if len(day) < 2:
			day = '0'+day
		return 'a/'+year+month+day
	#===========================================================================
	# def getTimeStr(self,content):
	# 	bracePos = content.index('{')-1
	# 	tempData = content[bracePos:]
	# 	pubTimeTail = tempData.index('pubtime')+len('pubtime')+2
	# 	timeStr = tempData[pubTimeTail:pubTimeTail+16]
	# 	return timeStr
	#===========================================================================
	    
	def parse(self,response):
# 		abcd = self.generateSubPath()
# 		print abcd
		url = self.base_url
		print("--------------******************--------------"+url)
		
		yield scrapy.Request(url,self.parseList)

	
	def parseList(self,response):
		urls = response.xpath("//a/@href").extract()
# 		print len(urls)
		print("--------------******************--------------"+str(len(urls)))
# 		temp = 'a/20170802'
		temp = self.generateSubPath()
		print("==================================="+temp)
# 		file = open("testfile.txt","w") 
		for url in urls:
# 			if 'http' in url and temp in url:
			if 'http' in url or temp in url:
				url = url 
# 				print("--------------????????????????????--------------"+url)
				if 'http' in url and temp in url:
# 					file.write(url+'\n') 
					print("--------------????????????????????--------------"+url)
					yield scrapy.Request(url,self.parseNews)
				elif temp in url:
					url = self.base_url+url
# 					file.write(url+'\n') 
					print("--------------????????????????????--------------"+url) 
					yield scrapy.Request(url,self.parseNews)
# 				yield scrapy.Request(url,self.parseNews)
		
	def parseNews(self,response):
		data = response.xpath("//div[@id='Cnt-Main-Article-QQ']")
		item = NewsSpiderItem()
		timee = data.xpath("//span[@class='article-time']/text()").extract()
# 		title = data.xpath("//div[@class='hd']//h1/text()").extract()
		content = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@style='TEXT-INDENT: 2em']/text()").extract()
		cc=''
		if len(content)>0:
			fileTitle = response.url[-10:-4]+".txt";
			file = open(fileTitle,"w") 
			scriptCnt = response.xpath("//script[1]/text()").extract()
			url = response.url
			title = response.xpath("//title/text()").extract()
			for c in content:
				cc = cc+c+'\n'
			content = cc.strip()
			print("--------------the content is : --------------"+content)
			print("--------------the title is :--------------"+title[0])
			print("--------------the url is :--------------"+url)
			position = scriptCnt[0].index('{')-1
			data = scriptCnt[0][position:]
			position = data.index('pubtime')+len('pubtime')+2
			time = data[position:position+16]
			print("--------------the time is :--------------"+time)
			file.write("\""+"url"+"\""+":"+"\""+url+"\""+'\n') 
			file.write("\""+"time"+"\""+":"+"\""+time+"\""+'\n') 
			title = u''.join(title[0]).encode('utf-8')
			content = u''.join(content).encode('utf-8')
			file.write("\""+"title"+"\""+":"+"\""+title+"\""+'\n') 
			file.write("\""+"content"+"\""+":"+"\""+content+"\""+'\n') 
			#===================================================================
			# file.write("\""+"title"+"\""+":"+"\""+title[0]+"\""+'\n') 
			# file.write("\""+"content"+"\""+":"+"\""+content+"\""+'\n') 
			#===================================================================
			file.close()
