import speech_recognition as sr
import pyttsx3
from googletrans import Translator
import streamlit as st
import tempfile
import os
import sounddevice as sd
import soundfile as sf
import numpy as np
import wave
import tempfile

class SpeechHandler:
    def __init__(self):
        self.recorder = None
        self.audio_file = None
        self.sample_rate = 44100
        self.recognizer = sr.Recognizer()
        self.recording_data = []
        self.translator = Translator()
        
    def start_recording(self):
        """Start recording audio"""
        # Create a temporary file for recording
        temp_file = tempfile.NamedTemporaryFile(delete=False, suffix='.wav')
        self.audio_file = temp_file.name
        self.recording_data = []
        
        def callback(indata, frames, time, status):
            if status:
                print(status)
            self.recording_data.append(indata.copy())
            
        # Start recording
        self.recorder = sd.InputStream(
            samplerate=self.sample_rate,
            channels=1,
            callback=callback
        )
        self.recorder.start()
        return self.audio_file
    
    def stop_recording(self):
        """Stop recording and save the audio file"""
        if self.recorder is None:
            return None
            
        # Stop recording
        self.recorder.stop()
        self.recorder.close()
        self.recorder = None
        
        # Combine all recorded chunks
        if len(self.recording_data) > 0:
            recording = np.concatenate(self.recording_data, axis=0)
            
            # Save the recording
            with wave.open(self.audio_file, 'wb') as wf:
                wf.setnchannels(1)
                wf.setsampwidth(2)
                wf.setframerate(self.sample_rate)
                wf.writeframes((recording * 32767).astype(np.int16).tobytes())
            
            return self.audio_file
        return None
    
    def speech_to_text(self, audio_file):
        """Convert speech to text"""
        try:
            with sr.AudioFile(audio_file) as source:
                audio = self.recognizer.record(source)
                text = self.recognizer.recognize_google(audio)
                return text
        except Exception as e:
            print(f"Error in speech recognition: {e}")
            return None
        
    def text_to_speech(self, text, language='en'):
        """Convert text to speech"""
        try:
            # Translate text if needed
            if language != 'en':
                translated = self.translator.translate(text, dest=language)
                text = translated.text
            
            # Generate speech
            self.engine.say(text)
            self.engine.runAndWait()
        except Exception as e:
            st.error(f"Error in text-to-speech: {str(e)}")
    
    def translate_text(self, text, target_lang='en'):
        """Translate text to target language"""
        try:
            translated = self.translator.translate(text, dest=target_lang)
            return translated.text
        except Exception as e:
            st.error(f"Error in translation: {str(e)}")
            return text
    
    def detect_language(self, text):
        """Detect the language of the text"""
        try:
            detected = self.translator.detect(text)
            return detected.lang
        except Exception as e:
            st.error(f"Error in language detection: {str(e)}")
            return 'en'