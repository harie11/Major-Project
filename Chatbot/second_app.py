from flask import Flask, render_template, request, jsonify # type: ignore 
from SENANA import analyze_sentiment
import SENANA

from Tbot0 import chatbot

from collections import Counter

import RC
import FER

import threading

count = 0

chat_history_ids = None

bot = True # True for therapist , False for random chater
inti = 0


app = Flask(__name__)

@app.route("/")
def index():
    return render_template('main.html')

@app.route('/get_greeting', methods=['GET'])
def get_greeting():
    
    return "Hello, I'm a chatbot! How can I assist you today?"

@app.route('/toggle', methods=['POST'])
def toggle():
    global bot
    bot = not bot
    return f"Bot state is now {'Therapist' if bot else 'Random Chat'}"


@app.route("/get", methods=["GET", "POST"])
def chat():
    msg = request.form["msg"]
    input = msg
    return get_Chat_response(input)


@app.route('/get_fer', methods=['GET'])
def get_fer():
    if(FER.emolist):
        data = Counter(FER.emolist).most_common(1)[0][0]
    else:
        data = "Neutral"
    return str(data)


@app.route("/get_senti", methods=["GET", "POST"])
def senti():
    msg = request.form["msg"]
    input = msg
    return analyze_sentiment(input)

def get_Chat_response(text):
    global chat_history_ids
    global count
    EMO = "neutral"
    
    print(FER.emolist)
    if(len(FER.emolist) >=3):
        EMO = Counter(FER.emolist).most_common(1)[0][0]
        print("Current emotion : ",EMO)
        
    
    if text.strip() == "":
        # If the user input is empty, then the chatbot sends a greeting message
        response = "Hello! How can I assist you today?"      
        
    if(EMO == "sad" and count < 2):
        count += 1
        response = "I see you are feeling down based on your facial expressions 😞.I can provide help and advice in Therapist mode. I'm sad to see you like this 🥺, i hope you cheer up soon"
    
    if(EMO == "Happy" and count < 2):
        count += 1
        response = "I see you are happy based on your facial expressions 😊.I hope you continue being happy.If you need any advice ask me in Therapist mode i'll be Happy to be of help 😌"
        
        
        # pretty print last ouput tokens from bot
    if(bot and (count != 1)):
        response = chatbot(text,SENANA.PS,EMO)
    else:
        response, chat_history_ids = RC.chater(text, chat_history_ids)
    count += 1
        
    return response 

def start_background_thread():
    thread = threading.Thread(target=FER.run_every_5_seconds)
    thread.daemon = True  # Daemon thread will exit when the main process exits
    thread.start()

if __name__ == '__main__':
    start_background_thread()
    app.run()
