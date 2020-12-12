# Generated from compiler/C.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

from llvmlite import ir
from .structTable import StructTable
from .symbolTable import SymbolTable


# This class defines a complete generic visitor for a parse tree produced by CParser.

class CVisitor(ParseTreeVisitor):
    BASE_TYPE = 0
    ARRAY_TYPE = 1
    ARRAY_2D_TYPE = 4
    FUNCTION_TYPE = 2

    CHAR_TYPE = ir.IntType(8)
    INT_TYPE = ir.IntType(32)
    FLOAT_TYPE = ir.FloatType()
    DOUBLE_TYPE = ir.DoubleType()
    VOID_TYPE = ir.VoidType()
    BOOL_TYPE = ir.IntType(1)

    def __init__(self):
        self.module = ir.Module()
        self.builder = None
        self.struct_table = StructTable()
        self.symbol_table = SymbolTable()

    # Visit a parse tree produced by CParser#program.
    # TODO: xuyihao
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#includeStatement.
    # TODO: xuyihao
    def visitIncludeStatement(self, ctx:CParser.IncludeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#library.
    # TODO: xuyihao
    def visitLibrary(self, ctx:CParser.LibraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declareStatement.
    # TODO: xuyihao
    def visitDeclareStatement(self, ctx:CParser.DeclareStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#definitionStatement.
    # TODO: xuyihao
    def visitDefinitionStatement(self, ctx:CParser.DefinitionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDefinitionStatement.
    # TODO: xuyihao
    def visitStructDefinitionStatement(self, ctx:CParser.StructDefinitionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structIdentifier.
    # TODO: xuyihao
    def visitStructIdentifier(self, ctx:CParser.StructIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structParam.
    # TODO: xuyihao
    def visitStructParam(self, ctx:CParser.StructParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionStatement.
    # TODO: xuyihao
    def visitFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#funcParameters.
    # TODO: xuyihao
    def visitFuncParameters(self, ctx:CParser.FuncParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#funcParameter.
    # TODO: xuyihao
    def visitFuncParameter(self, ctx:CParser.FuncParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compoundStatement.
    # TODO: xuyihao
    def visitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItemList.
    # TODO: xuyihao
    def visitBlockItemList(self, ctx:CParser.BlockItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    # TODO: xuyihao
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#primaryExpression.
    # TODO: dingyifeng
    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixExpression.
    # TODO: dingyifeng
    def visitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentExpressionList.
    # TODO: dingyifeng
    def visitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    # TODO: dingyifeng
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryOperator.
    # TODO: dingyifeng
    def visitUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#castExpression.
    # TODO: dingyifeng
    def visitCastExpression(self, ctx:CParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicativeExpression.
    # TODO: dingyifeng
    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additiveExpression.
    # TODO: dingyifeng
    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#shiftExpression.
    # TODO: dingyifeng
    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relationalExpression.
    # TODO: dingyifeng
    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equalityExpression.
    # TODO: dingyifeng
    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#andExpression.
    # TODO: dingyifeng
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#exclusiveOrExpression.
    # TODO: dingyifeng
    def visitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#inclusiveOrExpression.
    # TODO: dingyifeng
    def visitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAndExpression.
    # TODO: dingyifeng
    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#logicalOrExpression.
    # TODO: dingyifeng
    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#conditionalExpression.
    # TODO: dingyifeng
    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
    # TODO: dingyifeng
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentOperator.
    # TODO: dingyifeng
    def visitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    # TODO: dingyifeng
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStatement.
    # TODO: dingyifeng
    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#selectionStatement.
    # TODO: dingyifeng
    def visitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#ifStatement.
    # TODO: xuyihao
    def visitIfStatement(self, ctx:CParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#iterationStatement.
    # TODO: xuyihao
    def visitIterationStatement(self, ctx:CParser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#whileStatement.
    # TODO: xuyihao
    def visitWhileStatement(self, ctx:CParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#doWhileStatement.
    # TODO: xuyihao
    def visitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forStatement.
    # TODO: xuyihao
    def visitForStatement(self, ctx:CParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forCondition.
    # TODO: xuyihao
    def visitForCondition(self, ctx:CParser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forDeclaration.
    # TODO: xuyihao
    def visitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forExpression.
    # TODO: xuyihao
    def visitForExpression(self, ctx:CParser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jumpStatement.
    # TODO: xuyihao
    def visitJumpStatement(self, ctx:CParser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifier.
    # TODO: xuyihao
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#preservedTypeSpecifier.
    # TODO: xuyihao
    def visitPreservedTypeSpecifier(self, ctx:CParser.PreservedTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structSpecifier.
    # TODO: xuyihao
    def visitStructSpecifier(self, ctx:CParser.StructSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arrayIdentifier.
    # TODO: xuyihao
    def visitArrayIdentifier(self, ctx:CParser.ArrayIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arrayItem.
    # TODO: xuyihao
    def visitArrayItem(self, ctx:CParser.ArrayItemContext):
        return self.visitChildren(ctx)


    def output(self):
        pass

del CParser