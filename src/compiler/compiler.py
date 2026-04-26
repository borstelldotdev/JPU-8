from lexer import Lexer
from abstract_syntax_tree import AbstractSyntaxTree

def test_lexer():
    with open("examples/test.jcsr", "r", encoding="utf-8") as file:
        data = file.read()

    tokens = Lexer.tokenize(data)

    for token in tokens:
        print(token)

def test_ast():
    ast = AbstractSyntaxTree(None)
    ast.add_func("test")
    print()
    print(ast)

if __name__ == "__main__":
    test_lexer()