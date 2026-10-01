from dataclasses import dataclass
from typing import Optional

from brain.intent import IntentRecognizer


@dataclass
class BrainRequest:
    """
    Structured representation of what the user wants.
    """
    intent: str
    action: str
    target: Optional[str] = None
    query: Optional[str] = None


class Brain:

    def __init__(self):
        self.name = "JARVIS Brain"
        self.intent_recognizer = IntentRecognizer()

    def process(self, user_input: str) -> BrainRequest:

        # ------------------------------------------
        # Understand the user's input
        # ------------------------------------------
        intent = self.intent_recognizer.recognize(user_input)

        # ------------------------------------------
        # Extract target
        # ------------------------------------------
        target = self.intent_recognizer.extract_target(
            user_input
        )

        # ------------------------------------------
        # Follow-up search
        # ------------------------------------------
        if intent == "follow_up_search":

            query = user_input.lower().strip()

            return BrainRequest(
                intent="information_request",
                action="follow_up_search",
                query=query
            )

        # ------------------------------------------
        # Conversation
        # ------------------------------------------
        if intent == "conversation":

            return BrainRequest(
                intent="conversation",
                action="greeting"
            )

        # ------------------------------------------
        # Open something
        # ------------------------------------------
        if intent == "open":

            return BrainRequest(
                intent="open_request",
                action="open",
                target=target
            )

        # ------------------------------------------
        # Google search
        # ------------------------------------------
        if intent == "google_search":

            query = user_input.lower().strip()

            query = query.replace(
                "search google for ",
                "",
                1
            )

            query = query.replace(
                "google search ",
                "",
                1
            )

            return BrainRequest(
                intent="information_request",
                action="google_search",
                query=query.strip()
            )

        # ------------------------------------------
        # YouTube search
        # ------------------------------------------
        if intent == "youtube_search":

            query = user_input.lower().strip()

            query = query.replace(
                "search youtube for ",
                "",
                1
            )

            query = query.replace(
                "youtube search ",
                "",
                1
            )

            return BrainRequest(
                intent="information_request",
                action="youtube_search",
                query=query.strip()
            )

        # ------------------------------------------
        # Memory save
        # ------------------------------------------
        if intent == "memory_save":

            content = user_input.lower().strip()

            content = content.replace(
                "remember that ",
                "",
                1
            )

            content = content.replace(
                "remember this ",
                "",
                1
            )

            content = content.replace(
                "don't forget that ",
                "",
                1
            )

            content = content.replace(
                "do not forget that ",
                "",
                1
            )

            return BrainRequest(
                intent="memory_request",
                action="memory_save",
                query=content.strip()
            )

        # ------------------------------------------
        # Memory query
        # ------------------------------------------
        if intent == "memory_query":

            return BrainRequest(
                intent="memory_request",
                action="memory_query"
            )

        # ------------------------------------------
        # Generic search
        # ------------------------------------------
        if intent == "search":

            query = user_input.lower().strip()

            query = query.replace(
                "search for ",
                "",
                1
            )

            query = query.replace(
                "search ",
                "",
                1
            )

            return BrainRequest(
                intent="information_request",
                action="search",
                query=query.strip()
            )

        # ------------------------------------------
        # Unknown
        # ------------------------------------------
        return BrainRequest(
            intent="unknown",
            action="unknown",
            target=user_input.lower().strip()
        )

