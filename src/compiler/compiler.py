from lexer import Lexer

if __name__ == "__main__":
    with open("examples/test.jcsr", "r") as file:
        data = file.read()

    tokens = Lexer.tokenize(data)

    for token in tokens:
        print(token)
