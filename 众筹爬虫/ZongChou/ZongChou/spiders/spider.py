# -*- coding: utf-8 -*-
import json
import re

import requests
import scrapy
from pymongo import MongoClient
from scrapy import Request
from pyquery import PyQuery as pq

from ZongChou import settings
from ZongChou.items import Project_Info_Item, Rewards_Type_Item, Update_Item, Topic_Item, Support_Item
from ZongChou.settings import DEFAULT_REQUEST_HEADERS, START_PAGE, MAX_PAGE, PROJECT_INFO_AND_Rewards_Type_SWITCH, \
    Update_Info_SWITCH, Topic_Info_SWITCH, Support_Info_SWITCH
client = MongoClient(settings.MONGO_URI)
db = client[settings.MONGO_DB]

class SpiderSpider(scrapy.Spider):
    name = 'spider'
    allowed_domains = ['www.zhongchou.com']
    start_urls = ['http://www.zhongchou.com/']

    index_base_url = 'http://www.zhongchou.com/browse/p{page}'
    detail_base_url = 'http://www.zhongchou.com/deal-show/id-{id}'
    update_base_url = 'http://www.zhongchou.com/deal-march_list?id={id}&offset={offset}&page_size=10'
    topic_base_url = 'http://www.zhongchou.com/deal-topic_list?id={id}&offset={offset}&page_size=10'
    support_base_url = 'http://www.zhongchou.com/deal-support_list?id={id}&page_size=10&offset={offset}'

    def start_requests(self):
        # yield Request('http://www.zhongchou.com/deal-show/id-734350', self.parse_detail) #详细页测试 有抽奖的情况测试
        # yield Request(self.detail_base_url.format(id=354511), self.parse_detail) #详细页测试 有满额的情况测试
        # yield Request(self.update_base_url.format(id=393658, offset=0), self.parse_update) #更新页测试 有翻页
        # yield Request(self.update_base_url.format(id=382564, offset=0), self.parse_update) #更新页测试 无翻页
        # yield Request(self.update_base_url.format(id=736713, offset=0), self.parse_update) #更新页测试 无更新
        # yield Request(self.topic_base_url.format(id=382564,offset=0),self.parse_topic) #项目评论页测试 有翻页
        # yield Request(self.topic_base_url.format(id=734350,offset=0),self.parse_topic) #项目评论页测试 无翻页
        # yield Request(self.topic_base_url.format(id=737604,offset=0),self.parse_topic) #项目评论页测试 无评论
        # yield Request(self.support_base_url.format(id=382564,offset=0),self.parse_support) #项目支持记录页测试 有翻页
        for i in range(START_PAGE, MAX_PAGE):  # 对每一页发起请求 共有282页
            yield Request(self.index_base_url.format(page=i), self.parse_index)

    def parse_index(self, response):
        item_list = response.css('.ssCardItem')  # 获取项目列表
        id_list = []
        for item in item_list:
            url = item.css('.siteCardItemImgA.souSuo ::attr(href)').extract_first()  # 取出没给项目的链接
            id = re.search('id-(\d+)', url).group(1)  # 取出链接中的id
            id_list.append(id)
        for id in id_list:
            if PROJECT_INFO_AND_Rewards_Type_SWITCH:
                try:
                    yield Request(self.detail_base_url.format(id=id),self.parse_detail)  #项目基本信息表 项目回报设置表
                except ConnectionError:
                    yield Request(self.detail_base_url.format(id=id), self.parse_detail)
            if Update_Info_SWITCH:
                try:
                    yield Request(self.update_base_url.format(id=id,offset=0),self.parse_update) #项目更新信息表
                except ConnectionError:
                    yield Request(self.update_base_url.format(id=id, offset=0), self.parse_update)
            if Topic_Info_SWITCH:
                try:
                    yield Request(self.topic_base_url.format(id=id,offset=0),self.parse_topic) #项目评论表
                except ConnectionError:
                    yield Request(self.topic_base_url.format(id=id, offset=0), self.parse_topic)
            if Support_Info_SWITCH:
                try:
                    yield Request(self.support_base_url.format(id=id,offset=0),self.parse_support) #项目支持纪录表
                except ConnectionError:
                    yield Request(self.support_base_url.format(id=id, offset=0), self.parse_support)


    def parse_detail(self,response):
        doc = pq(response.text)
        project_url = response.url
        project_id = re.search('id-(\d+)',response.url).group(1)
        html_source = response.text
        project_name = doc('#move').text()
        start_user = doc('.faqipeeson .txt2 font').text()
        support_count = int(doc(' div.xqDetailRight > div.xqDetailDataBox > div:nth-child(1) > p > span.ftP').text().replace(',',''))
        getted_amount = float(doc(' div.xqDetailRight > div.xqDetailDataBox > div:nth-child(2) > p > span.ftP').text().replace(',','')[1:])
        target_amount = float(doc('div.xqDetailRight > div.xqRatioOuterBox > div.xqRatioText.clearfix > span.rightSpan > b').text().replace(',','')[1:])
        project_state =doc('div.xqDetailRight > div.xqRatioOuterBox > div.xqRatioText.clearfix > span.leftSpan').text().strip()
        project_schedule = doc('div.xqDetailBox > div.xqDetailRight > div.xqRatioOuterBox > p').text()
        project_type = doc('div.xqDetailRight > div.xqDetailBtnBox > div.xqDetailShareBox.clearfix > div > span.gy.siteIlB_item > a').text()
        location = doc('div.xqDetailRight > div.xqDetailBtnBox > div.xqDetailShareBox.clearfix > div > span.addr.siteIlB_item').text()
        project_tags = doc('div.xqDetailRight > div.xqDetailBtnBox > div.xqDetailShareBox.clearfix > div > span.label.siteIlB_item').text()
        project_description = doc('#xmxqBox').text()
        contact_name = doc('#right .contact-list .item-contact.item1 div.obj-body span:nth-child(2)').text()
        contact_address = doc('#right .contact-list .item-contact.item2 div.obj-body span:nth-child(2)').text()
        contact_tel = doc('#right .contact-list .item-contact.item3 div.obj-body span:nth-child(2)').text()
        update_count = int(doc('#xqTabNav_ul li:nth-child(2) b').text().replace(',',''))
        comment_count = int(doc('#xqTabNav_ul li:nth-child(3) b').text().replace(',',''))
        project_info_item = Project_Info_Item()
        for field in project_info_item.fields:
            try:
                project_info_item[field] = eval(field)
            except NameError:
                print('this field is not exit ',field)
        yield project_info_item



        #上面是构造project_info表的

        #以下是构造project_rewards表
        rewards = doc('#right > div > div:nth-child(1) > div:nth-child(1) >div').children('div')
        rewards_list = []
        for reward in rewards:
            if not pq(reward).has_class('my-lottery'):
                # 第一个reward是无私奉献，格式不同，要特殊处理
                if rewards.index(reward)==0:
                    reward = pq(reward)

                    # price = reward('#wszcWrap').text()
                    price = 0.0 #这里的捐献数额是可以自定的，可选1、5、10 ，或者自己设定，默认设为0.0 ，支持表中会有详细数额
                    donate_count = int(reward('h3 b').text().split(' ')[0])
                    title = reward('h3').text().split(' ')[0]
                    description = reward('.zcje_textP').text()
                    reward_get_time = None
                else:
                    reward = pq(reward)
                    price = float(reward('h3 b').text().replace(',','')[1:])
                    try:
                        donate_count = int(reward('h3').text().replace(',','').split(' ')[1])
                    except:
                        donate_count = int(re.search('限(\d+)人',reward('h3').text()).group(1))
                        print(donate_count)
                    title = reward('.zcje_title').text()
                    description = reward('.zcje_textP').text()
                    reward_get_time =reward('.zcjeFooter p b').text()
                # print('price:{0},count:{1},title:{2},des:{3}time:{4}'.format(price,donate_count,title,description,reward_get_time))
                reward_dict = {
                    'price':price,
                    'donate_count':donate_count,
                    'title':title,
                    'description':description,
                    'reward_get_time':reward_get_time,
                }
                rewards_list.append(reward_dict)
        donate_type_item = Rewards_Type_Item()
        for field in donate_type_item.fields:
            try:
                donate_type_item[field] = eval(field)
            except NameError:
                print('this field is not exit ', field)
        yield donate_type_item



    def parse_update(self,response):
        project_id = re.search('\?id=(\d+)&',response.url).group(1)
        json_list = []
        project_update = []
        r = json.loads(response.text)
        max_page = int(int(r['data']['count'])/10) #根据更新条数计算offset最大值，offset是从0开始的
        if int(r['data']['count']) % 10 == 0: max_page -= 1 #数量刚好为10的时候不翻页
        offsets = [x*10 for x in range(0,max_page+1)]
        for offset in offsets:
            try:
                result = requests.get(self.update_base_url.format(id=project_id,offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            except ConnectionError:
                result = requests.get(self.update_base_url.format(id=project_id, offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            result = json.loads(result.text)
            json_list.append(str(result))
            for item in result['data']['march_list']:
                create_time = item['create_time']
                user_id = item['user_id']
                user_name = item['user_name']
                log_info = item['log_info']
                is_self = item['is_self']
                update_dict = {
                    'create_time':create_time,
                    'user_id':user_id,
                    'user_name':user_name,
                    'log_info':log_info,
                    'is_self':is_self,
                }
                project_update.append(update_dict)
        update_item = Update_Item()
        for field in update_item.fields:
            try:
                update_item[field] = eval(field)
            except NameError:
                print('this field is not exit ', field)
        yield update_item


    def parse_topic(self,response):
        project_id = re.search('\?id=(\d+)&', response.url).group(1)
        r = json.loads(response.text)
        json_list = []
        topic_list = []
        max_page = int(int(r['data']['count'])/10)
        if int(r['data']['count'])%10==0:max_page-=1 #数量刚好为10的时候不翻页
        offsets = [x*10 for x in range(0,max_page+1)]
        for offset in offsets:
            try:
                result = requests.get(self.topic_base_url.format(id=project_id,offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            except ConnectionError:
                result = requests.get(self.topic_base_url.format(id=project_id, offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            result = json.loads(result.text)
            json_list.append(str(result))
            for item in result['data']['topic_list']:
                user_id = item['user_id']
                user_name = item['user_name']
                content = item['log_info']
                create_time = item['create_time']
                comment_list = []
                for comment in item['comment_list']:            #抓取评论
                    observer_id = comment['owner']['userID']
                    observer_name = comment['owner']['name']
                    comment_content = comment['content']
                    comment_time = comment['create_time']
                    comment_dict = {
                        'observer_id':observer_id,
                        'observer_name':observer_name,
                        'comment_content':comment_content,
                        'comment_time':comment_time,
                    }
                    comment_list.append(comment_dict)
                topic_dict = {
                    'user_id':user_id,
                    'user_name':user_name,
                    'content':content,
                    'create_time':create_time,
                    'comment_list':comment_list
                }
                topic_list.append(topic_dict)
        topic_item = Topic_Item()
        for field in topic_item.fields:
            try:
                topic_item[field] = eval(field)
            except NameError:
                print('this field is not exit ', field)
        yield topic_item




    def parse_support(self,response):
        project_id = re.search('\?id=(\d+)&', response.url).group(1)
        r = json.loads(response.text)
        json_list = []
        topic_list = []
        max_page = int(int(r['data']['count']) / 10)
        json_list = []
        support_list = []
        if int(r['data']['count']) % 10 == 0: max_page -= 1  # 数量刚好为10的时候不翻页
        offsets = [x * 10 for x in range(0, max_page + 1)]
        for offset in offsets:
            try:
                result = requests.get(self.support_base_url.format(id=project_id, offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            except ConnectionError:
                result = requests.get(self.support_base_url.format(id=project_id, offset=offset),headers=DEFAULT_REQUEST_HEADERS)
            result = json.loads(result.text)
            json_list.append(str(result))
            for item in result['data']['support_list']:
                user_id = item['user_id']
                user_name = item['user_name']
                deal_price = float(item['deal_price'].replace(',',''))
                return_type = item['return_type']
                deal_num = int(item['deal_num'])
                pay_time = item['pay_time']
                try:
                    total_price = deal_price*deal_num
                except:
                    total_price = 0
                support_dict = {
                    'user_id':user_id,
                    'user_name':user_name,
                    'deal_price':deal_price,
                    'return_type':return_type,
                    'deal_num':deal_num,
                    'pay_time':pay_time,
                    'total_price':total_price

                }
                support_list.append(support_dict)
        support_item = Support_Item()
        for field in support_item.fields:
            try:
                support_item[field]=eval(field)
            except NameError:
                print('this field is not exit ', field)
        yield support_item

