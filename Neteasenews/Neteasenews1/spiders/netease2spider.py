#-*- coding: utf-8 -*-

import re
import scrapy
path = r'D:\Experiment\IR_Scrapy\Neteasenews\result\\'

class NeteaseSpider(scrapy.Spider):
    name = "netease2"
    start_urls = [
        'http://travel.163.com/17/1126/08/D45FTEFF00068AIR.html', 
		'http://news.163.com/17/1126/02/D44QK3EQ0001875P.html',
		'http://news.163.com/17/1126/02/D44SLD3U00018AOR.html',
		'http://news.163.com/17/1126/01/D44NKF91000187VI.html'
    ]

    def parse(self, response):
		filename = response.url.split('/')[-4] + response.url.split('/')[-3] + '_' + response.url.split('/')[-2] + '_' + response.url.split('/')[-1].split('.')[0] + '.txt'
		
		f = open(path + filename, 'wb')
		f.write(response.url + '\n')
		
		titles = response.xpath('//*[@id="epContentLeft"]/h1').extract()
		for segment in titles:
			f.write(segment.encode('utf-8') + '\n')

		text = response.xpath('//*[@id="endText"]/p/text()').extract()
		for section in text:
			f.write(section.encode('utf-8') + '\n')
		f.close()
		
		next_pages = re.findall(r'http://[a-z]{1,7}.163.com/\d{2}/\d{4}/\d{2}/\w{16}.html',response.body)
		for next_page in next_pages:
			next_page = response.urljoin(next_page)
			yield scrapy.Request(next_page, callback=self.parse)