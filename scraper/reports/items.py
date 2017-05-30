# -*- coding: utf-8 -*-

from scrapy.item import Item, Field


class ReportsItem(Item):
	
	url = Field()
	link_text = Field()
	company = Field()
	content = Field()
	keywords = Field()
