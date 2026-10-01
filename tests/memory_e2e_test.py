import os
import tempfile
from datetime import datetime

from memory.memory_manager import MemoryManager
from memory.memory_retriever import MemoryRetriever
from memory.memory_store import MemoryStore
from memory.memory_types import (
    MemoryItem,
    SEMANTIC,
    EPISODIC,
    PREFERENCE,
    PROJECT,
    TEMPORARY,
    EXPLICIT
)


def create_memory(
    memory_id,
    memory_type,
    content,
    importance=5
):
    now = datetime.now()

    return MemoryItem(
        id=memory_id,
        type=memory_type,
        content=content,
        source=EXPLICIT,
        confidence=1.0,
        importance=importance,
        created_at=now,
        updated_at=now
    )


def create_test_manager(file_path):
    manager = MemoryManager()

    # Replace the normal memory store with
    # a temporary test store.
    manager.store = MemoryStore(file_path)
    manager.memories = []

    return manager


def test_all_five_memory_types():

    with tempfile.TemporaryDirectory() as temp_dir:

        memory_file = os.path.join(
            temp_dir,
            "memory.json"
        )

        # ------------------------------------------
        # Create manager
        # ------------------------------------------
        manager = create_test_manager(
            memory_file
        )

        # ------------------------------------------
        # Create five different memory types
        # ------------------------------------------
        memories = [

            create_memory(
                "test_semantic",
                SEMANTIC,
                "Python is a programming language",
                6
            ),

            create_memory(
                "test_episodic",
                EPISODIC,
                "Completed memory system Task 29",
                7
            ),

            create_memory(
                "test_preference",
                PREFERENCE,
                "User prefers Python",
                8
            ),

            create_memory(
                "test_project",
                PROJECT,
                "Project J is the personal JARVIS project",
                9
            ),

            create_memory(
                "test_temporary",
                TEMPORARY,
                "Current test session is active",
                3
            )
        ]

        # ------------------------------------------
        # Save all five memories
        # ------------------------------------------
        for memory in memories:
            manager.add_memory(memory)

        # ------------------------------------------
        # Verify file was created
        # ------------------------------------------
        assert os.path.exists(memory_file)

        # ------------------------------------------
        # Simulate JARVIS restart
        # ------------------------------------------
        manager_after_restart = create_test_manager(
            memory_file
        )

        manager_after_restart.memories = (
            manager_after_restart.store.load()
        )

        # ------------------------------------------
        # Create retriever using restarted manager
        # ------------------------------------------
        retriever = MemoryRetriever()

        retriever.memory_manager = (
            manager_after_restart
        )

        # ------------------------------------------
        # Verify all five memories exist
        # ------------------------------------------
        assert len(
            manager_after_restart.get_all_memories()
        ) == 5

        # ------------------------------------------
        # Verify each memory by ID
        # ------------------------------------------
        for memory in memories:

            retrieved = retriever.get_by_id(
                memory.id
            )

            assert retrieved is not None

            assert retrieved.id == memory.id

            assert retrieved.type == memory.type

            assert retrieved.content == memory.content

            assert retrieved.source == EXPLICIT

            assert retrieved.confidence == 1.0

        # ------------------------------------------
        # Verify retrieval by type
        # ------------------------------------------
        assert len(
            retriever.get_by_type(SEMANTIC)
        ) == 1

        assert len(
            retriever.get_by_type(EPISODIC)
        ) == 1

        assert len(
            retriever.get_by_type(PREFERENCE)
        ) == 1

        assert len(
            retriever.get_by_type(PROJECT)
        ) == 1

        assert len(
            retriever.get_by_type(TEMPORARY)
        ) == 1

        # ------------------------------------------
        # Verify content search
        # ------------------------------------------
        assert (
            retriever.search("programming")[0].type
            == SEMANTIC
        )

        assert (
            retriever.search("Task 29")[0].type
            == EPISODIC
        )

        assert (
            retriever.search("prefers Python")[0].type
            == PREFERENCE
        )

        assert (
            retriever.search("Project J")[0].type
            == PROJECT
        )

        assert (
            retriever.search("test session")[0].type
            == TEMPORARY
        )


if __name__ == "__main__":

    test_all_five_memory_types()

    print(
        "PASS: All five memory types "
        "saved, persisted, and retrieved successfully."
    )