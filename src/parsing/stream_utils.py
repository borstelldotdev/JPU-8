from src.parsing.tokens import Token

class TokenStream:
    def __init__(self, tokens: list[Token]) -> None:
        self.tokens = tokens
        self.pointer = -1

    def __next__(self) -> Token:
        self.pointer += 1
        if self.pointer >= len(self.tokens):
            raise StopIteration
        return self.tokens[self.pointer]

    def next(self) -> Token:
        return self.__next__()

    def preview(self) -> Token:
        return self.tokens[self.pointer + 1]


    def match(self, *args, force=False) -> tuple[Token, int] | None:
        next_token = next(self)
        assert len(args) != 0

        alternative = 0
        for arg in args:
            assert isinstance(arg, dict)
            if next_token.match(**arg):
                return next_token, alternative
            alternative += 1

        self.pointer -= 1
        if force:
            raise ParsingError(f"Expected {', '.join([arg.__repr__() for arg in args[:-1]])}" + \
                               f"{' or ' if len(args) > 1 else ''}{args[-1].__repr__()}; got {next_token}")
        return None

    def match_one(self, **kwargs) -> Token | None:
        result = self.match(kwargs)
        if result is None:
            return None
        return result[0]

    def expect(self, *args) -> tuple[Token, int]:
        match = self.match(*args, force=True)
        assert match is not None
        return match

    def expect_one(self, **kwargs) -> Token:
        return self.expect(kwargs)[0]

    def is_empty(self) -> bool:
        return self.pointer == len(self.tokens) - 1


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)
