import requests
import matplotlib.pyplot as plt
from matplotlib.patches import Rectangle
from PIL import Image
from io import BytesIO
from pprint import pprint

# 金鑰、端點、區域
key = ""
region = 'westus2'
endpoint = 'https://aien140001visionservice.cognitiveservices.azure.com/'
endpointUrl = f'{endpoint}vision/v3.0/ocr'

# 讀取圖片路徑
image_path = "./cute_image/output_address.jpg"
with open(image_path, "rb") as img_file:
    image_data = img_file.read()

# OCR 必要參數
headers = {'Ocp-Apim-Subscription-Key': key,
           'Content-Type': 'application/octet-stream'}
params = {
    'language': 'zh-Hant',
    'detectOrientation': 'true',
}

# 發送圖片到 OCR API 並獲取分析結果
response = requests.post(endpointUrl, headers=headers, params=params, data=image_data)
response.raise_for_status()
analysis = response.json()
pprint(analysis)

# 提取行信息
line_infos = [region["lines"] for region in analysis["regions"]]

# 將文字信息存儲到一個列表中
word_infos = []
for line in line_infos:
    for word_metadata in line:
        for word_info in word_metadata["words"]:
            word_infos.append(word_info)

# 輸出文字信息
print(word_infos)
print(word_infos[0]["text"])
print(word_infos[1]["text"])
print(word_infos[2]["text"])
