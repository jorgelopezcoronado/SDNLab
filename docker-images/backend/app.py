from flask import Flask, jsonify
from flask_cors import CORS
import random, json

app = Flask(__name__)
CORS(app)

class Greeting:
    def __init__(self, msg, language):
        self.msg = msg
        self.language = language

greetings = [
    Greeting("Hello, World!", "English"),
    Greeting("Bonjour le monde!", "French"),
    Greeting("Hola, mundo!", "Spanish"),
    Greeting("Hallo Welt!", "German"),
    Greeting("Прывітанне Сусвет!", "Belarussian"),
    Greeting("你好世界！", "Chinese" ),
    Greeting("Ciao mondo!", "Italian" ),
    Greeting("Hej världen!", "Swedish"),
    Greeting("Chào thế giới!", "Vietnamese"),
    Greeting("Ahoj světe!", "Czech")
]

@app.route('/')
def index():
    greeting = random.choice(greetings)
    return json.dumps(greeting.__dict__, ensure_ascii=False)

if __name__ == "__main__":
    app.run(host="0.0.0.0")

