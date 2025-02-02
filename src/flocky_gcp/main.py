from flask import Flask, Request, jsonify

app = Flask(__name__)

def hello_world(request: Request):
    """HTTP Cloud Function that returns a response from utils and handlers."""
    return jsonify({
        "message": "Hello, World",
    })

@app.route("/", methods=["GET"])
def local_hello_world():
    return hello_world(request=None)

if __name__ == "__main__":
    app.run(host="0.0.0.0", port=8080, debug=True)
