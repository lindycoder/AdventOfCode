from operator import itemgetter
from typing import List

import pytest
import sys
from hamcrest import assert_that, greater_than, is_


def compute(data):
    decks = parse_decks(data)

    while all(map(len, decks)):
        play_cards = {
            i: deck.pop(0) for i, deck in enumerate(decks)
        }

        ordered = sorted(play_cards.items(), key=itemgetter(1), reverse=True)
        decks[ordered[0][0]].extend(map(itemgetter(1), ordered))

    winning_deck = next(filter(lambda deck: len(deck) > 0, decks))
    return calculate_score(winning_deck)


def calculate_score(winning_deck):
    return sum((i + 1) * n for i, n in enumerate(reversed(winning_deck)))


def parse_decks(data):
    raw_decks = data.strip().split('\n\n')
    decks = []
    for raw_deck in raw_decks:
        decks.append(list(map(int, raw_deck.splitlines()[1:])))
    return decks


def compute2(data):
    decks = parse_decks(data)

    _, deck = play_recursive(decks)

    return calculate_score(deck)


def play_recursive(decks: List[List[int]]):
    infinity_check = [set() for _ in decks]

    while all(map(len, decks)):
        for i, deck in enumerate(decks):
            deck_tuple = tuple(deck)
            if deck_tuple in infinity_check[i]:
                return 0, decks[0]
            else:
                infinity_check[i].add(deck_tuple)

        play_cards = {
            i: deck.pop(0) for i, deck in enumerate(decks)
        }

        if all(len(deck) >= play_cards[i] for i, deck in enumerate(decks)):
            new_decks = [deck[:play_cards[i]] for i, deck in enumerate(decks)]
            winner, _ = play_recursive(new_decks)
        else:
            winner, _ = next(iter(sorted(play_cards.items(), key=itemgetter(1),
                                         reverse=True)))

        decks[winner].extend((play_cards.pop(winner),
                              next(iter(play_cards.values()))))

    return next((i, deck) for i, deck in enumerate(decks) if len(deck) > 0)


@pytest.mark.parametrize('val,expect', [
    ("""\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10    
""", 306)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
Player 1:
9
2
6
3
1

Player 2:
5
8
4
7
10
""", 291),
    ("""\
Player 1:
43
19

Player 2:
2
29
14    
""", greater_than(0)),  # Recursive one
    (None, greater_than(31921)),  # failed one
    (None, greater_than(33735)),  # failed one
])
def test_compute2(val, expect):
    assert_that(compute2(val or puzzle_input), is_(expect))


puzzle_input = """\
Player 1:
19
5
35
6
12
22
45
39
14
42
47
38
2
26
13
30
4
34
43
40
16
8
23
50
36

Player 2:
1
21
29
41
32
28
9
37
49
20
17
27
24
3
33
44
48
31
15
25
18
46
7
10
11
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
