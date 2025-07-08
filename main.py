from chatbot import EmotionAwareChatbot
import sys

def print_welcome():
    print("\n=== Emotion-Aware Chatbot ===")
    print("I'm here to chat and understand your emotions!")
    print("Type 'quit' to exit, 'summary' to see your emotional summary")
    print("===========================\n")

def main():
    chatbot = EmotionAwareChatbot()
    print_welcome()
    
    while True:
        try:
            user_input = input("You: ").strip()
            
            if user_input.lower() == 'quit':
                print("\nGoodbye! Take care!")
                break
            elif user_input.lower() == 'summary':
                summary = chatbot.get_emotional_summary()
                print("\nEmotional Summary:")
                print(f"Current Mood: {summary['current_mood']}")
                print(f"Emotional Trend: {summary['emotional_trend']}")
                print(f"Recent Moods: {', '.join(summary['recent_moods'])}")
                print()
                continue
            
            if not user_input:
                continue
            
            response = chatbot.generate_response(user_input)
            print(f"Bot: {response}\n")
            
        except KeyboardInterrupt:
            print("\nGoodbye! Take care!")
            break
        except Exception as e:
            print(f"\nI encountered an error: {str(e)}")
            print("Please try again or type 'quit' to exit.\n")

if __name__ == "__main__":
    main() 