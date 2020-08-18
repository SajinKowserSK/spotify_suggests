import flask
from flask import Flask, render_template

app = Flask(__name__)

@app.route("/")
def my_index():
    return render_template("index.html", token="Hello Flask + React")

@app.route("/time")
def get_current_time():
    return {'time':10}




app.run(debug=True)