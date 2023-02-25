import speech_recognition as sr
from googletrans import Translator
import pyttsx3
import openai
import os

#-----------------------------------------------------------
#setup chatGPT
openai.api_key = os.environ["OPENAI_API_KEY"] 
#-----------------------------------------------------------

#-----------------------------------------------------------
# setup voice engine for speaker
#-----------------------------------------------------------
voice_engine = pyttsx3.init()
for voice in voice_engine.getProperty('voices'):
  if 'English' in voice.name:
    english_voice_id = voice.id
  elif 'Tamil' in voice.name:
    tamil_voice_id = voice.id
  
voice_engine.setProperty('rate', 150)

#-----------------------------------------------------------
# create a translator object
#-----------------------------------------------------------
translator = Translator()

#-----------------------------------------------------------
# Initialize the speech recognizer (mic)
#-----------------------------------------------------------
r = sr.Recognizer()

#-----------------------------------------------------------
# Get the speaker output (in Tamil)
#-----------------------------------------------------------
def get_tamil_voice(): 
    # Open the microphone and start recording
    with sr.Microphone() as source:
        print("Speak something...")
        audio = r.listen(source)

    # Use Google Speech Recognition to transcribe the audio
    try:
        # Recognize audio as Tamil
        text = r.recognize_google(audio, language="ta-IN")
        print("You said: ", text)

        return text
    except sr.UnknownValueError:
        print("Sorry, I could not understand your voice")
    except sr.RequestError as e:
        print("Could not request results from Google Speech Recognition service; {0}".format(e))

#-----------------------------------------------------------
# Convert Tamil text to English
#-----------------------------------------------------------
def convert_tamil_to_english(text):
    result = translator.translate(text, src='ta', dest='en')
    print("Translation: ", result.text)

    return result.text

#-----------------------------------------------------------
# Convert English text to Tamil
#-----------------------------------------------------------
def convert_english_to_tamil(text):
    result = translator.translate(text, src='en', dest='ta')
    print("Translation: ", result.text)

    return result.text

#-----------------------------------------------------------
# Send English text to OpenAI API. Need to play with engin type
#-----------------------------------------------------------
def send_english_text_to_opanai(text):
    # Call the API to get a response
    # prompt = result.text
    response = openai.Completion.create(
        # engine="davinci",
        engine="text-davinci-003",
        prompt=text,
        max_tokens=60,
        n=1,
        stop=None,
        temperature=0.5,
    )

    print(response.choices[0].text.strip())
    return response.choices[0].text.strip()

#-----------------------------------------------------------
# Send english text to speaker
#-----------------------------------------------------------
def say_english_text(text):
    voice_engine.setProperty('voice', english_voice_id)
    # send translation to speaker
    voice_engine.say(text)
    voice_engine.runAndWait()
    
#-----------------------------------------------------------
# Send Tamil text to speaker
#-----------------------------------------------------------
def say_tamil_text(text):
    voice_engine.setProperty('voice', tamil_voice_id)
    # send translation to speaker
    voice_engine.say(text)
    voice_engine.runAndWait()


#-----------------------------------------------------------
# Call sequence. 1. Get tamil voice. 2. Convert to English
# 3. Send english text to OpenAI. 4. Convert responce to Tamil
#-----------------------------------------------------------
tamil_input = get_tamil_voice() #1
say_tamil_text(tamil_input)
english_input = convert_tamil_to_english(tamil_input) #2
say_english_text(english_input)
english_output = send_english_text_to_opanai(english_input) #3
say_english_text(english_output)
tamil_output = convert_english_to_tamil(english_output) #4
say_tamil_text(tamil_output)