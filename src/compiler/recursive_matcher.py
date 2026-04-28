from abc import ABC, abstractmethod
from typing import Any

class AbstactMatchPattern(ABC):
    @abstractmethod
    def match(self, data: Any) -> Any | None:
        raise NotImplementedError

class RecursiveMatcher:
    def __init__(self, patterns: list[AbstactMatchPattern]) -> None:
        self.patterns: list[AbstactMatchPattern] = patterns

    def match(self, data: Any):
        for pattern in self.patterns:
            attempt = pattern.match()
