import openai
import yaml
import sys
import numpy as np
from numpy.linalg import norm
import requests
from pydub import AudioSegment
import os

if __name__ == "__main__":
    with open('../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']

    openai.api_key = api_key

    print(os.getcwd())
    # sys.exit(0)

    # os.chdir('/python/GPT/chatGPT/speech2text/data')  # 使用 Colab 要換路徑使用

    # D:\python\GPT\chatGPT\speech2text\data

    song = AudioSegment.from_file("./data/test1.mp4")

    # PyDub handles time in milliseconds
    # ten_minutes = 10 * 60 * 1000
    ten_seconds = 10 * 1000

    first_ten_seconds = song[:ten_seconds]

    first_ten_seconds.export("test1_10.mp4", format="mp4")