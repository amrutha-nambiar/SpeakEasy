import streamlit as st
from deep_translator import GoogleTranslator, exceptions
from io import BytesIO

# Optional: gTTS (Text-to-Speech)
try:
    from gtts import gTTS
    tts_enabled = True
except ModuleNotFoundError:
    tts_enabled = False
    st.warning("Text-to-Speech not available. Install gTTS to enable audio feature.")

# Page config
st.set_page_config(page_title="🌐 SpeakEasy", layout="wide", page_icon="🌐")

# Elegant Styling with Gradient Header
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Roboto:wght@400;500;700&display=swap');

html, body, [class*="css"]  {
    font-family: 'Roboto', sans-serif;
}

.stButton>button {
    background-color: #008080;
    color: white;
    height: 3em;
    width: 100%;
    font-size: 16px;
    border-radius: 10px;
    margin-top: 5px;
}

.stTextArea textarea { font-size: 16px; height: 120px; }
.stTextInput input { font-size: 16px; height: 40px; }

.header-container {
    background: linear-gradient(90deg, #008080, #20B2AA);
    padding: 25px;
    border-radius: 12px;
    color: white;
    display: flex;
    align-items: center;
    margin-bottom: 20px;
}

.header-container img {
    width: 50px;
    height: 50px;
    margin-right: 15px;
}

.header-container h1 {
    margin: 0;
    font-size: 36px;
}

.header-container p {
    margin: 0;
    font-size: 18px;
    opacity: 0.9;
}
</style>
""", unsafe_allow_html=True)

# Header with logo and gradient
st.markdown("""
<div class="header-container">
    <img src="https://img.icons8.com/ios-filled/100/ffffff/globe.png" alt="Logo">
    <div>
        <h1>🌐 SpeakEasy</h1>
        <p>Translate text between languages instantly!</p>
    </div>
</div>
""", unsafe_allow_html=True)

# Sidebar info box
st.markdown("""
<div style="
    background-color:#E0F7FA;
    color:#006064;
    padding:15px;
    border-radius:10px;
    font-size:16px;
    font-weight:500;
    display:flex;
    align-items:center;
    margin-bottom: 20px;
">
<div style="margin-right:10px; font-size:20px;">⬅️</div>
<div>Use the <strong>left sidebar</strong> to select source/target languages, multi-language options, or swap languages.</div>
</div>
""", unsafe_allow_html=True)

# Supported languages
language_codes = {
    "English": "en", "Hindi": "hi", "French": "fr", "Spanish": "es",
    "German": "de", "Chinese (Simplified)": "zh-CN", "Chinese (Traditional)": "zh-TW",
    "Japanese": "ja", "Korean": "ko", "Russian": "ru", "Arabic": "ar",
    "Portuguese": "pt", "Italian": "it", "Turkish": "tr", "Dutch": "nl",
    "Swedish": "sv", "Norwegian": "no", "Danish": "da", "Finnish": "fi",
    "Polish": "pl", "Thai": "th", "Vietnamese": "vi", "Indonesian": "id",
    "Greek": "el", "Hebrew": "he", "Bengali": "bn", "Urdu": "ur",
    "Malay": "ms", "Filipino": "tl"
}
language_options = list(language_codes.keys())

# Session state
if "history" not in st.session_state:
    st.session_state.history = []

# Sidebar settings
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

# Translation button
if st.button("Translate") and text:
    src_code = "auto" if source_lang == "auto" else language_codes[source_lang]
    st.header("📝 Translation Results")

    for tgt_lang in multi_targets:
        try:
            tgt_code = language_codes[tgt_lang]
            translation = GoogleTranslator(source=src_code, target=tgt_code).translate(text)

            # Elegant card
            st.markdown(f"""
                <div style="
                    background-color:#F9F9F9;
                    color:#333333;
                    padding:20px;
                    border-radius:12px;
                    box-shadow: 0 4px 10px rgba(0,0,0,0.08);
                    margin-top:10px;
                ">
                <h4>{tgt_lang}:</h4>
                <p style="font-size:18px">{translation}</p>
                </div>
            """, unsafe_allow_html=True)

            st.session_state.history.append((text, tgt_lang, translation))

            if tts_enabled:
                tts = gTTS(translation, lang=tgt_code)
                audio_bytes = BytesIO()
                tts.write_to_fp(audio_bytes)
                audio_bytes.seek(0)
                st.audio(audio_bytes, format="audio/mp3")

            st.download_button(f"📥 Download {tgt_lang} Translation", translation, file_name=f"translation_{tgt_lang}.txt")

        except exceptions.NotValidPayload as e:
            st.error(f"Invalid text: {e}")
        except exceptions.LanguageNotSupportedException as e:
            st.error(f"Unsupported language: {e}")
        except Exception as e:
            st.error(f"Error: {e}")

# Recent translations
if st.session_state.history:
    with st.expander("📜 Recent Translations"):
        for i, (src_text, tgt_lang, trans) in enumerate(reversed(st.session_state.history[-5:])):
            st.write(f"{i+1}. **{tgt_lang}**: {trans}")
