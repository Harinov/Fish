import streamlit as st
from openai import OpenAI
from PIL import Image
import io

# Setting up OpenAI API key
client = OpenAI(api_key = st.secrets['OPENAI_SECRET_KEY'])

st.title("Fish Identifier and Recipe Suggester")

st.header("Upload an Image or Use Live Camera to Identify Fish")

# Image Upload
uploaded_file = st.file_uploader("Choose an image...", type=["jpg", "png"])

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

    # Call OpenAI API for fish identification
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=f"Identify the type of fish in the provided image and suggest a suitable recipe.",
        max_tokens=150
    )

    fish_info = response.choices[0].text.strip()
    return fish_info

if uploaded_file or picture:
    with st.spinner("Identifying fish and fetching recipe..."):
        fish_info = identify_fish_and_suggest_recipe(img)
        st.success(f"Fish Information: {fish_info}")
