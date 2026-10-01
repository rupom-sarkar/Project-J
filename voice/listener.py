import speech_recognition as sr


class Listener:
    def __init__(self):
        self.recognizer = sr.Recognizer()
        self.microphone = sr.Microphone()

    def listen(self):
        try:
            with self.microphone as source:
                print("Listening...")
                self.recognizer.adjust_for_ambient_noise(
                    source,
                    duration=0.5
                )

                audio = self.recognizer.listen(source)

            # Microphone is now CLOSED before recognition/speaking

            try:
                text = self.recognizer.recognize_google(audio)
                print(f"You: {text}")
                return text

            except sr.UnknownValueError:
                print("JARVIS: Sorry, sir. I didn't understand that.")
                return ""

            except sr.RequestError:
                print("JARVIS: Speech recognition service is unavailable.")
                return ""

        except Exception as e:
            print(f"JARVIS: Microphone error: {e}")
            return ""