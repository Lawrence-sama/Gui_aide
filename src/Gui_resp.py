#V0.1 感兴趣的店自动手机推送的功能


import requests, yaml, json
from attrdict import AttrDict
from fake_useragent import UserAgent
import json
import wxbot
import time
import datetime


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
# 将surplus「剩余量」存入csv 数据库
def data_preprocess(data: list):
    # 1.筛选出距离小于3km的店铺（distance<3000）,筛选出需要的信息，包括：sid，shopname，shopaddress，actuvityList
    # 2.在筛选出的信息里找目标店铺，如果有则发送，并把todayAlert设为true
    
    shop_infos = []
    for shop in data:
        plat = shop["activityList"][0]["platformType"]
        shop_info = {
            "index": 0,
            "sid": shop["sid"],
            "name": shop["shopname"],
            "plat": plat,
            "distance":shop["distance"]
            # "todayAlert":False
        }
        if shop_info["distance"] <=3000:
            shop_infos.append(shop_info)
    return shop_infos




def wxpusher(shop_infos):
    global todayAlert
    curr_time = datetime.datetime.now()
    if curr_time.hour not in [8,9,10,11,12,13,14,15,16,17,18,19]:
        return 
    for info in shop_infos:
        #  and curr_time.hour in [8,9,10,11,12,13,14,15,16,17,18,19]
        if info["sid"] in likes and not info["sid"] in todayAlert:
            # print("alarm")
            wxbot.sendmsg(title=info["name"], msg="你感兴趣的店铺")
            print("已发送店铺：" +info["name"])
            todayAlert.append(info["sid"])
    if  curr_time.hour == 0:
        todayAlert = []
    


# 『通知』 对比当前数据于上一次请求数据的差别，发送对应通知
def notice_match():
    # 「新活动」通知
    # 「售罄」通知
    pass
if __name__ == "__main__":
    # data = shop_resp()
    likes = [43490,42686,42492]
    todayAlert = []
    data = json.load(open("test.txt"))

    while True:
        shop_infos = data_preprocess(data)
        wxpusher(shop_infos)
        time.sleep(300)    


print("the end")

