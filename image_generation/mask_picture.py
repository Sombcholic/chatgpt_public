import openai
import time
import yaml
import sys
import matplotlib.pyplot as plt
import matplotlib.image as img
import numpy as np
import requests
from PIL import Image
from io import BytesIO

# https://platform.openai.com/docs/guides/images/introduction
if __name__ == "__main__":
    with open('../../chatgptAPI.yml', 'r') as f:
        data = yaml.safe_load(f)
        api_key = data['chatgpt_api']

    openai.api_key = api_key

    # 這個一定要png，然後一直沒有效果
    response = openai.Image.create_edit(
        image=open("./mask_img/origin.png", "rb"),
        mask=open("./mask_img/mask_real.png", "rb"),
        prompt="a white cat with ranidow head",
        n=1,
        size="1024x1024"
    )
    image_url = response['data'][0]['url']

    response = requests.get(image_url)
    image_data = response.content

    image = Image.open(BytesIO(image_data))
    image.save('./mask_img/edited_cat_raibowhead.jpg')