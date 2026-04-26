from typing import Any, Optional

class AbstractTreeNode:
    def __init__(self, parent: AbstractTreeNode | None) -> None:
        self.parent = parent

    def create_child(self, child_class: type[AbstractTreeNode], *child_data: Any) -> AbstractTreeNode:
        child = child_class(*child_data, parent=self)
        return child



class AbstractSyntaxTree(AbstractTreeNode):
    def __init__(self):
        super().__init__([], None)

    def add_func(self, func):
        pass

class Statement(DictLikeTreeNode):
    pass

class Code(ListLikeTreeNode):
    def __init__(self, statements: list[Statement], parent: AbstractTreeNode):
        super().__init__(statements, parent)
        self.statements = statements

class Function(ListLikeTreeNode):
    pass