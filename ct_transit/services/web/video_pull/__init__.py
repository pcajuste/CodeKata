from flask import Flask, jsonify

app = Flask(__name__)

@app.route("/")
def ct_transit():
    return jsonify("Hello CT Transit")
