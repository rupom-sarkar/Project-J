from flask import Flask, request, jsonify, send_from_directory
from flask_cors import CORS

from core.jarvis import Jarvis
from voice.speaker import Speaker
from voice.voice_loop import VoiceLoop

import threading


app = Flask(__name__, static_folder="frontend")
CORS(app)

jarvis = Jarvis()
speaker = Speaker()
voice_loop = VoiceLoop(jarvis, speaker)


@app.route("/")
def home():
    return send_from_directory("frontend", "index.html")


@app.route("/<path:filename>")
def frontend_files(filename):
    return send_from_directory("frontend", filename)


@app.route("/api/command", methods=["POST"])
def command():

    data = request.get_json()

    if not data or "command" not in data:
        return jsonify({
            "success": False,
            "error": "No command received."
        }), 400

    user_command = data["command"].strip()

    if not user_command:
        return jsonify({
            "success": False,
            "error": "Empty command."
        }), 400

    print(f"COMMAND RECEIVED: {user_command}")

    response = jarvis.respond(user_command)

    print(f"RESPONSE GENERATED: {response}")

    if response:
        speaker.speak(response)

    return jsonify({
        "success": True,
        "command": user_command,
        "response": response
    })


if __name__ == "__main__":

    print()
    print("========================================")
    print("        PROJECT-J // JARVIS")
    print("========================================")
    print("JARVIS backend starting...")
    print("Interface: http://127.0.0.1:5000")
    print("Voice system: ACTIVE")
    print("========================================")
    print()

    voice_thread = threading.Thread(
        target=voice_loop.run,
        daemon=True
    )

    voice_thread.start()

    app.run(
        host="127.0.0.1",
        port=5000,
        debug=False
    )