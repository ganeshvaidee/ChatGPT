from voicetotext import runChat
from flask import Flask

app = Flask(__name__)

@app.route('/')

def hello_world():
  runChat()

if __name__ == '__main__':
  app.run()