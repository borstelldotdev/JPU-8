from typing import Any
from abc import ABC, abstractmethod

from src.compiler.tokens import Token, TokenType, Operand, KeywordType, LiteralType
from src.compiler.prettyprint import *



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

    def prev(self) -> Token:
        self.pointer -= 1
        return self.tokens[self.pointer]



    def is_empty(self) -> bool:
        return self.pointer == len(self.tokens) - 1


class ParsingError(Exception):
    def __init__(self, message: str) -> None:
        super().__init__(message)



class AbstractTreeNode(ABC):
    def __init__(self, parent: AbstractTreeNode | None, *data) -> None:
        self.parent = parent

    def add_child(self, child: AbstractTreeNode) -> AbstractTreeNode | None:
        child.parent = self
        return child

    def __repr__(self):
        return f"{type(self).__name__}:{repr_dict(self.__dict__)}"

    @classmethod
    @abstractmethod
    def from_token_stream(cls, stream: TokenStream) -> AbstractTreeNode:
        raise NotImplementedError()


class AbstractSyntaxTree(AbstractTreeNode):
    def __init__(self, entrypoint: str="main") -> None:
        super().__init__(None)
        self.functions = {}
        self.entrypoint = entrypoint

    def add_func(self, func: Function) -> None:
        new = self.add_child(func)
        self.functions[new.name] = new

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> AbstractSyntaxTree:
        new = cls()
        while not stream.is_empty():
            next_token = stream.next()

            if next_token.match(token_type=TokenType.KEYWORD, subtype=KeywordType.FUNCTION):
                fn = Function.from_token_stream(stream)
                new.add_func(fn)
            else:
                # Maybe raise some errors??
                pass

        return new


class Function(AbstractTreeNode):
    def __init__(self, parent: AbstractTreeNode | None, name: str) -> None:
        super().__init__(parent)
        self.name = name
        self.statement: Statement | None = None


class AbstractStatement(AbstractTreeNode): pass

class Statement:
    class Combined(AbstractStatement):
        def __init__(self, parent: AbstractTreeNode, *statement_data: Any) -> None:
            super().__init__(parent)

    class Assignment(AbstractStatement):
        pass


    class IgnoredExpression(AbstractStatement):
        pass

class AbstractExpression(AbstractTreeNode): pass

class Expression:
    class Literal(AbstractExpression):
        pass

    class Call(AbstractExpression):
        pass



    class Add(AbstractExpression):
        pass

    class Sub(AbstractExpression):
        pass

    class Mul(AbstractExpression):
        pass

    class And(AbstractExpression):
        pass

    class Or(AbstractExpression):
        pass

    class Xor(AbstractExpression):
        pass

    class Not(AbstractExpression):
        pass

class AbstractComparison(AbstractTreeNode): pass

class Assignable(AbstractTreeNode):
    pass