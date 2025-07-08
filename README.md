# Emotion-Aware Chatbot

An advanced conversational agent that detects and responds to user emotions using state-of-the-art AI models.

## Features

- Text-based emotion detection using BERT
- Dynamic response generation
- Emotional memory system
- Adaptive conversation flow

## Setup

1. Create a virtual environment:
```bash
python -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

2. Install dependencies:
```bash
pip install -r requirements.txt
```

3. Run the chatbot:
```bash
python main.py
```

## Project Structure

- `main.py`: Main entry point of the application
- `emotion_detector.py`: Emotion detection module using BERT
- `chatbot.py`: Core chatbot logic and response generation
- `memory.py`: Emotional memory system
- `utils.py`: Utility functions and helpers

## Usage

The chatbot can be interacted with through a simple command-line interface. It will detect emotions in your messages and respond accordingly while maintaining context from previous interactions. 