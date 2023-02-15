吃吃龟推送助手



## 项目功能简介

使用 `requests` 对[吃吃龟商铺接口](https://shop.laiyangni.com/api/lyn/wechat/home/shopInfo/v2)发送请求，获取店铺信息，并以此为基础实现特别关注店铺提醒，自动抢单等功能

## 目前已实现的功能：

V0.1（2022.10.23）:

获取店铺信息，如果有在likes列表里的（即特别关注的）店铺，会通过微信推送消息进行提醒

避免打扰，只会在7:00 ~ 19:00 发送提醒。每家店铺每天只推送一次，每天1:00刷新

**v1.0(2023.2.15)**

1.修改了代码结构，采用mongoDB作为数据库

**在之前的基础上增加了：**
1. 从未在数据库中出现的新店出现后推送 
2. 曾经出现的店时隔14天以上时再次出现时进行推送
   
代码流程图：

![frame](https://github.com/Lawrence-sama/Gui_aide/blob/master/picture/Gui%20Assistant.jpg)


## 饼：

### 筛选播报

设定免打扰约束条件，筛选播报

1. 距离、营业时间【常规约束】
2. 店名，不参与外卖节活动的、价格不实惠的


### 自动抢购

【待开发】定时、定账号、定店铺活动发起抢购
