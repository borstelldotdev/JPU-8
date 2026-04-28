from src.compiler.parser import AbstractSyntaxTree, AbstractTreeNode

class CodeGenerator:
    def __init__(self, tree: AbstractSyntaxTree) -> None:
        self.tree: AbstractSyntaxTree = tree

    def recursive_visit(self, node: AbstractTreeNode):
        pass
