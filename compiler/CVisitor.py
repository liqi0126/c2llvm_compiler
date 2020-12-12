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
    def visitProgram(self, ctx:CParser.ProgramContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#includeStatement.
    def visitIncludeStatement(self, ctx:CParser.IncludeStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#library.
    def visitLibrary(self, ctx:CParser.LibraryContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#declareStatement.
    def visitDeclareStatement(self, ctx:CParser.DeclareStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#definitionStatement.
    def visitDefinitionStatement(self, ctx:CParser.DefinitionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structDefinitionStatement.
    def visitStructDefinitionStatement(self, ctx:CParser.StructDefinitionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structIdentifier.
    def visitStructIdentifier(self, ctx:CParser.StructIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structParam.
    def visitStructParam(self, ctx:CParser.StructParamContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#functionStatement.
    def visitFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#funcParameters.
    def visitFuncParameters(self, ctx:CParser.FuncParametersContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#funcParameter.
    def visitFuncParameter(self, ctx:CParser.FuncParameterContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#compoundStatement.
    def visitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#blockItemList.
    def visitBlockItemList(self, ctx:CParser.BlockItemListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#statement.
    def visitStatement(self, ctx:CParser.StatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#primaryExpression.
    def visitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#postfixExpression.
    def visitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#argumentExpressionList.
    def visitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryExpression.
    def visitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#unaryOperator.
    def visitUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#castExpression.
    def visitCastExpression(self, ctx:CParser.CastExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#multiplicativeExpression.
    def visitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#additiveExpression.
    def visitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#shiftExpression.
    def visitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#relationalExpression.
    def visitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#equalityExpression.
    def visitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#andExpression.
    def visitAndExpression(self, ctx:CParser.AndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#exclusiveOrExpression.
    def visitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#inclusiveOrExpression.
    def visitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalAndExpression.
    def visitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#logicalOrExpression.
    def visitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#conditionalExpression.
    def visitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#assignmentOperator.
    def visitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expression.
    def visitExpression(self, ctx:CParser.ExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#expressionStatement.
    def visitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#selectionStatement.
    def visitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#ifStatement.
    def visitIfStatement(self, ctx:CParser.IfStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#iterationStatement.
    def visitIterationStatement(self, ctx:CParser.IterationStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#whileStatement.
    def visitWhileStatement(self, ctx:CParser.WhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#doWhileStatement.
    def visitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forStatement.
    def visitForStatement(self, ctx:CParser.ForStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forCondition.
    def visitForCondition(self, ctx:CParser.ForConditionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forDeclaration.
    def visitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#forExpression.
    def visitForExpression(self, ctx:CParser.ForExpressionContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#jumpStatement.
    def visitJumpStatement(self, ctx:CParser.JumpStatementContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#typeSpecifier.
    def visitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#preservedTypeSpecifier.
    def visitPreservedTypeSpecifier(self, ctx:CParser.PreservedTypeSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#structSpecifier.
    def visitStructSpecifier(self, ctx:CParser.StructSpecifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arrayIdentifier.
    def visitArrayIdentifier(self, ctx:CParser.ArrayIdentifierContext):
        return self.visitChildren(ctx)


    # Visit a parse tree produced by CParser#arrayItem.
    def visitArrayItem(self, ctx:CParser.ArrayItemContext):
        return self.visitChildren(ctx)


    def output(self):
        pass

del CParser