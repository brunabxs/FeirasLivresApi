from flask import Flask
from src import greeting

app = Flask(__name__)

@app.route('/')
def hello():
    return greeting.hello()

if __name__ == '__main__':
    app.run()