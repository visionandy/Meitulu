# -*- coding: utf-8 -*-
import os
import sys
import uuid

import requests
import scrapy
from bs4 import BeautifulSoup

reload(sys)
sys.setdefaultencoding('utf-8')


class MeituluSpider(scrapy.Spider):
	name = "meitulu"
	allowed_domains = ["meitulu.com"]
	start_urls = [
		"https://www.meitulu.com/t/nvshen/",
		"https://www.meitulu.com/t/nvshen/2.html",
		"https://www.meitulu.com/t/nvshen/3.html",
		"https://www.meitulu.com/t/nvshen/4.html",
		"https://www.meitulu.com/t/nvshen/5.html",
		"https://www.meitulu.com/t/nvshen/6.html",
		"https://www.meitulu.com/t/nvshen/7.html",
		"https://www.meitulu.com/t/nvshen/8.html",
		"https://www.meitulu.com/t/nvshen/9.html",
		"https://www.meitulu.com/t/nvshen/10.html",
		"https://www.meitulu.com/t/nvshen/11.html",
		"https://www.meitulu.com/t/nvshen/12.html",
		"https://www.meitulu.com/t/nvshen/13.html",
		"https://www.meitulu.com/t/nvshen/14.html",
		"https://www.meitulu.com/t/nvshen/15.html",
		"https://www.meitulu.com/t/nvshen/16.html",
		"https://www.meitulu.com/t/nvshen/17.html",
		"https://www.meitulu.com/t/nvshen/18.html",
		"https://www.meitulu.com/t/nvshen/19.html",
		"https://www.meitulu.com/t/nvshen/20.html",
		"https://www.meitulu.com/t/nvshen/21.html",
		"https://www.meitulu.com/t/nvshen/22.html",
		"https://www.meitulu.com/t/nvshen/23.html",
		"https://www.meitulu.com/t/nvshen/24.html",
		"https://www.meitulu.com/t/nvshen/25.html",
		"https://www.meitulu.com/t/nvshen/26.html",
		"https://www.meitulu.com/t/nvshen/27.html",
	
	]
	
	def parse(self, response):
		soup = BeautifulSoup(response.text, "lxml")
		for slice in list(soup.find('ul', {'class': "img"}).children):
			if (type(slice.find("a")) != type(1)):
				yield scrapy.Request(url=str(slice.find("a").attrs['href']), callback=self.parse_category)
	
	def parse_category(self, response):
		res_page = []
		soup = BeautifulSoup(response.text, "lxml")
		pages_temp = list(soup.find('div', {'id': "pages"}).children)
		res_page = [response.text]
		for page in range(2, int(pages_temp[-3].get_text().encode("utf-8")) + 1):
			page_url = response.url[:-5] + "_" + str(page) + ".html"
			res_page.append(page_url)
		for i in res_page:
			yield scrapy.Request(url=i, callback=self.parse_content)
	
	def parse_content(self, response):
		soup_pages = BeautifulSoup(response.text, "lxml")
		images_pages = soup_pages.find_all('img', class_="content_img")
		images_pages = list(images_pages)
		for src in images_pages:
			self.downloadImg(response.url, src.attrs['src'], str(unicode(soup_pages.title.string)).split("_")[0])
	
	def downloadImg(self, refer, url, cate):
		response = requests.get(url, headers={
			'Host': 'mtl.ttsqgs.com',
			'Connection': 'Keep-Alive',
			'Accept': 'image/webp,image/apng,image/*,*/*;q=0.8',
			'Upgrade-Insecure-Requests': '1',
			'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/48.0.2564.116 Safari/537.36',
			'Referer': refer,
			'Accept-Encoding': 'gzip, deflate, br',
			'Accept-Language': 'lt,en-us;q=0.8,en;q=0.6,ru;q=0.4,pl;q=0.2'
		})
		self.mkdir(cate)
		
		with open(cate + "/" + os.path.basename(url), 'wb') as f:
			f.write(response.content)
	
	# 生成文件目录
	def mkdir(self, path):
		path = path.strip()
		path = path.rstrip("\\")
		isExists = os.path.exists(path)
		if not isExists:
			os.makedirs(path)
			print path + ' 创建成功'
			return True
		else:
			# 如果目录存在则不创建，并提示目录已存在
			print path + ' 目录已存在'
			return False