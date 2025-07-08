from collections import deque
import time
import speech_recognition as sr

class EmotionalMemory:
    def __init__(self, max_history=10):
        self.max_history = max_history
        self.conversation_history = deque(maxlen=max_history)
        self.emotional_context = {
            'current_mood': None,
            'mood_history': [],
            'emotional_trend': None
        }
        self.recognizer = sr.Recognizer()
    
    def get_speech_input(self, language='en-US'):
        """Get input from speech"""
        try:
            with sr.Microphone() as source:
                print("Listening...")
                audio = self.recognizer.listen(source, timeout=5)
                text = self.recognizer.recognize_google(audio, language=language)
                return text
        except sr.UnknownValueError:
            return "Could not understand audio"
        except sr.RequestError:
            return "Could not request results"
    
    def add_interaction(self, user_input, emotion_data, bot_response):
        """Add a new interaction to the memory"""
        interaction = {
            'timestamp': time.time(),
            'user_input': user_input,
            'emotion': emotion_data,
            'bot_response': bot_response
        }
        
        self.conversation_history.append(interaction)
        self._update_emotional_context(emotion_data)
    
    def _update_emotional_context(self, emotion_data):
        """Update the emotional context based on new emotion data"""
        self.emotional_context['current_mood'] = emotion_data['emotion']
        self.emotional_context['mood_history'].append(emotion_data['emotion'])
        
        # Keep only recent mood history
        if len(self.emotional_context['mood_history']) > self.max_history:
            self.emotional_context['mood_history'] = self.emotional_context['mood_history'][-self.max_history:]
        
        # Calculate emotional trend
        self._calculate_emotional_trend()
    
    def _calculate_emotional_trend(self):
        """Calculate the emotional trend based on recent history"""
        if len(self.emotional_context['mood_history']) < 2:
            self.emotional_context['emotional_trend'] = 'stable'
            return
        
        recent_moods = self.emotional_context['mood_history'][-3:]
        if all(mood == recent_moods[0] for mood in recent_moods):
            self.emotional_context['emotional_trend'] = 'stable'
        elif recent_moods[-1] == recent_moods[-2]:
            self.emotional_context['emotional_trend'] = 'stable'
        else:
            self.emotional_context['emotional_trend'] = 'changing'
    
    def get_recent_context(self, n=3):
        """Get the n most recent interactions"""
        return list(self.conversation_history)[-n:]
    
    def get_emotional_summary(self):
        """Get a summary of the current emotional state"""
        return {
            'current_mood': self.emotional_context['current_mood'],
            'emotional_trend': self.emotional_context['emotional_trend'],
            'recent_moods': self.emotional_context['mood_history'][-3:]
        }