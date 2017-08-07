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
import os

class TencentSpider(scrapy.Spider):

	name='tencent'
	start_urls = ['http://sports.qq.com/']
	allowed_domains=['sports.qq.com']

	base_url = 'http://sports.qq.com'
	tp = ['am','pm']

	day = ['02']
	year = ['2017']
	month = ['08']
	
	fileTitle = ''
	path_prefix = '../../../testdata/data/'

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
	
	#get the time from news page in string
	def getTimeStr(self,content):
		bracePos = content.index('{')-1
		tempData = content[bracePos:]
		pubTimeTail = tempData.index('pubtime')+len('pubtime')+2
		timeStr = tempData[pubTimeTail:pubTimeTail+16]
		return timeStr
	    
	def parse(self,response):
		url = self.base_url
# 		print("--------------******************path_prefix_1--------------"+self.path_prefix)
		
		yield scrapy.Request(url,self.parseList)

	
	def parseList(self,response):
# 		print("--------------******************path_prefix_2--------------"+self.path_prefix)
		urls = response.xpath("//a/@href").extract()
# 		temp="20170806" will be used at middle night
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
# 		print("--------------******************path_prefix_3--------------"+self.path_prefix)
		data = response.xpath("//div[@id='Cnt-Main-Article-QQ']")
		item = NewsSpiderItem()
		timee = data.xpath("//span[@class='article-time']/text()").extract()
		content = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@style='TEXT-INDENT: 2em']/text()").extract()
		cc=''
		if len(content)>0:
# 			current_dir = os.path.dirname(__file__)
			self.fileTitle = response.url[-10:-4]+".txt" 
# 			path_prefix = "../../../testdata/data/"
			scriptCnt = response.xpath("//script[1]/text()").extract()
			url = response.url
			title = response.xpath("//title/text()").extract()
			for c in content:
				cc = cc+c+'\n'
			content = cc.strip()
			time = self.getTimeStr(scriptCnt[0])
			
			if(url.find("sports.qq.com")>=0):
				#TODO: to abstract the following code to a method
				title = u''.join(title[0]).encode('utf-8')
				content = u''.join(content).encode('utf-8')
				self.save("tencent/sports/", url, time, title, content)
				 #==============================================================
				 # rel_path = path_prefix+"tencent/sports/"+fileTitle
				 # abs_file_path = os.path.join(current_dir, rel_path)
				 # print("--------------******************abs_file_path--------------"+abs_file_path)
				 # file = open(abs_file_path,"w") 
				 # file.write("\""+"url"+"\""+":"+"\""+url+"\""+'\n') 
				 # file.write("\""+"time"+"\""+":"+"\""+time+"\""+'\n') 
				 # title = u''.join(title[0]).encode('utf-8')
				 # content = u''.join(content).encode('utf-8')
				 # file.write("\""+"title"+"\""+":"+"\""+title+"\""+'\n') 
				 # file.write("\""+"content"+"\""+":"+"\""+content+"\""+'\n') 
				 # file.close()
				 #==============================================================
				 
	def save(self,newsType,newsUrl,newsTime,newsTitle,newsContent):
		print("--------------******************path_prefix_4--------------"+self.path_prefix)
		current_dir = os.path.dirname(__file__)
		print("--------------******************current_dir--------------"+current_dir)
		rel_path = self.path_prefix+newsType+self.fileTitle
		print("--------------******************rel_path--------------"+rel_path)
		abs_file_path = os.path.join(current_dir, rel_path)
		print("--------------******************abs_file_path--------------"+abs_file_path)
		file = open(abs_file_path,"w") 
		file.write("\""+"url"+"\""+":"+"\""+newsUrl+"\""+'\n') 
		file.write("\""+"time"+"\""+":"+"\""+newsTime+"\""+'\n') 
# 		title = u''.join(title[0]).encode('utf-8')
# 		content = u''.join(content).encode('utf-8')
		file.write("\""+"title"+"\""+":"+"\""+newsTitle+"\""+'\n') 
		file.write("\""+"content"+"\""+":"+"\""+newsContent+"\""+'\n') 
		file.close()
			
