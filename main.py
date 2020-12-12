import sys
from antlr4 import *

from compiler.CLexer import CLexer
from compiler.CParser import CParser
from compiler.CVisitor import CVisitor


def main(argv):
    input = FileStream(argv[1])
    lexer = CLexer(input)
    stream = CommonTokenStream(lexer)
    parser = CParser(stream)
    tree = parser.program()
    visitor = CVisitor()

    try:
        visitor.visit(tree)
    except:
        print('compilation error!')
        exit(0)

    with open('test.ll', 'w', encoding='utf-8') as f:
        f.write(visitor.output())


if __name__ == '__main__':
    main(sys.argv)
