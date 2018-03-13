from flask import Flask, render_template

app = Flask(__name__)

@app.route('/')
def settings():
    return render_template('settings.html')

app.run(port=5000, debug=True)