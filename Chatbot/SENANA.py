import tensorflow as tf
from transformers import TFAutoModelForSequenceClassification, AutoTokenizer

model_name = "nlptown/bert-base-multilingual-uncased-sentiment"
tokenizer = AutoTokenizer.from_pretrained(model_name)
model = TFAutoModelForSequenceClassification.from_pretrained(model_name)

PS = "neutral"

def analyze_sentiment(text):
    try:
        # Tokenize input text
        inputs = tokenizer(text, return_tensors="tf", padding=True, truncation=True, max_length=128)

        # Get model predictions
        outputs = model(inputs)[0]
        predicted_class = tf.argmax(outputs, axis=1).numpy()[0]

        # Map predicted class to sentiment label
        sentiments = {0: 'VERY NEGATIVE', 1: 'NEGATIVE', 2: 'NEUTRAL', 3: 'POSITIVE', 4: 'VERY POSITIVE'}
        predicted_sentiment = sentiments[predicted_class]
        global PS
        PS = predicted_sentiment
        print(f"Preddicted Sentiment in Text : {PS}")
        return predicted_sentiment
    except Exception as e:
        # Handle exceptions gracefully
        print("An error occurred:", e)
        return None