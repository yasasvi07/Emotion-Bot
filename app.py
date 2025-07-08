import streamlit as st
import plotly.graph_objects as go
import pandas as pd
import plotly.express as px
from chatbot import EmotionAwareChatbot
from emotion_detector import EmotionDetector
import streamlit.components.v1 as components

st.set_page_config(page_title="Emotion Bot", layout="wide")

# -------------------- UTILITY FUNCTIONS --------------------

# Update the title color in the CSS styles
st.markdown("""
    <style>
        .main-title {
            background-color: #00AEEF;
            color: #000000;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0 1rem 2rem 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            justify-content: center;
        }
    </style>
""", unsafe_allow_html=True)

# Update the emotion mappings in create_emotion_donut function
def create_emotion_donut(emotion_counts):
    """Create a donut chart for emotions"""
    if not emotion_counts:
        return None
    
    labels = list(emotion_counts.keys())
    values = list(emotion_counts.values())
    
    # Updated color mapping for emotions using blue shades
    colors = {
        'joy': '#FFA726',#FFD54F ',  #0066CC',      # Bright blue
        'sadness': '#003366',#64B5F6',  # Dark blue
        'anger': '#E53935',#3399FF',    # Light blue
        'fear': '#6A0DAD',#455A64',     #000080',     # Navy blue
        'surprise': 'FF7043',#4169E1', # Royal blue
        'neutral': 'B0BEC5',#87CEEB'   # Sky blue
    }
    
    fig = go.Figure(data=[go.Pie(
        labels=labels,
        values=values,
        hole=.6,
        marker_colors=[colors.get(emotion.lower(), '#ADD8E6') for emotion in labels],
        textinfo='label+percent'
    )])
    
    fig.update_layout(
        showlegend=True,
        margin=dict(t=0, b=0, l=0, r=0),
        annotations=[dict(text=f"{sum(values)}", x=0.5, y=0.5, font_size=24, showarrow=False)]
    )
    return fig

def plot_emotion_history():
    """Create a line plot of emotion history"""
    if "emotions" not in st.session_state:
        st.session_state.emotions = []
        
    if len(st.session_state.emotions) > 0:
        df = pd.DataFrame(st.session_state.emotions)
        fig = px.line(df, x='timestamp', y='emotion', title='Emotion History')
        st.plotly_chart(fig, use_container_width=True)
    else:
        st.write("No emotion history available yet.")

# -------------------- CSS STYLES --------------------
# In the CSS section
st.markdown("""
    <style>
        .user-message, .assistant-message {
            padding: 1rem;
            border-radius: 20px;
            max-width: 80%;
            margin-bottom: 0.5rem;
        }
        .user-message {
            background-color: #B0E0E6; /*#DCF8C6;*/
            align-self: flex-end;
            margin-left: auto;
        }
        .assistant-message {
            background-color: #E5E5EA;
            align-self: flex-start;
            margin-right: auto;
        }
        .st-emotion-chart {
            text-align: center;
        }
        .main-title {
            background-color: #00AEEF;
            color: #000000;
            padding: 1.5rem;
            border-radius: 12px;
            margin: 0 1rem 2rem 1rem;
            display: flex;
            align-items: center;
            gap: 1rem;
            justify-content: center;
        }
        .content-wrapper {
            display: flex;
            gap: 2rem;
            padding: 0 1rem;
            position: relative;  /* Added for absolute positioning of divider */
        }
        .content-wrapper::after {
            content: '';
            position: absolute;
            left: 66%;  /* Position divider between sections */
            top: 0;
            bottom: 0;
            width: 2px;
            background-color: #000000;  /* Black divider */
        }
        .chat-section {
            flex: 2;
            background: white;
            border-radius: 12px;
            margin-bottom: 1rem;
        }
        #chat-container {
            height: 100%;
            overflow-y: auto;
            padding: 1rem;
        }
        .emotion-section {
            flex: 1;
            background: white;
            padding: 1.5rem;
            border-radius: 12px;
            box-shadow: 0 2px 4px rgba(0,0,0,0.1);
        }
        [data-testid="stSidebar"] {
            background-color: #00AEEF;   /*#B0E0E6;   Changed to Powder Blue */
            padding: 1rem;
        }
        
        [data-testid="stSidebar"] > div:first-child {
            padding: 1rem;
            border-radius: 12px;
            background-color: #00AEEF; /* #E0FFFF;   Added Light Cyan background */
        }
    </style>
""", unsafe_allow_html=True)

# -------------------- HEADER --------------------
st.markdown("""
    <div class="main-title">
        <h1 style="margin:0; color: #000000;">🤖 AI powered Emotion Bot</h1>
    </div>
""", unsafe_allow_html=True)

# -------------------- SIDEBAR --------------------
with st.sidebar:
    st.header("⚙️ Settings")
    language = st.selectbox("🌍 Select Your Language", [
        "English", "Hindi : हिंदी", "Telugu : తెలుగు", "Tamil : தமிழ்", "Bengali : বাংলা", "Kannada : ಕನ್ನಡ",
        "Marathi : मराठी", "Gujarati : ગુજરાતી", "Malayalam : മലയാളം", "Punjabi : ਪੰਜਾਬੀ", "Urdu : اردو", "Odia : ଓଡ଼ିଆ", "Assamese : অসমীয়া", "Sanskrit : संस्कृतम्"
    ])
    input_method = st.radio("🎤 Input Method", ["Type", "Speak"])
    st.markdown("---")
    st.markdown("🕘 **Emotion History**")
    plot_emotion_history()

# -------------------- MAIN CONTENT --------------------
st.markdown('<div class="content-wrapper">', unsafe_allow_html=True)

col1, col2 = st.columns([2, 1], gap="large")

with col1:
    st.markdown('<div class="chat-section">', unsafe_allow_html=True)
    st.subheader("💬 Chat")
    
    # Add speech controls if speech input is selected
    if input_method == "Speak":
        # Get the language code from the selected language
        selected_lang = language.split(" : ")[0].lower()
        lang_codes = {
            'english': 'en-IN',  # Changed to Indian English
            'hindi': 'hi-IN',
            'telugu': 'te-IN',
            'tamil': 'ta-IN',
            'bengali': 'bn-IN',
            'kannada': 'kn-IN',
            'marathi': 'mr-IN',
            'gujarati': 'gu-IN',
            'malayalam': 'ml-IN',
            'punjabi': 'pa-IN',
            'urdu': 'ur-IN',
            'odia': 'or-IN',
            'assamese': 'as-IN',
            'sanskrit': 'sa-IN'
        }
        speech_lang_code = lang_codes.get(selected_lang, 'en-IN')

        col_rec1, col_rec2 = st.columns(2)
        with col_rec1:
            if st.button("🎤 Start Recording"):
                st.session_state.recording = True
                st.session_state.speech_text = ""
                
        with col_rec2:
            if st.button("⏹️ Stop Recording"):
                if 'recording' in st.session_state and st.session_state.recording:
                    st.session_state.recording = False
                    try:
                        import speech_recognition as sr
                        recognizer = sr.Recognizer()
                        with sr.Microphone() as source:
                            st.info("🎤 Adjusting for ambient noise... Please wait.")
                            recognizer.adjust_for_ambient_noise(source, duration=1)
                            st.info(f"🎤 Listening... Speak in {language.split(' : ')[0]}!")
                            try:
                                audio = recognizer.listen(source, timeout=5, phrase_time_limit=10)
                                st.info("Processing speech...")
                                speech_text = recognizer.recognize_google(audio, language=speech_lang_code)
                                
                                if speech_text:
                                    st.success(f"Recognized text: {speech_text}")
                                    st.session_state.messages.append({"role": "user", "content": speech_text})
                                    
                                    with st.spinner("Getting response..."):
                                        # First translate to English for emotion detection
                                        translated_text = st.session_state.chatbot.translate_to_english(speech_text, selected_lang)
                                        
                                        # Detect emotion from translated text
                                        emotion_data = st.session_state.chatbot.emotion_detector.detect_emotion(translated_text)
                                        
                                        # Get response in selected language
                                        response = st.session_state.chatbot.generate_response(speech_text, selected_lang)
                                        
                                        # Store emotion data
                                        emotion = emotion_data.get("emotion", "neutral")
                                        intensity = emotion_data.get("intensity", 0.5)
                                        st.session_state.emotions.append({
                                            "timestamp": len(st.session_state.emotions),
                                            "emotion": emotion,
                                            "intensity": intensity
                                        })
                                        
                                        st.session_state.messages.append({"role": "assistant", "content": response})
                                    st.rerun()
                            except sr.WaitTimeoutError:
                                st.error("No speech detected within timeout period")
                            except sr.UnknownValueError:
                                st.error("Could not understand the audio")
                            except sr.RequestError as e:
                                st.error(f"Could not request results; {str(e)}")
                    except Exception as e:
                        st.error(f"Error initializing microphone: {str(e)}")
                        st.info("Please check if your microphone is properly connected and accessible")

        if 'recording' in st.session_state and st.session_state.recording:
            st.info("🎤 Recording active... Click Stop when finished speaking")

    chat_history = st.container()

    if "messages" not in st.session_state:
        st.session_state.messages = []
    if "emotions" not in st.session_state:
        st.session_state.emotions = []

    # Display chat history
    for msg in st.session_state.messages:
        role = msg["role"]
        content = msg["content"]
        class_name = "user-message" if role == "user" else "assistant-message"
        chat_history.markdown(f'<div class="{class_name}">{content}</div>', unsafe_allow_html=True)

    prompt = st.chat_input("🎤 Share your thoughts...", key="chat_input")

    if 'chatbot' not in st.session_state:
        st.session_state.chatbot = EmotionAwareChatbot()

    if prompt:
        st.session_state.messages.append({"role": "user", "content": prompt})

        with st.spinner("Analyzing..."):
            selected_lang = language.split(" : ")[0].lower()
            
            # First translate the input to English for emotion detection
            translated_text = st.session_state.chatbot.translate_to_english(prompt, selected_lang)
            
            # Detect emotion from translated text
            emotion_data = st.session_state.chatbot.emotion_detector.detect_emotion(translated_text)
            
            # Get response in selected language
            response = st.session_state.chatbot.generate_response(prompt, selected_lang)
            
            # Store emotion
            emotion = emotion_data.get("emotion", "neutral")
            intensity = emotion_data.get("intensity", 0.5)
            st.session_state.emotions.append({
                "timestamp": len(st.session_state.emotions),
                "emotion": emotion,
                "intensity": intensity
            })
            
            st.session_state.messages.append({"role": "assistant", "content": response})

        st.rerun()

with col2:
    st.markdown('<div class="emotion-section">', unsafe_allow_html=True)
    st.subheader("🎭 Emotional Summary")

    if st.session_state.emotions:
        emotion_counts = {}
        # Emoji mapping for emotions
        emotion_emojis = {
            'joy': '😊',
            'sadness': '😢',
            'anger': '😠',
            'fear': '😨',
            'surprise': '😲',
            'neutral': '😐'
        }

        for e in st.session_state.emotions:
            emotion = e['emotion']
            emotion_counts[emotion] = emotion_counts.get(emotion, 0) + 1

        fig = create_emotion_donut(emotion_counts)
        st.plotly_chart(fig, use_container_width=True)

        for emotion, count in emotion_counts.items():
            percentage = round((count / sum(emotion_counts.values())) * 100)
            emoji = emotion_emojis.get(emotion.lower(), '🤔')
            st.markdown(f"""
                <div class="emotion-item">
                    <span>{emoji} {emotion}</span>
                    <span>{percentage}%</span>
                </div>
            """, unsafe_allow_html=True)
    else:
        st.write("Start chatting to see your emotional summary! 💭")
