import re


class IntentRecognizer:

    def recognize(self, user_input: str) -> str:

        command = user_input.lower().strip()
        words = re.findall(r"\b\w+\b", command)

        # ------------------------------------------
        # Google search
        # ------------------------------------------
        if (
            "search google" in command
            or "google search" in command
        ):
            return "google_search"

        # ------------------------------------------
        # YouTube search
        # ------------------------------------------
        if (
            "search youtube" in command
            or "youtube search" in command
        ):
            return "youtube_search"

        # ------------------------------------------
        # Follow-up search
        # ------------------------------------------
        follow_up_search_phrases = [
            "beginner ones",
            "advanced ones",
            "more examples",
            "more like this",
            "similar ones",
            "another one",
            "another",
            "for beginners",
            "for advanced users",
            "more tutorials",
            "more videos"
        ]

        if any(
            phrase in command
            for phrase in follow_up_search_phrases
        ):
            return "follow_up_search"

        # ------------------------------------------
        # Remember / save memory
        # ------------------------------------------
        remember_phrases = [
            "remember that",
            "remember this",
            "don't forget that",
            "do not forget that"
        ]

        if any(
            phrase in command
            for phrase in remember_phrases
        ):
            return "memory_save"

        # ------------------------------------------
        # Memory questions
        # ------------------------------------------
        memory_phrases = [
            "what do you remember",
            "what do you know about me",
            "what is my preferred",
            "what do i prefer",
            "what do i like",
            "do you remember"
        ]

        if any(
            phrase in command
            for phrase in memory_phrases
        ):
            return "memory_query"

        # ------------------------------------------
        # Generic search
        # ------------------------------------------
        if (
            "search for" in command
            or command.startswith("search ")
        ):
            return "search"

        # ------------------------------------------
        # Open / launch / start
        # ------------------------------------------
        if any(
            word in words
            for word in ["open", "launch", "start"]
        ):
            return "open"

        # ------------------------------------------
        # Conversation
        # ------------------------------------------
        if any(
            word in words
            for word in ["hello", "hi", "hey"]
        ):
            return "conversation"

        # ------------------------------------------
        # Conversational statements
        # ------------------------------------------
        conversational_starts = [
            "i'm learning ",
            "i am learning ",
            "i like ",
            "i love ",
            "i enjoy ",
            "i'm studying ",
            "i am studying "
        ]

        if any(
            command.startswith(phrase)
            for phrase in conversational_starts
        ):
            return "conversation"

        # ------------------------------------------
        # General conversational follow-up
        # ------------------------------------------
        if self.is_conversational_follow_up(command):
            return "conversation"

        # ------------------------------------------
        # Unknown
        # ------------------------------------------
        return "unknown"

    def is_conversational_follow_up(self, command: str) -> bool:
        """
        Detect general conversational follow-ups
        without requiring exact sentences.
        """

        words = re.findall(
            r"\b\w+\b",
            command
        )

        # ------------------------------------------
        # Continuation signals
        # ------------------------------------------
        continuation_words = [
            "more",
            "further",
            "deeper",
            "continue",
            "elaborate",
            "expand"
        ]

        if any(
            word in words
            for word in continuation_words
        ):
            return True

        # ------------------------------------------
        # Explanation signals
        # ------------------------------------------
        explanation_patterns = [
            "explain",
            "how does",
            "how do",
            "why does",
            "why do",
            "why is",
            "why are"
        ]

        if any(
            pattern in command
            for pattern in explanation_patterns
        ):
            return True

        # ------------------------------------------
        # Reference to previous conversation
        # ------------------------------------------
        context_words = [
            "it",
            "this",
            "that",
            "they",
            "them"
        ]

        has_context_reference = any(
            word in words
            for word in context_words
        )

        # ------------------------------------------
        # Contextual questions
        # ------------------------------------------
        if has_context_reference:

            contextual_patterns = [
                "what about",
                "how about",
                "can you explain",
                "can you tell me",
                "tell me about"
            ]

            if any(
                command.startswith(pattern)
                for pattern in contextual_patterns
            ):
                return True

        return False

    def extract_target(self, user_input: str) -> str:

        command = user_input.lower().strip()

        # Remove JARVIS addressing word
        command = re.sub(
            r"\bjarvis\b",
            "",
            command
        )

        # Remove polite words
        command = re.sub(
            r"\b(please|can you|could you|would you)\b",
            "",
            command
        )

        # Remove common action words
        command = re.sub(
            r"\b(open|launch|start)\b",
            "",
            command
        )

        # Remove extra punctuation
        command = re.sub(
            r"[^\w\s]",
            "",
            command
        )

        # Remove extra spaces
        command = re.sub(
            r"\s+",
            " ",
            command
        ).strip()

        return command

