# -*- coding: UTF-8 -*-
import openai
import yaml
import time

class chatGpt():
    def __init__(self):
        self.message = [{"role": "system", "content": '請用繁體中文回答，數字用阿拉伯數字'},
                        # {"role": "user", "content": '之前的對話紀錄如下：在這段對話中，對方問萬壽菊一周要澆水多少次。我回答說，澆水頻率會受到多重因素的影響，但一般建議每周澆水一到兩次，並在土壤表面感覺乾燥時進行澆水。另外，還提醒觀察植株狀況和環境因素，調整澆水頻率。如果你計畫來台北一日遊，以下是一些建議：1. 計畫行程：先列出你希望參觀的景點和活動，然後安排行程的時間。對於一日遊，最好選擇一些距離較近的景點，以充分利用你的時間。2. 交通方式：台北的公共交通系統非常方便，你可以考慮使用捷運、公車或TAXI。另外，租借腳踏車也是一個很好的選擇，讓你可以更輕鬆地穿梭在市區各處。3. 必參景點：台北有很多值得參觀的景點，包括台北101、故宮博物院、中正紀念堂、龍山寺等。你可以依照你的興趣和時間做出選擇。4. 美食：台北以美食聞名，你可以品嚐當地的小吃和夜市美食。士林夜市、饒河街夜市和九份老街都是很受歡迎的選擇。5. 文化體驗：台北也有許多可以體驗當地文化的活動，例如參加一個茶道體驗、參觀傳統市場或參與一個手作工坊。最重要的是要合理安排時間和交通，以確保你能夠充分地享受台北的魅力。希望這些建議對你有幫助！如果你還有其他問題，請隨時問我。祝你在台北一日遊中玩得愉快！'},
                        # {"role": "assistant", "content": '收到！'},
                        # {"role": "system", "content": '之前的對話紀錄如下：在這段對話中，對方問萬壽菊一周要澆水多少次。我回答說，澆水頻率會受到多重因素的影響，但一般建議每周澆水一到兩次，並在土壤表面感覺乾燥時進行澆水。另外，還提醒觀察植株狀況和環境因素，調整澆水頻率。如果你計畫來台北一日遊，以下是一些建議：1. 計畫行程：先列出你希望參觀的景點和活動，然後安排行程的時間。對於一日遊，最好選擇一些距離較近的景點，以充分利用你的時間。2. 交通方式：台北的公共交通系統非常方便，你可以考慮使用捷運、公車或TAXI。另外，租借腳踏車也是一個很好的選擇，讓你可以更輕鬆地穿梭在市區各處。3. 必參景點：台北有很多值得參觀的景點，包括台北101、故宮博物院、中正紀念堂、龍山寺等。你可以依照你的興趣和時間做出選擇。4. 美食：台北以美食聞名，你可以品嚐當地的小吃和夜市美食。士林夜市、饒河街夜市和九份老街都是很受歡迎的選擇。5. 文化體驗：台北也有許多可以體驗當地文化的活動，例如參加一個茶道體驗、參觀傳統市場或參與一個手作工坊。最重要的是要合理安排時間和交通，以確保你能夠充分地享受台北的魅力。希望這些建議對你有幫助！如果你還有其他問題，請隨時問我。祝你在台北一日遊中玩得愉快！'},
                        # {"role": "system", "content": '在這段對話中，對方問萬壽菊一周要澆水多少次。我回答說，澆水頻率會受到多重因素的影響，但一般建議每周澆水一到兩次，並在土壤表面感覺乾燥時進行澆水。另外，還提醒觀察植株狀況和環境因素，調整澆水頻率。'},
                        # {"role": "system", "content": '如果你計畫來台北一日遊，以下是一些建議：\n1. 計畫行程：先列出你希望參觀的景點和活動，然後安排行程的時間。對於一日遊，最好選擇一些距離較近的景點，以充分利用你的時間。\n2. 交通方式：台北的公共交通系統非常方便，你可以考慮使用捷運、公車或TAXI。另外，租借腳踏車也是一個很好的選擇，讓你可以更輕鬆地穿梭在市區各處。\n3. 必參景點：台北有很多值得參觀的景點，包括台北101、故宮博物院、中正紀念堂、龍山寺等。你可以依照你的興趣和時間做出選擇。\n4. 美食：台北以美食聞名，你可以品嚐當地的小吃和夜市美食。士林夜市、饒河街夜市和九份老街都是很受歡迎的選擇。\n4. 美食：台北以美食聞名，你可以品嚐當地的小吃和夜市美食。士林夜市、饒河街夜市和九份老街都是很受歡迎的選擇。\n5. 文化體驗：台北也有許多可以體驗當地文化的活動，例如參加一個茶道體驗、參觀傳統市場或參與一個手作工坊。\n最重要的是要合理安排時間和交通，以確保你能夠充分地享受台北的魅力。希望這些建議對你有幫助！如果你還有其他問題，請隨時問我。祝你在台北一日遊中玩得愉快！'}
        ]
        self.get_API()
        # self.history_message = '在這段對話中，對方問萬壽菊一周要澆水多少次。我回答說，澆水頻率會受到多重因素的影響，但一般建議每周澆水一到兩次，並在土壤表面感覺乾燥時進行澆水。另外，還提醒觀察植株狀況和環境因素，調整澆水頻率。如果你計畫來台北一日遊，以下是一些建議：1. 計畫行程：先列出你希望參觀的景點和活動，然後安排行程的時間。對於一日遊，最好選擇一些距離較近的景點，以充分利用你的時間。2. 交通方式：台北的公共交通系統非常方便，你可以考慮使用捷運、公車或TAXI。另外，租借腳踏車也是一個很好的選擇，讓你可以更輕鬆地穿梭在市區各處。3. 必參景點：台北有很多值得參觀的景點，包括台北101、故宮博物院、中正紀念堂、龍山寺等。你可以依照你的興趣和時間做出選擇。4. 美食：台北以美食聞名，你可以品嚐當地的小吃和夜市美食。士林夜市、饒河街夜市和九份老街都是很受歡迎的選擇。5. 文化體驗：台北也有許多可以體驗當地文化的活動，例如參加一個茶道體驗、參觀傳統市場或參與一個手作工坊。最重要的是要合理安排時間和交通，以確保你能夠充分地享受台北的魅力。希望這些建議對你有幫助！如果你還有其他問題，請隨時問我。祝你在台北一日遊中玩得愉快！'
        self.history_message = '在對話中，提到了萬壽菊的澆水頻率以及我對來台北一日遊的建議。另外，也回答了最有名的電影是哪一部的問題。這些包括《教父》、《肖申克的救贖》、《星際大戰》、《鐵達 尼號》等。然而，最有名的電影很難單一指定，因為每個人喜好不同。歡迎根據自己的興趣和喜好去觀賞電影！'

    def get_API(self):
        with open('../chatgptAPI.yml', 'r') as f:
            data = yaml.safe_load(f)
            openai.api_key = data['chatgpt_api']
    
    def ask(self, userInput: str):
        inputMessages = self.message

        if (self.history_message != ""):
            self.message.append({"role": "user", "content": '之前的對話紀錄如下：' + self.history_message})
            self.message.append({"role": "assistant", "content": '收到！'})

        self.message.append({"role": "user", "content": userInput})

        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= self.message,
            # max_tokens=8
        )
        self.message.append({"role": "assistant", "content": completion.choices[0].message.content})

        return completion

    def create_summary(self, number):
        self.message.append({"role": "system", "content": '請將剛剛的對話用' + str(number) + '字做個總結'})
        completion = openai.ChatCompletion.create(
            model="gpt-3.5-turbo",
            messages= self.message,
            # max_tokens=8
        )

        return completion


if __name__ == "__main__":
    start = time.time()

    chatgpt = chatGpt()

    userInput = input("請輸入內容: ")

    while userInput != 'quit':
        completion = chatgpt.ask(userInput)

        print('-----------------------------------------------------------')
        print('使用者詢問')
        print(userInput)
        print(chatgpt.message)
        print('chatGPT回答')
        print(completion.choices[0].message.content)
        print('-----------------------------------------------------------')
        print(completion.usage.total_tokens)

        end = time.time()
        print('運算時間: ', end-start)
        print()

        userInput = input("請輸入內容: ")

    print('歷史紀錄')
    completion = chatgpt.create_summary(100)
    print('chatGPT回答')
    print(completion.choices[0].message.content)
    print('-----------------------------------------------------------')
    print(completion.usage.total_tokens)