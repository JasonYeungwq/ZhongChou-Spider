# ZhongChou-Spider
本项目使用scrapy框架对众筹网的项目信息进行爬取，使用mongodb存储，分别输出四个表：项目基本信息表、项目回报信息表、评论信息表、项目更新表、项目支持表<br> 
*详情联系微信：991370838 Jason*
## 爬虫基本流程：（基于scrapy框架）
![](http://img.blog.csdn.net/20180123091722872)
##依赖包
Scrapy、json、re、pymongo、pyquery、requests
## Python版本：3.6.3
## 参数设置
Setting文件参数路径：ZongChou\ZongChou\settings.py
1. MONGO_URI    链接mongodb的参数
2. MONGO_DB 	数据库名称
3. START_PAGE   开始爬取的索引页
4. MAX_PAGE      最大索引页（需手动查看网页）
5. PROJECT_INFO_AND_Rewards_Type_SWITCH  描述中两个表开关
6. Update_Info_SWITCH                        Update_Info表爬取开关
7. Topic_Info_SWITCH                         Topic_Info表爬取开关
8. Support_Info_SWITCH                       Support_Info表爬取开关
## 运行流程
1. 配置好settings参数
2. 启动mongodb
3. Cmd打开ZongChou文件夹
4. 输入Scrapy crawl spider命令
## 5.	数据库字段说明
1.	Project_Info：
_id:                  系统分配的id<br> 
comment_count:        评论数<br> 
contact_address:      联系地址<br> 
contact_name:  	      联系人<br> 
contact_tel:   		  联系电话<br> 
getted_amount:	      已筹款<br> 
html_source:		  网页源码<br> 
location:			  地区<br> 
project_description:  项目描述（空的情况可能是只有图片）<br> 
project_id:	          项目id<br> 
project_name:         项目名称<br> 
project_schedule:	  项目进度<br> 
project_state:        项目状态<br> 
project_tags:         标签  <br> 
project_type:         项目类型<br> 
project_url:          项目链接<br> 
start_user:           发起人<br> 
support_count:        支持人数<br> 
target_amount:        目标筹资<br> 
update_count:         更新次数<br> 

2.	Rewards_Type：
_id:                  系统分配的id<br> 
html_source:		  网页源码<br> 
project_id:	          项目id<br> 
project_url:          项目链接<br> 
reward_list{<br> 
			price:                价格<br> 
         donate_count:         参与人数<br> 
         title:                 标题<br> 
         description:           描述<br> 
         reward_get_time:      回报时间<br> 
}
3.	Support_Info:
_id:                  系统分配的id<br> 
Json_list:            json源数据<br> 
project_id:	          项目id<br> 
support_list:{<br> 
           user_id:              支持者id<br> 
           user_name:            支持者name<br> 
           deal_price:           单价<br> 
           return_type:          回报类型：3为无私支持，0为回报支持<br> 
           deal_num:             数量<br> 
           pay_time:             支付时间<br> 
           total_price:          支付总额（计算所得，并非采集数据）<br> 
}
4.	Topic_Info:
_id:                  系统分配的id<br> 
Json_list:            json源数据<br> 
project_id:	          项目id<br> 
topic_list:{   <br> 
            user_id:           评论者id<br> 
            user_name:         评论者name<br> 
            content:           评论内容<br> 
            create_time:       评论时间<br> 
            comment_list{<br> 
observer_id:          回复者id<br> 
observer_name:        回复者name<br> 
comment_content:      回复内容<br> 
comment_time:         回复时间<br> 
}<br> 
<br> 
        }<br> 
<br> 
5.	Update_Info:
_id:                  系统分配的id<br> 
Json_list:            json源数据<br> 
project_id:	          项目id<br> 
project_update:{<br> 
              create_time:       更新时间<br> 
              user_id:           更新者id（若是系统自动更新则为0）<br> 
              user_name:         更新者name（若是系统自动更新则为空）<br> 
              log_info:          更新内容<br> 
              is_self:           是否为系统更新（1为系统更新，2为用户更新）<br> 
}<br> 
