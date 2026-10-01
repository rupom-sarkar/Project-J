from memory.memory_types import MemoryItem
from memory.memory_store import MemoryStore
from datetime import datetime


class MemoryManager:

    def __init__(self):
        self.store = MemoryStore()
        self.memories = self.store.load()

    def add_memory(self, memory: MemoryItem):

        if self.get_memory_by_id(memory.id) is not None:
            raise ValueError(
                f"Memory with ID '{memory.id}' already exists"
            )

        self.memories.append(memory)
        self.store.save(self.memories)

    def update_memory(self, memory: MemoryItem):

        for index, existing_memory in enumerate(self.memories):

            if existing_memory.id == memory.id:

                self.memories[index] = memory
                self.store.save(self.memories)

                return True

        return False

    def get_all_memories(self):

        return [
            memory
            for memory in self.memories
            if not self.is_expired(memory)
        ]

    def get_memory_by_id(self, memory_id: str):

        for memory in self.memories:

            if memory.id == memory_id:

                if self.is_expired(memory):
                    return None

                return memory

        return None

    def get_memories_by_type(self, memory_type: str):

        return [
            memory
            for memory in self.memories
            if memory.type == memory_type
            and not self.is_expired(memory)
        ]

    def search_memories(self, keyword: str):

        keyword = keyword.lower().strip()

        return [
            memory
            for memory in self.memories
            if keyword in memory.content.lower()
            and not self.is_expired(memory)
        ]

    def cleanup_expired_memories(self):

        original_count = len(self.memories)

        self.memories = [
            memory
            for memory in self.memories
            if not self.is_expired(memory)
        ]

        removed_count = original_count - len(self.memories)

        if removed_count > 0:
            self.store.save(self.memories)

        return removed_count

    def is_expired(self, memory: MemoryItem):

        if memory.expires_at is None:
            return False

        return datetime.now() >= memory.expires_at

    def delete_memory(self, memory_id: str):

        for memory in self.memories:

            if memory.id == memory_id:

                self.memories.remove(memory)
                self.store.save(self.memories)

                return True

        return False

