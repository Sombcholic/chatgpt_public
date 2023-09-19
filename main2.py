import openai
import time
import yaml


if __name__ == "__main__":
    with open('../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']

    openai.api_key = api_key

    start = time.time()

    # test1 = openai.ChatCompletion()
    
    # userInput = '使用者:我想吃炸機意麵!。\n请回应后再依次回答以下问题。A.请判断使用者问题的内容属性，4个字以内\nB.请依照使用者问题判断使用者情绪指数，四个字以内。\nC.判断使用者问题的情绪状态，1表示消极，5表示无情绪或快乐，10表示极度愤怒'
    # uInput = '大腸癌檢查'
    # userInput1 = '使用者: 我想知道' + uInput
    # userInput1 = '使用者: 我想知道' + uInput + '\n A.请判断上述使用者问题的内容属性，4个字以内\n B.请依照上述使用者问题判断使用者情绪指数，四个字以内。\n C.判断上述使用者问题的情绪状态，1表示消极，5表示无情绪或快乐，10表示极度愤怒'
    # userInput1 = '大腸癌檢查'
    # userInput2 = 'A.请判断上述使用者问题的内容属性，4个字以内\n B.请依照上述使用者问题判断使用者情绪指数，四个字以内。\n C.判断上述使用者问题的情绪状态，1表示消极，5表示无情绪或快乐，10表示极度愤怒'

    # uInput = '我想知道明天天氣'
    uInput = '我想知道股票'
    # uInput = '我想知道大腸症'
    # uInput = '我頭痛欲裂'
    userInput1 = '幫我判斷「' + uInput + '」是否使用任何病情相關的詞彙，1表示有，-1表示沒有'

    completion = openai.ChatCompletion.create(
        model="gpt-3.5-turbo",
        messages=[
            # {"role": "user", "content": "逆好，我是台灣人！很高興認識你"}
            {"role": "user", "content": userInput1}
        ],
        # max_tokens=8
    )

    # 使用者說: 我的肚子好痛阿!!!!\n\n 請判斷使用者的情緒指數，10為最大，1為最小，只需要呈現情緒指數。

    print('-----------------------------------------------------------')
    print('使用者詢問')
    print(userInput1)
    print('chatGPT回答')
    print(completion.choices[0].message.content)
    print('-----------------------------------------------------------')
    print(completion.usage.total_tokens)

    end = time.time()
    print('運算時間: ', end-start)
    print()