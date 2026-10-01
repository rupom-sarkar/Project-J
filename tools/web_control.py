import webbrowser


class WebController:

    def open_website(self, website):

        website = website.lower().strip()

        if "youtube" in website:
            webbrowser.open("https://www.youtube.com")
            return "Opening YouTube, Sir."

        elif "google" in website:
            webbrowser.open("https://www.google.com")
            return "Opening Google, Sir."

        elif "facebook" in website:
            webbrowser.open("https://www.facebook.com")
            return "Opening Facebook, Sir."

        else:
            return f"I don't know how to open {website} yet, Sir."

