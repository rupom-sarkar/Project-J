from brain.brain import BrainRequest
import re


class ConversationEngine:

    def respond(
        self,
        command: str,
        request: BrainRequest,
        context,
        memory_retriever
    ):

        # Normalize command
        command = command.lower().strip()
        command = re.sub(r"[^\w\s]", "", command)

        def update_conversation(topic=None):

            if topic is not None:
                context.set_conversation_topic(topic)

            context.set_last_conversational_statement(
                command
            )

            context.increment_conversation_turn()

        # ------------------------------------------
        # Greeting
        # ------------------------------------------
        words = command.split()

        greeting_words = [
            "hello",
            "hi",
            "hey"
        ]

        greeting_phrases = [
            "good morning",
            "good afternoon",
            "good evening"
        ]

        if (
            any(
                word in words
                for word in greeting_words
            )
            or any(
                phrase in command
                for phrase in greeting_phrases
            )
        ):

            update_conversation("greeting")

            return "Hello, Sir. How can I help you?"

        # ------------------------------------------
        # Identity
        # ------------------------------------------
        if (
            "who are you" in command
            or "what are you" in command
            or "your name" in command
        ):

            update_conversation("jarvis")

            return (
                "I am JARVIS, your personal AI assistant."
            )

        # ------------------------------------------
        # How are you
        # ------------------------------------------
        if (
            "how are you" in command
            or "how are you doing" in command
        ):

            update_conversation("jarvis")

            return (
                "I'm functioning perfectly, Sir."
            )

        # ------------------------------------------
        # Thanks
        # ------------------------------------------
        if any(
            phrase in command
            for phrase in [
                "thank you",
                "thanks",
                "thank u"
            ]
        ):

            update_conversation()

            return "You're welcome, Sir."

        # ------------------------------------------
        # Positive feedback
        # ------------------------------------------
        if any(
            phrase in command
            for phrase in [
                "good job",
                "well done",
                "nice work",
                "great job"
            ]
        ):

            update_conversation()

            return "Thank you, Sir."

        # ------------------------------------------
        # Python conversation
        # ------------------------------------------
        if "i like python" in command:

            memories = memory_retriever.search(
                "python"
            )

            update_conversation("python")

            if memories:
                return (
                    "I remember that you prefer Python, Sir."
                )

            return (
                "Python is a great choice, Sir."
            )

        # ------------------------------------------
        # Java conversation
        # ------------------------------------------
        if "i like java" in command:

            memories = memory_retriever.search(
                "java"
            )

            update_conversation("java")

            if memories:
                return (
                    "I remember that you like Java, Sir."
                )

            return (
                "Java is a solid choice, Sir."
            )

        # ------------------------------------------
        # What do you remember?
        # ------------------------------------------
        if (
            "what do you remember" in command
            or "what do you know about me" in command
        ):

            update_conversation("memory")

            memories = (
                memory_retriever
                .memory_manager
                .get_all_memories()
            )

            if not memories:
                return (
                    "I don't have any stored memories, Sir."
                )

            response = (
                "Here is what I remember, Sir:\n"
            )

            for memory in memories:
                response += (
                    f"- {memory.content}\n"
                )

            return response.strip()

        # ------------------------------------------
        # Detect learning statement
        # ------------------------------------------
        if (
            command.startswith("im learning ")
            or command.startswith("i am learning ")
        ):

            if command.startswith("im learning "):

                topic = command.replace(
                    "im learning ",
                    "",
                    1
                ).strip()

            else:

                topic = command.replace(
                    "i am learning ",
                    "",
                    1
                ).strip()

            if topic:

                update_conversation(topic)

                return (
                    f"That's great, Sir. "
                    f"Learning {topic} is a useful skill."
                )

        # ------------------------------------------
        # Contextual follow-up
        # ------------------------------------------
        previous_topic = (
            context.get_conversation_topic()
        )

        if previous_topic:

            continuation_words = [
                "more",
                "further",
                "deeper",
                "continue",
                "elaborate",
                "expand"
            ]

            explanation_patterns = [
                "explain",
                "how does",
                "how do",
                "why does",
                "why do",
                "why is",
                "why are"
            ]

            has_continuation = any(
                word in words
                for word in continuation_words
            )

            has_explanation = any(
                pattern in command
                for pattern in explanation_patterns
            )

            if (
                has_continuation
                or has_explanation
            ):

                update_conversation(
                    previous_topic
                )

                if has_explanation:

                    return (
                        f"Of course, Sir. I can explain "
                        f"{previous_topic}."
                    )

                return (
                    f"Certainly, Sir. We can continue "
                    f"discussing {previous_topic}."
                )

        # ------------------------------------------
        # Explicit contextual explanation
        # ------------------------------------------
        if command in [
            "explain it",
            "explain that",
            "explain this"
        ]:

            previous_topic = (
                context.get_conversation_topic()
            )

            if previous_topic:

                update_conversation(
                    previous_topic
                )

                return (
                    f"Of course, Sir. I can explain "
                    f"{previous_topic}."
                )

            update_conversation()

            return (
                "Of course, Sir. What would you like "
                "me to explain?"
            )

        # ------------------------------------------
        # Help
        # ------------------------------------------
        if command in [
            "help",
            "what can you do",
            "what can you do for me"
        ]:

            update_conversation("jarvis")

            return (
                "I can search the web, search YouTube, "
                "open applications and folders, remember "
                "information, retrieve memories, and "
                "handle basic conversations, Sir."
            )

        # ------------------------------------------
        # No deterministic response
        # ------------------------------------------
        return None