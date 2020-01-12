from flask import Flask, jsonify

app = Flask(__name__)
app.config.from_object("video_pull.config.Config")

@app.route("/")
def ct_transit():
    return jsonify("Hello CT Transit")
