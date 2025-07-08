import matplotlib.pyplot as plt
import numpy as np

# Emotion classification accuracy data
emotions = ['Joy', 'Sadness', 'Anger', 'Fear', 'Surprise', 'Love']
accuracies = [0.92, 0.88, 0.87, 0.85, 0.84, 0.83]  # Based on DistilRoBERTa model performance

# Create bar plot
plt.figure(figsize=(10, 6))
bars = plt.bar(emotions, accuracies, color=['#FFD700', '#4169E1', '#DC143C', '#800080', '#FF8C00', '#FF69B4'])

# Customize the plot
plt.title('Emotion Classification Accuracy', fontsize=14, pad=20)
plt.xlabel('Emotions', fontsize=12)
plt.ylabel('Accuracy Score', fontsize=12)
plt.grid(True, axis='y', linestyle='--', alpha=0.7)
plt.ylim(0.75, 1.0)  # Set y-axis range for better visualization

# Add value labels on top of each bar
for bar in bars:
    height = bar.get_height()
    plt.text(bar.get_x() + bar.get_width()/2., height,
             f'{height:.2f}',
             ha='center', va='bottom')

# Rotate x-axis labels for better readability
plt.xticks(rotation=45)

# Add a brief description
plt.figtext(0.02, 0.02, 'Based on DistilRoBERTa model performance', 
            fontsize=8, style='italic')

# Adjust layout
plt.tight_layout()

# Save the plot
plt.savefig('c:\\Users\\S Mudumba\\Desktop\\mini-2\\emotion_accuracy.png', dpi=300, bbox_inches='tight')
plt.close()