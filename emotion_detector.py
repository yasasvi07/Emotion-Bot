from transformers import pipeline
import torch

class EmotionDetector:
    def __init__(self):
        try:
            # Initialize the emotion classification pipeline
            self.emotion_classifier = pipeline(
                "text-classification",
                model="j-hartmann/emotion-english-distilroberta-base",
                return_all_scores=True,
                device=-1  # Use CPU instead of GPU
            )
        except Exception as e:
            print(f"Error initializing emotion classifier: {str(e)}")
            print("Falling back to default emotion detection...")
            self.emotion_classifier = None
        
        # Define emotion categories
        self.emotions = [
            'happy', 'sad', 'anger', 'fear', 'surprise', 'love'
        ]
        
        # Define emotion intensity thresholds
        self.intensity_thresholds = {
            'high': 0.7,
            'medium': 0.4,
            'low': 0.2
        }
    
    def detect_emotion(self, text):
        """
        Detect emotions in the given text
        Returns: dict with emotion and intensity
        """
        try:
            if self.emotion_classifier is None:
                # Fallback to simple emotion detection
                return self._fallback_emotion_detection(text)
            
            # Get emotion predictions
            results = self.emotion_classifier(text)[0]
            
            # Find the dominant emotion
            dominant_emotion = max(results, key=lambda x: x['score'])
            
            # Calculate intensity
            intensity = self._calculate_intensity(dominant_emotion['score'])
            
            return {
                'emotion': dominant_emotion['label'],
                'intensity': intensity,
                'confidence': dominant_emotion['score']
            }
        except Exception as e:
            print(f"Error in emotion detection: {str(e)}")
            return self._fallback_emotion_detection(text)
    
    def _fallback_emotion_detection(self, text):
        """Simple fallback emotion detection"""
        text = text.lower()
        if any(word in text for word in ['happy', 'joy', 'great', 'wonderful', 'excited']):
            return {'emotion': 'joy', 'intensity': 'medium', 'confidence': 0.5}
        elif any(word in text for word in ['sad', 'depressed', 'unhappy', 'down']):
            return {'emotion': 'sadness', 'intensity': 'medium', 'confidence': 0.5}
        elif any(word in text for word in ['angry', 'mad', 'frustrated', 'upset']):
            return {'emotion': 'anger', 'intensity': 'medium', 'confidence': 0.5}
        elif any(word in text for word in ['afraid', 'scared', 'fear', 'worried']):
            return {'emotion': 'fear', 'intensity': 'medium', 'confidence': 0.5}
        elif any(word in text for word in ['surprised', 'shocked', 'amazed']):
            return {'emotion': 'surprise', 'intensity': 'medium', 'confidence': 0.5}
        elif any(word in text for word in ['love', 'loved', 'loving']):
            return {'emotion': 'love', 'intensity': 'medium', 'confidence': 0.5}
        else:
            return {'emotion': 'joy', 'intensity': 'low', 'confidence': 0.3}
    
    def _calculate_intensity(self, score):
        """Calculate emotion intensity based on confidence score"""
        if score >= self.intensity_thresholds['high']:
            return 'high'
        elif score >= self.intensity_thresholds['medium']:
            return 'medium'
        else:
            return 'low'
    
    def get_emotion_context(self, text):
        """
        Get detailed emotion context including secondary emotions
        Returns: dict with primary and secondary emotions
        """
        try:
            if self.emotion_classifier is None:
                # Fallback to simple emotion detection
                primary = self._fallback_emotion_detection(text)
                return {
                    'primary_emotion': primary['emotion'],
                    'secondary_emotions': [
                        {'emotion': 'joy', 'score': 0.3},
                        {'emotion': 'surprise', 'score': 0.2}
                    ]
                }
            
            results = self.emotion_classifier(text)[0]
            
            # Sort emotions by score
            sorted_emotions = sorted(results, key=lambda x: x['score'], reverse=True)
            
            return {
                'primary_emotion': sorted_emotions[0]['label'],
                'secondary_emotions': [
                    {'emotion': e['label'], 'score': e['score']}
                    for e in sorted_emotions[1:3]
                ]
            }
        except Exception as e:
            print(f"Error in getting emotion context: {str(e)}")
            return self._fallback_emotion_detection(text) 