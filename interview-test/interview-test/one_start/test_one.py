# from random import shuffle
import random
import string
from copy import deepcopy


def combine_two_lists_parallel():
    """
    Combines two lists, in this case it will be of equal size, thus no need to account for unequal list size implying
    the obvious way. Note the test for the function appears to require number, letter format.
    :return: result_list : list of tuples.
    """
    result_list = []
    first_list = [1, 2, 3, 4, 5, 6]
    second_list = ['A', 'B', 'C', 'D', 'E', 'F']

    """
    A PEP20 way of iterating efficiently through 2 lists.
    
    Hint python has a built in method for this that takes two lists.
    
    Result should be a list of tuples: EX: [(C,3),...]
    """

    for first_list_value, second_list_value in zip(first_list, second_list):
        result_list.append((first_list_value, second_list_value))

    return result_list


def return_matches_in_list_parallel():
    """
    Find the matched words of the two strings. The random element kept screaming to use sets.
    :return: type set of a list of matched words.
    """
    result_list = []

    first_input_string = """Two of the fairest stars in all the heaven,
    Having some business, do entreat her eyes
    To twinkle in their spheres till they return.
    What if her eyes were there, they in her head?
    The brightness of her cheek would shame those stars,
    As daylight doth a lamp; her eyes in heaven
    Would through the airy region stream so bright
    That birds would sing and think it were not night.
    See, how she leans her cheek upon her hand!
    O, that I were a glove upon that hand,
    That I might touch that cheek
    """.replace(";", "").replace(",", "").replace(".", "").replace("?", "").replace("\n", "").strip().lower()

    second_input_string = """Sleep dwell upon thine eyes, peace in thy breast!
    Would I were sleep and peace, so sweet to rest!
    Hence will I to my ghostly father's cell,
    His help to crave, and my dear hap to tell.
    """.replace(";", "").replace(",", "").replace(".", "").replace("?", "").replace("\n", "").strip().lower()

    first_input_string = first_input_string.split()
    second_input_string = second_input_string.split()
    first_list = sorted(first_input_string, key=lambda k: random.random())
    second_list = sorted(second_input_string, key=lambda k: random.random())

    # in case its not random enough - lol.
    if first_list[0] == second_list[0]:
        second_list = sorted(second_list, key=lambda k: random.random())
    # print(first_list)
    # print(second_list)

    """
    Return matches found in both lists, as pythonic as possible
    
    """

    for word in set(first_list):
        if word in set(second_list):
            result_list.append(word)

    return set(result_list)


def count_shakespeare():
    """
    Find 3 things, total word count, longest word in length, and frequency of repeated words.
    Numbers and roman numerals are not excluded in this word count. only exclude punctuation
    :return: a dictionary of the following; occurances: object,  total: int, longest_word: int
    dictionary object (key,value ; word:freq_count), int (word count) and int (longest word length)
    """
    with open("one_start/shakespeare.txt") as file:
        shakespeare_text = file.read()
        # print(shakespeare_text)

        """
        The challenge here is to count the occurances of words occuring more than once.
        
        Also indicate the total word count of the piece of text as well as the longest word in the text.
        
        return {
            occurances: object,
            total: int,
            longest_word: int
        }
        
        """

    shakespeare_text_formatted = shakespeare_text.translate(str.maketrans('', '', string.punctuation)).lower()
    shakespeare_text_formatted_list = shakespeare_text_formatted.split()

    word_frequency = []
    frequency = {}
    longest_word = ''
    total = 0

    for word in shakespeare_text_formatted_list:

        # occurances word frequency count
        word_frequency.append(shakespeare_text_formatted_list.count(word))
        frequency = dict(zip(shakespeare_text_formatted_list, word_frequency))

        # longest_word
        if len(word) > len(longest_word):
            longest_word = word

        # total word count
        total += 1

    # normalize | remove single word occurances from the dictionary
    occurances = {key: value for key, value in frequency.items() if value != 1}

    # print(occurances)
    # print(total)
    # print(len(longest_word))

    return {"occurances": occurances, "total": total, "longest_word": len(longest_word)}


def infinite_loop():
    """
    List will keep on running, break the list on iteration 784 and return the list of results.
    Assume i should be appended to the result list and return that, place a break for i == 784
    :return: the results list
    """
    result_list = []
    i = 0
    while i < 1000:
        """
        Add potential code
        """
        result_list.append(i)
        if i == 784:
            break

        # print(i)

        i += 1

    return result_list


if __name__ == "__main__":
    infinite_loop()
