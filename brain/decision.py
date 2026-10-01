from brain.brain import BrainRequest


class BrainDecision:

    def decide(self, request: BrainRequest) -> str:

        # ------------------------------------------
        # Conversation
        # ------------------------------------------
        if request.intent == "conversation":
            return "conversation"

        # ------------------------------------------
        # Open request
        # ------------------------------------------
        if request.intent == "open_request":

            if request.action == "open":

                target = request.target.lower().strip()

                # File / folder
                folders = [
                    "downloads",
                    "documents",
                    "desktop",
                    "project j"
                ]

                if any(
                    folder in target
                    for folder in folders
                ):
                    return "open_folder"

                # Website
                websites = [
                    "youtube",
                    "google",
                    "facebook"
                ]

                if any(
                    site in target
                    for site in websites
                ):
                    return "open_website"

                # Application
                return "open_application"

        # ------------------------------------------
        # Information requests
        # ------------------------------------------
        if request.intent == "information_request":

            if request.action == "google_search":
                return "google_search"

            if request.action == "youtube_search":
                return "youtube_search"

            if request.action == "search":
                return "google_search"

            if request.action == "follow_up_search":
                return "google_search"

        # ------------------------------------------
        # Memory requests
        # ------------------------------------------
        if request.intent == "memory_request":

            if request.action == "memory_query":
                return "memory_query"

            if request.action == "memory_save":
                return "memory_save"

        # ------------------------------------------
        # Unknown
        # ------------------------------------------
        return "unknown"