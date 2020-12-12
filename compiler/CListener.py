# Generated from compiler/C.g4 by ANTLR 4.9
from antlr4 import *
if __name__ is not None and "." in __name__:
    from .CParser import CParser
else:
    from CParser import CParser

# This class defines a complete listener for a parse tree produced by CParser.
class CListener(ParseTreeListener):

    # Enter a parse tree produced by CParser#program.
    def enterProgram(self, ctx:CParser.ProgramContext):
        pass

    # Exit a parse tree produced by CParser#program.
    def exitProgram(self, ctx:CParser.ProgramContext):
        pass


    # Enter a parse tree produced by CParser#includeStatement.
    def enterIncludeStatement(self, ctx:CParser.IncludeStatementContext):
        pass

    # Exit a parse tree produced by CParser#includeStatement.
    def exitIncludeStatement(self, ctx:CParser.IncludeStatementContext):
        pass


    # Enter a parse tree produced by CParser#library.
    def enterLibrary(self, ctx:CParser.LibraryContext):
        pass

    # Exit a parse tree produced by CParser#library.
    def exitLibrary(self, ctx:CParser.LibraryContext):
        pass


    # Enter a parse tree produced by CParser#declareStatement.
    def enterDeclareStatement(self, ctx:CParser.DeclareStatementContext):
        pass

    # Exit a parse tree produced by CParser#declareStatement.
    def exitDeclareStatement(self, ctx:CParser.DeclareStatementContext):
        pass


    # Enter a parse tree produced by CParser#definitionStatement.
    def enterDefinitionStatement(self, ctx:CParser.DefinitionStatementContext):
        pass

    # Exit a parse tree produced by CParser#definitionStatement.
    def exitDefinitionStatement(self, ctx:CParser.DefinitionStatementContext):
        pass


    # Enter a parse tree produced by CParser#structDefinitionStatement.
    def enterStructDefinitionStatement(self, ctx:CParser.StructDefinitionStatementContext):
        pass

    # Exit a parse tree produced by CParser#structDefinitionStatement.
    def exitStructDefinitionStatement(self, ctx:CParser.StructDefinitionStatementContext):
        pass


    # Enter a parse tree produced by CParser#structIdentifier.
    def enterStructIdentifier(self, ctx:CParser.StructIdentifierContext):
        pass

    # Exit a parse tree produced by CParser#structIdentifier.
    def exitStructIdentifier(self, ctx:CParser.StructIdentifierContext):
        pass


    # Enter a parse tree produced by CParser#structParam.
    def enterStructParam(self, ctx:CParser.StructParamContext):
        pass

    # Exit a parse tree produced by CParser#structParam.
    def exitStructParam(self, ctx:CParser.StructParamContext):
        pass


    # Enter a parse tree produced by CParser#functionStatement.
    def enterFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        pass

    # Exit a parse tree produced by CParser#functionStatement.
    def exitFunctionStatement(self, ctx:CParser.FunctionStatementContext):
        pass


    # Enter a parse tree produced by CParser#funcParameters.
    def enterFuncParameters(self, ctx:CParser.FuncParametersContext):
        pass

    # Exit a parse tree produced by CParser#funcParameters.
    def exitFuncParameters(self, ctx:CParser.FuncParametersContext):
        pass


    # Enter a parse tree produced by CParser#funcParameter.
    def enterFuncParameter(self, ctx:CParser.FuncParameterContext):
        pass

    # Exit a parse tree produced by CParser#funcParameter.
    def exitFuncParameter(self, ctx:CParser.FuncParameterContext):
        pass


    # Enter a parse tree produced by CParser#compoundStatement.
    def enterCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        pass

    # Exit a parse tree produced by CParser#compoundStatement.
    def exitCompoundStatement(self, ctx:CParser.CompoundStatementContext):
        pass


    # Enter a parse tree produced by CParser#blockItemList.
    def enterBlockItemList(self, ctx:CParser.BlockItemListContext):
        pass

    # Exit a parse tree produced by CParser#blockItemList.
    def exitBlockItemList(self, ctx:CParser.BlockItemListContext):
        pass


    # Enter a parse tree produced by CParser#statement.
    def enterStatement(self, ctx:CParser.StatementContext):
        pass

    # Exit a parse tree produced by CParser#statement.
    def exitStatement(self, ctx:CParser.StatementContext):
        pass


    # Enter a parse tree produced by CParser#primaryExpression.
    def enterPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        pass

    # Exit a parse tree produced by CParser#primaryExpression.
    def exitPrimaryExpression(self, ctx:CParser.PrimaryExpressionContext):
        pass


    # Enter a parse tree produced by CParser#postfixExpression.
    def enterPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        pass

    # Exit a parse tree produced by CParser#postfixExpression.
    def exitPostfixExpression(self, ctx:CParser.PostfixExpressionContext):
        pass


    # Enter a parse tree produced by CParser#argumentExpressionList.
    def enterArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        pass

    # Exit a parse tree produced by CParser#argumentExpressionList.
    def exitArgumentExpressionList(self, ctx:CParser.ArgumentExpressionListContext):
        pass


    # Enter a parse tree produced by CParser#unaryExpression.
    def enterUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass

    # Exit a parse tree produced by CParser#unaryExpression.
    def exitUnaryExpression(self, ctx:CParser.UnaryExpressionContext):
        pass


    # Enter a parse tree produced by CParser#unaryOperator.
    def enterUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        pass

    # Exit a parse tree produced by CParser#unaryOperator.
    def exitUnaryOperator(self, ctx:CParser.UnaryOperatorContext):
        pass


    # Enter a parse tree produced by CParser#castExpression.
    def enterCastExpression(self, ctx:CParser.CastExpressionContext):
        pass

    # Exit a parse tree produced by CParser#castExpression.
    def exitCastExpression(self, ctx:CParser.CastExpressionContext):
        pass


    # Enter a parse tree produced by CParser#multiplicativeExpression.
    def enterMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        pass

    # Exit a parse tree produced by CParser#multiplicativeExpression.
    def exitMultiplicativeExpression(self, ctx:CParser.MultiplicativeExpressionContext):
        pass


    # Enter a parse tree produced by CParser#additiveExpression.
    def enterAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        pass

    # Exit a parse tree produced by CParser#additiveExpression.
    def exitAdditiveExpression(self, ctx:CParser.AdditiveExpressionContext):
        pass


    # Enter a parse tree produced by CParser#shiftExpression.
    def enterShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        pass

    # Exit a parse tree produced by CParser#shiftExpression.
    def exitShiftExpression(self, ctx:CParser.ShiftExpressionContext):
        pass


    # Enter a parse tree produced by CParser#relationalExpression.
    def enterRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        pass

    # Exit a parse tree produced by CParser#relationalExpression.
    def exitRelationalExpression(self, ctx:CParser.RelationalExpressionContext):
        pass


    # Enter a parse tree produced by CParser#equalityExpression.
    def enterEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        pass

    # Exit a parse tree produced by CParser#equalityExpression.
    def exitEqualityExpression(self, ctx:CParser.EqualityExpressionContext):
        pass


    # Enter a parse tree produced by CParser#andExpression.
    def enterAndExpression(self, ctx:CParser.AndExpressionContext):
        pass

    # Exit a parse tree produced by CParser#andExpression.
    def exitAndExpression(self, ctx:CParser.AndExpressionContext):
        pass


    # Enter a parse tree produced by CParser#exclusiveOrExpression.
    def enterExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by CParser#exclusiveOrExpression.
    def exitExclusiveOrExpression(self, ctx:CParser.ExclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by CParser#inclusiveOrExpression.
    def enterInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        pass

    # Exit a parse tree produced by CParser#inclusiveOrExpression.
    def exitInclusiveOrExpression(self, ctx:CParser.InclusiveOrExpressionContext):
        pass


    # Enter a parse tree produced by CParser#logicalAndExpression.
    def enterLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        pass

    # Exit a parse tree produced by CParser#logicalAndExpression.
    def exitLogicalAndExpression(self, ctx:CParser.LogicalAndExpressionContext):
        pass


    # Enter a parse tree produced by CParser#logicalOrExpression.
    def enterLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        pass

    # Exit a parse tree produced by CParser#logicalOrExpression.
    def exitLogicalOrExpression(self, ctx:CParser.LogicalOrExpressionContext):
        pass


    # Enter a parse tree produced by CParser#conditionalExpression.
    def enterConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        pass

    # Exit a parse tree produced by CParser#conditionalExpression.
    def exitConditionalExpression(self, ctx:CParser.ConditionalExpressionContext):
        pass


    # Enter a parse tree produced by CParser#assignmentExpression.
    def enterAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        pass

    # Exit a parse tree produced by CParser#assignmentExpression.
    def exitAssignmentExpression(self, ctx:CParser.AssignmentExpressionContext):
        pass


    # Enter a parse tree produced by CParser#assignmentOperator.
    def enterAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        pass

    # Exit a parse tree produced by CParser#assignmentOperator.
    def exitAssignmentOperator(self, ctx:CParser.AssignmentOperatorContext):
        pass


    # Enter a parse tree produced by CParser#expression.
    def enterExpression(self, ctx:CParser.ExpressionContext):
        pass

    # Exit a parse tree produced by CParser#expression.
    def exitExpression(self, ctx:CParser.ExpressionContext):
        pass


    # Enter a parse tree produced by CParser#expressionStatement.
    def enterExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        pass

    # Exit a parse tree produced by CParser#expressionStatement.
    def exitExpressionStatement(self, ctx:CParser.ExpressionStatementContext):
        pass


    # Enter a parse tree produced by CParser#selectionStatement.
    def enterSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        pass

    # Exit a parse tree produced by CParser#selectionStatement.
    def exitSelectionStatement(self, ctx:CParser.SelectionStatementContext):
        pass


    # Enter a parse tree produced by CParser#ifStatement.
    def enterIfStatement(self, ctx:CParser.IfStatementContext):
        pass

    # Exit a parse tree produced by CParser#ifStatement.
    def exitIfStatement(self, ctx:CParser.IfStatementContext):
        pass


    # Enter a parse tree produced by CParser#iterationStatement.
    def enterIterationStatement(self, ctx:CParser.IterationStatementContext):
        pass

    # Exit a parse tree produced by CParser#iterationStatement.
    def exitIterationStatement(self, ctx:CParser.IterationStatementContext):
        pass


    # Enter a parse tree produced by CParser#whileStatement.
    def enterWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#whileStatement.
    def exitWhileStatement(self, ctx:CParser.WhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#doWhileStatement.
    def enterDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass

    # Exit a parse tree produced by CParser#doWhileStatement.
    def exitDoWhileStatement(self, ctx:CParser.DoWhileStatementContext):
        pass


    # Enter a parse tree produced by CParser#forStatement.
    def enterForStatement(self, ctx:CParser.ForStatementContext):
        pass

    # Exit a parse tree produced by CParser#forStatement.
    def exitForStatement(self, ctx:CParser.ForStatementContext):
        pass


    # Enter a parse tree produced by CParser#forCondition.
    def enterForCondition(self, ctx:CParser.ForConditionContext):
        pass

    # Exit a parse tree produced by CParser#forCondition.
    def exitForCondition(self, ctx:CParser.ForConditionContext):
        pass


    # Enter a parse tree produced by CParser#forDeclaration.
    def enterForDeclaration(self, ctx:CParser.ForDeclarationContext):
        pass

    # Exit a parse tree produced by CParser#forDeclaration.
    def exitForDeclaration(self, ctx:CParser.ForDeclarationContext):
        pass


    # Enter a parse tree produced by CParser#forExpression.
    def enterForExpression(self, ctx:CParser.ForExpressionContext):
        pass

    # Exit a parse tree produced by CParser#forExpression.
    def exitForExpression(self, ctx:CParser.ForExpressionContext):
        pass


    # Enter a parse tree produced by CParser#jumpStatement.
    def enterJumpStatement(self, ctx:CParser.JumpStatementContext):
        pass

    # Exit a parse tree produced by CParser#jumpStatement.
    def exitJumpStatement(self, ctx:CParser.JumpStatementContext):
        pass


    # Enter a parse tree produced by CParser#typeSpecifier.
    def enterTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        pass

    # Exit a parse tree produced by CParser#typeSpecifier.
    def exitTypeSpecifier(self, ctx:CParser.TypeSpecifierContext):
        pass


    # Enter a parse tree produced by CParser#preservedTypeSpecifier.
    def enterPreservedTypeSpecifier(self, ctx:CParser.PreservedTypeSpecifierContext):
        pass

    # Exit a parse tree produced by CParser#preservedTypeSpecifier.
    def exitPreservedTypeSpecifier(self, ctx:CParser.PreservedTypeSpecifierContext):
        pass


    # Enter a parse tree produced by CParser#structSpecifier.
    def enterStructSpecifier(self, ctx:CParser.StructSpecifierContext):
        pass

    # Exit a parse tree produced by CParser#structSpecifier.
    def exitStructSpecifier(self, ctx:CParser.StructSpecifierContext):
        pass


    # Enter a parse tree produced by CParser#arrayIdentifier.
    def enterArrayIdentifier(self, ctx:CParser.ArrayIdentifierContext):
        pass

    # Exit a parse tree produced by CParser#arrayIdentifier.
    def exitArrayIdentifier(self, ctx:CParser.ArrayIdentifierContext):
        pass


    # Enter a parse tree produced by CParser#arrayItem.
    def enterArrayItem(self, ctx:CParser.ArrayItemContext):
        pass

    # Exit a parse tree produced by CParser#arrayItem.
    def exitArrayItem(self, ctx:CParser.ArrayItemContext):
        pass



del CParser