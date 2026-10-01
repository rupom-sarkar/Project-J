from memory.memory_manager import MemoryManager


class MemoryRetriever:

    def __init__(self):
        self.memory_manager = MemoryManager()

    def search(self, keyword: str):
        return self.memory_manager.search_memories(keyword)

    def get_by_id(self, memory_id: str):
        return self.memory_manager.get_memory_by_id(memory_id)

    def get_by_type(self, memory_type: str):
        return self.memory_manager.get_memories_by_type(memory_type)

    def get_best_match(self, keyword: str):

        memories = self.search(keyword)

        if not memories:
            return None

        return max(
            memories,
            key=lambda memory: (
                memory.importance,
                memory.confidence
            )
        )

