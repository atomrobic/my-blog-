import speech_recognition as sr
from transformers import pipeline
from pvporcupine import Porcupine
import pyttsx3
import struct
import os
import torch

# Create a tensor
tensor = torch.tensor([1, 2, 3])
print(tensor)
# Initialize text-to-speech engine
engine = pyttsx3.init()

# Wake word detection setup (Porcupine)
ACCESS_KEY = "YOUR_PICOVoice_ACCESS_KEY"  # Get this from Picovoice Console
WAKE_WORD = "computer"  # Replace with your chosen wake word
PORCUPINE_MODEL_PATH = Porcupine.MODEL_PATH
PORCUPINE_KEYWORD_PATHS = [Porcupine.KEYWORD_PATHS[WAKE_WORD]]
PORCUPINE_SENSITIVITY = 0.5

def speak(text):
    """Convert text to speech."""
    print(f"🤖: {text}")
    engine.say(text)
    engine.runAndWait()

def listen():
    """Capture voice input and convert it to text."""
    recognizer = sr.Recognizer()
    with sr.Microphone() as source:
        print("🎤 Listening...")
        recognizer.adjust_for_ambient_noise(source)
        audio = recognizer.listen(source)

    try:
        text = recognizer.recognize_google(audio)
        print(f"📝 You said: {text}")
        return text
    except sr.UnknownValueError:
        print("❌ Could not understand the audio.")
        return None
    except sr.RequestError:
        print("❌ Could not request results, check internet connection.")
        return None

def get_chatbot_response(prompt):
    """Generate a response using a local NLP model."""
    generator = pipeline('text-generation', model='gpt2')
    response = generator(prompt, max_length=50)
    return response[0]['generated_text']

def detect_wake_word():
    """Detect wake word using Porcupine."""
    porcupine = Porcupine(
        access_key=ACCESS_KEY,
        keyword_paths=PORCUPINE_KEYWORD_PATHS,
        sensitivities=[PORCUPINE_SENSITIVITY]
    )
    pa = None
    audio_stream = None

    try:
        import pyaudio
        pa = pyaudio.PyAudio()
        audio_stream = pa.open(
            rate=porcupine.sample_rate,
            channels=1,
            format=pyaudio.paInt16,
            input=True,
            frames_per_buffer=porcupine.frame_length
        )

        print(f"👂 Listening for wake word: '{WAKE_WORD}'")
        while True:
            pcm = audio_stream.read(porcupine.frame_length)
            pcm = struct.unpack_from("h" * porcupine.frame_length, pcm)
            keyword_index = porcupine.process(pcm)
            if keyword_index >= 0:
                print(f"👋 Wake word '{WAKE_WORD}' detected!")
                break
    finally:
        if audio_stream is not None:
            audio_stream.close()
        if pa is not None:
            pa.terminate()
        porcupine.delete()

if __name__ == "__main__":
    speak("Hello! I am your fully automatic AI assistant. Say the wake word to activate me.")

    while True:
        # Step 1: Detect wake word
        detect_wake_word()

        # Step 2: Listen for user input
        user_input = listen()
        if user_input:
            if "exit" in user_input.lower() or "quit" in user_input.lower():
                speak("Goodbye!")
                break

            # Step 3: Generate chatbot response
            response = get_chatbot_response(user_input)
            speak(response)