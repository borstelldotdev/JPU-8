from enum import Enum, auto
from typing import Optional, Any

class TokenType(Enum):
    IDENTIFIER = auto()
    LITERAL = auto()

    OPERAND = auto()
    KEYWORD = auto()

    OPENING_PARENTHESIS = auto()
    CLOSING_PARENTHESIS = auto()
    OPENING_SQUARE_BRACKET = auto()
    CLOSING_SQUARE_BRACKET = auto()
    OPENING_CURLY_BRACKET = auto()
    CLOSING_CURLY_BRACKET = auto()
    SEMICOLON = auto()
    HASHTAG = auto()
    COMMA = auto()
    DOT = auto()

class OperandType(Enum):
    PLUS = auto()
    MINUS = auto()
    STAR = auto()

    AMPERSAND = auto()
    PIPE = auto()
    UP_ARROW = auto()
    TILDE = auto()

    EQUALITY = auto()
    EXCLAMATION = auto()
    GREATER_THAN = auto()
    LESS_THAN = auto()

class KeywordType(Enum):
    IF = auto()
    ELSE = auto()
    WHILE = auto()
    TYPE = auto()
    FUNCTION = auto()
    RETURN = auto()

    CN_DEFINE = auto()
    CN_MACRO = auto()
    CN_ENTRYPOINT = auto()
    CN_SETUPPOINT = auto()

class LiteralType(Enum):
    STRING = auto()
    NUMBER = auto()


class Token:
    SUBTYPE_MAP = {
        TokenType.OPERAND: OperandType,
        TokenType.KEYWORD: KeywordType,
    }

    def __init__(self, token_type: TokenType, subtype: Optional[Enum]=None, value: Any=None, line=0, column=0):
        self.token_type = token_type
        self.subtype = subtype
        self.value = value

        self.line = line
        self.column = column

        if subtype is not None and token_type in self.SUBTYPE_MAP and not isinstance(subtype, self.SUBTYPE_MAP[token_type]):
            expected = self.SUBTYPE_MAP[token_type].__name__
            got = type(subtype).__name__

            raise TypeError(f"{token_type.name} expects {expected}, got {got}")

    def match(self, token_type=None, subtype=None, value=None) -> bool:
        return ((token_type is None or token_type is self.token_type) and
                (subtype is None or subtype is self.subtype) and
                (value is None or value is self.value))

    def __repr__(self):
        parts = [self.token_type.name]

        if self.subtype is not None:
            parts.append(self.subtype.name)

        if self.value is not None:
            parts.append(repr(self.value))

        joined = ", ".join(parts)
        return f"Token({joined}) at line {self.line}, column {self.column}"

