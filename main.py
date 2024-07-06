import streamlit as st
from openai import OpenAI
from PIL import Image
import io
import base64
import requests

# Setting up OpenAI API key
client = OpenAI(api_key=st.secrets['OPENAI_SECRET_KEY'])

st.title("Fish Identifier and Recipe Suggester")

st.header("Upload an Image or Use Live Camera to Identify Fish")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])
st.write(uploaded_file)

# Live Camera Input
use_camera = st.checkbox("Use live camera")

if use_camera:
    picture = st.camera_input("Take a picture")
else:
    picture = None

# Display uploaded image or captured picture
if uploaded_file or picture:
    if uploaded_file:
        img = Image.open(uploaded_file)
    else:
        img = Image.open(io.BytesIO(picture.getvalue()))

    st.image(img, caption="Uploaded/Captured Image", use_column_width=True)


def identify_fish_and_suggest_recipe(image):
    # Convert image to bytes
    img_bytes = io.BytesIO()
    image.save(img_bytes, format='JPEG')
    img_bytes = img_bytes.getvalue()

    def encode_image(file_path):
        with open(file_path, 'rb') as image_file:
            return base64.b64encode(image_file.read()).decode('utf-8')

    def vision_file(file_path):
        base64_image = encode_image(file_path)

        headers = {
            "Content-Type": "application/json",
            "Authorization": f"Bearer {userdata.get('OPENAI_API_KEY')}"
        }

        payload = {
            "model":
            "gpt-4o",
            "messages": [{
                "role":
                "user",
                "content": [{
                    "type": "text",
                    "text": "what is in this image?"
                }, {
                    "type": "image_url",
                    "image_url": {
                        "url": f"data:image/png;base64,{base64_image}"
                    }
                }]
            }],
            "max_tokens":
            20
        }

        response = requests.post("https://api.openai.com/v1/chat/completions",
                                 headers=headers,
                                 json=payload)

        (response.json()['choices'][0]['message']['content'])

    vision_file(uploaded_file)

    fish_info = response.choices[0].message.content
    return fish_info


if uploaded_file or picture:
    with st.spinner("Identifying fish and fetching recipe..."):
        fish_info = identify_fish_and_suggest_recipe(img)
        st.success(f"Fish Information: {fish_info}")
