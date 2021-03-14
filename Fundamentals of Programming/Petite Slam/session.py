class SparseMatrix:
    def __init__(self, lines, columns):
        self._lines = lines
        self._columns = columns
        self._values_list = []

    @property
    def lines(self):
        return self._lines

    @property
    def columns(self):
        return self._columns

    @property
    def values_list(self):
        return self._values_list

    def __str__(self):
        out_str = ""
        for i in range(0, self.lines):
            for j in range(0, self.columns):
                value = self.get(i, j)
                out_str += str(value) + " "
            out_str += "\n"
        return out_str

    def set(self, i, j, val):
        if i < 0 or (i > self.lines - 1):
            raise ValueError("line index out of range")
        if j < 0 or (j > self.columns - 1):
            raise ValueError("column index out of range")
        for value_list in self._values_list:
            if value_list[0] == i and value_list[1] == j:
                value_list[2] = val
                return None
        self._values_list.append([i, j, val])

    def get(self, i, j):
        if i < 0 or (i > self.lines - 1):
            raise ValueError("line index out of range")
        if j < 0 or (j > self.columns - 1):
            raise ValueError("column index out of range")
        for value_list in self._values_list:
            if value_list[0] == i and value_list[1] == j:
                return value_list[2]

        return 0


m1 = SparseMatrix(3, 3)
m1.set(1, 1, 2)
m1.set(2, 2, 4)
print(m1)
try:
    m1.set(3, 3, 99)
except Exception as e:
    print(type(e))
m1.set(1, 1, m1.get(1, 1)+1)
print(m1)
