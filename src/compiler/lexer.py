from enum import Enum, auto
from typing import Optional, Any

class TokenType(Enum):
    IDENTIFIER = auto()
    LITERAL = auto()

    OPERAND = auto()
    KEYWORD = auto()

    OPENING_BRACKET = auto()
    CLOSING_BRACKET = auto()
    OPENING_SQUARE_BRACKET = auto()
    CLOSING_SQUARE_BRACKET = auto()
    OPENING_CURLY_BRACKET = auto()
    CLOSING_CURLY_BRACKET = auto()
    SEMICOLON = auto()

class Operand(Enum):
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
    GOTO = auto()
    TYPE = auto()
    FUNCTION = auto()
    RETURN = auto()

class LiteralType(Enum):
    STRING = auto()
    NUMBER = auto()


class Token:
    SUBTYPE_MAP = {
        TokenType.OPERAND: Operand,
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

    def __repr__(self):
        parts = [self.token_type.name]

        if self.subtype is not None:
            parts.append(self.subtype.name)

        if self.value is not None:
            parts.append(repr(self.value))

        joined = ", ".join(parts)
        return f"Token({joined}) at line {self.line}, column {self.column}"





class Lexer:
    token_map = {
        "(": (TokenType.OPENING_BRACKET,),
        ")": (TokenType.CLOSING_BRACKET,),
        "[": (TokenType.OPENING_SQUARE_BRACKET,),
        "]": (TokenType.CLOSING_SQUARE_BRACKET,),
        "{": (TokenType.OPENING_CURLY_BRACKET,),
        "}": (TokenType.CLOSING_CURLY_BRACKET,),
        ";": (TokenType.SEMICOLON,),

        "+": (TokenType.OPERAND, Operand.PLUS),
        "-": (TokenType.OPERAND, Operand.MINUS),
        "*": (TokenType.OPERAND, Operand.STAR),
        "&": (TokenType.OPERAND, Operand.AMPERSAND),
        "|": (TokenType.OPERAND, Operand.PIPE),
        "^": (TokenType.OPERAND, Operand.UP_ARROW),
        "~": (TokenType.OPERAND, Operand.TILDE),

        "=": (TokenType.OPERAND, Operand.EQUALITY),
        ">": (TokenType.OPERAND, Operand.GREATER_THAN),
        "<": (TokenType.OPERAND, Operand.LESS_THAN),
        "!": (TokenType.OPERAND, Operand.EXCLAMATION),


        "if": (TokenType.KEYWORD, KeywordType.IF),
        "else": (TokenType.KEYWORD, KeywordType.ELSE),
        "func": (TokenType.KEYWORD, KeywordType.FUNCTION),
        "return": (TokenType.KEYWORD, KeywordType.RETURN),
        "goto": (TokenType.KEYWORD, KeywordType.GOTO),
        "while": (TokenType.KEYWORD, KeywordType.WHILE),
        "type": (TokenType.KEYWORD, KeywordType.TYPE),
    }

    delimiters = [" ", "#", "\n", "\t"]
    pseudo_delimiters = ["(", ")", "[", "]", "{", "}", ";", "+", "-", "*", "&", "|", "^", "~",
                         "=", ">", "<", "!"]
    string_delimiters = ["\"", "\'"]

    @staticmethod
    def attempt_tokenization(string: str, line: int, column: int, force=False) -> Token | None:
        if string in Lexer.token_map:
            return Token(*(Lexer.token_map[string]), line=line, column=(column - len(string)))


        if string[0] in Lexer.string_delimiters and string[-1] in Lexer.string_delimiters and len(string) >= 2:
            return Token(TokenType.LITERAL, LiteralType.STRING, value=string[1:-1], line=line, column=(column - len(string)))

        if force:
            try:
                return Token(TokenType.LITERAL, LiteralType.NUMBER, value=int(string, 0), line=line, column=(column - len(string)))
            except ValueError:
                return Token(TokenType.IDENTIFIER, value=string, line=line, column=(column - len(string)))

        return None


    @staticmethod
    def tokenize(to_parse: str):
        tokens: list[Token] = []
        line = 1
        column = 0
        char = -1
        total_length = len(to_parse)
        accumulator = ""

        inside_string = False
        inside_comment = False

        while char < total_length - 1:
            char += 1
            column += 1
            current_char = to_parse[char]

            if inside_comment and not current_char == "\n":
                continue

            if inside_string and not (current_char in ["\"", "\'"]):
                accumulator += current_char
                continue

            if current_char in Lexer.delimiters or current_char in Lexer.pseudo_delimiters:
                if accumulator and not inside_string:
                    tokens.append(Lexer.attempt_tokenization(accumulator, line, column, force=True))
                    accumulator = ""
                if current_char == "\n":
                    line += 1
                    column = 0

            if not (current_char in Lexer.delimiters):
                if current_char in ["\"", "\'"]:
                    inside_string = not inside_string

                accumulator += current_char
                result = Lexer.attempt_tokenization(accumulator, line, column)
                if result is not None:
                    tokens.append(result)
                    accumulator = ""

        return tokens
