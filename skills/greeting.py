def handle(command):

    if "hello" in command or "hi" in command or "hey" in command:
        return "Hello, sir. How can I help you?"

    if "how are you" in command or "how r u" in command:
        return "I'm functioning perfectly, sir."

    if "who are you" in command:
        return "I am JARVIS, your personal AI assistant."

    if "what are you" in command:
        return "I am JARVIS, your personal AI assistant."

    if "thank you" in command or "thanks" in command:
        return "You're welcome, sir."

    return None