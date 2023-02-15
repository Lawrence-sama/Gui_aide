from pymongo import MongoClient
import csv


client = MongoClient("localhost", 27017)
collection = client["GuiAssistant"]["shopsinfosDB"]


# for i in range(collection.find().sort([("index",-1)]).skip(0).limit(1)[0]["index"]):
#     collection.update_one({'index': i}, {"$set": {"lastAppear":collection.find_one({'index': i})["lastAppear"]+1}}) 
with open('db_gui/all_shop_infos_db.csv','r',encoding="utf-8") as csvfile:
    reader = csv.DictReader(csvfile)

    DBdata = [row for row in reader]


    for row in DBdata:
        
        ret = collection.insert_one({"index": int(row["index"]), "sid": int(row["sid"]),"name":row["name"],"plat":row["plat"],"lastAppear":int(row["lastAppear"])})
        print(ret)



# if collection.find_one({"sid": "45883"})["lastAppear"] >= 14:

# print(collection.find().sort([("index",-1)]).skip(0).limit(1)[0]["index"])

# collection.find().forEach(
# function(item){
# 	db.集合名.update(
#         {"_id":item._id}, 
#         {"$set":
#             {"CreatedTime":new Date(item.CreatedTime.getTime() + 1*60*60000)}})
# })

#     lastAppear = collection.find_one({"index": i})["lastAppear"]

#     result = collection.update_one({'index': i}, {"$set": {"lastAppear": lastAppear+1}})
