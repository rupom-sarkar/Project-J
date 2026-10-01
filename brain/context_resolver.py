from brain.brain import BrainRequest
from brain.context import Context


class ContextResolver:

    def resolve(self, request: BrainRequest, context: Context) -> BrainRequest:
        """
        Use previous context only for valid follow-up requests.
        Clear old context when the user starts an unrelated task.
        """

        # ------------------------------------------
        # Follow-up search
        # ------------------------------------------
        if (
            request.intent == "information_request"
            and request.action == "follow_up_search"
        ):

            previous_action = context.get_last_action()
            previous_query = context.get_last_query()

            # Continue previous YouTube search
            if previous_action == "youtube_search":

                query = request.query

                if previous_query:
                    query = f"{previous_query} {query}"

                return BrainRequest(
                    intent="information_request",
                    action="youtube_search",
                    query=query
                )

            # Continue previous Google search
            if previous_action == "google_search":

                query = request.query

                if previous_query:
                    query = f"{previous_query} {query}"

                return BrainRequest(
                    intent="information_request",
                    action="google_search",
                    query=query
                )

            # No previous search context
            context.clear()
            return request

        # ------------------------------------------
        # New request
        # Clear previous search context
        # ------------------------------------------
        if context.get_last_action() in [
            "google_search",
            "youtube_search"
        ]:
            context.clear()

        # ------------------------------------------
        # Explicit / generic search
        # ------------------------------------------
        if request.intent == "information_request":
            if request.action in [
                "google_search",
                "youtube_search",
                "search"
            ]:
                return request

        # ------------------------------------------
        # Everything else
        # ------------------------------------------
        return request