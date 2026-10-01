import subprocess


class Speaker:

    def speak(self, text):
        print(f"JARVIS: {text}")

        safe_text = text.replace("'", "''")

        powershell_command = (
            "Add-Type -AssemblyName System.Speech; "
            "$speak = New-Object System.Speech.Synthesis.SpeechSynthesizer; "
            f"$speak.Speak('{safe_text}');"
        )

        subprocess.run(
            ["powershell", "-NoProfile", "-Command", powershell_command],
            capture_output=True,
            text=True
        )