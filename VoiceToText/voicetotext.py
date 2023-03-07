import speech_recognition as speech_recog
from googletrans import Translator
import pyttsx3
import openai
import os
import importlib

initialized = 0

def setup():
    global voice_engine
    global english_voice_id
    global tamil_voice_id
    global translator
    global sr
    global initialized

    if (initialized == 0):
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
        translator  = Translator()

        #-----------------------------------------------------------
        # Initialize the speech recognizer (mic)
        #-----------------------------------------------------------
        sr = speech_recog.Recognizer()

        initialized = 1

#-----------------------------------------------------------
# Get the speaker output (in Tamil)
#-----------------------------------------------------------
def get_tamil_voice(): 
    # Open the microphone and start recording
    with speech_recog.Microphone() as source:
        print("Speak something...")
        audio = sr.listen(source)

    # Use Google Speech Recognition to transcribe the audio
    try:
        # Recognize audio as Tamil
        text = sr.recognize_google(audio, language="ta-IN")
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

    # This statement to import pyttsx3 is a hack. For some reason
    # the code gets hung on runAndWait after a few times. The hack is based 
    # on https://github.com/nateshmbhat/pyttsx3/issues/126
    importlib.reload(pyttsx3)
    voice_engine = pyttsx3.init()
    voice_engine.setProperty('voice', english_voice_id)
    voice_engine.setProperty('rate', 150)

    # send translation to speaker
    voice_engine.say(text)
    voice_engine.runAndWait()
    
#-----------------------------------------------------------
# Send Tamil text to speaker
#-----------------------------------------------------------
def say_tamil_text(text):
    # This statement to import pyttsx3 is a hack. For some reason
    # the code gets hung on runAndWait after a few times. The hack is based 
    # on https://github.com/nateshmbhat/pyttsx3/issues/126
    importlib.reload(pyttsx3)
    voice_engine = pyttsx3.init()

    voice_engine.setProperty('voice', tamil_voice_id)
    voice_engine.setProperty('rate', 150)

    # send translation to speaker
    voice_engine.say(text)
    voice_engine.runAndWait()


def runChat():
    setup()

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

# while (True):
#  runChat()