from voicetotext import runChat
from flask import Flask, render_template, request

app = Flask(__name__)

@app.route('/')
def index():
    print("In / route!")
    return render_template('index.html')

@app.route('/click', methods=['POST'])
def click():
    # print("Button clicked!")
    runChat()

    return "Success"

if __name__ == '__main__':
    app.run(debug=True)

