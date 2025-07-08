from transformers import pipeline
import random
from emotion_detector import EmotionDetector
from memory import EmotionalMemory
from utils import SpeechHandler
from googletrans import Translator

class EmotionAwareChatbot:
    def __init__(self):
        self.translator = Translator()
        self.emotion_detector = EmotionDetector()
        self.memory = EmotionalMemory()
        self.speech_handler = SpeechHandler()
        try:
            self.conversation_pipeline = pipeline(
                "text2text-generation",
                model="google/flan-t5-large",
                device=-1
            )
        except Exception as e:
            print(f"Error initializing conversation pipeline: {str(e)}")
            self.conversation_pipeline = None

    def translate_to_english(self, text, source_lang):
        if source_lang == 'english':
            return text
            
        try:
            lang_codes = {
                'hindi': 'hi',
                'telugu': 'te',
                'tamil': 'ta',
                'bengali': 'bn',
                'kannada': 'kn',
                'marathi': 'mr',
                'gujarati': 'gu',
                'malayalam': 'ml',
                'punjabi': 'pa',
                'urdu': 'ur',
                'odia': 'or',
                'assamese': 'as',
                'sanskrit': 'sa'
            }
            
            source_code = lang_codes.get(source_lang, 'en')
            translation = self.translator.translate(text, src=source_code, dest='en')
            return translation.text
        except Exception as e:
            print(f"Translation error: {e}")
            return text

    def generate_response(self, user_input, target_lang='en'):
        try:
            # First translate input to English if needed
            english_input = self.translate_to_english(user_input, target_lang)
            
            # Detect emotion in English text
            emotion_data = self.emotion_detector.detect_emotion(english_input)
            emotional_summary = self.memory.get_emotional_summary()
            
            # Generate base response in English
            base_response = self._generate_base_response(emotion_data, emotional_summary)
            follow_up = self._generate_follow_up(emotion_data, english_input)
            final_response = self._add_contextual_elements(base_response, follow_up, emotional_summary)
            
            # Translate response to target language if not English
            if target_lang != 'english':
                try:
                    lang_codes = {
                        'hindi': 'hi',
                        'telugu': 'te',
                        'tamil': 'ta',
                        'bengali': 'bn',
                        'kannada': 'kn',
                        'marathi': 'mr',
                        'gujarati': 'gu',
                        'malayalam': 'ml',
                        'punjabi': 'pa',
                        'urdu': 'ur',
                        'odia': 'or',
                        'assamese': 'as',
                        'sanskrit': 'sa'
                    }
                    target_code = lang_codes.get(target_lang, 'en')
                    final_response = self.translator.translate(final_response, src='en', dest=target_code).text
                except Exception as e:
                    print(f"Translation error: {e}")
            
            # Store interaction in memory
            self.memory.add_interaction(user_input, emotion_data, final_response)
            
            return final_response
            
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            return "I apologize, but I'm having trouble processing that right now. Could you please try again?"

    def _generate_base_response(self, emotion_data, emotional_summary):
        try:
            emotion = emotion_data['emotion']
            intensity = emotion_data['intensity']
            
            context = (
                f"Given a user feeling {emotion} with {intensity} intensity, "
                "generate an empathetic and helpful response that addresses their emotional state. "
                "The response should be natural, supportive, and engaging, similar to how a "
                "professional counselor would respond. Include specific observations about "
                "their emotional state and offer appropriate support or guidance."
            )
            
            response = self.conversation_pipeline(
                context,
                max_length=200,
                min_length=50,
                num_beams=5,
                no_repeat_ngram_size=2,
                early_stopping=True
            )[0]['generated_text']
            
            return response
            
        except Exception as e:
            print(f"Error in response generation: {str(e)}")
            return "I understand how you're feeling. Would you like to tell me more?"

    def _generate_follow_up(self, emotion_data, user_input):
        try:
            context = (
                f"Based on the message: '{user_input}' and emotion: {emotion_data['emotion']}, "
                "generate a thoughtful follow-up question that encourages deeper discussion "
                "and shows understanding of their emotional state. The question should be "
                "open-ended and empathetic."
            )
            
            follow_up = self.conversation_pipeline(
                context,
                max_length=100,
                min_length=20,
                num_beams=3,
                no_repeat_ngram_size=2
            )[0]['generated_text']
            
            return follow_up
            
        except Exception as e:
            print(f"Error generating follow-up: {str(e)}")
            return "Can you tell me more about that?"
    
    def _add_contextual_elements(self, base_response, follow_up, emotional_summary):
        """Add contextual elements to the response based on emotional history"""
        response = base_response + " " + follow_up
        
        if emotional_summary['emotional_trend'] == 'changing':
            response += " I notice your mood has been changing lately. Would you like to talk about that?"
        elif emotional_summary['emotional_trend'] == 'stable':
            if len(emotional_summary['recent_moods']) > 1:
                response += f" You've been feeling {emotional_summary['current_mood']} consistently. Is there anything specific on your mind?"
        
        return response
    
    def get_emotional_summary(self):
        """Get a summary of the current emotional state"""
        return self.memory.get_emotional_summary()
    
    def speak_response(self, text, language='en'):
        """Convert response to speech"""
        self.speech_handler.text_to_speech(text, language)