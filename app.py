import streamlit as st
import speech_recognition as sr
from gtts import gTTS
from langchain_core.messages import HumanMessage, AIMessage
from agent import agent_app
import os

# 1. Setup Page
st.set_page_config(page_title="Telugu Sarkari Agent", page_icon="🏛️")
st.title("🏛️ ప్రభుత్వ పథకాల సహాయకుడు (Government Scheme Agent)")

# 2. Helper Functions for Voice
def record_audio():
    r = sr.Recognizer()
    
    # --- FIXED SETTINGS FOR LONGER LISTENING ---
    r.pause_threshold = 1.5   # Wait 1.5s of silence before stopping (prevents cutting off)
    r.energy_threshold = 300  # Better sensitivity for quiet rooms
    # -------------------------------------------

    with sr.Microphone() as source:
        st.info("🎤 Listening... (You have 10 seconds to speak)")
        
        # Quick adjustment for background noise
        r.adjust_for_ambient_noise(source, duration=0.5)
        
        try:
            # Listen for up to 10 seconds, and allow 10-second phrases
            audio = r.listen(source, timeout=10, phrase_time_limit=10)
            
            # Recognize Telugu
            text = r.recognize_google(audio, language="te-IN")
            return text
            
        except sr.WaitTimeoutError:
            return None # No speech detected
        except sr.UnknownValueError:
            return None # Detected sound but couldn't understand words
        except sr.RequestError:
            return "API_ERROR"

def text_to_speech(text):
    # 'te' is the language code for Telugu
    tts = gTTS(text=text, lang="te")
    # Save over the same file to avoid clutter
    filename = "response.mp3"
    if os.path.exists(filename):
        os.remove(filename)
    tts.save(filename)
    return filename

def clean_response_text(content):
    """
    Cleans the specific list format returned by Gemini/LangChain
    Example input: [{'type': 'text', 'text': 'Hello'}] -> Output: 'Hello'
    """
    if isinstance(content, list):
        full_text = ""
        for item in content:
            if isinstance(item, dict) and 'text' in item:
                full_text += item['text'] + " "
        return full_text.strip()
    return str(content)

# 3. Initialize Chat History
if "messages" not in st.session_state:
    st.session_state["messages"] = []

# 4. Display History
for msg in st.session_state["messages"]:
    if isinstance(msg, HumanMessage):
        with st.chat_message("user"):
            st.write(msg.content)
    elif isinstance(msg, AIMessage):
        with st.chat_message("assistant"):
            # Clean the text before showing
            clean_text = clean_response_text(msg.content)
            st.write(clean_text)

# 5. The "Speak" Button
if st.button("🎤 మాట్లాడండి (Tap to Speak)"):
    # --- Step A: Listen ---
    user_text = record_audio()
    
    if user_text and user_text != "API_ERROR":
        # Show User Input
        st.chat_message("user").write(user_text)
        st.session_state["messages"].append(HumanMessage(content=user_text))
        
        # --- Step B: Think (Agent) ---
        with st.spinner("ఆలోచిస్తున్నాను... (Thinking...)"):
            # Run the LangGraph Agent
            # We pass the full history so the agent remembers previous details
            result = agent_app.invoke({"messages": st.session_state["messages"]})
            
            # Get latest message
            agent_msg = result["messages"][-1]
            agent_text_raw = agent_msg.content
            
            # Clean it for display and speech
            agent_text_clean = clean_response_text(agent_text_raw)
            
            # Save to history
            # IMPORTANT: We save the raw message to keep the state valid, 
            # but we display the clean version.
            st.session_state["messages"] = result["messages"]

        # --- Step C: Speak (TTS) ---
        st.chat_message("assistant").write(agent_text_clean)
        
        audio_file = text_to_speech(agent_text_clean)
        st.audio(audio_file, format="audio/mp3", autoplay=True)

    elif user_text == "API_ERROR":
        st.error("Internet connection error. Please check your connection.")
    else:
        st.warning("క్షమించండి, నాకు వినిపించలేదు (Sorry, I couldn't hear you). Please try again.")