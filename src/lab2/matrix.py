def transpose(mat):
    if not mat:
        return []
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError"
    res = []
    for j in range(n):
        new_row = []
        for i in range(len(mat)):
            new_row.append(mat[i][j])
        res.append(new_row)
    return res


def row_sums(mat):
    if not mat:
        return []
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError"
    res = []
    for row in mat:
        s = 0
        for x in row:
            s += x
        res.append(s)
    return res


def col_sums(mat):
    if not mat:
        return []
    n = len(mat[0])
    for row in mat:
        if len(row) != n:
            return "ValueError"
    res = []
    for j in range(n):
        s = 0
        for i in range(len(mat)):
            s += mat[i][j]
        res.append(s)
    return res


print("transpose")
print(transpose([[1, 2, 3]]))
print(transpose([[1], [2], [3]]))
print(transpose([[1, 2], [3, 4]]))
print(transpose([]))
print(transpose([[1, 2], [3]]))

print("................................................... ")
print("row_sums")
print(row_sums([[1, 2, 3], [4, 5, 6]]))
print(row_sums([[-1, 1], [10, -10]]))
print(row_sums([[0, 0], [0, 0]]))
print(row_sums([[1, 2], [3]]))

print("................................................... ")
print("col_sums")
print(col_sums([[1, 2, 3], [4, 5, 6]]))
print(col_sums([[-1, 1], [10, -10]]))
print(col_sums([[0, 0], [0, 0]]))
print(col_sums([[1, 2], [3]]))
