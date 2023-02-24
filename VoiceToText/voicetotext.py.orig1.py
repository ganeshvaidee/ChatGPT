import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import openai
import os

#-----------------------------------------------------------
#setup chatGPT
openai.api_key = "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" # os.environ["OPENAI_API_KEY"]
#-----------------------------------------------------------

# setup voice engine
engine = pyttsx3.init()

# set properties for the voice
voices = engine.getProperty('voices')
for voice in voices:
    print(voice.id)

engine.setProperty('voice', voices[0].id)  # you can change the index to select a different voice
engine.setProperty('rate', 150)  # you can adjust the speaking rate (words per minute)

# create a translator object
translator = Translator()

# Initialize the recognizer
r = sr.Recognizer()

# Open the microphone and start recording
with sr.Microphone() as source:
    print("Speak something...")
    audio = r.listen(source)

# Use Google Speech Recognition to transcribe the audio
try:
    # Recognize audio as Tamil
    text = r.recognize_google(audio, language="ta-IN")
    print("You said: ", text)

    # Translate to English
    result = translator.translate(text, src='ta', dest='en')
    # result = translator.translate(text, src='en', dest='ta')
    print("Translation: ", result.text)

    # send translation to speaker
    engine.say(result.text)
    engine.runAndWait()

    
    # Call the API to get a response
    # prompt = result.text
    response = openai.Completion.create(
        # engine="davinci",
        engine="text-davinci-003",
        prompt=result.text,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    # Print the response from the API
    print(response.choices[0].text.strip())

    # send response to speaker in Tamil
    result = translator.translate(response.choices[0].text.strip(), src='en', dest='ta')
    print(result)
    
    engine.setProperty('voice', voices[1].id)  # you can change the index to select a different voice
    engine.setProperty('rate', 150)  # you can adjust the speaking rate (words per minute)
    engine.say(result.text)
    engine.runAndWait()

except sr.UnknownValueError:
    print("Sorry, I could not understand your voice")
except sr.RequestError as e:
    print("Could not request results from Google Speech Recognition service; {0}".format(e))