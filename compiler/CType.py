from llvmlite import ir

CHAR_TYPE = ir.IntType(8)
INT_TYPE = ir.IntType(32)
FLOAT_TYPE = ir.FloatType()
DOUBLE_TYPE = ir.DoubleType()
VOID_TYPE = ir.VoidType()
BOOL_TYPE = ir.IntType(1)

BASE_TYPE = 0
ARRAY_TYPE = 1
ARRAY_2D_TYPE = 4
FUNCTION_TYPE = 2