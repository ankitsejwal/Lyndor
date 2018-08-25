from flask import Flask, request, jsonify, render_template
import time, json

app = Flask(__name__)

@app.route('/')
def home():
    ''' render settings page'''
    return render_template('settings.html', timestamp = time.time())

@app.route('/update', methods=['POST'])
def update():
    ''' update settings.json '''
    data = request.get_json()
    settings_file = open("./static/js/settings.json", "w")
    json.dump(data, settings_file, indent=4)
    return home()

app.run(port=5000, debug=True)