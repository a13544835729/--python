import requests
import time
import json
import pandas as pd
import pymysql


load_list=[]
for page_num in range(1,14):
    url='https://www.lagou.com/jobs/positionAjax.json?px=default&city=%E5%B9%BF%E5%B7%9E&needAddtionalResult=false'
    my_data={
        'first':'true',
        'pn':page_num,
        'kd':'数据分析'
    }
    my_header={
        'Accept': 'application / json, text / javascript, * / *; q = 0.01',
        'Referer':'https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/p-city_213?px=default',
        'User-Agent':'Mozilla/5.0 (X11; Linux x86_64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/73.0.3683.75 Safari/537.36'
    }
    urls='https://www.lagou.com/jobs/list_%E6%95%B0%E6%8D%AE%E5%88%86%E6%9E%90/p-city_213?px=default#filterBox'
    s=requests.Session()
    s.get(urls,headers=my_header,timeout=3)
    cookie=s.cookies

    response=s.post(url,data=my_data,headers=my_header,cookies=cookie,timeout=5).text
    # print(response)
    dict_all=json.loads(response)
    # print(dict_all)
    dict_detail=dict_all['content']['positionResult']['result']
    #循环插入字段
    for item in dict_detail:
        msg_all = []
        msg_all.append(item['positionName'])
        msg_all.append(item['companyFullName'])
        msg_all.append(item['companySize'])
        msg_all.append(item['industryField'])
        msg_all.append(item['financeStage'])
        msg_all.append(item['skillLables'])
        msg_all.append(item['district'])
        msg_all.append(item['salary'])
        msg_all.append(item['workYear'])
        msg_all.append(item['education'])
        msg_all.append(item['positionAdvantage'])
        #插入总表
        load_list.append(msg_all)

#转成csv
# print(load_list)
df=pd.DataFrame(load_list,columns=['职位名称','公司名称','公司规模','行业','融资','技能要求','地区','薪资','工作经验','学历','福利'])
df.to_csv('lagou_job.csv',index=False)


# create table lagou values('职位名称' varchar(20),'公司名称' varchar(128),'公司规模' ,'行业','融资','技能要求','地区','薪资','工作经验','学历','福利')




