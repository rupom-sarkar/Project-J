from dataclasses import dataclass
from datetime import datetime
from typing import Optional


SEMANTIC = "semantic"
EPISODIC = "episodic"
PREFERENCE = "preference"
PROJECT = "project"
TEMPORARY = "temporary"
EXPLICIT = "explicit"
INFERRED = "inferred"
SYSTEM = "system"


@dataclass
class MemoryItem:

    id: str
    type: str
    content: str
    source: str
    confidence: float
    importance: int
    created_at: datetime
    updated_at: datetime
    expires_at: Optional[datetime] = None

    def __post_init__(self):

        allowed_types = [
            SEMANTIC,
            EPISODIC,
            PREFERENCE,
            PROJECT,
            TEMPORARY
        ]

        allowed_sources = [
            EXPLICIT,
            INFERRED,
            SYSTEM
       ]

        if not self.id:
            raise ValueError("Memory ID cannot be empty")

        if self.type not in allowed_types:
            raise ValueError(
                f"Invalid memory type: {self.type}"
            )

        if not self.content:
            raise ValueError(
                "Memory content cannot be empty"
            )

        if self.source not in allowed_sources:
            raise ValueError(
                f"Invalid memory source: {self.source}"
            )

        if not 0.0 <= self.confidence <= 1.0:
            raise ValueError(
                "Confidence must be between 0.0 and 1.0"
            )

        if not 1 <= self.importance <= 10:
            raise ValueError(
                "Importance must be between 1 and 10"
            )

        if self.expires_at is not None:

            if self.expires_at < self.created_at:
                raise ValueError(
                    "Expiration time cannot be before creation time"
                )

