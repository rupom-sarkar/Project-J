import subprocess


class AppController:

    def open_application(self, app_name):

        app_name = app_name.lower().strip()

        if "chrome" in app_name:
            subprocess.run(
                ["powershell", "-Command", "Start-Process 'chrome.exe'"]
            )
            return "Opening Google Chrome, Sir."

        elif "notepad" in app_name:
            subprocess.run(
                ["powershell", "-Command", "Start-Process 'notepad.exe'"]
            )
            return "Opening Notepad, Sir."

        elif "calculator" in app_name or "calc" in app_name:
            subprocess.run(
                ["powershell", "-Command", "Start-Process 'calc.exe'"]
            )
            return "Opening Calculator, Sir."

        elif "vs code" in app_name or "visual studio code" in app_name:
            subprocess.run(
                ["powershell", "-Command", "Start-Process 'code.exe'"]
            )
            return "Opening Visual Studio Code, Sir."

        else:
            return f"I don't know how to open {app_name} yet, Sir."