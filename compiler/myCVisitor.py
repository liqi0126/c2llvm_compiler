# Generated from compiler/C.g4 by ANTLR 4.9
import re

from antlr4 import *

if __name__ is not None and "." in __name__:
    from .CParser import CParser
    from .CVisitor import CVisitor
else:
    from CParser import CParser
    from CVisitor import CVisitor


from llvmlite import ir
from .structTable import StructTable, FuncTable
from .symbolTable import SymbolTable, createTable


class SemanticError(Exception):
    """语义错误基类"""

    def __init__(self, msg, ctx=None):
        super().__init__()
        if ctx:
            self.line = ctx.start.line  # 错误出现位置
            self.column = ctx.start.column
        else:
            self.line = 0
            self.column = 0
        self.msg = msg

    def __str__(self):
        return "SemanticError: " + str(self.line) + ":" + str(self.column) + " " + self.msg


class ToLLVMVisitor(CVisitor):
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
        self.module.triple = "x86_64-pc-linux-gnu" # llvm.Target.from_default_triple()
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128" # llvm.create_mcjit_compiler(backing_mod, target_machine)

        self.builder = None
        self.symbol_table = SymbolTable(None)
        self.lst_continue = None
        self.lst_break = None
        self.func_table = FuncTable()
        self.struct_table = StructTable()
        self.struct_instance_ing = False  # 是否在实例化结构体

    def visitCompilationUnit(self, ctx):
        for i in ctx.children:
            self.visit(i)

    def visitFunctionDefinition(self, ctx):
        assert ctx.declarationList() == None
        _type = self.visit(ctx.declarationSpecifiers())
        name, params = self.visit(ctx.declarator())
        args = [i for i, j in params]
        fnty = ir.FunctionType(_type, args)
        func = ir.Function(self.module, fnty, name=name)
        block = func.append_basic_block(name="entry")
        self.builder = ir.IRBuilder(block)
        self.symbol_table.insert(name, value=func)
        self.symbol_table = createTable(self.symbol_table)
        func_args = func.args
        arg_names = [j for i, j in params]
        assert len(arg_names) == len(func_args)
        for seq, name in enumerate(arg_names):
            arg = func_args[seq]
            arg_ptr = self.builder.alloca(arg.type, name=name)
            self.builder.store(arg, arg_ptr)
            self.symbol_table.insert(name, value=arg_ptr)
        self.visit(ctx.compoundStatement())
        if _type == self.VOID_TYPE:
            try:
                self.builder.ret_void()
            except:
                pass
        self.symbol_table = self.symbol_table.getFather()

    def visitDeclarator(self, ctx: CParser.DeclaratorContext):
        return self.visit(ctx.directDeclarator())

    def visitDirectDeclarator(self, ctx: CParser.DirectDeclaratorContext):
        if ctx.Identifier():
            name = self.visit(ctx.Identifier())
            btype = (self.BASE_TYPE, None)
            self.symbol_table.insert(name, btype)
            return name
        elif ctx.children[1].getText() == '[':
            name = self.visit(ctx.directDeclarator())
            if self.symbol_table.getType(name) is not None and self.symbol_table.getValue(name) is None:
                # 二维数组的情况
                btype, length = self.symbol_table.getType(name)
                if btype == self.ARRAY_TYPE:
                    first_dimension = length
                    second_dimension = self.visit(ctx.assignmentExpression())
                    dim = (first_dimension, second_dimension)
                    btype = (self.ARRAY_2D_TYPE, dim)
                    self.symbol_table.insert(name, btype=btype)
                    return name

            # 普通一维数组
            length = self.visit(ctx.assignmentExpression())
            btype = (self.ARRAY_TYPE, length)
            self.symbol_table.insert(name, btype=btype)
            return name
        elif ctx.children[1].getText() == '(':
            name = self.visit(ctx.directDeclarator())
            btype = (self.FUNCTION_TYPE, None)
            self.symbol_table.insert(name, btype)
            if ctx.parameterTypeList():
                params = self.visit(ctx.parameterTypeList())
            else:
                params = []
            return name, params

    def visitTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        if ctx.pointer():
            _type = self.visit(ctx.typeSpecifier())
            return ir.PointerType(_type)
        elif ctx.structOrUnionSpecifier():
            return self.visit(ctx.structOrUnionSpecifier())
        elif ctx.typedefName():
            return self.visit(ctx.typedefName())
        else:
            _type = {
                'int': self.INT_TYPE,
                'char': self.CHAR_TYPE,
                'float': self.FLOAT_TYPE,
                'double': self.DOUBLE_TYPE,
                'void': self.VOID_TYPE
            }.get(ctx.getText())
            return _type

    def visitStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        if ctx.structDeclarationList():
            # 结构本身的声明/定义
            label_ = self.visit(ctx.structOrUnion())
            if label_ == 'struct':
                # 结构体
                if ctx.Identifier():
                    # 非匿名结构
                    struct_name = ctx.Identifier().getText()
                    if self.symbol_table.getValue(struct_name):
                        # 重定义
                        print("Redefintion error!")
                    else:
                        self.is_defining_struct = struct_name
                        tmp_list = self.visit(ctx.structDeclarationList())
                        index = 0
                        ele_list = []
                        param_list = []
                        for ele in tmp_list:
                            param_list.append(ele['name'])
                            ele_list.append(ele['type'])
                        new_struct = ir.global_context.get_identified_type(name=struct_name)
                        new_struct.set_body(*ele_list)
                        # 将struct定义插入结构体表，记录
                        self.struct_table.insert(struct_name, new_struct, param_list)
                        return new_struct
        else:
            # 结构实体的定义
            label_ = self.visit(ctx.structOrUnion())
            if label_ == 'struct':
                # 结构体
                struct_name = ctx.Identifier().getText()
                new_struct = ir.global_context.get_identified_type(name=struct_name)
                return new_struct

    def visitTypedefName(self, ctx: CParser.TypedefNameContext):
        return ctx.getText()

    def visitStructDeclarationList(self, ctx: CParser.StructDeclarationListContext):
        if ctx.structDeclarationList():
            sub_list = self.visit(ctx.structDeclarationList())
            sub_dict = self.visit(ctx.structDeclaration())
            sub_list.append(sub_dict)
            return sub_list
        else:
            return [self.visit(ctx.structDeclaration())]

    def visitStructDeclaration(self, ctx: CParser.StructDeclarationContext):
        if ctx.structDeclaratorList():
            type_ = self.visit(ctx.specifierQualifierList())
            name_ = self.visit(ctx.structDeclaratorList())
            # return ir.ArrayType(type_,len_)
            str___ = ctx.structDeclaratorList().getText()
            len_ = int(re.findall(r'\d+', str___)[0])
            return {"type": ir.ArrayType(type_, len_), "name": name_}
        elif ctx.staticAssertDeclaration():
            print("Oops, not supported yet!")
        else:
            return self.visit(ctx.specifierQualifierList())

    def visitStructDeclaratorList(self, ctx: CParser.StructDeclaratorListContext):
        if not ctx.structDeclaratorList():
            return self.visit(ctx.structDeclarator())
        else:
            print("Oops, not supported in struct declarator list!")

    def visitStructDeclarator(self, ctx: CParser.StructDeclaratorContext):
        if len(ctx.children) == 1:
            return self.visit(ctx.declarator())
        else:
            print("Oops, not supported in struct declarator!")

    def visitSpecifierQualifierList(self, ctx: CParser.SpecifierQualifierListContext):
        if ctx.typeQualifier():
            print("typeQualifier not supported yet!")
        if not ctx.specifierQualifierList():
            return self.visit(ctx.typeSpecifier())
        else:
            sub_dict = {'type': self.visit(ctx.children[0]),
                        'name': self.visit(ctx.children[1])}
            return sub_dict

    def visitStructOrUnion(self, ctx: CParser.StructOrUnionContext):
        return ctx.getText()

    def visitDeclarationSpecifiers(self, ctx):
        return self.visit(ctx.children[-1])

    def visitDeclarationSpecifier(self, ctx: CParser.DeclarationSpecifierContext):
        return self.visit(ctx.children[0])

    def visitDeclaration(self, ctx):
        _type = self.visit(ctx.declarationSpecifiers())
        # if type(_type)==ir.types.IdentifiedStructType:
        #     # 如果是结构体，就没有初始化值操作。结构体定义在declarationSpecifiers中。
        #     if ctx.initDeclaratorList():
        #         print("xxx:",ctx.initDeclaratorList().getText())
        #     return ''
        if not ctx.initDeclaratorList():
            return ''
        declarator_list = self.visit(ctx.initDeclaratorList())
        for name, init_val in declarator_list:
            if isinstance(name, tuple):
                # 函数类型
                _func = name
                name = _func[0]
                params = _func[1]
                args = [i for i, j in params]
                fnty = ir.FunctionType(_type, args, var_arg=True)
                func = ir.Function(self.module, fnty, name=name)
                _type2 = self.symbol_table.getType(name)
                self.symbol_table.insert(name, btype=_type2, value=func)
                continue
            elif type(_type) == ir.types.IdentifiedStructType:
                # 结构体实例化，不需要初始值设定
                ptr_struct = self.struct_table.getPtr(_type.name)
                # 从结构体表获取定义
                ptr_struct_instance_ = self.builder.alloca(ptr_struct)
                # 结构体实例化，分配内存
                self.symbol_table.insert(name, value=ptr_struct_instance_)
                # 存入符号表，先记录struct类型指针，再记录当前实例化指针
                continue

            _type2 = self.symbol_table.getType(name)
            if _type2[0] == self.ARRAY_TYPE:
                # 1D数组类型
                length = _type2[1]
                arr_type = ir.ArrayType(_type, length.constant)
                if self.builder:
                    temp = self.builder.alloca(arr_type, name=name)
                    if init_val:
                        # 有初值
                        l = len(init_val)
                        if l > length.constant:
                            # 数组过大
                            return
                        for i in range(l):
                            indices = [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)]
                            ptr = self.builder.gep(ptr=temp, indices=indices)
                            self.builder.store(init_val[i], ptr)

                else:
                    temp = ir.GlobalValue(self.module, arr_type, name=name)
                # 保存指针
                temp = self.builder.bitcast(temp, ir.PointerType(_type))
                temp_ptr = self.builder.alloca(temp.type)
                self.builder.store(temp, temp_ptr)
                temp = temp_ptr
                self.symbol_table.insert(name, btype=_type2, value=temp)

            elif _type2[0] == self.ARRAY_2D_TYPE:
                # 2D数组类型
                dim = _type2[1]
                first_dim = dim[0]
                second_dim = dim[1]
                first_dim_c = first_dim.constant
                second_dim_c = second_dim.constant
                inner_arr_type = ir.ArrayType(_type, second_dim_c)  # int *
                for_outer_type = ir.PointerType(_type)  # int *
                arr_type = ir.ArrayType(for_outer_type, first_dim_c)  # int **
                outer_arr = self.builder.alloca(arr_type, name=name)  # int ***
                for i in range(first_dim_c):
                    temp = self.builder.alloca(inner_arr_type)  # int **
                    temp = self.builder.bitcast(temp, ir.PointerType(_type))  # int *
                    indices = [ir.Constant(self.INT_TYPE, 0), ir.Constant(self.INT_TYPE, i)]
                    ptr = self.builder.gep(ptr=outer_arr, indices=indices)
                    self.builder.store(temp, ptr)
                temp = self.builder.bitcast(outer_arr, ir.PointerType(for_outer_type))
                temp_ptr = self.builder.alloca(temp.type)
                self.builder.store(temp, temp_ptr)
                self.symbol_table.insert(name, btype=_type2, value=temp_ptr)

            else:
                # 普通变量
                if self.builder:
                    temp = self.builder.alloca(_type, size=1, name=name)
                    if init_val:
                        self.builder.store(init_val, temp)
                else:
                    temp = ir.GlobalValue(self.module, _type, name=name)

                # 保存指针
                self.symbol_table.insert(name, btype=_type2, value=temp)

    def visitAssignmentExpression(self, ctx: CParser.AssignmentExpressionContext):
        # TODO: dingyifeng
        if len(ctx.children) == 1:
            conditional_expression = self.visit(ctx.children[0])
            return conditional_expression
        elif len(ctx.children) == 3:
            unary_expression, unary_expression_pointer = self.visit(ctx.children[0])
            origin = self.builder.load(unary_expression)
            if unary_expression_pointer is True:
                assignment_operator = self.visit(ctx.children[1])
                assignment_expression = self.visit(ctx.children[2])
                if assignment_operator == '=':
                    return self.builder.store(assignment_expression, unary_expression)
                elif assignment_operator == '<<=':
                    edited = self.builder.shl(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '>>=':
                    edited = self.builder.ashr(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '&=':
                    edited = self.builder.and_(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '^=':
                    edited = self.builder.xor(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '|=':
                    edited = self.builder.or_(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '*=':
                    edited = self.builder.mul(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '/=':
                    edited = self.builder.sdiv(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '+=':
                    edited = self.builder.add(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '-=':
                    edited = self.builder.sub(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                elif assignment_operator == '%=':
                    edited = self.builder.srem(origin, assignment_expression)
                    return self.builder.store(edited, unary_expression)
                else:
                    raise Exception()
            else:
                raise Exception()

    def visitConditionalExpression(self, ctx: CParser.ConditionalExpressionContext):
        # TODO: dingyifeng
        # has changed
        logical_or_expression = self.visit(ctx.children[0])
        if len(ctx.children) == 1:
            return logical_or_expression
        elif len(ctx.children) == 5:
            operator_expression_questionmark = ctx.children[1]
            expression = self.visit(ctx.children[2])
            operator_expression_colon = ctx.children[3]
            conditional_expression = self.visit(ctx.children[4])
            if operator_expression_questionmark.getText() != '?' or operator_expression_colon.getText() != ':':
                raise Exception()
            else:
                raise Exception()
        else:
            raise Exception()


    def visitLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        # TODO: dingyifeng
        # has changed
        inclusive_or_expression = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return inclusive_or_expression
        elif len(ctx.children) == 3:
            logical_and_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if operator_expression.getText() != '&&':
                raise Exception()
            else:
                return self.builder.and_(logical_and_expression, inclusive_or_expression)
        else:
            raise Exception()

    def visitInclusiveOrExpression(self, ctx: CParser.InclusiveOrExpressionContext):
        # TODO: dingyifeng
        # has changed
        exclusive_or_expression = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return exclusive_or_expression
        elif len(ctx.children) == 3:
            inclusive_or_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if operator_expression.getText() != '|':
                raise Exception()
            else:
                return self.builder.or_(inclusive_or_expression, exclusive_or_expression)
        else:
            raise Exception()

    def visitExclusiveOrExpression(self, ctx: CParser.ExclusiveOrExpressionContext):
        # TODO: dingyifeng
        # has changed
        and_expression = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return and_expression
        elif len(ctx.children) == 3:
            exclusive_or_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if operator_expression.getText() != '^':
                raise Exception()
            else:
                return self.builder.xor(exclusive_or_expression, and_expression)
        else:
            raise Exception()

    def visitAndExpression(self, ctx: CParser.AndExpressionContext):
        # TODO: dingyifeng
        # has changede
        equality_expression = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return equality_expression
        elif len(ctx.children) == 3:
            and_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if operator_expression.getText() != '&':
                raise Exception()
            else:
                return self.builder.and_(and_expression, equality_expression)
        else:
            raise Exception()

    def visitLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        # TODO: dingyifeng
        # has changed
        logical_and_expression = self.visit(ctx.children[len(ctx.children)-1])
        if len(ctx.children) == 1:
            return logical_and_expression
        elif len(ctx.children) == 3:
            logical_or_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if operator_expression.getText() != '||':
                raise Exception()
            else:
                return self.builder.or_(logical_or_expression, logical_and_expression)
        else:
            raise Exception()

    def visitEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        # TODO: dingyifeng
        # has changed
        relational_expression = self.visit(ctx.children[len(ctx.children)-1])
        if len(ctx.children) == 1:
            return relational_expression
        elif len(ctx.children) == 3:
            equality_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if equality_expression.type == self.FLOAT_TYPE:
                # todo: fix
                return self.builder.fcmp_ordered(cmpop=operator_expression.getText(), lhs=equality_expression
                                                 , rhs=relational_expression)
            else:
                return self.builder.icmp_signed(cmpop=operator_expression.getText(), lhs=equality_expression
                                                , rhs=relational_expression)
        else:
            raise Exception()


    def visitRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        # TODO: dingyifeng
        # has changed
        shift_expression = self.visit(ctx.children[len(ctx.children)-1])
        shift_type = shift_expression.type
        if len(ctx.children) == 1:
            return shift_expression
        elif len(ctx.children) == 3:
            relational_expression = self.visit(ctx.children[0])
            operator_expression = ctx.children[1]
            if relational_expression.type == self.FLOAT_TYPE:
                # todo: fix
                # print(eval(shift_expression))
                # shift_expression = self.builder.sitofp(shift_expression, float)
                # print(shift_expression)
                # print(shift_type == self.FLOAT_TYPE)
                # if shift_expression.type != self.FLOAT_TYPE:
                #     shift_expression = self.builder.sitofp(shift_expression, float)
                return self.builder.fcmp_ordered(cmpop=operator_expression.getText(), lhs=relational_expression
                                                 , rhs=shift_expression)
            else:
                return self.builder.icmp_signed(cmpop=operator_expression.getText(), lhs=relational_expression
                                                , rhs=shift_expression)
        else:
            raise Exception()


    def visitShiftExpression(self, ctx: CParser.ShiftExpressionContext):
        # TODO: dingyifeng
        # has changed
        additive_expression = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return additive_expression
        elif len(ctx.children) == 3:
            shift_expression = self.visit(ctx.children[0])
            if ctx.children[1].getText() == '<<':
                return self.builder.shl(shift_expression, additive_expression)
            elif ctx.children[1].getText() == '>>':
                return self.builder.ashr(shift_expression, additive_expression)
            else:
                raise Exception()
        else:
            raise Exception()

    def visitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        # TODO: dingyifeng
        # has changed
        multiplicative_expression = self.visit(ctx.children[len(ctx.children)-1])
        if len(ctx.children) == 1:
            return multiplicative_expression
        elif len(ctx.children) == 3:
            additive_expression = self.visit(ctx.children[0])
            if ctx.children[1].getText() == '+':
                return self.builder.add(additive_expression, multiplicative_expression)
            elif ctx.children[1].getText() == '-':
                return self.builder.sub(additive_expression, multiplicative_expression)
            else:
                raise Exception()
        else:
            raise Exception()

    def visitMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        # TODO: dingyifeng
        # has changed
        cast_expression, _ = self.visit(ctx.children[len(ctx.children) - 1])
        if len(ctx.children) == 1:
            return cast_expression
        elif len(ctx.children) == 3:
            multiplicative_expression = self.visit(ctx.children[0])
            if ctx.children[1].getText() == '*':
                return self.builder.mul(multiplicative_expression, cast_expression)
            elif ctx.children[1].getText() == '/':
                return self.builder.sdiv(multiplicative_expression, cast_expression)
            elif ctx.children[1].getText() == '%':
                return self.builder.srem(multiplicative_expression, cast_expression)
            else:
                raise Exception()
        else:
            raise Exception()

    def visitCastExpression(self, ctx: CParser.CastExpressionContext):
        # TODO: dingyifeng
        # has changed
        if len(ctx.children) == 1:
            unary_expression, unary_expression_pointer = self.visit(ctx.children[0])
            if unary_expression_pointer is True:
                unary_expression_pointer = unary_expression
                unary_expression = self.builder.load(unary_expression_pointer)
            return unary_expression, unary_expression_pointer
        elif len(ctx.children) == 4 or len(ctx.children) == 5:
            if ctx.children[len(ctx.children)-4] != '(' or ctx.children[len(ctx.children)-2] != ')':
                raise Exception()
            else:
                cast_expression, cast_expression_pointer = self.visit(ctx.children[len(ctx.children)-1])
                type_name = self.visit(ctx.children[len(ctx.children)-3])
                cast_expression = self.builder.bitcast(cast_expression, type_name)
                return cast_expression, cast_expression_pointer

    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        # TODO: dingyifeng
        # has changed
        if len(ctx.children) == 1:
            postfix_expression, _ = self.visit(ctx.children[0])
            return postfix_expression, _
        elif len(ctx.children) == 2:
            operator = ctx.children[0]
            if operator.getText() == '++':
                unary_expression, unary_expression_pointer = self.visit(ctx.children[1])
                if unary_expression_pointer is True:
                    unary_expression_pointer = unary_expression
                    unary_expression = self.builder.load(unary_expression_pointer)
                    unary_expression = self.builder.add(unary_expression, ir.Constant(self.INT_TYPE, 1))
                    self.builder.store(unary_expression, unary_expression_pointer)
                return unary_expression, unary_expression_pointer
            elif operator.getText() == '--':
                unary_expression, unary_expression_pointer = self.visit(ctx.children[1])
                if unary_expression_pointer is True:
                    unary_expression_pointer = unary_expression
                    unary_expression = self.builder.load(unary_expression_pointer)
                    unary_expression = self.builder.sub(unary_expression, ir.Constant(self.INT_TYPE, 1))
                    self.builder.store(unary_expression, unary_expression_pointer)
                return unary_expression, unary_expression_pointer
            elif operator.getText() == 'sizeof':
                raise Exception()
            elif operator.getText() == '&&':
                raise Exception()
            else:
                unary_expression, unary_expression_pointer = self.visit(ctx.children[1])
                if operator.getText() == '&':
                    return unary_expression_pointer, False
                elif operator.getText() == '*':
                    if unary_expression_pointer is True:
                        unary_expression_pointer = unary_expression
                        unary_expression = self.builder.load(unary_expression_pointer)
                    return unary_expression, unary_expression_pointer
                elif operator.getText() == '+':
                    return unary_expression, False
                elif operator.getText() == '-':
                    return self.builder.neg(unary_expression), False
                elif operator.getText() == '~':
                    return self.builder.not_(unary_expression), False
                elif operator.getText() == '!':
                    if unary_expression.type != self.FLOAT_TYPE:
                        return self.builder.icmp_signed(cmpop='==', lhs=unary_expression
                                                        , rhs=ir.Constant(self.INT_TYPE, 0)), False
                    else:
                        return self.builder.fcmp_ordered(cmpop='==', lhs=unary_expression
                                                         , rhs=ir.Constant(self.FLOAT_TYPE, 0)), False
        else:
            raise Exception()

    def handlePostfixExpressionInstance(self, ctx, postfix_operator):
        postfix_expression = ctx.children[0]
        identifier = ctx.children[2]
        postfix_expression_pointer = self.symbol_table.getValue(postfix_expression.getText())
        if postfix_operator.getText() == '.':
            identifier_index = self.struct_table.getParamIndice(postfix_expression_pointer.type.pointee.name
                                                                , identifier.getText())
        elif postfix_operator.getText() == '->':
            identifier_index = self.struct_table.getParamIndice(postfix_expression_pointer.type.pointee.pointee.name
                                                                , identifier.getText())
        else:
            raise Exception()
        # constant type?
        identifier_indices = [ir.Constant(self.INT_TYPE, 0), ir.Constant(self.INT_TYPE, identifier_index)]
        return postfix_expression_pointer, identifier_indices

    def visitPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        # TODO: dingyifeng
        # has changed
        if len(ctx.children) == 1:
            primary_expression = self.visit(ctx.children[0])
            return primary_expression
        else:
            postfix_expression, postfix_expression_pointer = self.visit(ctx.children[0])
            if postfix_expression_pointer is True:
                if len(ctx.children) == 2:
                    postfix_operator = ctx.children[1]
                    if postfix_operator.getText() == '++':
                        postfix_expression_pointer = postfix_expression
                        postfix_expression = self.builder.load(postfix_expression_pointer)
                        self.builder.store(postfix_expression, postfix_expression_pointer)
                        new_postfix_expression = self.builder.add(postfix_expression, ir.Constant(self.INT_TYPE, 1))
                        self.builder.store(new_postfix_expression, postfix_expression_pointer)
                        return postfix_expression, postfix_expression_pointer
                    elif postfix_operator.getText() == '--':
                        postfix_expression_pointer = postfix_expression
                        postfix_expression = self.builder.load(postfix_expression_pointer)
                        self.builder.store(postfix_expression, postfix_expression_pointer)
                        new_postfix_expression = self.builder.sub(postfix_expression, ir.Constant(self.INT_TYPE, 1))
                        self.builder.store(new_postfix_expression, postfix_expression_pointer)
                        return postfix_expression, postfix_expression_pointer
                    else:
                        raise Exception()
                elif len(ctx.children) == 3:
                    postfix_operator = ctx.children[1]
                    if postfix_operator.getText() == '(':
                        argument_expression_list = []
                        return self.builder.call(postfix_expression, argument_expression_list), False
                    elif postfix_operator.getText() == '.':
                        postfix_expression_pointer, identifier_indices \
                            = self.handlePostfixExpressionInstance(ctx, postfix_operator)
                        postfix_expression_pointer = self.builder.gep(ptr=postfix_expression_pointer
                                                                      , indices=identifier_indices)
                        return postfix_expression_pointer, True
                    elif postfix_operator.getText() == '->':
                        postfix_expression_pointer, identifier_indices \
                            = self.handlePostfixExpressionInstance(ctx, postfix_operator)
                        postfix_expression_pointer = self.builder.gep(ptr=self.builder.load(postfix_expression_pointer)
                                                                      , indices=identifier_indices)
                        return postfix_expression_pointer, True
                    else:
                        raise Exception()
                elif len(ctx.children) == 4:
                    postfix_operator = ctx.children[1]
                    if postfix_operator.getText() == '[':
                        postfix_expression = self.builder.load(postfix_expression)
                        postfix_expression_array_type = self.builder.load(postfix_expression).type
                        postfix_expression_pointer_type = ir.PointerType(ir.ArrayType(postfix_expression_array_type, 0))
                        postfix_expression_pointer = self.builder.bitcast(postfix_expression, postfix_expression_pointer_type)
                        postfix_expression_index = self.visit(ctx.children[2])
                        postfix_expression_indices = [ir.Constant(self.INT_TYPE, 0), postfix_expression_index]
                        postfix_expression_pointer = self.builder.gep(ptr=postfix_expression_pointer, indices=postfix_expression_indices)
                        return postfix_expression_pointer, True
                    elif postfix_operator.getText() == '(':
                        argument_expression_list = self.visit(ctx.children[2])
                        return self.builder.call(postfix_expression, argument_expression_list), False
                    else:
                        raise Exception()
                else:
                    raise Exception()
            else:
                raise Exception()

    def visitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        # TODO: dingyifeng
        # has changed
        if len(ctx.children) == 1:
            if ctx.Identifier():
                identifier = ctx.children[0]
                value = self.symbol_table.getValue(identifier.getText())
                return value, True
            elif ctx.Constant():
                constant = ctx.children[0]
                constant_value = eval(constant.getText())
                if constant_value.__class__ == int:
                    return ir.Constant(self.INT_TYPE, constant_value), False
                elif constant_value.__class__ == float:
                    return ir.Constant(self.FLOAT_TYPE, constant_value), False
                elif constant_value.__class__ == str:
                    constant_value = ord(constant_value)
                    return ir.Constant(self.CHAR_TYPE, constant_value), False
                else:
                    raise Exception()
            elif ctx.StringLiteral():
                string_literal = eval(ctx.StringLiteral()[0].getText())
                string = [ir.Constant(self.CHAR_TYPE, ord(i)) for i in string_literal]
                string = string + [ir.Constant(self.CHAR_TYPE, 0)]
                string_literal_pointer = self.builder.alloca(ir.ArrayType(self.CHAR_TYPE, len(string)))
                self.builder.store(ir.Constant.literal_array(string), string_literal_pointer)
                string_literal_pointer = self.builder.bitcast(string_literal_pointer, ir.PointerType(self.CHAR_TYPE))
                return string_literal_pointer, False
        elif len(ctx.children) == 3:
            if ctx.children[0] != '(' or ctx.children[2] != ')':
                raise Exception()
            else:
                expression = self.visit(ctx.children[1])
                return expression, False
        else:
            raise Exception()

    def visitArgumentExpressionList(self, ctx: CParser.ArgumentExpressionListContext):
        # TODO: dingyifeng
        # has changed
        result_arg = []
        if ctx.argumentExpressionList():
            result_arg = self.visit(ctx.argumentExpressionList())
        result_arg.append(self.visit(ctx.assignmentExpression()))
        return result_arg

    def visitCompoundStatement(self, ctx):
        for i in ctx.children:
            self.visit(i)

    def visitBlockItem(self, ctx):
        if ctx.statement():
            return self.visit(ctx.statement())
        return self.visit(ctx.declaration())

    def visitInitDeclaratorList(self, ctx):
        declarator_list = []
        declarator_list.append(self.visit(ctx.initDeclarator()))
        if ctx.initDeclaratorList():
            declarator_list += self.visit(ctx.initDeclaratorList())
        return declarator_list

    def visitInitDeclarator(self, ctx):
        if ctx.initializer():
            declarator = (self.visit(ctx.declarator()), self.visit(ctx.initializer()))
        else:
            declarator = (self.visit(ctx.declarator()), None)
        return declarator

    def visitInitializer(self, ctx):
        if ctx.assignmentExpression():
            return self.visit(ctx.assignmentExpression())
        elif ctx.initializerList():
            return self.visit(ctx.initializerList())

    def visitJumpStatement(self, ctx):
        # xuyihao
        if ctx.Return():
            if ctx.expression():
                _value = self.visit(ctx.expression())
                try:
                    self.builder.ret(_value)
                except:
                    pass
            else:
                try:
                    self.builder.ret_void()
                except:
                    pass

        elif ctx.Continue():
            if self.lst_continue:
                self.builder.branch(self.lst_continue)
            else:
                raise Exception()
        elif ctx.Break():
            if self.lst_break:
                self.builder.branch(self.lst_break)
            else:
                raise Exception()

    def visitIterationStatement(self, ctx: CParser.IterationStatementContext):
        # xuyihao
        if ctx.While():
            block_name = self.builder.block.name
            self.symbol_table = createTable(self.symbol_table)
            init_block = self.builder.append_basic_block(name='{}.init'.format(block_name))
            do_block = self.builder.append_basic_block(name='{}.do'.format(block_name))
            end_block = self.builder.append_basic_block(name='{}.end'.format(block_name))
            lst_continue, lst_break = self.lst_continue, self.lst_break
            self.lst_continue, self.lst_break = init_block, end_block
            try:
                self.builder.branch(init_block)
            except:
                pass
            self.builder.position_at_start(init_block)
            expression = self.visit(ctx.expression())
            self.builder.cbranch(expression, do_block, end_block)
            self.builder.position_at_start(do_block)
            self.visit(ctx.statement())
            try:
                self.builder.branch(init_block)
            except:
                pass
            self.builder.position_at_start(end_block)
            self.lst_continue, self.lst_break = lst_continue, lst_break
            self.symbol_table = self.symbol_table.getFather()
        elif ctx.Do():
            pass
        elif ctx.For():
            block_name = self.builder.block.name
            self.symbol_table = createTable(self.symbol_table)
            init_block = self.builder.append_basic_block(name='{}.init'.format(block_name))
            cond_block = self.builder.append_basic_block(name='{}.cond'.format(block_name))
            do_block = self.builder.append_basic_block(name='{}.do'.format(block_name))
            end_block = self.builder.append_basic_block(name='{}.end'.format(block_name))
            lst_continue, lst_break = self.lst_continue, self.lst_break
            self.lst_continue, self.lst_break = cond_block, end_block
            self.builder.branch(init_block)
            self.builder.position_at_start(init_block)
            cond_exp, exp = self.visit(ctx.forCondition())
            self.builder.branch(cond_block)
            self.builder.position_at_start(cond_block)
            condition = self.visit(cond_exp)
            self.builder.cbranch(condition, do_block, end_block)
            self.builder.position_at_start(do_block)
            self.visit(ctx.statement())
            if exp:
                self.visit(exp)
            try:
                self.builder.branch(cond_block)
            except:
                pass
            self.builder.position_at_start(end_block)
            self.lst_continue, self.lst_break = lst_continue, lst_break
            self.symbol_table = self.symbol_table.getFather()

    def visitForCondition(self, ctx: CParser.ForConditionContext):
        # xuyihao
        self.visit(ctx.forDeclaration())
        return ctx.forExpression(0), ctx.forExpression(1)

    def visitForDeclaration(self, ctx: CParser.ForDeclarationContext):
        # xuyihao
        _type = self.visit(ctx.declarationSpecifiers())
        declarator_list = self.visit(ctx.initDeclaratorList())
        for name, init_val in declarator_list:
            _type2 = self.symbol_table.getType(name)
            if _type2[0] == self.ARRAY_TYPE:
                # 数组类型
                length = _type2[1]
                arr_type = ir.ArrayType(_type, length.constant)
                if self.builder:
                    temp = self.builder.alloca(arr_type, name=name)
                    if init_val:
                        # 有初值
                        l = len(init_val)
                        if l > length.constant:
                            # 数组过大
                            return
                        for i in range(l):
                            indices = [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), i)]
                            ptr = self.builder.gep(ptr=temp, indices=indices)
                            self.builder.store(init_val[i], ptr)
                        temp = self.builder.bitcast(temp, ir.PointerType(_type))
                        temp_ptr = self.builder.alloca(temp.type)
                        self.builder.store(temp, temp_ptr)
                        temp = temp_ptr
                else:
                    temp = ir.GlobalValue(self.module, arr_type, name=name)
                # 保存指针
                self.symbol_table.insert(name, btype=_type2, value=temp)

            else:
                # 普通变量
                if self.builder:
                    temp = self.builder.alloca(_type, size=1, name=name)
                    if init_val:
                        self.builder.store(init_val, temp)

                # 保存指针
                self.symbol_table.insert(name, btype=_type2, value=temp)

    def visitSelectionStatement(self, ctx: CParser.SelectionStatementContext):
        # xuyihao
        if ctx.If():
            branches = ctx.statement()
            if len(branches) == 2:  # 存在else if/else语句
                block_name = self.builder.block.name
                if_block = self.builder.append_basic_block(name='{}.if'.format(block_name))
                then_block = self.builder.append_basic_block(name='{}.then'.format(block_name))
                else_block = self.builder.append_basic_block(name='{}.else'.format(block_name))
                end_block = self.builder.append_basic_block(name='{}.end'.format(block_name))
                try:
                    self.builder.branch(if_block)
                except:
                    pass
                self.builder.position_at_start(if_block)
                expr_val = self.visit(ctx.expression())
                self.builder.cbranch(expr_val, then_block, else_block)
                self.builder.position_at_start(then_block)
                self.symbol_table = createTable(self.symbol_table)
                self.visit(branches[0])
                self.symbol_table = self.symbol_table.getFather()
                try:
                    self.builder.branch(end_block)
                except:
                    pass
                self.builder.position_at_start(else_block)
                self.symbol_table = createTable(self.symbol_table)
                self.visit(branches[1])
                self.symbol_table = self.symbol_table.getFather()
                try:
                    self.builder.branch(end_block)
                except:
                    pass
                self.builder.position_at_start(end_block)
            else:  # 只有if分支
                block_name = self.builder.block.name
                if_block = self.builder.append_basic_block(name='{}.if'.format(block_name))
                then_block = self.builder.append_basic_block(name='{}.then'.format(block_name))
                end_block = self.builder.append_basic_block(name='{}.end'.format(block_name))
                try:
                    self.builder.branch(if_block)
                except:
                    pass
                self.builder.position_at_start(if_block)
                expr_val = self.visit(ctx.expression())
                self.builder.cbranch(expr_val, then_block, end_block)
                self.builder.position_at_start(then_block)
                self.symbol_table = createTable(self.symbol_table)
                self.visit(branches[0])
                self.symbol_table = self.symbol_table.getFather()
                try:
                    self.builder.branch(end_block)
                except:
                    pass
                self.builder.position_at_start(end_block)

    def visitTerminal(self, node):
        return node.getText()

    def visitInitializerList(self, ctx: CParser.InitializerListContext):
        ans = [self.visit(ctx.initializer())]
        if ctx.initializerList():
            ans = self.visit(ctx.initializerList()) + ans
        return ans

    def visitParameterTypeList(self, ctx: CParser.ParameterTypeListContext):
        if ctx.parameterList():
            return self.visit(ctx.parameterList())

    def visitParameterList(self, ctx: CParser.ParameterListContext):
        if ctx.parameterList():
            _param_list = self.visit(ctx.parameterList())
        else:
            _param_list = []
        _param_decl = self.visit(ctx.parameterDeclaration())
        _param_list.append(_param_decl)
        return _param_list

    def visitParameterDeclaration(self, ctx: CParser.ParameterDeclarationContext):
        _type = self.visit(ctx.declarationSpecifiers())
        _name = self.visit(ctx.declarator())
        return _type, _name

    def output(self):
        """返回代码"""
        return repr(self.module)

del CParser
