import pandas as pd
from transformers import pipeline
import warnings
import os

# Hides annoying terminal warnings
warnings.filterwarnings('ignore') 

print("1. Waking up the AI... (Downloading the model might take a minute the first time!)")
sentiment_model = pipeline("sentiment-analysis", model="distilbert-base-uncased-finetuned-sst-2-english")

print("2. Reading the sliced Yelp dataset...")
# Now we read the small CSV you created!
df = pd.read_csv('data/yelp_small.csv')

# The specific categories we want the AI to hunt for
aspect_keywords = {
    "Product": ["coffee", "food", "drink", "taste", "menu", "latte", "cake", "delicious"],
    "Ambiance": ["vibe", "quiet", "noisy", "music", "seat", "atmosphere", "crowd", "chill"],
    "Service": ["staff", "waiter", "friendly", "slow", "wait", "service", "rude"],
    "Utility": ["wifi", "plug", "socket", "internet", "power", "study"]
}

results = []

print("3. Analyzing reviews... Let the AI do its thing.")
for index, row in df.iterrows():
    review_text = str(row['Review']).lower()
    
    found_aspects = []
    for aspect, keywords in aspect_keywords.items():
        if any(keyword in review_text for keyword in keywords):
            found_aspects.append(aspect)
    
    if found_aspects:
        ai_result = sentiment_model(review_text[:512])[0] 
        results.append({
            "Review": row['Review'],
            "Aspects_Mentioned": ", ".join(found_aspects),
            "Sentiment": ai_result['label'],
            "AI_Confidence": round(ai_result['score'], 2)
        })

analyzed_df = pd.DataFrame(results)

print("\n--- AI Analysis Complete ---")
print(f"Found {len(analyzed_df)} reviews that specifically matched our aspects.")

os.makedirs('data', exist_ok=True)
analyzed_df.to_csv('data/yelp_analyzed.csv', index=False)
print("Saved the final results to data/yelp_analyzed.csv!")