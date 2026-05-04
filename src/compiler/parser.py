from abc import ABC, abstractmethod
from typing import Any
from enum import Enum, auto

from parsing.tokens import Token, TokenType, OperandType, KeywordType, LiteralType
from src.compiler.prettyprint import *


class AbstractTreeNode(ABC):
    def __init__(self) -> None:
        self.parent: AbstractTreeNode | None = None
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

class IdenifiableAbstractTreeNode(AbstractTreeNode):
    def __init__(self, name) -> None:
        super().__init__()
        self.identifier = name

    def add_to_scope(self):
        assert self.parent is not None
        par: AbstractTreeNode = self.parent
        while not isinstance(par, HasScope):
            assert par.parent is not None
            par = par.parent

class HasScope:
    def __init__(self) -> None:
        self.in_scope: dict[str, IdenifiableAbstractTreeNode] = {}
    
    def add_to_scope(self, identifiable: Idenifiable):
        assert identifiable.identifier is not None
        self.in_scope[identifiable.identifier] = identifiable


class AbstractSyntaxTree(AbstractTreeNode, HasScope):
    def __init__(self, entrypoint: str="main") -> None:
        super().__init__()
        self.entrypoint = entrypoint

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> AbstractSyntaxTree:
        new = cls()
        while not stream.is_empty():
            statement = Statement.from_token_stream(stream)

        return new

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


class CompoundStatement(Statement, HasScope):
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


class FunctionStatement(Statement, Idenifiable):
    def __init__(self, name: str, statement: Statement, arguments: list[str]) -> None:
        super(Statement, self).__init__()
        super(Idenifiable, self).__init__(name)
        
        self.statement = statement
        self.arguments = arguments
        self.add_child(statement)

    @classmethod
    def from_token_stream(cls, stream: TokenStream) -> FunctionStatement:
        identifier = stream.expect_one(token_type=TokenType.IDENTIFIER)
        stream.expect_one(token_type=TokenType.OPENING_PARENTHESIS)
        args = []

        while not stream.match_one(token_type=TokenType.CLOSING_PARENTHESIS):
            args.append(stream.expect_one(token_type=TokenType.IDENTIFIER))
            stream.match_one(token_type=TokenType.COMMA)
        statement = Statement.from_token_stream(stream)

        return cls(identifier.value, statement, args)



class ConditionType(Enum):
    EQUALITY = auto()
    NOT_EQUALITY = auto()

    GREATER_THAN = auto()
    LESS_THAN = auto()
    GREATER_THAN_OR_EQUAL = auto()
    LESS_THAN_OR_EQUAL = auto()


class Condition(AbstractTreeNode):
    def __init__(self) -> None:
        super().__init__()



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

