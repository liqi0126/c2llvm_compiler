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

        self._continue = None
        self._break = None

    # Visit a parse tree produced by CParser#program.
    # TODO: xuyihao
    def visitProgram(self, ctx: CParser.ProgramContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#includeStatement.
    # TODO: xuyihao
    def visitIncludeStatement(self, ctx: CParser.IncludeStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#library.
    # TODO: xuyihao
    def visitLibrary(self, ctx: CParser.LibraryContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#declareStatement.
    # TODO: xuyihao
    def visitDeclareStatement(self, ctx: CParser.DeclareStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#definitionStatement.
    # TODO: xuyihao
    def visitDefinitionStatement(self, ctx: CParser.DefinitionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#structDefinitionStatement.
    # TODO: xuyihao
    def visitStructDefinitionStatement(self, ctx: CParser.StructDefinitionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#structIdentifier.
    # TODO: xuyihao
    def visitStructIdentifier(self, ctx: CParser.StructIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#structParam.
    # TODO: xuyihao
    def visitStructParam(self, ctx: CParser.StructParamContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#functionStatement.
    # TODO: xuyihao
    def visitFunctionStatement(self, ctx: CParser.FunctionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#funcParameters.
    # TODO: xuyihao
    def visitFuncParameters(self, ctx: CParser.FuncParametersContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#funcParameter.
    # TODO: xuyihao
    def visitFuncParameter(self, ctx: CParser.FuncParameterContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#compoundStatement.
    # TODO: xuyihao
    def visitCompoundStatement(self, ctx: CParser.CompoundStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#blockItemList.
    # TODO: xuyihao
    def visitBlockItemList(self, ctx: CParser.BlockItemListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#statement.
    # TODO: xuyihao
    def visitStatement(self, ctx: CParser.StatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#primaryExpression.
    # TODO: dingyifeng
    def visitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#postfixExpression.
    # TODO: dingyifeng
    def visitPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#argumentExpressionList.
    # TODO: dingyifeng
    def visitArgumentExpressionList(self, ctx: CParser.ArgumentExpressionListContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryExpression.
    # TODO: dingyifeng
    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#unaryOperator.
    # TODO: dingyifeng
    def visitUnaryOperator(self, ctx: CParser.UnaryOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#castExpression.
    # TODO: dingyifeng
    def visitCastExpression(self, ctx: CParser.CastExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#multiplicativeExpression.
    # TODO: dingyifeng
    def visitMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#additiveExpression.
    # TODO: dingyifeng
    def visitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#shiftExpression.
    # TODO: dingyifeng
    def visitShiftExpression(self, ctx: CParser.ShiftExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#relationalExpression.
    # TODO: dingyifeng
    def visitRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#equalityExpression.
    # TODO: dingyifeng
    def visitEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#andExpression.
    # TODO: dingyifeng
    def visitAndExpression(self, ctx: CParser.AndExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#exclusiveOrExpression.
    # TODO: dingyifeng
    def visitExclusiveOrExpression(self, ctx: CParser.ExclusiveOrExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#inclusiveOrExpression.
    # TODO: dingyifeng
    def visitInclusiveOrExpression(self, ctx: CParser.InclusiveOrExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#logicalAndExpression.
    # TODO: dingyifeng
    def visitLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#logicalOrExpression.
    # TODO: dingyifeng
    def visitLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#conditionalExpression.
    # TODO: dingyifeng
    def visitConditionalExpression(self, ctx: CParser.ConditionalExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#assignmentExpression.
    def visitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        # TODO: dingyifeng
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#assignmentOperator.
    # TODO: dingyifeng
    def visitAssignmentOperator(self, ctx: CParser.AssignmentOperatorContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#expression.
    # TODO: dingyifeng
    def visitExpression(self, ctx: CParser.ExpressionContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#expressionStatement.
    # TODO: dingyifeng
    def visitExpressionStatement(self, ctx: CParser.ExpressionStatementContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#selectionStatement.
    # DONE: dingyifeng
    def visitSelectionStatement(self, ctx: CParser.SelectionStatementContext):
        if ctx.ifStatement():
            return self.visitIfStatement(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#ifStatement.
    # DONE: xuyihao
    def visitIfStatement(self, ctx: CParser.IfStatementContext):
        block_name = self.builder.block.name
        if_block = self.builder.block.append_basic_block(name='{}.if'.format(block_name))
        stat_block = self.builder.block.append_basic_block(name='{}.stat'.format(block_name))
        branch_num = len(ctx.statement())
        if branch_num >= 2:
            else_block = self.builder.block.append_basic_block(name='{}.else'.format(block_name))
            end_block = self.builder.block.append_basic_block(name='{}.end'.format(block_name))
            try:
                self.builder.branch(if_block)
            except:
                print('visitIfStatement if_block except!\n')
                pass

            self.builder.position_at_start(if_block)
            if_expression_val = self.visit(ctx.expression())
            self.builder.cbranch(if_expression_val, stat_block, else_block)
            self.builder.position_at_start(stat_block)
            self.symbol_table.enter_scope()
            self.visit(ctx.statement()[0])
            self.symbol_table.quit_scope()

            try:
                self.builder.branch(end_block)
            except:
                print('visitIfStatement if_block except!\n')
                pass

            self.builder.position_at_start(else_block)
            self.symbol_table.enter_scope()
            self.visit(ctx.statement()[1])
            self.symbol_table.quit_scope()
            try:
                self.builder.branch(end_block)
            except:
                print('visitIfStatement if_block except!\n')
                pass
            self.builder.position_at_start(end_block)
        else:
            end_block = self.builder.block.append_basic_block(name='{}.end'.format(block_name))

            self.builder.branch(if_block)
            self.builder.position_at_start(if_block)
            if_expression_val = self.visit(ctx.expression())

            self.builder.cbranch(if_expression_val, stat_block, end_block)
            self.builder.position_at_start(stat_block)
            self.symbol_table.enter_scope()
            self.visit(ctx.statement()[0])
            self.symbol_table.quit_scope()

            self.builder.branch(end_block)
            self.builder.position_at_start(end_block)


    # Visit a parse tree produced by CParser#iterationStatement.
    # DONE: xuyihao
    def visitIterationStatement(self, ctx: CParser.IterationStatementContext):
        if ctx.whileStatement():
            return self.visitWhileStatement(ctx)
        elif ctx.doWhileStatement():
            return self.visitDoWhileStatement(ctx)
        elif ctx.forStatement():
            return self.visitForStatement(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#whileStatement.
    # DONE: xuyihao
    def visitWhileStatement(self, ctx: CParser.WhileStatementContext):

        block_name = self.builder.block.name
        cond_block = self.builder.append_basic_block(name="{}.cond".format(block_name))     # while的条件部分
        stat_block = self.builder.append_basic_block(name="{}.stat".format(block_name))     # while的主函数体部分
        end_block = self.builder.append_basic_block(name="{}.end".format(block_name))       # while的结束部分

        temp_continue = self._continue
        temp_break = self._break
        self._continue = cond_block
        self._break = end_block

        self.builder.branch(cond_block)
        self.builder.position_at_start(cond_block)
        cond_val = self.visit(ctx.expression())
        self.symbol_table.enter_scope()

        self.builder.cbranch(cond_val, stat_block, end_block)
        self.builder.position_at_start(stat_block)
        self.visit(ctx.statement())

        # 尝试再次访问开头？
        try:
            self.builder.branch(cond_block)
        except:
            print('visitWhileStatement except!\n')
            pass

        self.builder.position_at_start(end_block)

        self.symbol_table.quit_scope()
        self._continue, self._break = temp_continue, temp_break

    # Visit a parse tree produced by CParser#doWhileStatement.
    # TODO: xuyihao
    def visitDoWhileStatement(self, ctx: CParser.DoWhileStatementContext):
        block_name = self.builder.block.name
        do_block = self.builder.append_basic_block(name="{}.do".format(block_name))
        stat_block = self.builder.append_basic_block(name="{}.stat".format(block_name))
        cond_block = self.builder.append_basic_block(name="{}.cond".format(block_name))
        end_block = self.builder.append_basic_block(name="{}.end".format(block_name))

        temp_continue = self._continue
        temp_break = self._break
        self._continue = cond_block
        self._break = end_block

        

        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forStatement.
    # DONE: xuyihao
    def visitForStatement(self, ctx: CParser.ForStatementContext):
        self.symbol_table.enter_scope()

        block_name = self.builder.block.name
        cond_block = self.builder.append_basic_block(name='{}.cond'.format(block_name))
        stat_block = self.builder.append_basic_block(name='{}.stat'.format(block_name))
        end_block = self.builder.append_basic_block(name='{}.end'.format(block_name))

        # SLN
        temp_continue = self._continue
        temp_break = self._break
        self._continue = cond_block
        self._break = end_block

        condition_expression, expression = self.visit(ctx.forCondition())
        self.builder.branch(cond_block)
        self.builder.position_at_start(cond_block)
        for_condition = self.visit(condition_expression)
        self.builder.cbranch(for_condition, stat_block, end_block)
        self.builder.position_at_start(stat_block)
        self.visit(ctx.statement())
        if expression:
            self.visit(expression)
        self.builder.branch(cond_block) # 试试不加try
        self.builder.position_at_start(end_block)
        self._continue = temp_continue
        self._break = temp_break

        self.symbol_table.quit_scope()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forCondition.
    # DONE: xuyihao
    def visitForCondition(self, ctx: CParser.ForConditionContext):
        if ctx.forDeclaration():
            self.visit(ctx.forDeclaration())
        elif ctx.expression():
            self.visit(ctx.expression())
        return ctx.forExpression(0), ctx.forExpression(1)

    # Visit a parse tree produced by CParser#forDeclaration.
    # TODO: xuyihao
    def visitForDeclaration(self, ctx: CParser.ForDeclarationContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#forExpression.
    # TODO: xuyihao
    def visitForExpression(self, ctx: CParser.ForExpressionContext):

        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#jumpStatement.
    # DONE: xuyihao
    def visitJumpStatement(self, ctx: CParser.JumpStatementContext):
        if ctx.Continue():
            if self._continue:
                self.builder.branch(self._continue)
            else:
                raise Exception()
        elif ctx.Return():
            if ctx.expression():
                ret_value = self.visit(ctx.expression())
                try:
                    self.builder.ret(ret_value)
                except:
                    pass
            else:
                try:
                    self.builder.ret_void()
                except:
                    pass

        elif ctx.Break():
            if self._break:
                self.builder.branch(self._break)
            else:
                raise Exception()
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#typeSpecifier.
    # DONE: xuyihao
    def visitTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        if ctx.preservedTypeSpecifier():
            return self.visitPreservedTypeSpecifier(ctx)
        elif ctx.structSpecifier():
            return self.visitStructSpecifier(ctx)
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#preservedTypeSpecifier.
    # DONE: xuyihao
    def visitPreservedTypeSpecifier(self, ctx: CParser.PreservedTypeSpecifierContext):
        if ctx.Int():
            return {'int': self.INT_TYPE}.get(ctx.getText())
        elif ctx.Double():
            return {'double': self.DOUBLE_TYPE}.get(ctx.getText())
        elif ctx.Char():
            return {'float': self.FLOAT_TYPE}.get(ctx.getText())
        elif ctx.Float():
            return {'char': self.CHAR_TYPE}.get(ctx.getText())
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#structSpecifier.
    # TODO: xuyihao
    def visitStructSpecifier(self, ctx: CParser.StructSpecifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#arrayIdentifier.
    # TODO: xuyihao
    def visitArrayIdentifier(self, ctx: CParser.ArrayIdentifierContext):
        return self.visitChildren(ctx)

    # Visit a parse tree produced by CParser#arrayItem.
    # TODO: xuyihao
    def visitArrayItem(self, ctx: CParser.ArrayItemContext):
        return self.visitChildren(ctx)

    def output(self):
        pass


del CParser
