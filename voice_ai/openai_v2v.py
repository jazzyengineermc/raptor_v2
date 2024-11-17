import speech_recognition as sr
import pyttsx3

# Initialize the recognizer and TTS engine
recognizer = sr.Recognizer()
tts_engine = pyttsx3.init()

# OpenAI API key (replace with your actual API key)
openai_api_key = 'your-openai-api-key'

# Set up the OpenAI client
import openai
openai.api_key = openai_api_key

def recognize_speech_from_microphone():
    with sr.Microphone() as source:
        recognizer.adjust_for_ambient_noise(source)
        print("Listening for 'Raptor'...")
        
        while True:
            audio = recognizer.listen(source)
            try:
                text = recognizer.recognize_google(audio, language="en-US")
                if "raptor" in text.lower():
                    print("Detected wake word: Raptor")
                    return text
                elif "bye" in text.lower() or "goodbye" in text.lower():
                    print("User is saying goodbye. Exiting...")
                    exit(0)
            except sr.UnknownValueError:
                continue

def generate_response(prompt):
    response = openai.Completion.create(
        engine="text-davinci-003",
        prompt=prompt,
        max_tokens=150,
        n=1,
        stop=None,
        temperature=0.7
    )
    return response.choices[0].text.strip()

def text_to_speech(text, voice_id):
    voices = tts_engine.getProperty('voices')
    if voice_id < len(voices):
        tts_engine.setProperty('voice', voices[voice_id].id)
    else:
        print(f"Voice ID {voice_id} not available. Using default voice.")
    
    tts_engine.say(text)
    tts_engine.runAndWait()

if __name__ == "__main__":
    # Set the MBROLA voice ID (e.g., 1 for mbrola_us1, 2 for mbrola_us2, etc.)
    mbrola_voice_id = 0

    while True:
        # Recognize speech with the wake word "Raptor"
        recognized_text = recognize_speech_from_microphone()
        
        if recognized_text:
            # Remove the wake word and any leading/trailing whitespace
            prompt = recognized_text.replace("raptor", "").strip()
            
            # Generate a response using OpenAI API
            response_text = generate_response(prompt)
            
            # Convert the response text to speech with the specified MBROLA voice
            text_to_speech(response_text, mbrola_voice_id)
