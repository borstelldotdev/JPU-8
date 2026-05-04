from src.parsing.tokens import *
from src.parsing.stream_utils import TokenStream
from src.parsing.lexer import Lexer

class WTFError(Exception):
    def __init__(self, message: str):
        super().__init__(message)

class Instruction:
    def __init__(self, data: int, intermediate: int | None = None):
        self.data: int = data
        self.intermediate: int = intermediate if intermediate is not None else 0

class InstructionPair:
    def __init__(self, flg_set_instruction: Instruction, flg_unset_instruction: Instruction):
        self.flg_set: Instruction = flg_set_instruction
        self.flg_unset: Instruction = flg_unset_instruction

class Assembler:
    def __init__(self):
        pass

    def assemble(self, code: str):
        tokens = Lexer.tokenize(code)
        token_stream = TokenStream(tokens)

        while not token_stream.is_empty():
            token, option = token_stream.expect({"token_type": TokenType.DOT},
                                                {"token_type": TokenType.HASHTAG},
                                                {"token_type": TokenType.IDENTIFIER},
                                                {"token_type": TokenType.LITERAL, "subtype": LiteralType.NUMBER})

            match option:
                case 0: # <dot>: section
                    pass
                case 1: # #compiler-annotation
                    pass
                case 2: # identifier
                    pass
                case 3: # literal number
                    pass
                case _:
                    raise WTFError("Huh?")
