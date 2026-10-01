from voice.listener import Listener


listener = Listener()

text = listener.listen()

print(f"Recognized: {text}")