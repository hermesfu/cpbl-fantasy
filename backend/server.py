from flask import Flask
from dotenv import load_dotenv
import os

load_dotenv()
msg = os.getenv("MESSAGE")

app = Flask(__name__)

@app.route('/')
def home():
    return msg

if __name__ == '__main__':
    app.run(debug=True)