from core.jarvis import Jarvis


def test_multi_turn_conversation():

    jarvis = Jarvis()

    # Turn 1
    response = jarvis.respond(
        "I'm learning Python"
    )

    assert response is not None

    assert (
        jarvis.context.get_conversation_topic()
        == "python"
    )

    assert (
        jarvis.context.get_last_conversational_statement()
        == "i'm learning python"
    )

    assert (
        jarvis.context.get_conversation_turns()
        == 1
    )

    # Turn 2
    response = jarvis.respond(
        "Tell me more"
    )

    assert response is not None

    assert (
        jarvis.context.get_conversation_topic()
        == "python"
    )

    assert (
        jarvis.context.get_last_conversational_statement()
        == "tell me more"
    )

    assert (
        jarvis.context.get_conversation_turns()
        == 2
    )

    # Turn 3
    response = jarvis.respond(
        "Explain it"
    )

    assert response is not None

    assert (
        jarvis.context.get_conversation_topic()
        == "python"
    )

    assert (
        jarvis.context.get_last_conversational_statement()
        == "explain it"
    )

    assert (
        jarvis.context.get_conversation_turns()
        == 3
    )


if __name__ == "__main__":

    test_multi_turn_conversation()

    print(
        "PASS: Multi-turn conversation "
        "context works correctly."
    )