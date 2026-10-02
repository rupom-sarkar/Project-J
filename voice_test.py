from voice.listener import Listener


def main():
    listener = Listener()

    text = listener.listen()

    print(f"Recognized: {text}")


if __name__ == "__main__":
    main()
