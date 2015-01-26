def collapse_list(nested_list):
    # collapses a list of multiple iterable objects into a single list containing the elements of each iterable object
    from collections import Iterable

    new_list = []

    for i in nested_list:
        try:
            new_list += i
        except TypeError:  # i is not iterable
            new_list.append(i)

    if any([isinstance(i, Iterable) for i in new_list]):  # if the list still contains a sequence
        return collapse_list(new_list)
    else:
        return new_list
