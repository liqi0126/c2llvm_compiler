class StructTable:
    def __init__(self):
        self.type_list = {}

    def getPtr(self, name):
        if name not in self.type_list.keys():
            return None
        return self.type_list[name]['ptr']

    def getParamIndice(self,name,param_name):
        if name not in self.type_list.keys():
            return None
        return self.type_list[name]['param_list'].index(param_name)

    def insert(self, name, ptr,param_list):
        # ptr 指结构体定义指针， param_dist指参数映射字典
        self.type_list[name] = {"ptr":ptr,"param_list":param_list}


class FuncTable:
    def __init__(self):
        self.func_list = {}

    def getValue(self, name):
        if name not in self.func_list.keys():
            return None
        return self.func_list[name]

    def insert(self, name, value):
        self.func_list[name] = value
