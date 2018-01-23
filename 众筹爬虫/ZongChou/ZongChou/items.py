# -*- coding: utf-8 -*-

# Define here the models for your scraped items
#
# See documentation in:
# http://doc.scrapy.org/en/latest/topics/items.html

import scrapy
from scrapy import Field


class Project_Info_Item(scrapy.Item):
    project_id =Field()
    html_source =Field()
    project_name =Field()
    start_user =Field()
    support_count =Field()
    getted_amount =Field()
    target_amount =Field()
    project_state =Field()
    project_schedule =Field()
    project_type =Field()
    location =Field()
    project_tags =Field()
    project_description =Field()
    contact_name =Field()
    contact_address =Field()
    contact_tel =Field()
    update_count =Field()
    comment_count =Field()
    project_url = Field()

class Rewards_Type_Item(scrapy.Item):
    project_id = Field()
    rewards_list = Field()
    html_source = Field()
    project_url = Field()

class Update_Item(scrapy.Item):
    project_id = Field()
    json_list = Field()
    project_update = Field()

class Topic_Item(scrapy.Item):
    project_id = Field()
    json_list = Field()
    topic_list = Field()

class Support_Item(scrapy.Item):
    project_id = Field()
    json_list = Field()
    support_list = Field()