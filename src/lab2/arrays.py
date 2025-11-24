empty_list = []


def find_min_max(values):
    if values == empty_list:
        return "ValueError"
    return min(values), max(values)


def get_unique_sorted(values):
    if values == empty_list:
        return "ValueError"
    return list(set(sorted(values)))


def flatten_list(nested):

    if nested == empty_list:
        return "ValueError"
    flat_list = []
    for sublist in nested:
        for item in sublist:
            if not isinstance(item, int):
                return "TypeError"
            flat_list.append(item)
    return flat_list


print("find_min_max")
print(find_min_max([3, -1, 5, 5, 0]))
print(find_min_max([42]))
print(find_min_max([-5, -2, -9]))
print(find_min_max([]))
print(" ")

print("get_unique_sorted")
print(get_unique_sorted([3, 1, 2, 1, 3]))
print(get_unique_sorted([]))
print(get_unique_sorted([-1, -1, 0, 2, 2]))
print(get_unique_sorted([1.0, 1, 2.5, 2.5, 0]))

print(" ")

print("flatten_list")
print(flatten_list([[1, 2], [3, 4]]))
print(flatten_list([[1, 2], (3, 4, 5)]))
print(flatten_list([[1], [], [2, 3]]))
print(flatten_list([[[1, 2], "ab"]]))
