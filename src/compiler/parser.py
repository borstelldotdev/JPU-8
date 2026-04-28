from abc import ABC, abstractmethod
from typing import Any

from src.compiler.tokens import Token, TokenType, OperandType, KeywordType, LiteralType
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



class AbstractTreeNode(ABC):
    def __init__(self) -> None:
        self.parent = None
        self.child_nodes: list[AbstractTreeNode] = []

    def add_child(self, child: AbstractTreeNode) -> AbstractTreeNode | None:
        child.parent = self
        self.child_nodes.append(child)
        return child

    def __repr__(self):
        return f"{type(self).__name__}:{repr_dict(dict(self.__dict__))}"

    @classmethod
    @abstractmethod
    def from_token_stream(cls, stream: TokenStream) -> AbstractTreeNode:
        raise NotImplementedError()


class AbstractSyntaxTree(AbstractTreeNode):
    def __init__(self, entrypoint: str="main") -> None:
        super().__init__()
        self.functions: dict[str, Function] = {}
        self.entrypoint = entrypoint

    def add_func(self, func: Function) -> None:
        self.add_child(func)
        self.functions[func.name] = func

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> AbstractSyntaxTree:
        new = cls()
        while not stream.is_empty():
            next_token, alternative = stream.expect({"token_type": TokenType.KEYWORD, "subtype": KeywordType.FUNCTION},
                                                    {"token_type": TokenType.HASHTAG})
            match alternative:
                case 0:
                    new.add_func(Function.from_token_stream(stream))
                case 1:
                    compiler_annotation = stream.expect({"token_type": TokenType.IDENTIFIER})[0]
                    # Do something ...

        return new

class Function(AbstractTreeNode):
    def __init__(self, name: str, statement: Statement, arguments: list[str]) -> None:
        super().__init__()
        self.name = name
        self.statement = statement
        self.arguments = arguments
        self.add_child(statement)

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> Function:
        identifier = stream.expect_one(token_type=TokenType.IDENTIFIER)
        stream.expect_one(token_type=TokenType.OPENING_PARENTHESIS)
        args = []

        while not stream.match_one(token_type=TokenType.CLOSING_PARENTHESIS):
            args.append(stream.expect_one(token_type=TokenType.IDENTIFIER))
            stream.match_one(token_type=TokenType.COMMA)
        statement = Statement.from_token_stream(stream)

        return cls(identifier.value, statement, args)


class Statement(AbstractTreeNode):
    def __init__(self):
        super().__init__()
        pass

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> Statement:
        identifier, alternative = stream.expect({"token_type": TokenType.OPENING_CURLY_BRACKET},
                                                {"token_type": TokenType.KEYWORD, "subtype": KeywordType.IF},
                                                {"token_type": TokenType.KEYWORD, "subtype": KeywordType.RETURN},
                                                {"token_type": TokenType.KEYWORD, "subtype": KeywordType.WHILE},
                                                {"token_type": TokenType.IDENTIFIER})
        match alternative:
            case 0: # `{`
                return CompoundStatement.from_token_stream(stream)
            case 1: # if
                stream.expect_one(token_type=TokenType.OPENING_PARENTHESIS)
                expression = Expression.from_token_stream(stream)
                stream.expect_one(token_type=TokenType.CLOSING_PARENTHESIS)
                if_body = Statement.from_token_stream(stream)
                else_body = None

                if stream.match_one(token_type=TokenType.KEYWORD, subtype=KeywordType.ELSE):
                    else_body = Statement.from_token_stream(stream)

            case 2: # return
                stream.expect_one(token_type=TokenType.SEMICOLON)
            case 3: # while
                stream.expect_one(token_type=TokenType.OPENING_PARENTHESIS)
            case 4: # <identifier>
                token, alternative = stream.expect({"token_type": TokenType.OPENING_PARENTHESIS},
                                                   {"token_type": TokenType.OPERAND, "subtype": OperandType.EQUALITY})
                match alternative:
                    case 0: # `(`
                        args: list[Expression] = []
                        while not stream.match_one(token_type=TokenType.CLOSING_PARENTHESIS):
                            args.append(Expression.from_token_stream(stream))
                            stream.match_one(token_type=TokenType.COMMA)
                        stream.expect_one(token_type=TokenType.SEMICOLON)
                        return CallStatement(function=identifier.value, arguments=args)
                    case 1: # `=`
                        expression = Expression.from_token_stream(stream)
                        stream.expect_one(token_type=TokenType.SEMICOLON)
                        return AssignmentStatement(Variable(identifier.value), expression)
        raise ParsingError(f"Unexpected parsing error")


class CompoundStatement(Statement):
    def __init__(self, statements: list[Statement]) -> None:
        super().__init__()
        self.statements = statements
        for statement in statements:
            self.add_child(statement)

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> CompoundStatement:
        statements: list[Statement] = []
        while not stream.match_one(token_type=TokenType.CLOSING_CURLY_BRACKET):
            statements.append(Statement.from_token_stream(stream))
        return cls(statements)

class AssignmentStatement(Statement):
    def __init__(self, assignable: Variable, assign_to: Expression) -> None:
        super().__init__()
        self.assignable = assignable
        self.assign_to = assign_to
        self.add_child(assign_to)

class CallStatement(Statement):
    def __init__(self, function: str, arguments: list[Expression]) -> None:
        super().__init__()
        self.function = function
        self.arguments = arguments

class ConditionalStatement(Statement):
    def __init__(self, if_body: Statement, else_body: Statement | None):
        super().__init__()
        self.if_body = if_body
        self.else_body = else_body
        self.add_child(if_body)
        if else_body is not None:
            self.add_child(else_body)





class Expression(AbstractTreeNode):
    def __init__(self) -> None:
        super().__init__()

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> Expression:
        token, alternative = stream.expect({"token_type": TokenType.LITERAL},
                                {"token_type": TokenType.IDENTIFIER})

        a = None
        match alternative:
            case 0: # Literal
                assert isinstance(token.subtype, LiteralType)
                a = Literal(token.subtype, token.value)
            case 1: # Identifier
                a = Variable(token.value)
        assert a is not None


        operand = stream.match_one(token_type=TokenType.OPERAND)
        if operand:
            b = Expression.from_token_stream(stream)
            assert isinstance(operand.subtype, OperandType)
            return Operand(a, b, operand.subtype)
        else:
            return a

class Variable(Expression):
    def __init__(self, name) -> None:
        super().__init__()
        self.name = name

class Literal(Expression):
    def __init__(self, literal_type: LiteralType, value: Any) -> None:
        super().__init__()
        self.literal_type = literal_type
        self.value = value


class Operand(Expression):
    def __init__(self, a: Expression, b: Expression, operand: OperandType) -> None:
        super().__init__()
        self.a = a
        self.b = b
        self.operand = operand


def parse(tokens: list[Token]) -> AbstractSyntaxTree:
    token_stream = TokenStream(tokens)
    ast = AbstractSyntaxTree.from_token_stream(token_stream)
    return ast

