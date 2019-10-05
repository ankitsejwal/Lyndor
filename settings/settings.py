#!/usr/bin/env python
# -*- coding: utf-8 -*-

''' Flask based web server to edit settings.json '''

from flask import Flask, request, jsonify, render_template
import time, json, os

app = Flask(__name__)

@app.route('/')
def home():
    ''' render settings page'''
    return render_template('settings.html', timestamp = time.time())

@app.route('/update', methods=['POST'])
def update():
    ''' update settings.json '''
    data = request.get_json()
    filename = os.path.join(app.static_folder, 'js/settings.json')
    settings_file = open(filename, "w")
    json.dump(data, settings_file, indent=4)
    return home()

if __name__ == "__main__":
    app.run(port=5005)