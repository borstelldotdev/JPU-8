from lexer import Lexer
from abstract_syntax_tree import AbstractSyntaxTree

def test_lexer():
    with open("examples/test.jcsr", "r") as file:
        data = file.read()

    tokens = Lexer.tokenize(data)

    for token in tokens:
        print(token)


if __name__ == "__main__":
    ast = AbstractSyntaxTree(None)
    ast.add_func("test")
    print()
    print(ast)
