import streamlit as st
import io
import requests
from PIL import Image, ImageDraw, ImageFont


st.title('顔認証アプリ')

subscription＿key = '70ed7d3ea7aa4f2b913029bdb4bad691'
assert subscription＿key

face_api_url = 'https://20200219ryooo.cognitiveservices.azure.com/face/v1.0/detect'

uploaded_file = st.file_uploader("画像をアップロードしてください",type='jpg')
if uploaded_file is not None:
    img = Image.open(uploaded_file)
    font = ImageFont.truetype("arial.ttf", 32)

    with io.BytesIO() as output:
        img.save(output, format="JPEG")
        binary_img = output.getvalue() #バイナリ取得
        
    headers = {
        'Content-Type': 'application/octet-stream',
        'Ocp-Apim-Subscription-Key': subscription_key}

    params = {
        'returnFaceId': 'true',
        'returnFaceAttributes': 'age,gender,headPose,smile,facialHair,glasses,emotion,hair,makeup,occlusion,accessories,blur,exposure,noise'
    }
    res = requests.post(face_api_url, params=params,headers=headers, data=binary_img)
    
    results = res.json()

    for result in results:
        rect = result['faceRectangle']
        text = str(result['faceAttributes']['gender']) + "," + (str(result['faceAttributes']['age']))
        
        draw = ImageDraw.Draw(img)
        draw.rectangle([(rect['left'],rect['top']),(rect['left']+rect['width'],rect['top']+rect['height'])],fill=None,outline='blue',width=5)
        draw.text(((rect['left']+rect['width']/12),rect['top']-30),text,font=font,fill=None,outline='blue',width = 100)


    st.image(img, caption='Uploaded Image', use_column_width=True)
