from llvmlite import ir


class StructTable:
    def __init__(self):
        self.struct_dict = {}

    def add_struct(self, name, member_list, type_list):
        if name in self.struct_dict:
            return {'succeed': False, 'reason': f'{name} has already been defined!'}

        self.struct_dict[name] = {'member': member_list, 'type': ir.LiteralStructType(type_list)}
        return {'succeed': True}

    def get_member_id(self, name, member):
        if name not in self.struct_dict:
            return None
        member_list = self.struct_dict[name]['member']

        return member_list.index(member)

    def get_member_type(self, name, member):
        if name not in self.struct_dict:
            return None
        struct = self.struct_dict[name]
        index = struct['member'].index(member)
        type = struct['type'].elements[index]
        return type
