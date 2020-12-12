class SymbolTable:
    def __init__(self):
        self.table = [{}]
        self.level = 0

    def get_item(self, key):
        for i in range(self.level, -1, -1):
            if key in self.table[i]:
                return self.table[i][key]
        return None

    def add_item(self, key, value):
        if key in self.table[self.level]:
            return {'succeed': False, 'reason': f'{key} has already been defined in this scope!'}
        self.table[self.level][key] = value
        return {'succeed': True}

    def key_exists(self, key):
        for i in range(self.level, -1, -1):
            if key in self.table[i]:
                return True
        return False

    def enter_scope(self):
        self.level += 1
        self.table.append({})

    def quit_scope(self):
        if self.level == 0:
            return
        self.table.pop(-1)
        self.level -= 1

    def is_global(self):
        return self.level == 1

