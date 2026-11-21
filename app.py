from flask import Flask, request

app = Flask(__name__)

text = ""
index = 0


def encode(character):
    if character == " ":
        return "10000000"

    number = ord(character.upper()) - 64
    bits = format(number, "06b")
    shift = "1" if character.isupper() else "0"

    return "1" + shift + bits


@app.post("/r")
def receive():
    global text, index

    data = request.get_json()
    text = data["text"][:512]
    index = 0

    return {"status": "received"}


@app.get("/logic")
def send():
    global index

    if index >= len(text):
        return {"value": "00000000"}

    character = text[index]
    index += 1

    return {"value": encode(character)}


@app.get("/health")
def health():
    return {"ok": True}
    
