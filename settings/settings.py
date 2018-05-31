from flask import Flask, render_template
import time, json

app = Flask(__name__)

@app.route('/')
def home():
    return render_template('settings.html', timestamp = time.time())

@app.route('/test')
def test():
    with open('./settings/settings.json', 'r') as data:
        data = json.load(data)
        return data['preferences']
app.run(port=5000, debug=True)                                     