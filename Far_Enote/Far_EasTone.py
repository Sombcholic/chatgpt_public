import openai
import yaml
import time
import sys
import copy

class chatGpt():
    def __init__(self):
        self.message = []
        self.get_API()
        self.history_message = ''
        self.system_message = {}

    def set_history_message(self, history_message):
        self.history_message = history_message
        self.message = []
        # self.message.append({"role": "system", "content": '我們曾經有對話，對話紀錄如下：' + history_message})
        # self.message.append({"role": "user", "content": '讓我了解以前有過的對話'})
        # self.message.append({"role": "assistant", "content": '我們有過一些對話，對話紀錄如下：' + history_message})

    def set_system_message(self, system_message):
        self.system_message = system_message

    def set_message(self, dataList):
        self.message = dataList

    def get_API(self):
        with open('../../chatgptAPI.yml', 'r') as f:
            data = yaml.safe_load(f)
            openai.api_key = data['chatgpt_api']
    
    def ask(self, userInput: str):
        input_messages = []
        input_messages.append(copy.deepcopy(self.system_message))

        # print()
        # print('第一次看到input_messages')
        # print(input_messages)
        # print('第一次看到system_message')
        # print(system_message)

        if (self.history_message != ""):
            # input_messages.append({"role": "user", "content": '讓我知道以前的對話紀錄'})
            # input_messages.append({"role": "assistant", "content": '我們的對話紀錄如下：' + self.history_message})
            input_messages[0]["content"] = (input_messages[0]["content"] + '，知道以下這些對話資訊：「' + self.history_message + '」，請記住這些訊息，')
            # input_messages[0]["content"] = (input_messages[0]["content"] + '，' + self.history_message + '，')
            # input_messages[0]["content"] = (input_messages[0]["content"] + '，我們有過一些對話，對話紀錄如下：「' + self.history_message + '」，請記住這些訊息，')

        # print(input_messages)
        # sys.eixt(0)

        # print()
        # print('目前的input_messages')
        # print(input_messages)
        # print('目前的self.message')
        # print(self.message)

        input_messages += self.message

        input_messages.append({"role": "user", "content": userInput})
        self.message.append({"role": "user", "content": userInput})

        # print('**************************************************')
        # print('丟進去chatgpt的message')
        # print(input_messages)
        # print('**************************************************')

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= input_messages,
            # max_tokens=300
        )
        input_messages.append({"role": "assistant", "content": completion.choices[0].message.content})
        self.message.append({"role": "assistant", "content": completion.choices[0].message.content})

        return completion
    
    def create_summary(self, number):
        completion = ""

        try:
            conversation_summary = []

            # system
            conversation_summary.append({"role": "system", "content": '你是一個文學家，用字簡潔'})
            # conversation_summary.append({"role": "system", "content": '請用最多' + str(number) + '個字清楚羅列我們的對話，每一個使用者的問題都要談到'})
            conversation_summary.append({"role": "assistant", "content": '我們之前的對話紀錄如下：' + self.history_message})
            # conversation_summary.append({"role": "user", "content": '讓我了解以前的對話'})
            # conversation_summary.append({"role": "assistant", "content": self.history_message})
            # conversation_summary.append({"role": "assistant", "content": '我們之前的對話紀錄如下：' + self.history_message})
            # conversation_summary.append({"role": "assistant", "content": '我們有過一些對話，對話紀錄如下：' + self.history_message})
            
            conversation_summary += self.message
            conversation_summary.append({"role": "user", "content": '請用最多' + str(number) + '個字濃縮描述我們的對話，每一個問題都要談到，包括我們之前的對話紀錄'})

            # print('-----------------------------')
            # print('看看目前處理的summary')
            # print(conversation_summary)
            # print('-----------------------------')

            completion = openai.ChatCompletion.create(
                model="gpt-3.5-turbo",
                messages= conversation_summary,
                # max_tokens=300
            )
        except:
            ...

        return completion

class User():
    def __init__(self, userName = 'JAJA'):
        self.userName = userName
        self.history_message = ''
        
        self.load_data()
    
    def save_data(self):
        path = self.userName + '.txt'
        f = open(path, 'w', encoding='UTF-8')
        f.write(self.history_message)

    def load_data(self):
        try:
            path = self.userName + '.txt'
            f = open(path, 'r', encoding='UTF-8')
            self.history_message = f.read()
        except:
            ...



if __name__ == "__main__":
    token = 0

    start = time.time()

    chatgpt = chatGpt()
    user = User('Joelu')

    userInput = input("請輸入想詢問的內容: ")

    system_message = {"role": "system", "content": "你角色扮演客服人員。妳的名字叫做遠傳小幫手-愛瑪，妳服務的公司叫做遠傳電信，公司地址在臺北市大安區敦化南路2段207號28樓，連絡電話為(02)7723-5000，傳真為(02)7723-5199，文字客服專員服務時間為：週一~週五 09:00~20:00，\
                        目前促銷活動為4G 499/599吃到飽，\
                        請用這個身分回答所有的問題並以客為尊，不要回答任何chatgpt相關話題，可以和使用者閒聊，回答不能超過100個字"}
                        # 請用這個身分回答我所有的問題，不要回答任何chatgpt相關話題，假如詢問任何有關模型、資料、chatgpt的問題，全部回答不知道，不能讓人知道你是chatgpt"}


    chatgpt.set_system_message(system_message)
    chatgpt.set_history_message(user.history_message)

    while userInput != 'quit':

        # 我猜應該要3400
        if (token >= 3500):
            # 怕token過多，先儲存
            gpt_summary = chatgpt.create_summary(600)
            if (gpt_summary != ''):
                user.history_message = gpt_summary.choices[0].message.content
                user.save_data()

            user.load_data()
            # 重新設定chatgpt參數
            chatgpt.set_history_message(user.history_message)

            token = 0

        completion = chatgpt.ask(userInput)

        print('-----------------------------------------------------------')
        print('chatGPT回答')
        print(completion.choices[0].message.content)
        print('-----------------------------------------------------------')
        # print(completion.usage.total_tokens)
        token = completion.usage.total_tokens

        end = time.time()
        # print('運算時間: ', end-start)
        # print()

        userInput = input("請輸入想詢問的內容: ")

    
    print('歷史紀錄')
    gpt_summary = chatgpt.create_summary(600)
    token = gpt_summary.usage.total_tokens
    print('chatGPT回答')
    print(gpt_summary.choices[0].message.content)
    # print('最後的總token')
    # print(token)

    if (gpt_summary != ''):
        user.history_message = gpt_summary.choices[0].message.content
        user.save_data()