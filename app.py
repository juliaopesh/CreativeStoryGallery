import streamlit as st
import requests
import json
import base64
from io import BytesIO
from PIL import Image

# Set your Gemini API Key
GEMINI_API_KEY = "AIzaSyCADiHvj7uQ0Ekovs_Gg1zQYoZtYUKqDNQ"

# Define the Gemini API URL
GEMINI_API_URL = f"https://generativelanguage.googleapis.com/v1beta/models/gemini-1.5-flash:generateContent?key={GEMINI_API_KEY}"

st.title("Creative Story Gallery")
st.write("Upload an artwork, and AI will generate a story based on it!")

# Upload an image
uploaded_image = st.file_uploader("Upload your artwork", type=["png", "jpg", "jpeg"])

if uploaded_image:
    st.image(uploaded_image, caption="Your Artwork", use_container_width=True)

    # Convert image to Base64
    image_bytes = uploaded_image.read()
    base64_image = base64.b64encode(image_bytes).decode("utf-8")

    if st.button("Generate Story"):
        with st.spinner("Analyzing image and generating story..."):
            try:
                # Step 1: Describe the Image Using Gemini API
                description_payload = {
                    "contents": [{
                        "parts": [
                            {"text": "Describe this image in detail."},
                            {"inline_data": {
                                "mime_type": "image/jpeg",
                                "data": base64_image
                            }}
                        ]
                    }]
                }

                response = requests.post(GEMINI_API_URL, json=description_payload, headers={"Content-Type": "application/json"})

                if response.status_code == 200:
                    description_data = response.json()
                    image_description = description_data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    st.error(f"Failed to process image. Error: {response.text}")
                    image_description = "An artistic and creative image."

                # Step 2: Generate a Story from the Description
                story_payload = {
                    "contents": [{
                        "parts": [{"text": f"Write a short creative story inspired by this artwork: {image_description}"}]
                    }]
                }

                story_response = requests.post(GEMINI_API_URL, json=story_payload, headers={"Content-Type": "application/json"})

                if story_response.status_code == 200:
                    story_data = story_response.json()
                    story_text = story_data["candidates"][0]["content"]["parts"][0]["text"]
                else:
                    st.error(f"Failed to generate story. Error: {story_response.text}")
                    story_text = "No story generated."

                # Display the story
                st.write("### ✨ AI-Generated Story")
                st.write(story_text)

            except Exception as e:
                st.error(f"Error: {e}")
