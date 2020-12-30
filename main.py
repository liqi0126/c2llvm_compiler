import sys
from antlr4 import *
from antlr4.tree.Trees import Trees

from compiler.CLexer import CLexer
from compiler.CParser import CParser
from compiler.myCVisitor import ToLLVMVisitor

def main(argv):
    input = FileStream(argv[1])
    lexer = CLexer(input)
    stream = CommonTokenStream(lexer)
    stream.fill()

    # print('token:')
    # print([token.type for token in stream.tokens][:-1])

    parser = CParser(stream)

    tree = parser.compilationUnit()
    # print('tree:')
    # print(Trees.toStringTree(tree, None, parser))

    visitor = ToLLVMVisitor()
    visitor.visit(tree)

    with open('test.ll', 'w', encoding='utf-8') as f:
        f.write(visitor.output())


if __name__ == '__main__':
    main(sys.argv)
