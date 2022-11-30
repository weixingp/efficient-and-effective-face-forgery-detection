from flask import Flask, render_template

app = Flask(__name__)


@app.get("/")
def home_page():
    return render_template('index.html')
