from one_start.test_one import *
import asyncio

"""
Question, look in the one_start directory for challenges in test_one 

"""

if __name__ == "__main__":
    # First test
    assert combine_two_lists_parallel() == [(1, 'A'), (2, 'B'), (3, 'C'), (4, 'D'), (5, 'E'), (6, 'F')]

    # Second test
    test_set = ['were', 'would', 'i', 'upon', 'eyes', 'and', 'in', 'so', 'to']
    assert set(return_matches_in_list_parallel()) == set(test_set)

    # Third test
    test_dictionary = {"occurances": {}, "total": 1656, "longest_word": 15}
    assert count_shakespeare()["total"] == test_dictionary["total"]
    assert count_shakespeare()["longest_word"] == test_dictionary["longest_word"]
    assert count_shakespeare()["occurances"] != test_dictionary["occurances"]       # note the negative test

    # Fourth test
    test_list = [x for x in range(0, 784)]
    compare_infinite = infinite_loop()
    assert compare_infinite[99] == test_list[99]
    assert compare_infinite[1] == test_list[1]
