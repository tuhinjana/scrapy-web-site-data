import scrapy
from scrapy.spiders import CrawlSpider, Rule
from scrapy.linkextractors import LinkExtractor
from ..items import UrpartsItem


class ManufacturerSpider(scrapy.Spider):
    name = 'manufacturer'
    allowed_domains = ['www.urparts.com']
    start_urls = ['http://www.urparts.com/index.cfm/page/catalogue']
    base_url = 'http://www.urparts.com/'
    all_data = {}

    def parse(self, response):
        
        all_manufacturers = response.xpath('//*[@id="content"]/div/div/ul/li')
        for each_manu in all_manufacturers:
            text = './/a/text()'
            manu_title = each_manu.xpath(text).extract_first().strip()
            path = './/a/@href'
            category_url = each_manu.xpath(path).extract()

            category_url = self.base_url + category_url[0]
            self.all_data[manu_title] = {}
            req = scrapy.Request(category_url, callback=self.parse_category)
            req.meta['manu_title'] = manu_title
            yield req

    def parse_category(self, response):
            manu_title = response.meta['manu_title']
            categories = response.xpath('//*[@id="content"]/div/div/ul/li')
            if categories:
                for model in categories:
                    category_name = model.xpath('.//a/text()').extract_first().strip()
                    category_url = model.xpath('.//a/@href').extract_first()
                    category_url = self.base_url + category_url
                    self.all_data[manu_title][category_name] = {}
                    req = scrapy.Request(category_url, callback=self.parse_model)
                    req.meta['manu_title'] = manu_title
                    req.meta['category_title'] = category_name
                    yield req

    def parse_model(self, response, ):
        manu_title = response.meta['manu_title']
        category_title = response.meta['category_title']
        models = response.xpath('//*[@id="content"]/div/div[2]/ul/li')
        if models:
            for model in models:
                    model_title = model.xpath('.//a/text()').extract_first()
                    model_url = model.xpath('.//a/@href').extract_first()
                    model_url = self.base_url + model_url
                    self.all_data[manu_title][category_title][model_title] = {}
                    req = scrapy.Request(model_url, callback=self.parse_parts)
                    req.meta['manu_title'] = manu_title
                    req.meta['category_title'] = category_title
                    req.meta['model_title'] = model_title
                    yield req

    def parse_parts(self, response, ):
        manu_title = response.meta['manu_title']
        category_title = response.meta['category_title']
        model_title = response.meta['model_title']
        parts = response.xpath('//*[@id="content"]/div/div/div/ul/li')
        if parts:
            for part in parts[:1]:
                    part_title = part.xpath('./a/text()').extract_first().replace('-', '').strip()
                    pc_name = part.xpath('./a/span/text()').extract_first().strip()
                    self.all_data[manu_title][category_title][model_title][part_title] = {}
                    item = UrpartsItem()

                    item['manufacturer'] = manu_title
                    item['category'] = category_title
                    item['model'] = model_title
                    item['part'] = part_title
                    item['part_category'] = pc_name
                    yield item

