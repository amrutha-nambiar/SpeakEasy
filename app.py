import streamlit as st
from deep_translator import GoogleTranslator

# Page config
st.set_page_config(
    page_title="🌐 SpeakEasy",
    layout="centered",
    page_icon="🌐"
)

# Custom styling
st.markdown(
    """
    <style>
    .stButton>button {
        background-color: #4CAF50;
        color: white;
        height: 3em;
        width: 100%;
        font-size: 18px;
        border-radius: 10px;
    }
    .stTextArea textarea {
        font-size: 16px;
        height: 120px;
        background-color: #f0f0f0;
    }
    .stTextInput input {
        font-size: 16px;
        height: 40px;
    }
    .stSuccess {
        background-color: #e0ffe0 !important;
        color: black !important;
        padding: 10px;
        border-radius: 8px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 SpeakEasy")
st.write("Translate text between languages instantly!")

# User input
text = st.text_area("Enter text to translate:")

col1, col2 = st.columns(2)

with col1:
    source_lang = st.text_input("Source language (e.g., en for English)", value="auto")

with col2:
    target_lang = st.text_input("Target language (e.g., hi for Hindi)", value="hi")

# Translate button
if st.button("Translate") and text:
    try:
        translation = GoogleTranslator(source=source_lang, target=target_lang).translate(text)
        st.success(f"**Translated Text:**\n\n{translation}", icon="✅")
    except Exception as e:
        st.error(f"Error: {e}")
