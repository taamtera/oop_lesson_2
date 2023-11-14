data = [
    {'embarked': 'C', 'gender': 'male', 'class': 3},
    {'embarked': 'S', 'gender': 'female', 'class': 1},
    {'embarked': 'Q', 'gender': 'male', 'class': 2},
    {'embarked': 'C', 'gender': 'female', 'class': 1},
    {'embarked': 'C', 'gender': 'female', 'class': 1},
    {'embarked': 'S', 'gender': 'male', 'class': 2},
    {'embarked': 'Q', 'gender': 'female', 'class': 3},
    {'embarked': 'C', 'gender': 'male', 'class': 1},
    {'embarked': 'S', 'gender': 'female', 'class': 3},
    {'embarked': 'Q', 'gender': 'male', 'class': 2},
    # Add more data...
    # Repeat the structure with different values
]


sorting_keys = ['embarked', 'gender', 'class']

unique_data_set = {tuple((key, item[key]) for key in sorting_keys) for item in data}
sorted_data = sorted([dict(item) for item in unique_data_set], key=lambda x: tuple(x[key] for key in reversed(sorting_keys)))


for item in sorted_data:
    print(item)

