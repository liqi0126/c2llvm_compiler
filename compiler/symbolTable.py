def createTable(currentTable=None):
    newTable = SymbolTable(currentTable)
    currentTable.addChild(newTable)
    return newTable
BASE_TYPE = 0
ARRAY_TYPE = 1
FUNCTION_TYPE = 2

class SymbolTable:
    def __init__(self, father):
        self.symbol_list = {}
        self.value_list = {}
        self.children = []
        self.father = father

    def addChild(self, child):
        self.children.append(child)

    def getFather(self):
        return self.father

    def getType(self, name):
        if name not in self.symbol_list.keys():
            if self.father:
                return self.father.getType(name)
            else:
                return None
        return self.symbol_list[name]

    def getValue(self, name):
        if name not in self.value_list.keys():
            if self.father:
                return self.father.getValue(name)
            else:
                return None
        return self.value_list[name]

    def insert(self, name, btype=BASE_TYPE, value=None):
        '''

        :param name:
        :param btype: 一般不需要
        :param value: 指针
        :return:
        '''
        self.symbol_list[name] = btype
        self.value_list[name] = value


class ArrayType:
    def __init__(self):
        self.length = 0
        self.child_type = None


class BasicType:
    def __init__(self):
        self.llvm_type = None
