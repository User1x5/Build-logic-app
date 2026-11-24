from flask import Flask, request

app = Flask(__name__)

text = ""
index = 0



def encode(character):
    # Six-bit positions for normal characters
    symbols = {
        "-": "100101",
        "=": "100110",
        ".": "100111",
        ",": "101000",
        ";": "101001",
        "/": "101010",

        "à": "101011",
        "å": "101100",
        "ç": "101101",
        "è": "101110",
        "é": "101111",
        "ê": "110000",
        "î": "110001",
        "ï": "110010",
        "û": "110011",

        "|": "110100",
        "[": "110101",
        "]": "110110",
        '"': "110111"
    }

    # Shifted keyboard characters
    shifted = {
        "!": "1",
        "@": "2",
        "#": "3",
        "$": "4",
        "%": "5",
        "?": "6",
        "&": "7",
        "*": "8",
        "(": "9",
        ")": "0",
        "_": "-",
        "+": "=",
        "'": ",",
        ":": ";",
        "~": "/",
        "À": "à",
        "Å": "å",
        "Ç": "ç",
        "È": "è",
        "É": "é",
        "Ê": "ê",
        "Î": "î",
        "Ï": "ï",
        "Û": "û",
        "{": "[",
        "}": "]",
        "^": '"'
    }

    # Space
    if character == " ":
        return "10000000"

    # Letters
    if "a" <= character.lower() <= "z" and len(character) == 1:
        number = ord(character.lower()) - 96
        bits = format(number, "06b")
        shift = "1" if character.isupper() else "0"

        return "1" + shift + bits

    # Shifted symbols
    if character in shifted:
        base = shifted[character]
        return "11" + symbols.get(
            base,
            format(ord(base) - 48, "06b")
        )

    # Normal symbols
    if character in symbols:
        return "10" + symbols[character]

    # Unsupported character
    return "10000000"



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
    
