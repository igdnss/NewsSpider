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

	start_urls = ['http://news.qq.com']
	name='tencent'
	allowed_domains=['news.qq.com']

	base_url = 'http://news.qq.com'
	tp = ['am','pm']

	day = ['02']
	year = ['2017']
	month = ['08']
	
	fileName = ''
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
# 				TODO: fix bug: has an error when extract pubtime
		bracePos = content.index('{')-1
		tempData = content[bracePos:]
		pubTimeTail = tempData.index('pubtime')+len('pubtime')+2
		#=======================================================================
		# try:
		# 	pubTimeTail = tempData.index('pubtime')+len('pubtime')+2
		# except ValueError,e:
		# 	print 'pubtime: '+e
		# finally:
		# 	quit()
		#=======================================================================
		timeStr = tempData[pubTimeTail:pubTimeTail+16]
		return timeStr
	    
	def parse(self,response):
		url = self.base_url
		
		yield scrapy.Request(url,self.parseList)

	
	def parseList(self,response):
		print("--------------parsing list--------------")
		urls = response.xpath("//a/@href").extract()
# 		temp="20170806" #will be used at middle night
		temp = self.generateSubPath()
		print("===================================")
		for url in urls:
			if(url.find('sports.qq.com')>=0 and len(url)==21):
				print("--------------sports--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://finance.qq.com/')>=0 and len(url)==22):
				print("--------------finance--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			
			#===================================================================
			# if(url.find('http://finance.qq.com/')>=0 and len(url)==22):
			# 	print("--------------finance--------------"+url)
			# 	yield scrapy.Request(url,self.parseType,dont_filter=True)	
			#===================================================================
				
				
			elif(url.find('http://ent.qq.com/')>=0 and len(url)==18):
				print("--------------ent--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://tech.qq.com/')>=0 and len(url)==19):
				print("--------------tech--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://auto.qq.com/')>=0 and len(url)==19):
				print("--------------auto--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://house.qq.com/')>=0 and len(url)==20):
				print("--------------house--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://fashion.qq.com/')>=0 and len(url)==22):
				print("--------------fashion--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			elif(url.find('http://cul.qq.com/')>=0 and len(url)==18):
				print("--------------cul--------------"+url)
				yield scrapy.Request(url,self.parseType,dont_filter=True)
			
	# parse kinds of type of news
	def parseType(self,response):
		print("--------------parsing type--------------")
		urls = response.xpath("//a/@href").extract()
		temp = self.generateSubPath()
		for url in urls:
			if 'http' in url or temp in url:
				url = url 
				if 'http' in url and temp in url:
					print("--------------with http url--------------"+url)
					yield scrapy.Request(url,self.parseNews,dont_filter=True)
				elif temp in url:
					url = response.url+url
					print("--------------with temp url--------------"+url)
					yield scrapy.Request(url,self.parseNews,dont_filter=True)
			
	def parseNews(self,response):
		print("--------------parsing news--------------")
		data = response.xpath("//div[@id='Cnt-Main-Article-QQ']")
		item = NewsSpiderItem()
		timee = data.xpath("//span[@class='article-time']/text()").extract()
		content = response.xpath("//div[@id='Cnt-Main-Article-QQ']/p[@style='TEXT-INDENT: 2em']/text()").extract()
		cc=''
		if len(content)>0:
			self.fileName = response.url[-10:-4]+".txt" 
			scriptCnt = response.xpath("//script[1]/text()").extract()
			url = response.url
			title = response.xpath("//title/text()").extract()
			for c in content:
				cc = cc+c+'\n'
			content = cc.strip()
			time = self.getTimeStr(scriptCnt[0])
			print("--------------questions urls--------------"+response.url)
			title = u''.join(title[0]).encode('utf-8')
			print("--------------questions title--------------"+title)
			content = u''.join(content).encode('utf-8')
			print("--------------content title--------------"+content)
			if(len(content) > 0):
				if(url.find("sports.qq.com") >= 0):
					self.save("tencent/sports/", url, time, title, content)
				elif(url.find("finance.qq.com") >= 0 or url.find("money.qq.com") >= 0 or url.find("stock.qq.com") >= 0):
					self.save("tencent/finance/", url, time, title, content)
				elif(url.find("ent.qq.com") >= 0): 
					self.save("tencent/ent/", url, time, title, content)
				elif(url.find("tech.qq.com") >= 0):
					self.save("tencent/tech/", url, time, title, content)
				elif(url.find("auto.qq.com") >= 0): 
					self.save("tencent/auto/", url, time, title, content)
				elif(url.find("house.qq.com") >= 0):
					self.save("tencent/house/", url, time, title, content)
				elif(url.find("fashion.qq.com") >= 0): 
					self.save("tencent/fashion/", url, time, title, content)
				elif(url.find("cul.qq.com") >= 0):
					self.save("tencent/cul/", url, time, title, content)
				 
	def save(self,newsType,newsUrl,newsTime,newsTitle,newsContent):
		print("--------------saving file--------------")
		current_dir = os.path.dirname(__file__)
		rel_path = self.path_prefix+newsType+self.fileName
		abs_file_path = os.path.join(current_dir, rel_path)
		print("--------------******************abs_file_path--------------"+abs_file_path)
		file = open(abs_file_path,"w") 
		file.write("\""+"url"+"\""+":"+"\""+newsUrl+"\""+'\n') 
		file.write("\""+"time"+"\""+":"+"\""+newsTime+"\""+'\n') 
		file.write("\""+"title"+"\""+":"+"\""+newsTitle+"\""+'\n') 
		file.write("\""+"content"+"\""+":"+"\""+newsContent+"\""+'\n') 
		file.close()
			
