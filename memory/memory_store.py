import json
from datetime import datetime
from memory.memory_types import MemoryItem


class MemoryStore:

    def __init__(self, file_path="memory/memory.json"):
        self.file_path = file_path

    def save(self, memories):
        data = []

        for memory in memories:
            data.append({
                "id": memory.id,
                "type": memory.type,
                "content": memory.content,
                "source": memory.source,
                "confidence": memory.confidence,
                "importance": memory.importance,
                "created_at": memory.created_at.isoformat(),
                "updated_at": memory.updated_at.isoformat(),
                "expires_at": (
                    memory.expires_at.isoformat()
                    if memory.expires_at
                    else None
                )
            })

        with open(self.file_path, "w", encoding="utf-8") as file:
            json.dump(data, file, indent=4)

    def load(self):
        try:
            with open(self.file_path, "r", encoding="utf-8") as file:
                data = json.load(file)

        except FileNotFoundError:
            return []

        memories = []

        for item in data:

            created_at = datetime.fromisoformat(
                item["created_at"]
            )

            updated_at = datetime.fromisoformat(
                item["updated_at"]
            )

            expires_at = None

            if item["expires_at"] is not None:
                expires_at = datetime.fromisoformat(
                    item["expires_at"]
                )

            memory = MemoryItem(
                id=item["id"],
                type=item["type"],
                content=item["content"],
                source=item["source"],
                confidence=item["confidence"],
                importance=item["importance"],
                created_at=created_at,
                updated_at=updated_at,
                expires_at=expires_at
            )

            memories.append(memory)

        return memories