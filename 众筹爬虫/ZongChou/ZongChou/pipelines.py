# -*- coding: utf-8 -*-

# Define your item pipelines here
#
# Don't forget to add your pipeline to the ITEM_PIPELINES setting
# See: http://doc.scrapy.org/en/latest/topics/item-pipeline.html
import pymongo
from pymongo import MongoClient

from ZongChou import settings
from ZongChou.items import Project_Info_Item, Rewards_Type_Item, Update_Item, Topic_Item, Support_Item
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

class ZongchouPipeline(object):
    def process_item(self, item, spider):
        return item

class MongoPipiline(object):
    def __init__(self,mongo_uri,mongo_db):
        self.mongo_uri = mongo_uri
        self.mongo_db = mongo_db

    @classmethod
    def from_crawler(cls,cralwer):
        return cls(
            mongo_uri = cralwer.settings.get('MOGO_URI'),
            mongo_db = cralwer.settings.get('MONGO_DB')
        )


    def open_spider(self, spider):
        self.client = pymongo.MongoClient(self.mongo_uri)
        self.db = self.client[self.mongo_db]

    def close_spider(self, spider):
        self.client.close()

    def process_item(self, item, spider):
        if isinstance(item,Project_Info_Item):
            self.db['Project_Info'].update({'project_id':item['project_id']},dict(item),True)
        elif isinstance(item,Rewards_Type_Item):
            self.db['Rewards_Type'].update({'project_id': item['project_id']}, dict(item), True)
        elif isinstance(item,Update_Item):
            self.db['Update_Info'].update({'project_id': item['project_id']}, dict(item), True)
        elif isinstance(item,Topic_Item):
            self.db['Topic_Info'].update({'project_id': item['project_id']}, dict(item), True)
        elif isinstance(item,Support_Item):
            self.db['Support_Info'].update({'project_id': item['project_id']}, dict(item), True)



        return item