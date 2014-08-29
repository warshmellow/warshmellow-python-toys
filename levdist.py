"""
author: warshmellow

Implements a solution to Levenshtein Distance problem. The problem asks,
given a list of test words, and a dictionary, compute the size of the friends
network of each test word. Two words are friends if their Levenshtein Distance
is 1. The Levenshtein distance is the number of letter substititions,
injections, and removals from one word to form the other. The friends network
of a word is all the word, all friends of the word, all friends of those,
etc..

Solution: For a given test word, generates all Levenshtein distance 1 variants
and iteratively removes them and their distance 1 variants from the
dictionary, and theirs, until we can't anymore.
"""

import string
import sys


def dist_one_word_variants(input_word):
    """
    Generator outputting all words Levenshtein distance 1 away from input_word,
    assuming lowercase and English a-z only.
    """
    # Work with lowercase copy of input word
    word = input_word.lower()

    for i in range(len(word)):  # For each index in b
        for variant_letter in string.ascii_lowercase:   # For letters [a..z]
            if variant_letter != word[i]:
                # Substitute b[i] with variant letter
                yield word[:i] + variant_letter + word[i + 1:]
                # Inject variant letter before word[i]
                yield word[:i] + variant_letter + word[i:]
        # Remove word[i]
        yield word[:i] + word[i + 1:]

    for variant_letter in string.ascii_lowercase:   # For letters [a..z]
        yield word + variant_letter     # Append variant letter after word


def network(test_word, corpus):
    """
    Returns a frozenset of a network of words in corpus of test_word
    """
    # Grow connected component, starting with test_word,
    # by generating variants that are also in the corpus
    # Reduce the corpus each time with matches
    # Add the matches to the connected component
    # Repeat for all words in the connected component
    # Stop when the matches turn up empty
    connected_component = {test_word}
    matches = frozenset({test_word})
    reduced_corpus = set(corpus)

    while len(matches) > 0:
        matches = frozenset({
            matched_word
            for word in connected_component
            for matched_word in dist_one_word_variants(word)
            if matched_word in reduced_corpus})

        reduced_corpus = reduced_corpus.difference(matches)
        connected_component = connected_component.union(matches)

    return connected_component


def network_size(test_word, corpus):
    """
    Returns size of the friends network of test_word in corpus, i.e.,
    the number of words in corpus that are test_word, Levenshtein
    distance 1 away from test_word, distance 1 away from them, etc..
    """
    return len(network(test_word, corpus))


def main():
    """
    Reads words from file and prints network size of words.
    """
    with open(sys.argv[1], 'r') as test_cases:
        # Create iterator from test cases to maintain state,
        # to stop read at test_words_stopping_point, and resume after
        test_cases_iter = iter(test_cases)
        test_words_stopping_point = 'END OF INPUT'

        # Get test words from file
        test_words = []
        for test in test_cases_iter:
            if test.rstrip() != test_words_stopping_point:
                test_words.append(test.rstrip())
            else:
                break

        # Dictionary words stored in a frozen set called corpus
        corpus = set()
        for test in test_cases_iter:
            corpus.add(test.rstrip())
        corpus = frozenset(corpus)

        # Compute network size for test words and print
        for test_word in test_words:
            print network_size(test_word, corpus)


if __name__ == '__main__':
    main()
