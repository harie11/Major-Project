import requests

# Set OpenRouter API Key
API_KEY = "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"  
API_URL = "https://openrouter.ai/api/v1/chat/completions"

conversation_history = []  # Initialize an empty chat history

def get_chatbot_personality(facial_emotion, text_sentiment):
    mood_prompts = {
        "happy": "You are an enthusiastic and friendly therapist. Keep the conversation light and engaging.",
        "sad": "You are a caring and supportive therapist. Speak gently and provide emotional support.",
        "angry": "You are a patient and understanding therapist. Respond calmly and help the user cool down.",
        "neutral": "You are a conversational therapist. Engage naturally and listen attentively.",
        "surprise": "You are an attentive therapist. Acknowledge their surprise and keep the chat engaging.",
        "fear": "You are a reassuring therapist. Speak softly and help the user feel safe."
    }

    sentiment_prompts = {
        "LABEL_0": "You are a compassionate therapist who listens with empathy and understanding.", #Negative
        "LABEL_1": "You are a friendly, encouraging therapist who celebrates progress.",            #positive
        "LABEL_2": "You are a thoughtful therapist providing guidance."                             #Neutral
    }

    # Combine facial and text emotion prompts
    return f"{mood_prompts.get(facial_emotion, 'Be a friendly and engaging therapist.')}" \
           f" {sentiment_prompts.get(text_sentiment, '')}"

def chatbot(prompt, sentiment,facial_emotion):
    global conversation_history  

    system_prompt = get_chatbot_personality(facial_emotion, sentiment)

    # If it's a new conversation, add the system prompt
    if not conversation_history:
        conversation_history.append({"role": "system", "content": system_prompt})

    # Add the user's message to history
    conversation_history.append({"role": "user", "content": prompt})

    # Keep the last 10 messages
    MAX_HISTORY = 10
    conversation_history = conversation_history[-MAX_HISTORY:]

    headers = {
        "Authorization": f"Bearer {API_KEY}",
        "Content-Type": "application/json"
    }

    data = {
        "model": "mistralai/mistral-nemo:free",
        "messages": conversation_history  # Use the chat history
    }

    response = requests.post(API_URL, headers=headers, json=data)

    if response.status_code == 200:
        ai_response = response.json()["choices"][0]["message"]["content"]
        
        # Remove '**' formatting
        clean_response = ai_response.replace("**", "   ")
        
        # Add AI response to history
        conversation_history.append({"role": "assistant", "content": clean_response})

        return clean_response
    else:
        return f"Error: {response.json()}"