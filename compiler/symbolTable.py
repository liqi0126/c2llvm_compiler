from .CType import *

class SymbolTable:
    def __init__(self, father=None):
        self.symbol_list = {}
        self.value_list = {}
        self.children = None
        self.father = father

    def enter_scope(self):
        self.children = SymbolTable(self)
        return self.children

    def leave_scope(self):
        return self.father

    def get_type(self, name):
        if name in self.symbol_list:
            return self.symbol_list[name]
        if self.father:
            return self.father.get_type(name)
        else:
            return None

    def get_value(self, name):
        if name in self.value_list:
            return self.value_list[name]
        if self.father:
            return self.father.get_value(name)
        else:
            return None

    def insert(self, name, btype=BASE_TYPE, value=None):
        self.symbol_list[name] = btype
        self.value_list[name] = value
