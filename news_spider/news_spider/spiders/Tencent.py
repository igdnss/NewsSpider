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

	start_urls = ['http://sports.qq.com/']
	name='tencent'
	allowed_domains=['sports.qq.com']

	base_url = 'http://sports.qq.com'
	tp = ['am','pm']

	day = ['02']
	year = ['2017']
	month = ['08']

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
		url = self.base_url
		print("--------------******************--------------"+url)
		
		yield scrapy.Request(url,self.parseList)

	
	def parseList(self,response):
		urls = response.xpath("//a/@href").extract()
		temp = self.generateSubPath()
		print("===================================")
		for url in urls:
			if 'http' in url or temp in url:
				url = url 
				if 'http' in url and temp in url:
					yield scrapy.Request(url,self.parseNews)
				elif temp in url:
					url = self.base_url+url
					yield scrapy.Request(url,self.parseNews)
		
	def parseNews(self,response):
		data = response.xpath("//div[@id='Cnt-Main-Article-QQ']")
		item = NewsSpiderItem()
		timee = data.xpath("//span[@class='article-time']/text()").extract()
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
			position = scriptCnt[0].index('{')-1
			data = scriptCnt[0][position:]
			position = data.index('pubtime')+len('pubtime')+2
			time = data[position:position+16]
			file.write("\""+"url"+"\""+":"+"\""+url+"\""+'\n') 
			file.write("\""+"time"+"\""+":"+"\""+time+"\""+'\n') 
			title = u''.join(title[0]).encode('utf-8')
			content = u''.join(content).encode('utf-8')
			file.write("\""+"title"+"\""+":"+"\""+title+"\""+'\n') 
			file.write("\""+"content"+"\""+":"+"\""+content+"\""+'\n') 
			file.close()
