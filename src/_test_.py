# import Gui_resp
import csv
# import pandas as pd
# data = Gui_resp.shop_resp()
import datetime

 

 
# filename='test.txt'
# with open(filename,'w') as file_obj:
#   file_obj.write(data)
#   print("success")

# Gui_resp.data_preprocess(data)



#???????
# with open('db_gui/all_shop_infos_db.csv','r',encoding="utf-8") as csvfile:

#   reader = csv.DictReader(csvfile)

#   DBdata = [row for row in reader]

#   dbsid = {}
#   for row in DBdata:
#     dbsid.update({row["sid"]:row["index"]})
#   print(list(dbsid.keys()))


if datetime.datetime.now().hour == 15:
    print(15)
