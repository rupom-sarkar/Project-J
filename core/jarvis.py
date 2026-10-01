from datetime import datetime

from brain.brain import Brain
from brain.decision import BrainDecision
from brain.context import Context
from brain.context_resolver import ContextResolver

from memory.memory_retriever import MemoryRetriever
from memory.memory_manager import MemoryManager
from memory.memory_types import (
    MemoryItem,
    PREFERENCE,
    EXPLICIT
)

from tools.app_control import AppController
from tools.web_control import WebController
from tools.search_control import SearchController
from tools.file_control import FileController

from conversation.conversation_engine import ConversationEngine

from core.ui_bridge import UIBridge


class Jarvis:

    def __init__(self):

        self.name = "JARVIS"

        # ==========================================
        # BRAIN
        # ==========================================

        self.brain = Brain()

        self.decision = BrainDecision()

        self.context = Context()

        self.context_resolver = ContextResolver()

        # ==========================================
        # CONVERSATION
        # ==========================================

        self.conversation_engine = (
            ConversationEngine()
        )

        # ==========================================
        # MEMORY
        # ==========================================

        self.memory_retriever = (
            MemoryRetriever()
        )

        self.memory_manager = (
            MemoryManager()
        )

        # ==========================================
        # TOOLS
        # ==========================================

        self.app_controller = (
            AppController()
        )

        self.web_controller = (
            WebController()
        )

        self.search_controller = (
            SearchController()
        )

        self.file_controller = (
            FileController()
        )

        # ==========================================
        # FRONTEND UI BRIDGE
        # ==========================================

        self.ui_bridge = UIBridge()

        self.ui_bridge.start()

    # ==================================================
    # MAIN JARVIS RESPONSE
    # ==================================================

    def respond(self, command):

        command = command.lower().strip()

        # ==========================================
        # JARVIS VISUAL POWER CONTROL
        # ==========================================

        if command in [
            "turn on",
            "turn on jarvis",
            "activate",
            "activate jarvis",
            "wake up",
            "wake up jarvis"
        ]:

            self.ui_bridge.turn_on()

            return (
                "JARVIS systems activated, Sir."
            )

        if command in [
            "turn off",
            "turn off jarvis",
            "deactivate",
            "deactivate jarvis",
            "sleep",
            "sleep jarvis"
        ]:

            self.ui_bridge.turn_off()

            return (
                "JARVIS systems deactivated, Sir."
            )

        # ==========================================
        # BRAIN
        # ==========================================

        request = self.brain.process(
            command
        )

        # ==========================================
        # CONTEXT
        # ==========================================

        request = self.context_resolver.resolve(
            request,
            self.context
        )

        self.context.update(
            request
        )

        # ==========================================
        # DECISION
        # ==========================================

        decision = self.decision.decide(
            request
        )

        # ==========================================
        # MEMORY SAVE
        # ==========================================

        if decision == "memory_save":

            content = request.query

            if not content:

                return (
                    "I need something to remember, Sir."
                )

            memory_id = (
                "mem_"
                + datetime.now().strftime(
                    "%Y%m%d%H%M%S%f"
                )
            )

            now = datetime.now()

            memory = MemoryItem(
                id=memory_id,
                type=PREFERENCE,
                content=content,
                source=EXPLICIT,
                confidence=1.0,
                importance=8,
                created_at=now,
                updated_at=now
            )

            self.memory_manager.add_memory(
                memory
            )

            return (
                "I'll remember that, Sir."
            )

        # ==========================================
        # MEMORY QUERY
        # ==========================================

        if decision == "memory_query":

            memories = (
                self.memory_retriever
                .memory_manager
                .get_all_memories()
            )

            if not memories:

                return (
                    "I don't have any stored "
                    "memories, Sir."
                )

            response = (
                "Here is what I remember, Sir:\n"
            )

            for memory in memories:

                response += (
                    f"- {memory.content}\n"
                )

            return response.strip()

        # ==========================================
        # CONVERSATION
        # ==========================================

        if decision == "conversation":

            response = (
                self.conversation_engine.respond(
                    command,
                    request,
                    self.context,
                    self.memory_retriever
                )
            )

            if response is not None:

                return response

        # ==========================================
        # OPEN APPLICATION
        # ==========================================

        if decision == "open_application":

            return (
                self.app_controller
                .open_application(
                    request.target
                )
            )

        # ==========================================
        # OPEN FOLDER
        # ==========================================

        if decision == "open_folder":

            return (
                self.file_controller
                .open_folder(
                    request.target
                )
            )

        # ==========================================
        # OPEN WEBSITE
        # ==========================================

        if decision == "open_website":

            return (
                self.web_controller
                .open_website(
                    request.target
                )
            )

        # ==========================================
        # GOOGLE SEARCH
        # ==========================================

        if decision == "google_search":

            return (
                self.search_controller
                .google_search(
                    request.query
                )
            )

        # ==========================================
        # YOUTUBE SEARCH
        # ==========================================

        if decision == "youtube_search":

            return (
                self.search_controller
                .youtube_search(
                    request.query
                )
            )

        # ==========================================
        # FALLBACK COMMANDS
        # ==========================================

        if "how are you" in command:

            return (
                "I'm functioning perfectly, Sir."
            )

        if (
            "your name" in command
            or "who are you" in command
        ):

            return (
                "I am JARVIS, "
                "your personal AI assistant."
            )

        if "time" in command:

            current_time = (
                datetime.now().strftime(
                    "%I:%M %p"
                )
            )

            return (
                f"The current time is "
                f"{current_time}, Sir."
            )

        if (
            "date" in command
            or "today" in command
        ):

            current_date = (
                datetime.now().strftime(
                    "%A, %B %d, %Y"
                )
            )

            return (
                f"Today is "
                f"{current_date}, Sir."
            )

        # ==========================================
        # EXIT
        # ==========================================

        if command in [
            "goodbye",
            "good bye",
            "exit",
            "quit",
            "shutdown"
        ]:

            return (
                "Goodbye, Sir."
            )

        # ==========================================
        # UNKNOWN COMMAND
        # ==========================================

        return (
            f"I heard you say: {command}"
        )


# ==================================================
# DIRECT PYTHON TEST
# ==================================================

if __name__ == "__main__":

    jarvis = Jarvis()

    print(
        "JARVIS is online, Sir."
    )

    print(
        "Type 'exit' to shut down."
    )

    while True:

        command = input(
            "You: "
        )

        response = (
            jarvis.respond(
                command
            )
        )

        print(
            "JARVIS:",
            response
        )

        if command.lower().strip() in [
            "goodbye",
            "good bye",
            "exit",
            "quit",
            "shutdown"
        ]:

            break