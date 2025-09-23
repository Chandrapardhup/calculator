from flask import Flask, request, jsonify

app = Flask(__name__)

@app.route("/add")
def add():
    try:
        x = float(request.args.get("x", 0))
        y = float(request.args.get("y", 0))
        return jsonify({"result": x + y})
    except:
        return jsonify({"error": "Invalid input"})

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=5000)

