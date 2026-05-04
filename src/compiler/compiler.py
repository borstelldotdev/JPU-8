from parsing.lexer import Lexer
from src.compiler.parser import parse
from compiler.ast_optimizer import *


def compile(code: str):
    tokens = Lexer.tokenize(code)
    ast = parse(tokens)
    matcher = RecursiveMatcher.new(ast)
    optimized_ast = matcher.optimize()

    return ast.__repr__()

def test():
    with open("examples/test.jacscript", "r", encoding="utf-8") as file:
        data = file.read()

    ast = compile(data)

if __name__ == "__main__":
    test()