# Remove equal adjacent elements
#
# Example input: [1, 2, 2, 3]
# Example output: [1, 2, 3]


def remove_adjacent(lst):
    if len(lst) <= 1:
        return lst
    newlst = []
    newlst.append(lst[0])
    for i in range(1, len(lst)):
        if lst[i] != lst[i - 1]:
            newlst.append(lst[i])
    return newlst


# Merge two sorted lists in one sorted list in linear time
#
# Example input: [2, 4, 6], [1, 3, 5]
# Example output: [1, 2, 3, 4, 5, 6]

def linear_merge(lst1, lst2):
    i = 0
    j = 0
    newlst = []
    while i < len(lst1) and j < len(lst2):
        if lst1[i] < lst2[j]:
            newlst.append(lst1[i])
            i += 1
        else:
            newlst.append(lst2[j])
            j += 1

    newlst.extend(lst1[i:])
    newlst.extend(lst2[j:])

    return newlst


# print(remove_adjacent([1, 2, 2, 3]))
# print(linear_merge([2, 4, 6], [1, 3, 5, 8]))
