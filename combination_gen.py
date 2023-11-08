from itertools import product


def gen_comb_list(list_set):
    return list(product(*list_set))


print(gen_comb_list([[1, 2, 3]]))
print(gen_comb_list([[1, 2, 3], [4, 5]]))
