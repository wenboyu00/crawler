# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

from scrapy import Item, Field


class NewItem(Item):
    # 如果用动态插入，最好键名与列表名一致
    title = Field()
    contents = Field()
    editor = Field()
    source = Field()
    time = Field()
    comment = Field()


class AcfunItem(Item):
    title = Field()
    contents = Field()
    UP = Field()
    time = Field()
    comments = Field()
    onlook = Field()
