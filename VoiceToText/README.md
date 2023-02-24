# ChatGPT
My first project trying to learn a bit about ChatGPT while dabbling more with Python. This is an application that takes 
* A Tamil sentence as input via a Mic
* Converts it to English
* Sends the English text to OpenAI API
* Gets the response
* Translates the response back into Tamil. 
* Sends the Tamil response to the speaker

# Things to improve
* Error Handling, including translating the error in Tamil (if possible)
* Creating a single "Engine" for the speaker

# Setup
This code was tested on Windows using Python 3.11.2. Python libraries I need (with the command line)
* pip install SpeechRecognition
* python.exe -m pip install --upgrade pip
* pip install pipwin
* pipwin install pyaudio
* pip install googletrans==4.0.0-rc1

I had to setup my laptop to support Tamil on my laptop:
* First add the language following instructions from this link - https://support.microsoft.com/en-us/windows/download-language-pack-for-speech-24d06ef3-ca09-ddcc-70a0-63606fd16394. This will add the registry keys under HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens. 
* However, Python seems to look for the audio language entries under HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens. Do the following:
  * Export the language registry settings from Computer\HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech_OneCore\Voices\Tokens to a folder
  * Go to the folder where the registry entry was exported, open the registry data using Notepad and modify "Speech_OneCore" to "Speech' in two places
  * Save the file and double click on it. This will add the registry entry for the language under \HKEY_LOCAL_MACHINE\SOFTWARE\Microsoft\Speech\Voices\Tokens
  * This link has more detail steps to do the above: https://puneet166.medium.com/how-to-added-more-speakers-and-voices-in-pyttsx3-offline-text-to-speech-812c83d14c13

