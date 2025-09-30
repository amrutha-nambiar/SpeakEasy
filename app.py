import streamlit as st
from googletrans import Translator, LANGUAGES

translator = Translator()

# Page config
st.set_page_config(
    page_title="🌐 SpeakEasy",
    layout="centered",
    page_icon="🌐"
)

# Styling with markdown
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
        margin-top: 10px;
    }
    .stTextArea textarea {
        font-size: 16px;
        height: 120px;
    }
    .stTextInput input {
        font-size: 16px;
        height: 40px;
    }
    </style>
    """,
    unsafe_allow_html=True
)

st.title("🌐 SpeakEasy")
st.write("Translate text between languages instantly!")

# Language options
language_options = sorted(LANGUAGES.values())
lang_codes = {v: k for k, v in LANGUAGES.items()}

# User input
text = st.text_area("Enter text to translate:")

col1, col2 = st.columns(2)

with col1:
    source_lang = st.selectbox("Source language", ["auto"] + language_options, index=0)

with col2:
    target_lang = st.selectbox("Target language", language_options, index=21)  # default: Hindi

# Translate button
if st.button("Translate") and text:
    try:
        src_code = "auto" if source_lang == "auto" else lang_codes[source_lang]
        tgt_code = lang_codes[target_lang]

        translation = translator.translate(text, src=src_code, dest=tgt_code)
        translated_text = translation.text

        # Display translation in a nice card
        st.markdown(
            f"""
            <div style="background-color:#00796B;color:white;padding:15px;
                        border-radius:12px;margin-top:10px">
            <h4>Translated Text:</h4>
            <p style="font-size:18px">{translated_text}</p>
            </div>
            """,
            unsafe_allow_html=True
        )
    except Exception as e:
        st.error(f"Error: {e}")
