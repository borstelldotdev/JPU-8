from lexer import Lexer
from parser import parse

def test():
    with open("examples/test.jcsr", "r", encoding="utf-8") as file:
        data = file.read()

    tokens = Lexer.tokenize(data)


    ast = parse(tokens)
    print(ast)

if __name__ == "__main__":
    test()