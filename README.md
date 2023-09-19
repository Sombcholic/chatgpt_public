# 系統需求
1. python: 3.7  
2. pipenv  
  
使用pipenv install 即可安裝全部的library  
  
# chatgpt-API KEY 文件  
請在此資料夾內新增chatgpt-API key文件  
因為在生成資料集的程式有使用到兩個api節點，因此要建立兩個API KEY，範例如下  
chatgpt_api: sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX
chatgpt_api2: sk-XXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXXX

# createDataset folder
希望透過chatgpt指數型成長dataset數量，詳細說明請詳閱該資料夾README.md  
  
# embedding
引用chatgpt的word embedding來測試字詞間的相似度

# Far_Enotr
嘗試讓chatgpt扮演遠傳客服人員，並且在system角色中加入已知的推銷訊息  
  
# image_generation
透過官方API文件實作image相關的測試  
1. mask_picture.py: 將去背的地方使用promt加入新的元素  
2. generate_picture.py: 透過prompt生成文件  
3. variation.py: 可將圖片些微的改變進而變成新的圖片，有進行過俄羅斯套娃實驗，以原圖片生成新圖，並用這張新圖繼續生成，測試結果為第三張圖片後將會開始失真  

# speech2text  
透過官方API文件實作speech2text相關的測試  
  
# TestNote  
個人進行prompt後整理的Note  

# remember_sentence.py  
測試使用chatgpt整理過往資訊，最大化縮減使用chatgpt的花費以及增加記憶功能  