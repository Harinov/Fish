import streamlit as st
from PIL import Image
import requests
import base64

# Configure API key
GOOGLE_API_KEY = st.secrets['GOOGLE_API_KEY']

# Function to call Google Vision API
def identify_fish(image):
    api_key = GOOGLE_API_KEY
    endpoint = f"https://vision.googleapis.com/v1/images:annotate?key={api_key}"

    # Convert image to base64
    image_content = base64.b64encode(image.read()).decode()

    headers = {
        "Content-Type": "application/json"
    }

    payload = {
        "requests": [{
            "image": {
                "content": image_content
            },
            "features": [{
                "type": "LABEL_DETECTION",
                "maxResults": 1
            }]
        }]
    }

    response = requests.post(endpoint, headers=headers, json=payload)

    if response.status_code != 200:
        st.error(f"Request to Google Vision API failed with status code {response.status_code}")
        return None

    result = response.json()

    if "error" in result:
        st.error(f"Error from Google Vision API: {result['error']['message']}")
        return None

    # Process the result to extract fish type and recipe
    label_annotations = result['responses'][0].get('labelAnnotations', [])
    if not label_annotations:
        st.error("No labels detected in the image.")
        return None

    fish_name = label_annotations[0]['description']
    recipe = fetch_recipe_for_fish(fish_name)  # Replace with actual logic to fetch recipe

    return {
        'fish_name': fish_name,
        'description': f'A delicious {fish_name}.',
        'recipe': recipe
    }

# Function to fetch recipe for the fish
def fetch_recipe_for_fish(fish_name):
    # Placeholder for fetching recipe based on fish name
    # Replace with actual recipe fetching logic
    return f"Example Recipe for {fish_name}"

# Function to handle live camera input (reuses the identify_fish function)
def identify_fish_from_camera(image):
    return identify_fish(image)

# Streamlit interface
st.title("Fish Identifier and Recipe Suggestion")

st.write("""
    Upload an image of the fish or use your live camera to identify the fish and get recipe suggestions.
""")

# Upload an image
uploaded_image = st.file_uploader("Upload an image of the fish", type=["jpg", "jpeg", "png"])

if uploaded_image is not None:
    image = Image.open(uploaded_image)
    st.image(image, caption='Uploaded Image.', use_column_width=True)
    st.write("")
    st.write("Identifying...")

    # Call the identify_fish function
    result = identify_fish(uploaded_image)

    if result:
        st.write(f"*Fish Name:* {result['fish_name']}")
        st.write(f"*Description:* {result['description']}")
        st.write(f"*Recipe:* {result['recipe']}")

# Use live camera
st.write("Or use your live camera to identify the fish.")

camera_image = st.camera_input("Take a picture")

if camera_image is not None:
    image = Image.open(camera_image)
    st.image(image, caption='Captured Image.', use_column_width=True)
    st.write("")
    st.write("Identifying...")

    # Call the identify_fish_from_camera function
    result = identify_fish_from_camera(camera_image)

    if result:
        st.write(f"*Fish Name:* {result['fish_name']}")
        st.write(f"*Description:* {result['description']}")
        st.write(f"*Recipe:* {result['recipe']}")
