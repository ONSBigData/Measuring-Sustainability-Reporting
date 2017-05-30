# -*- coding: utf-8 -*-
from scrapy.spiders import Spider
from scrapy.http import Request
from scrapy.http.response.html import HtmlResponse
from scrapy.linkextractors import LinkExtractor
from urlparse import urlparse
import re


from reports.items import ReportsItem


class WebSpider(Spider):
    
    name = "SustainabilityBot"
    

    def __init__(self, *args, **kwargs):
        super(WebSpider, self).__init__(*args, **kwargs)
        
        self.file_path = "seeds.txt"
        self.whitelist = ['csr', 'environment', 'sustainab', 'responsib', 'footprint']
        self.blacklist = ['document', 'blog', 'product', 'news', 'press', 'archive', 'search', 'login']
        self.extractor = LinkExtractor()

    def start_requests(self):
        with open(self.file_path) as f:
            for line in f:
                [url, company] = line.split(',')
                try:
                    url = url.strip()
                    request = Request(url)
                    request.meta.update(company = company.strip())
                    yield request
                except:
                    continue

    def parse(self, response):
        if not isinstance(response, HtmlResponse):
            return

        domain_origin = urlparse(response.url).netloc
        url = response.url

        if (response.meta.get('keywords', ())):
            yield self.process_item(response)


        for link in self.extractor.extract_links(response):
            
            domain_this = urlparse(link.url).netloc


            # Go to the next loop if it goes outside the current domain
            if (domain_this != domain_origin):
                continue

            link_str = ' '.join([link.text.lower(), link.url.lower()])
            keywords = list(set(re.findall("|".join(self.whitelist), link_str, flags = re.I)))
            flashcards = list(set(re.findall("|".join(self.blacklist), link_str, flags = re.I)))

            if ((not keywords) and (flashcards)):
            	continue
            

            request = Request(url = link.url)
            request.meta.update(link_text = link.text)
            request.meta.update(keywords = keywords)
            request.meta.update(company = response.meta['company'])

            yield request

            

    def process_item(self, response):
        
        item = ReportsItem()

        item['url'] = response.url
        item['link_text'] = response.meta['link_text']
        item['company'] = response.meta['company']
        item['content'] = response.body
        item['keywords'] = response.meta['keywords']

        return item