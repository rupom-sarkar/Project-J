class Context:

    def __init__(self):
        # ------------------------------------------
        # Existing task context
        # ------------------------------------------
        self.last_command = None
        self.last_intent = None
        self.last_action = None
        self.last_target = None
        self.last_query = None

        # ------------------------------------------
        # Conversation context
        # ------------------------------------------
        self.conversation_topic = None
        self.last_conversational_statement = None
        self.conversation_turns = 0

    # ----------------------------------------------
    # Existing context methods
    # ----------------------------------------------

    def update(self, request):
        self.last_command = request.target
        self.last_intent = request.intent
        self.last_action = request.action
        self.last_target = request.target
        self.last_query = request.query

    def get_last_target(self):
        return self.last_target

    def get_last_query(self):
        return self.last_query

    def get_last_action(self):
        return self.last_action

    def get_last_intent(self):
        return self.last_intent

    # ----------------------------------------------
    # Conversation methods
    # ----------------------------------------------

    def set_conversation_topic(self, topic):
        self.conversation_topic = topic

    def get_conversation_topic(self):
        return self.conversation_topic

    def set_last_conversational_statement(self, statement):
        self.last_conversational_statement = statement

    def get_last_conversational_statement(self):
        return self.last_conversational_statement

    def increment_conversation_turn(self):
        self.conversation_turns += 1

    def get_conversation_turns(self):
        return self.conversation_turns

    # ----------------------------------------------
    # Clear everything
    # ----------------------------------------------

    def clear(self):
        self.last_command = None
        self.last_intent = None
        self.last_action = None
        self.last_target = None
        self.last_query = None

        self.conversation_topic = None
        self.last_conversational_statement = None
        self.conversation_turns = 0