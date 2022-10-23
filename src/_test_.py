import Gui_resp
 

data = Gui_resp.shop_resp()
print(data)

 

 
filename='test.txt'
with open(filename,'w') as file_obj:
  file_obj.write(data)


# Gui_resp.data_preprocess(data)