from flask import Flask, request, json
from flask_cors import CORS

app = Flask(__name__)
CORS(app)

@app.route('/')
def index():
    return "Welcome to RISC-V Assembler"

@app.route('/check-health')
def check_health():
    return "The server is running"

import assembler
import core
import diassembler
import Pipeline

if __name__ == "__main__":
    app.run()