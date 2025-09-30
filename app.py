import streamlit as st
from deep_translator import GoogleTranslator, exceptions
from gtts import gTTS
from io import BytesIO

# Page config
st.set_page_config(
    page_title="🌐 SpeakEasy",
    layout="centered",
    page_icon="🌐"
)

# Styling
st.markdown("""
<style>
.stButton>button {background-color: #4CAF50;color: white;height: 3em;width: 100%;font-size: 18px;border-radius: 10px;margin-top: 10px;}
.stTextArea textarea {font-size: 16px; height: 120px;}
.stTextInput input {font-size: 16px; height: 40px;}
</style>
""", unsafe_allow_html=True)

st.title("🌐 SpeakEasy")
st.write("Translate text between languages instantly!")

# Supported languages
language_codes = {
    "English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es",
    "German": "de", "Chinese (Simplified)": "zh-CN", "Japanese": "ja",
    "Russian": "ru", "Arabic": "ar"
}

language_options = list(language_codes.keys())

# Initialize session state
if "history" not in st.session_state:
    st.session_state.history = []

# User input
text = st.text_area("Enter text to translate:")

col1, col2, col3 = st.columns([1,1,1])

with col1:
    source_lang = st.selectbox("Source language", ["auto"] + language_options, index=0)
with col2:
    target_lang = st.selectbox("Target language", language_options, index=1)
with col3:
    if st.button("🔄 Swap"):
        source_lang, target_lang = target_lang, source_lang
        st.experimental_rerun()

# Multi-language selection
multi_targets = st.multiselect("Translate into multiple languages:", language_options, default=[target_lang])

# Translate button
if st.button("Translate") and text:
    src_code = "auto" if source_lang == "auto" else language_codes[source_lang]
    
    st.subheader("Translations")
    for tgt_lang in multi_targets:
        try:
            tgt_code = language_codes[tgt_lang]
            translator = GoogleTranslator(source=src_code, target=tgt_code)
            translation = translator.translate(text)
            
            # Detect language if auto
            detected_lang = ""
            if source_lang == "auto":
                detected_lang = translator.detect(text)
                st.info(f"Detected Language: {detected_lang}")
            
            # Display translation
            st.markdown(f"""
                <div style="background-color:#00796B;color:white;padding:15px;border-radius:12px;margin-top:10px">
                <h4>{tgt_lang}:</h4>
                <p style="font-size:18px">{translation}</p>
                </div>
            """, unsafe_allow_html=True)
            
            # Save history
            st.session_state.history.append((text, tgt_lang, translation))
            
            # Text-to-speech
            tts = gTTS(translation, lang=tgt_code)
            audio_bytes = BytesIO()
            tts.write_to_fp(audio_bytes)
            audio_bytes.seek(0)
            st.audio(audio_bytes, format="audio/mp3")
            
            # Download translation
            st.download_button(f"Download {tgt_lang} Translation", translation, file_name=f"translation_{tgt_lang}.txt")
            
        except exceptions.NotValidPayload as e:
            st.error(f"Invalid text: {e}")
        except exceptions.LanguageNotSupportedException as e:
            st.error(f"Unsupported language: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# Display recent history
if st.session_state.history:
    st.subheader("Recent Translations")
    for i, (src_text, tgt_lang, trans) in enumerate(reversed(st.session_state.history[-5:])):
        st.write(f"{i+1}. **{tgt_lang}**: {trans}")
