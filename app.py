import streamlit as st
from deep_translator import GoogleTranslator, exceptions
from io import BytesIO

# Optional: gTTS (Text-to-Speech) safe import
try:
    from gtts import gTTS
    tts_enabled = True
except ModuleNotFoundError:
    tts_enabled = False
    st.warning("Text-to-Speech not available. Install gTTS to enable audio feature.")

# Page config
st.set_page_config(page_title="🌐 SpeakEasy", layout="wide", page_icon="🌐")

# Custom Fonts and Styling
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');
html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
}
.stButton>button {
    background-color: #4CAF50;
    color: white;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border-radius: 10px;
    margin-top: 5px;
}
.stTextArea textarea { font-size: 16px; height: 120px; }
.stTextInput input { font-size: 16px; height: 40px; }
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

# Session state for history
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar for settings
with st.sidebar:
    st.header("⚙️ Settings")
    source_lang = st.selectbox("Source language", ["auto"] + language_options, index=0)
    target_lang = st.selectbox("Target language", language_options, index=1)
    multi_targets = st.multiselect("Translate into multiple languages:", language_options, default=[target_lang])
    if st.button("🔄 Swap Languages"):
        source_lang, target_lang = target_lang, source_lang
        st.experimental_rerun()

# User input
text = st.text_area("Enter text to translate:")

# Main translation button
if st.button("Translate") and text:
    src_code = "auto" if source_lang == "auto" else language_codes[source_lang]

    st.header("📝 Translation Results")
    for tgt_lang in multi_targets:
        try:
            tgt_code = language_codes[tgt_lang]

            # Translate
            translation = GoogleTranslator(source=src_code, target=tgt_code).translate(text)

            # Display translation in modern card
            st.markdown(f"""
                <div style="
                    background-color:#FFFFFF;
                    color:#000000;
                    padding:20px;
                    border-radius:12px;
                    box-shadow: 0 4px 6px rgba(0,0,0,0.1);
                    margin-top:10px;
                ">
                <h4>{tgt_lang}:</h4>
                <p style="font-size:18px">{translation}</p>
                </div>
            """, unsafe_allow_html=True)

            # Save history
            st.session_state.history.append((text, tgt_lang, translation))

            # Text-to-Speech
            if tts_enabled:
                tts = gTTS(translation, lang=tgt_code)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format="audio/mp3")

            # Download translation
            st.download_button(f"📥 Download {tgt_lang} Translation", translation, file_name=f"translation_{tgt_lang}.txt")

        except exceptions.NotValidPayload as e:
            st.error(f"Invalid text: {e}")
        except exceptions.LanguageNotSupportedException as e:
            st.error(f"Unsupported language: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# Recent translations in expandable panel
if st.session_state.history:
    with st.expander("📜 Recent Translations"):
        for i, (src_text, tgt_lang, trans) in enumerate(reversed(st.session_state.history[-5:])):
            st.write(f"{i+1}. **{tgt_lang}**: {trans}")
