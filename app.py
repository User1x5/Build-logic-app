from flask import Flask, request

app = Flask(__name__)

@app.route("/", methods=["GET"])
def home():
    return "RobloxBridge is online!"

@app.route("/logic", methods=["GET", "POST"])
def logic():

    if request.method == "POST":
        data = request.get_json(silent=True)

        if not isinstance(data, dict):
            return "0", 400

        value = data.get("value")

        print("Roblox sent:", value) 
        # Return 42 as an 8-bit response
        return jsonify({"value": "00101010"})  

    return jsonify({"value": "00101010"})
  
