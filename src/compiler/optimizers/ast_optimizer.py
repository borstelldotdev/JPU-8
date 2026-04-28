from src.compiler.parser import *
from abc import ABC, abstractmethod

class AbstractPattern:
    @staticmethod
    @abstractmethod
    def match(node: AbstractTreeNode) -> AbstractTreeNode | None:
        raise NotImplementedError()



class RecursiveMatcher:
    def __init__(self, ast: AbstractSyntaxTree) -> None:
        self.ast = ast
        self.patterns: list[type[AbstractPattern]] = []
    
    def add_pattern(self, pattern: type[AbstractPattern]):
        self.patterns.append(pattern)
    
    def add_patterns(self, pattens: list[type[AbstractPattern]]):
        self.patterns.extend(pattens)

    def optimize(self):
        self.visit(self.ast)

    def visit(self, node: AbstractTreeNode):
        for child in range(len(node.child_nodes)):

            match, pattern = self.match_all(node.child_nodes[child])
            if match is not None:
                print(f"Found optimization for {type(node.child_nodes[child]).__name__}, using optimization {pattern}")
                node.child_nodes[child] = match
            self.visit(node.child_nodes[child])

    def match_all(self, node: AbstractTreeNode) -> tuple[AbstractTreeNode, type[AbstractPattern]] | tuple[None, None]:
        for patten in self.patterns:
            match = patten.match(node)
            if match is not None:
                return (match, patten)
        return (None, None)
    

    @classmethod
    def new(cls, ast: AbstractSyntaxTree) -> RecursiveMatcher:
        new = cls(ast)
        new.add_patterns([
            TwoLitterals
        ])

        return new

class TwoLitteralOperation(AbstractPattern):
    @staticmethod
    def match(node: AbstractTreeNode) -> AbstractTreeNode | None:
        if isinstance(node, Operand) and isinstance(node.a, Literal) and isinstance(node.b, Literal):
            match node.operand:
                case OperandType.PLUS:
                    return Literal(LiteralType.NUMBER, node.a.value + node.b.value)
                # TODO: Add more cases
        return None



