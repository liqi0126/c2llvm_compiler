import re


from .CParser import CParser
from .CVisitor import CVisitor
from .CType import *
from .structTable import StructTable
from .symbolTable import SymbolTable
from .Errors import SemanticError, UnSupportedError

from llvmlite import ir




class ToLLVMVisitor(CVisitor):
    def __init__(self):
        super().__init__()
        self.module = ir.Module()
        self.module.triple = "x86_64-pc-linux-gnu"
        self.module.data_layout = "e-m:e-i64:64-f80:128-n8:16:32:64-S128"

        self.builder = None
        self.symbol_table = SymbolTable()
        self.lst_continue = None
        self.lst_break = None
        self.struct_table = StructTable()

    def visitCompilationUnit(self, ctx):
        for i in ctx.children:
            self.visit(i)

    def visitFunctionDefinition(self, ctx):
        # TODO: liqi
        assert ctx.declarationList() is None
        func_type = self.visit(ctx.declarationSpecifiers())
        func_name, func_params = self.visit(ctx.declarator())

        # TODO: ???
        func_args = [i for i, j in func_params]
        llvm_fnty = ir.FunctionType(func_type, func_args)
        llvm_func = ir.Function(self.module, llvm_fnty, name=func_name)

        block = llvm_func.append_basic_block(name=f"{func_name}.entry")

        self.builder = ir.IRBuilder(block)
        self.symbol_table.insert(func_name, value=llvm_func)
        self.symbol_table = self.symbol_table.enter_scope()

        func_args = llvm_func.args
        # TODO: optim
        arg_names = [j for i, j in func_params]
        for seq, name in enumerate(arg_names):
            arg = func_args[seq]
            arg_ptr = self.builder.alloca(arg.type, name=name)
            self.builder.store(arg, arg_ptr)
            self.symbol_table.insert(name, value=arg_ptr)
        self.visit(ctx.compoundStatement())

        if func_type == VOID_TYPE:
            self.builder.ret_void()

        self.symbol_table = self.symbol_table.leave_scope()

    def visitDeclarator(self, ctx: CParser.DeclaratorContext):
        return self.visit(ctx.directDeclarator())

    def visitDirectDeclarator(self, ctx: CParser.DirectDeclaratorContext):
        # TODO: liqi
        if ctx.Identifier():
            name = self.visit(ctx.Identifier())
            btype = (BASE_TYPE, None)
            self.symbol_table.insert(name, btype)
            return name
        elif ctx.children[1].getText() == '[':
            name = self.visit(ctx.directDeclarator())
            if self.symbol_table.get_type(name) is not None and self.symbol_table.get_value(name) is None:
                # 二维数组的情况
                btype, length = self.symbol_table.get_type(name)
                if btype == ARRAY_TYPE:
                    first_dimension = length
                    second_dimension = self.visit(ctx.assignmentExpression())
                    dim = (first_dimension, second_dimension)
                    btype = (ARRAY_2D_TYPE, dim)
                    self.symbol_table.insert(name, btype=btype)
                    return name

            # 普通一维数组
            length = self.visit(ctx.assignmentExpression())
            btype = (ARRAY_TYPE, length)
            self.symbol_table.insert(name, btype=btype)
            return name
        elif ctx.children[1].getText() == '(':
            name = self.visit(ctx.directDeclarator())
            btype = (FUNCTION_TYPE, None)
            self.symbol_table.insert(name, btype)
            if ctx.parameterTypeList():
                params = self.visit(ctx.parameterTypeList())
            else:
                params = []
            return name, params

    def visitTypeSpecifier(self, ctx: CParser.TypeSpecifierContext):
        if ctx.Void():
            return VOID_TYPE
        elif ctx.Char():
            return CHAR_TYPE
        elif ctx.Int():
            return INT_TYPE
        elif ctx.Float():
            return FLOAT_TYPE
        elif ctx.Double():
            return DOUBLE_TYPE
        if ctx.pointer():
            type = self.visit(ctx.typeSpecifier())
            return ir.PointerType(type)
        elif ctx.structOrUnionSpecifier():
            return self.visit(ctx.structOrUnionSpecifier())
        elif ctx.typedefName():
            return self.visit(ctx.typedefName())
        else:
            raise UnSupportedError("unsupported type", ctx)

    def visitStructOrUnionSpecifier(self, ctx: CParser.StructOrUnionSpecifierContext):
        if ctx.structDeclarationList():
            if not ctx.Identifier():
                raise UnSupportedError("don't support anonymous struct", ctx)
            struct_name = ctx.Identifier().getText()
            if self.symbol_table.get_value(struct_name):
                raise SemanticError("redefinition", ctx)
            else:
                dec_list = self.visit(ctx.structDeclarationList())
                param_list, type_list = [], []
                for dec in dec_list:
                    param_list.append(dec['name'])
                    type_list.append(dec['type'])
                new_struct = ir.global_context.get_identified_type(name=struct_name)
                new_struct.set_body(*type_list)
                self.struct_table.insert(struct_name, new_struct, param_list, type_list)
                return new_struct
        else:
            struct_name = ctx.Identifier().getText()
            new_struct = ir.global_context.get_identified_type(name=struct_name)
            return new_struct

    def visitTypedefName(self, ctx: CParser.TypedefNameContext):
        return ctx.getText()

    def visitStructDeclarationList(self, ctx: CParser.StructDeclarationListContext):
        # TODO: liqi
        if ctx.structDeclarationList():
            sub_list = self.visit(ctx.structDeclarationList())
            sub_dict = self.visit(ctx.structDeclaration())
            sub_list.append(sub_dict)
            return sub_list
        else:
            return [self.visit(ctx.structDeclaration())]

    def visitStructDeclaration(self, ctx: CParser.StructDeclarationContext):
        # TODO: liqi
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
        # TODO: liqi
        if not ctx.structDeclaratorList():
            return self.visit(ctx.structDeclarator())
        else:
            print("Oops, not supported in struct declarator list!")

    def visitStructDeclarator(self, ctx: CParser.StructDeclaratorContext):
        # TODO: liqi
        if len(ctx.children) == 1:
            return self.visit(ctx.declarator())
        else:
            print("Oops, not supported in struct declarator!")

    def visitSpecifierQualifierList(self, ctx: CParser.SpecifierQualifierListContext):
        # TODO: liqi
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
        # TODO: liqi
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
                _type2 = self.symbol_table.get_type(name)
                self.symbol_table.insert(name, btype=_type2, value=func)
                continue
            elif type(_type) == ir.types.IdentifiedStructType:
                # 结构体实例化，不需要初始值设定
                ptr_struct = self.struct_table.get_ptr(_type.name)
                # 从结构体表获取定义
                ptr_struct_instance_ = self.builder.alloca(ptr_struct)
                # 结构体实例化，分配内存
                self.symbol_table.insert(name, value=ptr_struct_instance_)
                # 存入符号表，先记录struct类型指针，再记录当前实例化指针
                continue

            _type2 = self.symbol_table.get_type(name)
            if _type2[0] == ARRAY_TYPE:
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

            elif _type2[0] == ARRAY_2D_TYPE:
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
                    indices = [ir.Constant(INT_TYPE, 0), ir.Constant(INT_TYPE, i)]
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
        if ctx.conditionalExpression():
            return self.visit(ctx.conditionalExpression())
        elif ctx.unaryExpression():
            lhs, pt = self.visit(ctx.unaryExpression())
            if not pt:
                raise Exception()
            op_ = self.visit(ctx.assignmentOperator())
            value_ = self.visit(ctx.assignmentExpression())
            if op_ == '=':
                return self.builder.store(value_, lhs)
            elif op_ == '+=':
                old_value_ = self.builder.load(lhs)
                new_value_ = self.builder.add(value_, old_value_)
                return self.builder.store(new_value_, lhs)
            elif op_ == '-=':
                old_value_ = self.builder.load(lhs)
                new_value_ = self.builder.sub(old_value_, value_)
                return self.builder.store(new_value_, lhs)
            elif op_ == '*=':
                old_value_ = self.builder.load(lhs)
                new_value_ = self.builder.mul(old_value_, value_)
                return self.builder.store(new_value_, lhs)
            elif op_ == '/=':
                old_value_ = self.builder.load(lhs)
                new_value_ = self.builder.sdiv(old_value_, value_)
                return self.builder.store(new_value_, lhs)
            elif op_ == '%=':
                old_value_ = self.builder.load(lhs)
                new_value_ = self.builder.srem(old_value_, value_)
                return self.builder.store(new_value_, lhs)
            else:
                print("unknown assignment operator")

    def visitAssignmentOperator(self, ctx: CParser.AssignmentOperatorContext):
        # TODO: dingyifeng
        return (ctx.getText())

    def visitConditionalExpression(self, ctx: CParser.ConditionalExpressionContext):
        # TODO: dingyifeng
        if len(ctx.children) == 1:
            # 如果没有('?' expression ':' conditionalExpression)?部分
            return self.visit(ctx.logicalOrExpression())

    def visitLogicalAndExpression(self, ctx: CParser.LogicalAndExpressionContext):
        # TODO: dingyifeng
        if ctx.logicalAndExpression():
            # 如果有多个'与'语句
            lhs = self.visit(ctx.inclusiveOrExpression())
            # result = self.builder.alloca(self.BOOL_TYPE)
            rhs = self.visit(ctx.logicalAndExpression())
            # with self.builder.if_else(lhs) as (then, otherwise):
            #     with then:
            #         self.builder.store(self.BOOL_TYPE(1), result)
            #     with otherwise:
            #         rhs = self.visit(ctx.logicalAndExpression())
            #         self.builder.store(rhs, result)
            return self.builder.and_(lhs, rhs)
        else:
            return self.visit(ctx.inclusiveOrExpression())

    def visitInclusiveOrExpression(self, ctx: CParser.InclusiveOrExpressionContext):
        # TODO: dingyifeng
        if ctx.inclusiveOrExpression():
            # 上述第二种情况
            return self.visit(ctx.inclusiveOrExpression())
        else:
            return self.visit(ctx.exclusiveOrExpression())

    def visitExclusiveOrExpression(self, ctx: CParser.ExclusiveOrExpressionContext):
        # TODO: dingyifeng
        if ctx.exclusiveOrExpression():
            # 上述第二种情况
            return self.visit(ctx.exclusiveOrExpression())
        else:
            return self.visit(ctx.andExpression())

    def visitAndExpression(self, ctx: CParser.AndExpressionContext):
        # TODO: dingyifeng
        if ctx.andExpression():
            return self.visit(ctx.andExpression())
        else:
            return self.visit(ctx.equalityExpression())

    def visitLogicalOrExpression(self, ctx: CParser.LogicalOrExpressionContext):
        # TODO: dingyifeng
        if ctx.logicalOrExpression():
            lhs = self.visit(ctx.logicalOrExpression())
            rhs = self.visit(ctx.logicalAndExpression())
            return self.builder.or_(lhs, rhs)
        else:
            return self.visit(ctx.logicalAndExpression())

    def visitEqualityExpression(self, ctx: CParser.EqualityExpressionContext):
        # TODO: dingyifeng
        if len(ctx.children) == 1:
            return self.visit(ctx.relationalExpression())
        else:
            op = ctx.children[1].getText()
            lhs = self.visit(ctx.equalityExpression())
            rhs = self.visit(ctx.relationalExpression())
            return self.builder.icmp_signed(cmpop=op, lhs=lhs, rhs=rhs)

    def visitRelationalExpression(self, ctx: CParser.RelationalExpressionContext):
        # TODO: dingyifeng
        if len(ctx.children) == 1:
            return self.visit(ctx.shiftExpression())
        else:
            lhs = self.visit(ctx.relationalExpression())
            rhs = self.visit(ctx.shiftExpression())
            op = ctx.children[1].getText()
            converted_target = lhs.type
            if rhs.type == INT_TYPE or rhs.type == CHAR_TYPE:
                return self.builder.icmp_signed(cmpop=op, lhs=lhs, rhs=rhs)
            elif rhs.type == FLOAT_TYPE:
                return self.builder.fcmp_signed(cmpop=op, lhs=lhs, rhs=rhs)
            else:
                print("unknown type")

    def visitShiftExpression(self, ctx: CParser.ShiftExpressionContext):
        # TODO: dingyifeng
        if len(ctx.children) == 1:
            return self.visit(ctx.additiveExpression())
        else:
            print("you can't do that")

    def visitAdditiveExpression(self, ctx: CParser.AdditiveExpressionContext):
        # TODO: dingyifeng
        _mul = self.visit(ctx.multiplicativeExpression())
        if ctx.additiveExpression():
            _add = self.visit(ctx.additiveExpression())

            if ctx.Plus():
                return self.builder.add(_add, _mul)
            elif ctx.Minus():
                return self.builder.sub(_add, _mul)

        else:
            return _mul

    def visitMultiplicativeExpression(self, ctx: CParser.MultiplicativeExpressionContext):
        # TODO: dingyifeng
        _cast, _ = self.visit(ctx.castExpression())
        if ctx.multiplicativeExpression():
            _mul = self.visit(ctx.multiplicativeExpression())
            if ctx.Star():
                return self.builder.mul(_mul, _cast)
            elif ctx.Div():
                return self.builder.sdiv(_mul, _cast)
            elif ctx.Mod():
                return self.builder.srem(_mul, _cast)
        else:
            return _cast

    def visitCastExpression(self, ctx: CParser.CastExpressionContext):
        # TODO: dingyifeng
        if ctx.unaryExpression():
            res = self.visit(ctx.unaryExpression())
            val, pt = res[0], res[1]
            if pt is True:
                pt = val
                val = self.builder.load(val)

            return val, pt

        if ctx.typeName():
            _target_type = self.visit(ctx.typeName())
            val, pt = self.visit(ctx.castExpression())
            val = self.builder.bitcast(val, _target_type)
            return val, pt

    def visitUnaryExpression(self, ctx: CParser.UnaryExpressionContext):
        # TODO: dingyifeng
        if ctx.postfixExpression():
            return self.visit(ctx.postfixExpression())

        if ctx.unaryOperator():
            val, pt = self.visit(ctx.castExpression())
            op = self.visit(ctx.unaryOperator())
            if op == '-':
                return self.builder.neg(val), False
            elif op == '&':
                if pt:
                    return pt, False
                else:
                    raise Exception()
            elif op == '*':
                pt = val
                val = self.builder.load(pt)
                return val, pt

        if ctx.PlusPlus():
            val, pt = self.visit(ctx.unaryExpression())
            if pt:
                pt = val
                val = self.builder.load(pt)
                new_val = self.builder.add(val, ir.Constant(INT_TYPE, 1))
                self.builder.store(new_val, pt)
                return new_val, pt
            else:
                raise Exception()

        if ctx.MinusMinus():
            val, pt = self.visit(ctx.unaryExpression())
            if pt:
                pt = val
                val = self.builder.load(pt)
                new_val = self.builder.add(val, ir.Constant(INT_TYPE, -1))
                self.builder.store(new_val, pt)
                return new_val, pt
            else:
                raise Exception()

    def visitPostfixExpression(self, ctx: CParser.PostfixExpressionContext):
        # TODO: dingyifeng
        if ctx.primaryExpression():
            return self.visit(ctx.primaryExpression())

        elif ctx.expression():
            # 获取指向指针的指针
            var, pt = self.visit(ctx.postfixExpression())
            if not pt:
                raise Exception()
            # 得到指针的值
            var = self.builder.load(var)
            # 获取指针指向的类型
            value = self.builder.load(var)
            arr_type = ir.PointerType(ir.ArrayType(value.type, 100))
            # 将指针转换为指向数组的指针
            var = self.builder.bitcast(var, arr_type)
            # 获取 index 并构造 indices
            index = self.visit(ctx.expression())
            indices = [ir.Constant(INT_TYPE, 0), index]
            # 取值
            ptr = self.builder.gep(ptr=var, indices=indices)
            return ptr, True
        elif ctx.postfixExpression():
            if ctx.children[1].getText() == '(':
                # 表示是一个函数声明
                if ctx.argumentExpressionList():
                    args_ = self.visit(ctx.argumentExpressionList())
                else:
                    args_ = []
                lhs, _ = self.visit(ctx.postfixExpression())
                return self.builder.call(lhs, args_), False
            elif ctx.children[1].getText() == '.':
                struct_instance_ptr_name = ctx.postfixExpression().getText()
                param_name = ctx.Identifier().getText()
                struct_instance_ptr = self.symbol_table.get_value(struct_instance_ptr_name)
                struct_type_name = struct_instance_ptr.type.pointee.name
                indice_ = self.struct_table.get_param_indice(struct_type_name, param_name)
                indices = [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), indice_)]
                ptr = self.builder.gep(ptr=struct_instance_ptr, indices=indices)
                return ptr, True
            elif ctx.children[1].getText() == '->':
                struct_instance_ptr_name = ctx.postfixExpression().getText()
                param_name = ctx.Identifier().getText()
                struct_instance_ptr = self.symbol_table.get_value(struct_instance_ptr_name)
                struct_type_name = struct_instance_ptr.type.pointee.pointee.name
                new_ptr = self.builder.load(struct_instance_ptr)
                # 先将结构体指针load为结构体
                indice_ = self.struct_table.get_param_indice(struct_type_name, param_name)
                indices = [ir.Constant(ir.IntType(32), 0), ir.Constant(ir.IntType(32), indice_)]
                ptr = self.builder.gep(ptr=new_ptr, indices=indices)
                return ptr, True
            else:
                print("Ooops, unsupported type in postfix expression!")

    def visitPrimaryExpression(self, ctx: CParser.PrimaryExpressionContext):
        # TODO: dingyifeng
        _str = ctx.getText()
        if ctx.Identifier():
            rhs = self.symbol_table.get_value(ctx.Identifier().getText())
            return rhs, True
        if ctx.Constant():
            _str = ctx.Constant().getText()
            val = eval(_str)
            if val.__class__ == int:
                return ir.Constant(INT_TYPE, val), False
            elif val.__class__ == float:
                return ir.Constant(FLOAT_TYPE, val), False
            elif val.__class__ == str:
                val = ord(val)
                return ir.Constant(CHAR_TYPE, val), False
            else:
                raise Exception()
        elif ctx.StringLiteral():
            _str = eval(ctx.StringLiteral()[0].getText())
            _str_array = [ir.Constant(CHAR_TYPE, ord(i)) for i in _str] + [ir.Constant(CHAR_TYPE, 0)]
            temp = ir.Constant.literal_array(_str_array)
            arr_type = ir.ArrayType(CHAR_TYPE, len(_str_array))
            ptr = self.builder.alloca(arr_type)
            self.builder.store(temp, ptr)
            ptr = self.builder.bitcast(ptr, ir.PointerType(CHAR_TYPE))
            return ptr, False
        elif ctx.expression():
            print("pppp")
            print("ctx.expression().getText()", ctx.expression().getText())
            return self.visit(ctx.expression()), False
        else:
            print("Oops, not supported in primary expression")

    def visitArgumentExpressionList(self, ctx: CParser.ArgumentExpressionListContext):
        if not ctx.argumentExpressionList():
            return [self.visit(ctx.assignmentExpression())]

        _args = self.visit(ctx.argumentExpressionList())
        _args.append(self.visit(ctx.assignmentExpression()))
        return _args

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
        # TODO: xuyihao
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
        # TODO: xuyihao
        if ctx.While():
            block_name = self.builder.block.name
            self.symbol_table = self.symbol_table.enter_scope()
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
            self.symbol_table = self.symbol_table.leave_scope()
        elif ctx.Do():
            pass
        elif ctx.For():
            block_name = self.builder.block.name
            self.symbol_table = self.symbol_table.enter_scope()
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
            self.symbol_table = self.symbol_table.leave_scope()

    def visitForCondition(self, ctx: CParser.ForConditionContext):
        # TODO: xuyihao
        self.visit(ctx.forDeclaration())
        return ctx.forExpression(0), ctx.forExpression(1)

    def visitForDeclaration(self, ctx: CParser.ForDeclarationContext):
        # TODO: xuyihao
        _type = self.visit(ctx.declarationSpecifiers())
        declarator_list = self.visit(ctx.initDeclaratorList())
        for name, init_val in declarator_list:
            _type2 = self.symbol_table.get_type(name)
            if _type2[0] == ARRAY_TYPE:
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
        # TODO: xuyihao
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
                self.symbol_table = self.symbol_table.enter_scope()
                self.visit(branches[0])
                self.symbol_table = self.symbol_table.leave_scope()
                try:
                    self.builder.branch(end_block)
                except:
                    pass
                self.builder.position_at_start(else_block)
                self.symbol_table = self.symbol_table.enter_scope()
                self.visit(branches[1])
                self.symbol_table = self.symbol_table.leave_scope()
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
                self.symbol_table = self.symbol_table.enter_scope()
                self.visit(branches[0])
                self.symbol_table = self.symbol_table.leave_scope()
                try:
                    self.builder.branch(end_block)
                except:
                    pass
                self.builder.position_at_start(end_block)

    def visitTerminal(self, node):
        return node.getText()

    def visitInitializerList(self, ctx: CParser.InitializerListContext):
        # TODO: liqi
        ans = [self.visit(ctx.initializer())]
        if ctx.initializerList():
            ans = self.visit(ctx.initializerList()) + ans
        return ans

    def visitParameterTypeList(self, ctx: CParser.ParameterTypeListContext):  # DONE
        if ctx.parameterList():
            return self.visit(ctx.parameterList())

    def visitParameterList(self, ctx: CParser.ParameterListContext):  # DONE
        param_list = self.visit(ctx.parameterList()) if ctx.parameterList() else []
        new_param = self.visit(ctx.parameterDeclaration())
        param_list.append(new_param)
        return param_list

    def visitParameterDeclaration(self, ctx: CParser.ParameterDeclarationContext):  # DONE
        return [self.visit(ctx.declarationSpecifiers()), self.visit(ctx.declarator())]

    def output(self):
        return repr(self.module)


del CParser
