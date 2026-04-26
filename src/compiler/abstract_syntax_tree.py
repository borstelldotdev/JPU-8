from typing import Any, Optional

class AbstractTreeNode:
    def __init__(self, parent: AbstractTreeNode | None, *data) -> None:
        self.parent = parent

    def create_child(self, child_class: type[AbstractTreeNode], *child_data: Any) -> AbstractTreeNode | None:

        child = child_class(self, *child_data)
        return child

    @staticmethod
    def indent(text: str):
        lines = text.splitlines()
        lines = ["\t" + line for line in lines]
        return "\n".join(lines)

    @staticmethod
    def _repr_object(obj):
        if isinstance(obj, list) or isinstance(obj, tuple):
            return AbstractTreeNode._repr_iterable(obj)
        if isinstance(obj, dict):
            return AbstractTreeNode._repr_dict(obj)
        return obj.__repr__()

    @staticmethod
    def _repr_iterable(obj):
        vals = []
        for val in obj:
            vals.append(AbstractTreeNode._repr_object(val))
        return "\n" + AbstractTreeNode.indent("\n".join(vals))

    @staticmethod
    def _repr_dict(obj: dict):
        vals = []
        for val in obj:
            if val == "parent":
                continue

            vals.append(val + ": " + AbstractTreeNode._repr_object(obj[val]))

        return "\n" + AbstractTreeNode.indent("\n".join(vals))

    def __repr__(self):
        return f"{type(self).__name__}:{self._repr_dict(self.__dict__)}"



class AbstractSyntaxTree(AbstractTreeNode):
    def __init__(self, parent: AbstractTreeNode | None) -> None:
        super().__init__(parent)
        self.functions = {}
        self.entrypoint = "main"

    def add_func(self, *func_data):
        new: Optional[Function] = self.create_child(Function, *func_data)
        self.functions[new.name] = new


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

    class Assignment(Statement):
        pass


    class IgnoredExpression(AbstractExpression)

class Statement(AbstractTreeNode):
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