import os, ast, sys
from openai import OpenAI
import speech_recognition as sr
import pyttsx3
from Espeak import *

# Initialize the recognizer and TTS engine
# recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()
tts_engine.setProperty("rate", 180)

voice = vmbrit
es = Espeak()
es.talk(voice, speech='Greetings and salutations')

uid = "jreide"
# Author vietjovi@gmail.com
# Replace with the actual port where your LM Studio server is running
base_url = "http://raptor-ai:1234/v1" 

client = OpenAI(base_url=base_url, api_key="lm-studio")

def openAIRequest(question = "", userId = ""):
    response = client.chat.completions.create(
        model="qwen2.5-coder-7b-instruct",
        messages = [
            # {"role": "system", "content": "Assistant is a large language model trained by OpenAI."},
            {"role": "system", "content": "You are a helpful AI assistant.  KEEP RESPONCESES VERY SHORT AND CONVERSATIONAL"},
            {"role": "user", "content": question},
        ],
        user = userId
    )
    
    # print(response)
    return response.choices[0].message.content

def openAIRequestWithPastMessages(pastMsg = [], question = "", userId = ""):
    msg = [{'role': 'system', 'content': 'You are a helpful AI assistant.  KEEP RESPONCESES VERY SHORT AND CONVERSATIONAL'}]
    # print(type(pastMsg))
    # print(pastMsg)
    for m in pastMsg:
        msg.append(m)
    msg.append({'role': 'user', 'content': question})
    # print(msg)

    try:
        response = client.chat.completions.create(
        model="qwen2.5-coder-7b-instruct",
        messages = msg,
        user = userId
    )
        
        # print(response)
        answer = response.choices[0].message.content
    except Exception as e:
        answer = "Sorry, I can not answer your question. Please try again."
        print(e)
    
    pastMsg.append({'role': 'user', 'content': question})
    pastMsg.append({'role': 'assistant', 'content': answer})
    # print(pastMsg)
    savePastMessages(userId, pastMsg)

    return answer

def loadPastMessages(uid):
    pastMessages = []
    dataPath = "/home/jreide/chatbot/jreide"
    if os.path.exists(dataPath):
        try:
            with open(dataPath, "r") as f:
                pastMessages = f.read()
        except:
            pastMessages = []
            return pastMessages
    else:
        return pastMessages

    if pastMessages is None:
        pastMessages = []
        return pastMessages
    return ast.literal_eval(pastMessages)

def savePastMessages(uid, msg):
    dataPath = "/home/jreide/chatbot/jreide"
    #Clean first message
    if len(msg) > int(20):
        msg = msg[2:]

    try:
        with open(dataPath, "w") as f:
            pastMessages = f.write(str(msg))
        return True
    except Exception as e:
        return False

def text_to_speech(text2):
    es.talk(voice, speech=text2)

def main():
    userInput = ''
    userId = "user_123"
    print("Enter 'bye' or 'exit' to quit")
    while ((userInput.lower() != 'exit') and (userInput.lower() != 'bye')):
        userInput = input("You: ")
        if ((userInput.lower() == 'exit') or (userInput.lower() == 'bye')):
            text2 = "Goodbye. See you later."
            text_to_speech(text2)
            sys.exit(0)
        # print(userInput)
        # print("OpenAI-Bot: " + openAIRequestWithPastMessages(loadPastMessages(userId), userInput, userId))
        text2 = openAIRequestWithPastMessages(loadPastMessages(userId), userInput, userId)
        text_to_speech(text2)
    # print('Goodbye. See you!')
    text2 = "Goodbye. See you!"
    text_to_speech(text2)
    return True

if __name__ == "__main__":
    main()