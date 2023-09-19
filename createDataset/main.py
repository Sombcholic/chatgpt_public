import openai
import time
import yaml
import traceback
from opencc import OpenCC
import numpy as np
import os
import string
import pandas as pd

class createDataset():
    def __init__(self):
        self.user_input = ""
        self.gpt_segment = []
        self.keyword_list = []
        self.token_sum = 0
        self.keywordDict = {}
        self.keyword_sentence = {}
        self.similar_sentence = {}
        self.pre_keyword_sentence = {}
        self.pre_similar_sentence = {}
        self.process = ''

        self.datapath = ''
        self.pre_datapath = ''
        self.class_data = []


    def segment(self):
        gpt_input = '請幫我斷詞「' + self.user_input + '」'
        result = self.gpt(gpt_input, 4)

        self.gpt_segment = result.split('/')
        
        print('目前的segment處理結果為-> ', result)
    
    def generate_word(self, keyword_list: list, generateNum: int):
        self.keyword_list = keyword_list
        
        for word in keyword_list:
            if (word != ""):
                gpt_input = '請給我' + str(generateNum) + '個「' + word + '」不重複且相同意思的字詞，用序列的方式提供'
                try:
                    with open('./data/word/keywordDict.yml', 'r', encoding="utf-8") as f:
                        data = yaml.safe_load(f)
                        if (data is not None):
                            self.keywordDict = data
                except Exception as e:
                    print(e)
                    ...

                # print(self.keywordDict)     

                if (self.keywordDict.get(word) is None):
                    result = self.gpt(gpt_input, 5)
                    split_word = result.split('\n')

                    # 利用opencc 簡轉中
                    cc = OpenCC('s2twp')

                    i = 1
                    for w in split_word:
                        # 簡轉中
                        new_w = cc.convert(w)
                        # 去掉序列資料
                        new_w = new_w.replace(str(i) + '. ', '')
                        # 去掉標點符號
                        new_w = new_w.translate(str.maketrans('', '', string.punctuation))
                        # 去掉空格
                        new_w = new_w.replace(' ', '')

                        split_word[i-1] = new_w
                        i += 1

                    self.keywordDict[word] = split_word 

                    if (self.keywordDict != {}):
                        with open('./data/word/keywordDict.yml', 'w', encoding='utf-8') as f:
                            yaml.dump(self.keywordDict, f, allow_unicode=True)


    # 採用將keyword陣列存成replace_index [5, 9] 第一個關鍵字有6個相似字詞，第二個關鍵字有10個關鍵字詞
    # temp_index預設為[0, 0]，用來定位目前的陣列Index
    def create_keyword_sentence(self):
        merge_sentence = ''

        replace_index = []
        temp_index = []
        string_list = []

        for w in self.keyword_list:
            replace_index.append(len(self.keywordDict[w]) - 1)
            string_list.append(self.keywordDict.get(w))
            temp_index.append(0)

        count = 0
        while temp_index != replace_index:
            
            i = 0
            sentence = self.user_input
            for t in temp_index:
                sentence = sentence.replace(self.keyword_list[i], string_list[i][t])
                i += 1

            if (self.keyword_sentence.get(self.user_input) is None):
                self.keyword_sentence[self.user_input] = {
                    'keyword_list': self.keyword_list,
                    'sentence': [sentence]
                }
            else:
                if (sentence not in self.keyword_sentence[self.user_input].get('sentence')):
                    self.keyword_sentence[self.user_input]['sentence'].append(sentence)
            
            temp_index = self.count_index(temp_index, replace_index)
            
            if (count == 20):
                break

            count += 1

        with open('./data/keyword_sentence/' + self.datapath + '.yml', 'w', encoding='utf-8') as f:
            yaml.dump(self.keyword_sentence, f, allow_unicode=True)

    # 進位機制
    def count_index(self, temp_index, replace_index):
        finished = False

        i = len(temp_index) - 1

        while finished is False:
            if (temp_index[i] < replace_index[i]):
                temp_index[i] += 1
                finished = True

            else:
                for x in range(i, len(temp_index)):
                    temp_index[x] = 0
                
                if (i > 0):
                    i -= 1


        return temp_index


    def create_similar_sentence(self, number):
        target_sentence = self.keyword_sentence.get(self.user_input)
        
        for s in target_sentence['sentence']:
            
            find_data = False
            find_pre_data = False

            try:
                if (self.similar_sentence.get(s) is not None and self.similar_sentence[s].get('keyword_list') == self.keyword_list):
                    find_data = True
            except:
                ...

            try:
                if (self.pre_similar_sentence.get(s) is not None and self.pre_similar_sentence[s]['keyword_list'] == self.keyword_list):
                    find_pre_data = True
            except:
                ...

            if (find_data is False):
                if (find_pre_data is True):
                    self.similar_sentence[s] = self.pre_similar_sentence.get(s)

                    with open('./data/similar_sentence/' + self.datapath + '.yml', 'w', encoding='utf-8') as f:
                        yaml.dump(self.similar_sentence, f, allow_unicode=True)
                else:
                    self.similar_sentence[s] = {
                        'keyword_list': self.keyword_list,
                        'sentence': []
                    }

                    print('Create similar sentence')
                    print(s)

                    gpt_input = '請給我' + str(number) + '個「' + s + '」不重複且相同意思的中文句子，用序列的方式提供'
                    result = self.gpt(gpt_input, 5)

                    split_sentence = result.split('\n')

                    # 利用opencc 簡轉中
                    cc = OpenCC('s2twp')

                    i = 0
                    for w in split_sentence:
                        cc.convert(w)
                        for x in range(1, 20):
                            w = w.replace(str(x) + '. ', '').replace(str(x) + '.', '')
                        split_sentence[i-1] = w
                        i += 1

                    for sentence in split_sentence:
                        if (sentence not in self.similar_sentence[s].get('sentence') and sentence != ''):
                            self.similar_sentence[s]['sentence'].append(sentence)

                    with open('./data/similar_sentence/' + self.datapath + '.yml', 'w', encoding='utf-8') as f:
                        yaml.dump(self.similar_sentence, f, allow_unicode=True)

            self.create_data()
                    
            
    def gpt(self, gpt_input, timesleep = 15):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                # {"role": "user", "content": "逆好，我是台灣人！很高興認識你"} 
                {"role": "user", "content": gpt_input}
            ],
            # max_tokens=8
            )

        self.token_sum += completion.usage.total_tokens

        time.sleep(timesleep)

        return completion.choices[0].message.content
    
    def load_data(self, datapath, pre_datapath = ""):
        self.datapath = datapath


        self.pre_datapath = pre_datapath

        try:
            with open('./data/word/keywordDict.yml', 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if (data is not None):
                    self.keywordDict = data
        except Exception as e:
            print(e)
            ...

        try:
            with open('./data/similar_sentence/' + self.datapath + '.yml', 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if (data is not None):
                    self.similar_sentence = data
        except Exception as e:
            print(e)
            ...

        try:
            with open('./data/similar_sentence/' + self.pre_datapath + '.yml', 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if (data is not None):
                    self.pre_similar_sentence = data
        except Exception as e:
            print(e)
            ...

        try:
            with open('./data/keyword_sentence/' + self.pre_datapath + '.yml', 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if (data is not None):
                    self.pre_keyword_sentence = data
        except Exception as e:
            print(e)
            ...

    def create_data(self):
        label_content = []

        for t in self.class_data:
            try:
                if (self.keyword_sentence.get(t[0]) is not None):
                    keyword_sentence = self.keyword_sentence.get(t[0])

                    for k_s in keyword_sentence['sentence']:
                        if (self.similar_sentence.get(k_s) is not None):
                            similar_sentence = self.similar_sentence[k_s].get('sentence')

                            for s_s in similar_sentence:
                                label_content.append([str(t[1]), s_s])
            except:
                # print(traceback.print_exc())
                ...

        df = pd.DataFrame(label_content, columns=['label', 'content'])
        df.to_csv('./data/dataset/' + datapath + '.csv', encoding='utf8')  
            

if __name__ == "__main__":
    with open('../../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']
        api_key2 = data['chatgpt_api2']
    
    dirs = ['./data/keyword_sentence', './data/similar_sentence']

    for d in dirs:
        try:
            os.makedirs(d)
        except:
            ...

    openai.api_key = api_key

    # 假如0 代表使用一個API，假如process = 1，可以切換另外一個，不過要用terminal多開一個
    process = 1
    # pre_datapath = ''
    datapath = '20230626-Test1-class16-sheet'

    if (process == 1):
        pre_datapath = datapath +  str(process - 1)
    else:
        pre_datapath = datapath +  str(process + 1)
    
    cd = createDataset()
    cd.load_data(datapath + str(process), pre_datapath)


    data = [
        ['我想查詢電信發票是否中獎', ['查詢', '電信', '發票', '是否', '中獎'], 1],
        ['我想查詢電信發票兌獎', ['查詢', '電信', '發票', '兌獎'], 1],
        ['我想查詢是否中獎', ['查詢', '是否', '中獎'], 1],
        ['我想查詢發票中獎通知', ['查詢', '發票', '中獎', '通知'], 1],
        ['我想查詢發票號碼', ['查詢', '發票'], 1],
        ['我想領取中獎發票', ['領取', '中獎', '發票'], 1],
        ['我想查詢中獎發票領獎步驟', ['查詢', '中獎', '發票', '領獎', '步驟'], 1],
        ['我想查詢發票載具歸戶設定', ['查詢', '發票'], 1],
        ['想知道有什麼漫遊方案', ['知道'], 2],
        ['我想詢問國家的電信漫遊方案', ['詢問'], 2],
        ['我想詢問熱門的電信漫遊方案', ['詢問'], 2],
        ['我想詢問香港的電信漫遊方案', ['詢問'], 2],
        ['我想詢問中國的電信漫遊方案', ['詢問'], 2],
        ['我想詢問日本的電信漫遊方案', ['詢問'], 2],
        ['我想詢問澳門的電信漫遊方案', ['詢問'], 2],
        ['我想詢問泰國的電信漫遊方案', ['詢問'], 2],
        ['我想詢問南韓的電信漫遊方案', ['詢問'], 2],
        ['我想詢問新加坡的電信漫遊方案', ['詢問'], 2],
        ['我想詢問菲律賓的電信漫遊方案', ['詢問'], 2],
        ['我想詢問美國漫的電信遊方案', ['詢問'], 2],
        ['我想詢問越南的電信漫遊方案', ['詢問'], 2],
        ['我想詢問更多的電信漫遊資訊', ['詢問'], 2],
        ['我想查詢預付卡漫遊', ['預付卡'], 2],
        ['我想知道合約到期日', ['知道', '合約', '到期日'], 3],
        ['我想查詢合約到期日', ['查詢', '合約', '到期日'], 3],
        ['我想查詢合約資訊及優惠', ['合約資訊', '優惠'], 3],
        ['預付卡到期日', ['預付卡', '到期日'], 3],
        ['我想詢問帳單折抵', ['詢問'], 4],
        ['關於帳單折抵的說明', ['詢問', '說明'], 4],
        ['我想詢問帳單的折抵卷', ['詢問'], 4],
        ['我想詢問帳單折抵卷說明', ['詢問', '說明'], 4],
        ['我想詢問帳單折抵卷', ['詢問', '說明'], 4],
        ['我想知道關於帳單折抵卷懶人包', ['知道', '關於', '詢問', '說明'], 4],
        ['我想詢問帳單折抵卷懶人包', ['詢問', '說明'], 4],
        ['我想查詢本期的帳單', ['查詢', '本期', '帳單'], 5],
        ['我想查詢名下遠傳其他手機門號費用', ['查詢', '其他', '手機', '費用'], 5],
        ['我想要手機門號停機', ['想要', '手機', '停機'], 5],
        ['我想詢問攜出後最後一期帳單', ['詢問', '攜出後', '帳單'], 5],
        ['攜出後最後一期帳單', ['攜出後', '帳單'], 5],
        ['攜出後最後一次帳單', ['攜出後', '帳單'], 5],
        ['我想查詢攜出後最後一次帳單', ['查詢', '攜出後', '帳單'], 5],
        ['關於通話收費明細', ['關於', '通話', '收費'], 6],
        ['我想詢問通話收費明細', ['詢問', '通話收費'], 6],
        ['我想詢問不用出門快速繳費', ['詢問'], 7],
        ['我想使用信用卡繳費', ['使用', '信用卡', '繳費'], 7],
        ['我想使用銀行轉帳', ['使用', '銀行轉帳'], 7],
        ['我想繳款', ['繳款'], 7],
        ['我想查詢其他門號費用', ['查詢', '其他'], 7],
        ['我想查詢其他門號費用及繳款', ['查詢', '其他', '繳款'], 7],
        ['我想查詢預付卡如何儲值', ['查詢', '如何', '儲值'], 7],
        ['我想使用預付卡', ['使用'], 7],
        ['我想申請門號復話', ['申請'], 8],
        ['我想線上繳費立即復話', ['繳費', '立即'], 8],
        ['我想請愛瑪先協助復話', ['協助'], 8],
        ['已繳費仍無法使用', ['繳費', '無法使用'], 8],
        ['我想要小額收費代付', ['收費'], 9],
        ['我想要開啟小額代收', ['開啟'], 9],
        ['我想要關閉小額代收', ['關閉'], 9],
        ['我想查詢小額收費交易紀錄', ['查詢', '收費', '交易', '紀錄'], 9],
        ['我想查詢小額收費交易失敗原因', ['查詢', '收費', '交易', '失敗原因'], 9],
        ['我想查詢小額收費增加額度方法。', ['查詢', '增加', '額度'], 9],
        ['我想查詢小額收費增加額度方法', ['查詢', '增加額度'], 9],
        ['我想要小額付費申請退款', ['退款'], 9],
        ['我想查詢小額收費繳費後無法使用代收', ['查詢', '收費繳費', '無法使用代收'], 9],
        ['我想查詢GooglePlay代收', ['查詢'], 10],
        ['我想開啟GooglePlay代收', ['開啟'], 10],
        ['我想關閉GooglePlay代收', ['關閉'], 10],
        ['我想查詢GooglePlay交易紀錄', ['查詢', '交易', '紀錄'], 10],
        ['我想查詢GooglePlay交易失敗原因', ['查詢', '交易', '失敗原因'], 10],
        ['我想查詢GooglePlay增加額度方法', ['查詢', '增加額度'], 10],
        ['我想查詢GooglePlay申請退款', ['查詢', '申請退款'], 10],
        ['我想查詢GooglePlay繳費後無法使用代收', ['查詢', '無法使用代收'], 10],
        ['我想查詢iTunesStore代收', ['查詢'], 11],
        ['我想開啟AppleStore代收', ['開啟'], 11],
        ['我想關閉AppleStore代收', ['關閉'], 11],
        ['我想查詢AppleStore交易紀錄', ['查詢', '交易', '紀錄'], 11],
        ['我想查詢AppleStore交易失敗原因', ['查詢', '交易', '失敗原因'], 11],
        ['我想查詢AppleStore申請退款', ['查詢', '申請退款'], 11],
        ['我想查詢AppleStore繳費後無法使用代收', ['查詢', '無法使用代收'], 11],
        ['我想知道friDay影音異動', ['影音異動'], 12],
        ['關於friDay影音異動', ['關於'], 12],
        ['我想詢問單門號續約', ['詢問', '續約'], 13],
        ['我想詢問單門號續約。', ['詢問', '單門號續約'], 13],
        ['我想查看單門號優惠', ['查看', '優惠'], 13],
        ['我想查看單門號優惠。', ['查看', '單門號優惠'], 13],
        ['關於新啟用/攜碼的問題', ['關於'], 14],
        ['關於新啟用的問題', ['關於'], 14],
        ['關於攜碼的問題', ['關於'], 14],
        ['我想詢問新申辦/攜碼', ['詢問'], 14],
        ['我想詢問新申辦', ['詢問'], 14],
        ['關於攜碼問題解答', ['關於'], 14],
        ['我想詢問攜碼方案優惠', ['詢問', '優惠'], 14],
        ['我想要新辦一個門號', ['新辦'], 14],
        ['我想詢問單買手機優惠', ['詢問', '優惠'], 14],
        ['我想詢問線上續約優惠', ['詢問', '線上續約', '優惠'], 15],
        ['我想詢問旗艦機款購機優惠', ['詢問', '購機', '優惠'], 15],
        ['我想詢問買小送大超深優惠', ['詢問', '優惠'], 15],
        ['我想詢問三星旗艦機超划算', ['詢問', '超划算'], 15],
        ['我想詢問網路門市空機優惠', ['詢問', '網路門市', '空機優惠'], 15],
        ['我想詢問iPhone14促銷方案', ['詢問', '促銷方案'], 15],
        ['關於iPhone14促銷方案', ['關於', '促銷方案'], 15],
        ['我想詢問網路門市熱門活動', ['詢問', '網路門市', '熱門活動'], 15],
        ['我想詢問AirPods Pro優惠', ['詢問', '優惠'], 15],
        ['我想了解遠傳定位手錶方案', ['了解', '定位手錶', '方案'], 15],
        ['我想詢問老客戶續約獨享好康', ['詢問', '老客戶', '續約', '獨享好康'], 15],
        ['我想詢問新辦攜碼單門號優惠', ['詢問', '新辦', '優惠'], 15],
        ['關於家用寬頻優惠', ['關於', '家用寬頻', '優惠'], 16],
        ['關於家用寬頻優惠費率', ['關於', '家用寬頻', '費率'], 16],
        ['關於家用寬頻相關費用', ['關於', '家用寬頻', '費用'], 16],
        ['我想詢問家用寬頻可供申裝區域', ['詢問', '家用寬頻', '可供申裝區域'], 16],
        ['我想詢問家用寬頻找專門問方案', ['詢問', '家用寬頻'], 16],
        ['我想要寬頻問題報修', ['想要', '寬頻問題', '報修'], 16],
        ['我想詢問寬頻取消方法', ['詢問', '寬頻取消'], 16],
        ['我想詢問friDay影音取消方法', ['詢問', '影音取消'], 16],
        ['我想詢問數位萬事通取消方法', ['詢問', '取消方法'], 16],
    ]
    
    user_input = []
    keyword_list = []
    class_data = []

    # 決定取用的部分
    # data = data[81:]

    for d in data:
        user_input.append(d[0])
        keyword_list.append(d[1])
        class_data.append([d[0], d[2]])

    cd.class_data = class_data

    if (process == 1):
        openai.api_key = api_key2
        # user_input.reverse()
        # keyword_list.reverse()
        user_input = user_input[round(len(user_input)/2):]
        keyword_list = keyword_list[round(len(keyword_list)/2):]
    else:
        user_input = user_input[0:round(len(user_input)/2)]
        keyword_list = keyword_list[0:round(len(keyword_list)/2)]

    i = 0
    for _input in user_input:
        print('目前跑的process')
        print(process)
        print('目前處理得input')
        print(_input)
        cd.user_input = _input
        cd.generate_word(keyword_list[i], 10)

        # cd.create_keyword_sentence()
        # # break
        # cd.create_similar_sentence(10)
        # cd.create_data()
        i += 1

