# from itertools import product
# gen_comb_list = (lambda list_set: list(product(*list_set)))

def gen_comb_list(list_set, ls: list = [], a: list = []):
    for i in list_set[0]:
        if len(list_set) == 1:
            a.append(ls + [i])
        else:
            gen_comb_list(list_set[1:], ls + [i])
    return a

# print(gen_comb_list([[1, 2, 3]]))
print(gen_comb_list([[1, 2, 3], [4, 5], [4, 5]]))
