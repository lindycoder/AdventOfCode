def group(iterable, key):
    return groupby(sorted(iterable, key=key), key=key)
