from typing import Any, Optional
from abc import ABC, abstractmethod

class AbstractTreeNode(ABC):
    @abstractmethod
    def __init__(self, data: Any, parent: AbstractTreeNode | None) -> None:
        raise NotImplementedError

    @abstractmethod
    def get_child(self, key) -> AbstractTreeNode | None:
        raise NotImplementedError

    @abstractmethod
    def get_children(self) -> list[AbstractTreeNode] | dict[Any, AbstractTreeNode]:
        raise NotImplementedError

    @abstractmethod
    def create_child(self, child_class: type[AbstractTreeNode], child_data: Any,
                     key: Optional[Any] = None) -> AbstractTreeNode:
        raise NotImplementedError



class ListLikeTreeNode(AbstractTreeNode):
    def __init__(self, data, parent: AbstractTreeNode | None):
        self.data = data
        self.parent: AbstractTreeNode | None = parent
        self.children: list[AbstractTreeNode] = []

    def get_child(self, key) -> AbstractTreeNode | None:
        return self.children[key]

    def get_children(self) -> list[AbstractTreeNode]:
        return self.children

    def create_child(self, child_class: type[AbstractTreeNode], child_data: Any,
                     key: Optional[Any] = None) -> AbstractTreeNode:
        child = child_class(child_data, parent=self)
        self.children.append(child)
        return child



class DictLikeTreeNode(AbstractTreeNode):
    def __init__(self, data, parent: AbstractTreeNode | None):
        self.data = data
        self.parent: AbstractTreeNode | None = parent
        self.children: dict[Any, AbstractTreeNode] = {}

    def get_child(self, key) -> AbstractTreeNode | None:
        return self.children[key]

    def get_children(self) -> dict[Any, AbstractTreeNode]:
        return self.children

    def create_child(self, child_class: type[AbstractTreeNode], child_data: Any,
                     key: Optional[Any] = None) -> AbstractTreeNode:
        child = child_class(child_data, parent=self)
        self.children[key] = child
        return child


class AbstractSyntaxTree(ListLikeTreeNode):
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