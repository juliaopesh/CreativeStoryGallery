import streamlit as st
import os
from transformers import pipeline

# Disable Streamlit's file watcher entirely
os.environ["STREAMLIT_SERVER_ENABLE_FILE_WATCHER"] = "false"

# Initialize the text generator with truncation enabled
generator = pipeline(
    "text-generation",
    model="gpt2",
    truncation=True  # Explicitly enable truncation
)

st.title("Creative Story Gallery")
st.write("Welcome to the Creative Story Gallery app!")

uploaded_image = st.file_uploader("Upload your artwork", type=["png", "jpg", "jpeg"])
if uploaded_image is not None:
    st.image(uploaded_image, caption="Your Artwork", use_container_width=True)
    story_prompt = st.text_input("Describe your artwork in a few words:")
    if st.button("Generate Story"):
        story = generator(
            f"Generate a story about a child's drawing of {story_prompt}.",
            max_length=150  # Adjust the length of the generated story
        )
        st.write("**Your Story:**")
        st.write(story[0]['generated_text'])