from dataclasses import dataclass, field
from typing import List, Optional

@dataclass
class ConversationTurn:
    role: str
    content: str

@dataclass
class ConversationState:
    turns: List[ConversationTurn] = field(default_factory=list)

    act: Optional[str] = None
    chapter: Optional[str] = None
    section: Optional[str] = None

    awaiting_clarification: bool = False

    def add_user(self, text: str):
        self.turns.append(ConversationTurn("user", text))

    def add_assistant(self, text: str):
        self.turns.append(ConversationTurn("assistant", text))

    def last_n(self, n: int = 6) -> List[ConversationTurn]:
        return self.turns[-n:]

    def set_anchor(self, act=None, chapter=None, section=None):
        if self.awaiting_clarification:
            return

        self.act = act or self.act
        self.chapter = chapter or self.chapter
        self.section = section or self.section

    def mark_ambiguous(self):
        self.awaiting_clarification = True

    def clear_ambiguity(self):
        self.awaiting_clarification = False

