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
        self.datapath = ''
        self.dataname = ''
        self.sick_sentence = {}

    def set_datapath(self, path):
        self.datapath = path
    
    def set_dataname(self, name):
        self.dataname = name
        
    def gpt(self, gpt_input, timesleep = 5):
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages=[
                {"role": "user", "content": gpt_input}
            ],
            # max_tokens=8
            )

        # self.token_sum += completion.usage.total_tokens

        time.sleep(timesleep)

        return completion.choices[0].message.content
    
    def load_data(self):
        try:
            with open('./data/hospital/' + self.dataname + '.yml', 'r', encoding="utf-8") as f:
                data = yaml.safe_load(f)
                if (data is not None):
                    self.sick_sentence = data
        except Exception as e:
            print(e)
            ...

    def generate_word(self, data, num):
        gpt_input = '請給我' + str(num) + '句病人諮詢醫生，可能屬於' + data + '的條列式病症例句，不要有重複的'


        result = self.gpt(gpt_input, 5)
        split_word = result.split('\n')

        print('找到了')
        print(gpt_input)

        # 利用opencc 簡轉中
        cc = OpenCC('s2twp')

        i = 1
        for w in split_word:
            try:
                if (int(w[0]) in range(num+1)):
                    # 簡轉中
                    new_w = cc.convert(w)
                    # 去掉序列資料
                    new_w = new_w.replace(str(i) + '. ', '')
                    # 去掉標點符號
                    new_w = new_w.translate(str.maketrans('', '', string.punctuation))
                    # 去掉空格
                    new_w = new_w.replace(' ', '')

                    if (self.sick_sentence.get(data) is None):
                        self.sick_sentence[data] = [new_w]
                    else:
                        self.sick_sentence[data].append(new_w)
                    i += 1
            except:
                ...
        
        # print('看看這裡')
        # print(self.sick_sentence)

        if (self.sick_sentence != {}):
            with open('./data/hospital/' + self.dataname + '.yml', 'w', encoding='utf-8') as f:
                yaml.dump(self.sick_sentence, f, allow_unicode=True)


if __name__ == "__main__":
    with open('../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']
        api_key2 = data['chatgpt_api2']

    # openai.api_key = api_key2
    datapath = './data/hospital/'
    # dataname = '乳腺外科'
    # dataname = '婦科'
    process = 1

    if process == 0:
        openai.api_key = api_key
        dataname = '骨與軟組織腫瘤科'

        # 第一個的
        dataset = [
            '乳癌',
            '前列腺癌',
            '肺癌',
            '大腸直腸癌',
            '膀胱癌',
            '食道癌',
            '頭頸部癌',
            '腦腫瘤',
            '肝癌',
            '胰臟癌',
            '子宮頸癌',
            '卵巢癌',
            '腎癌',
            '皮膚癌',
            '骨髓瘤',
            '甲狀腺癌',
            '恶性淋巴瘤',
            '肝外膽管癌',
            '肝轉移瘤',
            '骨肉瘤',
            '胸腺瘤',
            '胃癌',
            '胰島細胞瘤',
            '腎上腺皮質癌',
            '胃肠道間質瘤',
            '子宮內膜癌',
            '鼻咽癌',
            '頭頸部鱗狀細胞癌',
            '攝護腺腺病',
            '骨肉瘤',
            '卵巢上皮癌',
            '腎盂癌',
            '胃泌素瘤',
            '甲狀旁腺癌',
            '胰臟內分泌腫瘤',
            '胰臟內分泌腫瘤',
            '侵襲性乳腺癌',
            '骨癌',
            '卵巢囊腫',
            '胃泌素瘤',
            '骨肉瘤',
            '胰臟內分泌腫瘤',
            '骨癌',
            '胃泌素瘤',
            '肝細胞癌',
            '膽管癌',
            '肺腺癌',
            '膽囊癌',
            '胃泌素瘤',
            '胰臟內分泌腫瘤',
        ]
    else:
        openai.api_key = api_key2
        dataname = '醫學影像科'

        dataset = [
            '肺炎',
            '肺栓塞',
            '肺結核',
            '心肌梗塞',
            '腦中風',
            '腦腫瘤',
            '腦出血',
            '骨折',
            '腎結石',
            '膀胱癌',
            '膀胱結石',
            '腎上腺腫瘤',
            '膽囊炎',
            '膽結石',
            '胰臟炎',
            '胰臟腫瘤',
            '乳癌',
            '子宮頸癌',
            '子宮內膜異位症',
            '卵巢囊腫',
            '卵巢腫瘤',
            '甲狀腺結節',
            '甲狀腺癌',
            '頸動脈狹窄',
            '乳房纖維腺瘤',
            '乳腺增生',
            '前列腺增生',
            '前列腺癌',
            '肝膿瘍',
            '肝囊腫',
            '肝細胞癌',
            '腸梗阻',
            '腸息肉',
            '腸癌',
            '腸充氣',
            '骨肉瘤',
            '淋巴瘤',
            '甲狀腺功能亢進症',
            '腎囊腫',
            '腎癌',
            '腎結核',
            '腎囊腫',
            '腎囊性病變',
            '腎切除',
            '腎衰竭',
            '膀胱異位',
            '膀胱充氣',
            '膀胱萎縮',
            '膀胱腫瘤',
            '膀胱發育不全',
        ]
    
    cd = createDataset()
    cd.set_datapath(datapath)
    cd.set_dataname(dataname)
    cd.load_data()

    for data in dataset:
        if (cd.sick_sentence.get(data) is None):
            cd.generate_word(data, 30)
        # else:
        #     print(data)
        #     break
