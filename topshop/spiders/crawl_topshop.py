import scrapy
import time
import logging
import requests

from random import randint
from selenium import webdriver
from topshop.items import TOPItem

class TOPSpider(scrapy.Spider):
    name = "topshop"
    allowed_domains = ["asos.com"]
    start_urls = [
        "http://www.asos.com/Women/New-In-Clothing/Cat/pgecategory.aspx?cid=2623&r=2#/parentID=-1&pge=1&pgeSize=36&sort=-1",
    ]

    def __init__(self):
        self.driver = webdriver.Firefox()
        
    def parse(self, response):
        payload = {'cid':'2623', 'currentPage':'9', 'pageSize':'36','pageSort':'-1','countryId':'10085'} 
        r = requests.get(response.url, params=payload)
        logging.debug(r)
        self.driver.get(response.url)
        while True:
            next = self.driver.find_element_by_xpath("//li[@class='page-skip']/a")
            logging.debug ("next defined")
            try:
                logging.debug ("it got here")
                next.click()
                time.sleep(randint(2,6))
                yield scrapy.Request(response.url, callback=self.parse_item_content)
                logging.debug (self.driver.current_url)
            except:
                logging.debug ("there's something wrong!")
                break
                
        self.driver.close()
        
    def parse_item_content(self, response):
        for sel in response.xpath("//ul[@id='items']/li"):
            item = TOPItem()
            item["product_title"] = sel.xpath("a[@class='desc']/text()").extract()
            item["product_link"] = sel.xpath("a[@class='desc']/@href").extract()
            item["product_price"] = sel.xpath("div/span[@class='price']/text()").extract()
            item["product_img"] = sel.xpath("div/a[@class='productImageLink']/img/@src").extract()
            yield item