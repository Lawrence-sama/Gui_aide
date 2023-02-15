

import requests, yaml, json
from attrdict import AttrDict
from fake_useragent import UserAgent
import json
import wxbot



import time
import datetime
from pymongo import MongoClient
current_day_info = []
likes = [43490,42686,42492,43964]


client = MongoClient("localhost", 27017)
collection = client["GuiAssistant"]["shopsinfosDB"]

def shop_resp() -> dict:
    # 读取参数配置文件
    yaml_file = "config/gui.yaml"
    with open(yaml_file, 'rt', encoding="utf-8") as f:
        args = AttrDict(yaml.safe_load(f))

    ua = UserAgent()

    HEADERS = {
        "Content-Type": "application/json",
        "User-Agent": ua.random,
    }

    # 发起 post 请求
    resp = requests.post(args.resp.url, 
                        data=json.dumps(args.resp.data), 
                        headers=HEADERS)
    data = json.dumps(resp.json()["data"]["records"], indent=4, 
                        separators=(',', ': '), 
                        ensure_ascii=False)
    resp.close()
    return data


# 『数据预处理』 筛选满足条件的活动，整理成表格，保存为csv 存入数据库

def data_preprocess(data: list):
    # 1.筛选出距离小于3km的店铺（distance<3000）,
    # 2.筛选出需要的信息，包括：sid（店铺id），shopname（店铺名称），"platformType": 平台类型
    # "todayStartTime": 活动开始时间 "todayEndTime": 活动结束时间，"full": 最低实付，"sub": 返现额
    
    shop_infos = []
    for shop in data:
        # plat = shop["activityList"][0]["platformType"] 弃用代码
        shop_info = {
            "sid": shop["sid"],
            "name": shop["shopname"],
            "platformType":shop["platformType"],
            "todayStartTime":shop["todayStartTime"],
            "todayEndTime":shop["todayEndTime"],
            "full":shop["full"],
            "sub":shop["sub"],
            "surplus":shop["surplus"],
            "distance":shop["distance"]
        }

        if shop_info["distance"] <=3000:
            shop_infos.append(shop_info)
    return shop_infos


def wxpusher(info,msg):
    
    wxbot.sendmsg(title=info["shopname"], msg=msg)
    print("已发送店铺：" +info["shopname"])

    
def currentday_check(shop_infos):
    global current_day_info
    if shop_infos in current_day_info or shop_infos == current_day_info:
        return False
    else:
        current_new = []
        for i in shop_infos:
            if i in  current_day_info:
                continue
            else:
                current_day_info.append(i)
                current_new.append(i)
        print("本日有店铺上新",datetime.datetime.now(),current_new)
        database_check(current_new)
        
    
def database_check(current_new):
    #1.读入DB中的sid，lastAppear
    #2.current_new的sid是否在DB中
    #3.如果不在，存储信息+alarm
    #4.如果在，查看时间是否超过14，如果超过，alarm。将所有时间归零
    for row in current_new:
        if collection.find_one({"sid": row["sid"]}):
            # print(collection.find_one({"sid": row["sid"]}))
            if collection.find_one({"sid": row["sid"]}):
                # collection.update_one({"sid": row["sid"]}, {"$set": {"lastAppear": 0}})
                if collection.find_one({"sid": row["sid"]})["lastAppear"] >= 14:
                    collection.update_one({"sid": row["sid"]}, {"$set": {"lastAppear": 0}})
                    wxpusher(info=row,msg="店铺时隔多天（14+）重新出现")
                    print("已发送店铺：" +row["shopname"])
                    print("reappeared_alarm")
        else:
            collection.insert_one({"index": collection.find().sort([("index",-1)]).skip(0).limit(1)[0]["index"]+1, "sid": row["sid"],"name":row["shopname"],"plat":row["platformType"],"lastAppear":0})
            
            wxpusher(info=row,msg="出现了数据库中没有的新店铺")
            
            print("new shop alarm")
            print("已发送店铺：" +row["shopname"])


        likelist_check(current_new)



def likelist_check(current_new):
    for info in current_new:
        
        if info["sid"] in likes:
            likes.remove(info["sid"])
            # wxpusher()
            wxpusher(info=info,msg="在likelist里的店铺")

            # wxbot.sendmsg(title=info["name"], msg="你感兴趣的店铺"

            print("like_check_已发送店铺：" +info["shopname"])




def daily_upgrade():
    global current_day_info
    # 清空前需要存一下信息
    print(current_day_info)
    current_day_info = []

    for i in range(collection.find().sort([("index",-1)]).skip(0).limit(1)[0]["index"]):
        collection.update_one({'index': i}, {"$set": {"lastAppear":collection.find_one({'index': i})["lastAppear"]+1}}) 
    time.sleep(36000)
    




# 『通知』 对比当前数据于上一次请求数据的差别，发送对应通知
def notice_match():
    # 「新活动」通知
    # 「售罄」通知
    pass
if __name__ == "__main__":
    while 1:
        data = shop_resp()
        upgrate_time = time.localtime().tm_hour
        time.sleep(300)
        if upgrate_time == 20:
            print("daily_upgrade",datetime.datetime.now())
            daily_upgrade()
