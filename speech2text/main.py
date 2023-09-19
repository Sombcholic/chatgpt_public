import openai
import yaml
import sys
import numpy as np
from numpy.linalg import norm
import requests

# https://platform.openai.com/docs/guides/speech-to-text
if __name__ == "__main__":
    with open('../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']

    openai.api_key = api_key


    audio_file= open("./data/test1.mp4", "rb")
    transcript = openai.Audio.transcribe("whisper-1", audio_file)

    sentence = (transcript.text).replace(' ', '，')

    print(sentence)
