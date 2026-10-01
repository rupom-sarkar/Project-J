from voice.listener import Listener
from voice.speaker import Speaker


class VoiceLoop:

    def __init__(self, jarvis, speaker=None):
        self.jarvis = jarvis
        self.listener = Listener()
        self.speaker = speaker or Speaker()
        self.running = True

    def run(self):
        print("JARVIS voice system ready. Listening...")

        while self.running:

            command = self.listener.listen()

            if not command:
                continue

            print(f"VOICE COMMAND: {command}")

            response = self.jarvis.respond(command)

            if response:
                self.speaker.speak(response)

            if command.lower().strip() in [
                "exit",
                "quit",
                "shutdown jarvis",
                "stop listening"
            ]:
                self.running = False

        print("JARVIS voice system stopped.")