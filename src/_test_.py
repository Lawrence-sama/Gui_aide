import Gui_resp
 

data = Gui_resp.shop_resp()


 

 
filename='test.txt'
with open(filename,'w') as file_obj:
  file_obj.write(data)
  print("success")

# Gui_resp.data_preprocess(data)