import openai
import yaml
import sys
import numpy as np
from numpy.linalg import norm
import requests
from scipy.spatial.distance import cosine
import time

# https://platform.openai.com/docs/guides/embeddings/what-are-embeddings
if __name__ == "__main__":
    with open('../../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']

    openai.api_key = api_key

    sentenceList = [
        "火車",
        "鐵道列車",
        "巴士",
        "列車",
        "家人",
        "斯巴達",
        "馬自達",
        "車車車",
        "火焰",
    ]

    embeddingList = []

    for sentence in sentenceList:
        start = time.time()
        response = openai.Embedding.create(
            input=sentence,
            model="text-embedding-ada-002"
        )
        
        embeddings = response['data'][0]['embedding']
        embeddingList.append(embeddings)

        end = time.time()

        print('轉化的時間: ', end - start)


    for i in range(len(embeddingList)-1):
        similarity = np.dot(embeddingList[0],embeddingList[0+i])/(norm(embeddingList[0])*norm(embeddingList[0+i]))
        print('計算相似度==>' + sentenceList[0] + '-' + sentenceList[0+i])
        print(similarity)


    # similarity = np.dot(embeddingList[0],embeddingList[1])/(norm(embeddingList[0])*norm(embeddingList[1]))

    # print(similarity)
