import re
import sys
from functools import partial
from operator import ne

import pytest
from hamcrest import assert_that, is_

value_re = re.compile(r'^"(\w)"$')

not_false = partial(ne, False)


def all_of(rules, msg):
    remainders = [msg]
    for rule in rules:
        new_remainders = []

        for remainder in remainders:
            new_remainders.extend(rule(remainder))

        remainders = new_remainders

    return remainders


def any_of(rules, msg):
    results = []

    for rule in rules:
        results.extend(rule(msg))

    return results


def resolve_pointer(rules, number, msg):
    return rules[number](msg)


def value_matcher(value, msg):
    return [msg[1:]] if msg and msg[0] == value else []


def compile_rules(rules):
    compiled = {}

    for rule in rules:

        number, definition = rule.split(': ')

        if value_re.match(definition):
            value = value_re.match(definition).group(1)
            compiled_rule = partial(value_matcher, value)
        else:
            or_rules = []
            for or_part in definition.split(' | '):
                and_rules = []
                for and_part in or_part.split(' '):
                    and_rules.append(partial(resolve_pointer,
                                             compiled, int(and_part)))
                or_rules.append(partial(all_of, and_rules))
            compiled_rule = partial(any_of, or_rules)

        compiled[int(number)] = compiled_rule

    return compiled


def matching_messages(messages, rule_0):
    return len(list(filter(lambda e: e and '' in e, map(rule_0, messages))))


def compute(data):
    rules, messages = data.strip().split('\n\n')

    return matching_messages(messages.splitlines(),
                             compile_rules(rules.splitlines())[0])


def compute2(data):
    rules, messages = data.strip().split('\n\n')

    rules = rules.splitlines()
    for i, rule in enumerate(rules):
        if rule.startswith('8:'):
            rules[i] = '8: 42 | 42 8'
        elif rule.startswith('11:'):
            rules[i] = '11: 42 31 | 42 11 31'

    return matching_messages(messages.splitlines(),
                             compile_rules(rules)[0])


@pytest.mark.parametrize('val,expect', [
    ("""\
0: 4 1 5
1: 2 3 | 3 2
2: 4 4 | 5 5
3: 4 5 | 5 4
4: "a"
5: "b"

ababbb
bababa
abbbab
aaabbb
aaaabbb
""", 2)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


"""
42 - babbb | baabb | bbbab | bbbbb
31 - abaaa | aabaa
"""
"""
            [          11          ] 
                  [    11   ] 
  42    42    42    42    31    31
babbb baabb bbbab bbbbb aabaa abaaa

bbbabbbbbbaabaaabaaa
"""


@pytest.mark.parametrize('val,expect', [
    ("""\
42: 9 14 | 10 1
9: 14 27 | 1 26
10: 23 14 | 28 1
1: "a"
11: 42 31
5: 1 14 | 15 1
19: 14 1 | 14 14
12: 24 14 | 19 1
16: 15 1 | 14 14
31: 14 17 | 1 13
6: 14 14 | 1 14
2: 1 24 | 14 4
0: 8 11
13: 14 3 | 1 12
15: 1 | 14
17: 14 2 | 1 7
23: 25 1 | 22 14
28: 16 1
4: 1 1
20: 14 14 | 1 15
3: 5 14 | 16 1
27: 1 6 | 14 18
14: "b"
21: 14 1 | 1 14
25: 1 1 | 1 14
22: 14 14
8: 42
26: 14 22 | 1 20
18: 15 15
7: 14 5 | 1 21
24: 14 1

abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
""", 12)
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


"""
other

bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""

"""
ok
bbabbbbaabaabba
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
"""
"""

all
# abbbbbabbbaaaababbaabbbbabababbbabbbbbbabaaaa
bbabbbbaabaabba
babbbbaabbbbbabbbbbbaabaaabaaa
aaabbbbbbaaaabaababaabababbabaaabbababababaaa
bbbbbbbaaaabbbbaaabbabaaa
bbbababbbbaaaaaaaabbababaaababaabab
ababaaaaaabaaab
ababaaaaabbbaba
baabbaaaabbaaaababbaababb
abbbbabbbbaaaababbbbbbaaaababb
aaaaabbaabaaaaababaa
# aaaabbaaaabbaaa
aaaabbaabbaaaaaaabbbabbbaaabbaabaaa
# babaaabbbaaabaababbaabababaaab
aabbbbbaabbbaaaaaabbbbbababaaaaabbaaabba
"""
puzzle_input = """\
70: 90 92 | 53 50
99: 90 102 | 53 22
24: 130 90
125: 85 53 | 100 90
61: 53 58 | 90 26
88: 33 53 | 46 90
32: 65 90 | 90 53
48: 46 53
116: 53 50 | 90 18
40: 53 83 | 90 81
54: 46 53 | 5 90
36: 50 90 | 130 53
58: 92 90 | 130 53
2: 19 53 | 75 90
95: 53 46 | 90 19
124: 46 53 | 33 90
79: 91 53 | 7 90
46: 90 90 | 53 90
87: 9 90 | 84 53
122: 90 46 | 53 33
15: 89 90 | 79 53
41: 90 4 | 53 119
7: 53 128 | 90 128
93: 53 120 | 90 37
121: 15 53 | 103 90
91: 90 33 | 53 110
5: 53 90 | 65 53
26: 53 19 | 90 107
44: 53 75 | 90 32
23: 107 53 | 50 90
33: 90 53 | 90 90
75: 53 53 | 90 90
18: 65 65
59: 53 107 | 90 32
104: 90 33 | 53 46
20: 121 90 | 123 53
100: 90 75 | 53 46
131: 18 90 | 46 53
9: 90 67 | 53 105
37: 53 75 | 90 128
3: 53 29 | 90 22
120: 53 92 | 90 33
35: 55 53 | 30 90
115: 65 107
106: 90 46 | 53 19
89: 90 59 | 53 68
83: 90 46 | 53 130
25: 90 87 | 53 41
11: 42 31
84: 53 117 | 90 34
8: 42
53: "a"
86: 53 6 | 90 12
76: 53 78 | 90 97
52: 126 90 | 115 53
31: 53 35 | 90 20
112: 110 90 | 32 53
82: 101 90 | 127 53
119: 53 27 | 90 93
117: 90 81 | 53 23
57: 82 53 | 43 90
105: 90 126 | 53 21
111: 53 32 | 90 110
68: 53 18 | 90 46
73: 71 90 | 24 53
49: 77 90 | 48 53
81: 90 50 | 53 75
102: 32 53 | 128 90
12: 92 53 | 19 90
60: 62 90 | 108 53
101: 53 104 | 90 62
65: 53 | 90
50: 53 90
97: 53 56 | 90 64
63: 99 90 | 39 53
43: 90 125 | 53 60
66: 130 90 | 33 53
27: 53 2 | 90 14
4: 3 90 | 74 53
118: 53 76 | 90 57
113: 86 53 | 13 90
56: 90 28 | 53 54
38: 36 90 | 69 53
39: 10 53 | 23 90
14: 90 50 | 53 18
45: 53 72 | 90 40
21: 130 90 | 107 53
30: 90 113 | 53 1
19: 53 53 | 90 53
130: 53 53
110: 53 65 | 90 90
0: 8 11
77: 53 110 | 90 92
62: 53 33 | 90 19
126: 50 90
29: 75 53 | 5 90
129: 98 53 | 47 90
47: 53 94 | 90 95
71: 107 53
92: 53 53 | 90 65
127: 22 53 | 109 90
6: 92 53 | 32 90
51: 26 90 | 66 53
107: 90 53 | 53 90
72: 90 124 | 53 104
1: 53 96 | 90 52
103: 53 73 | 90 61
74: 2 90 | 131 53
64: 90 7 | 53 122
67: 53 70 | 90 104
42: 53 25 | 90 118
123: 63 90 | 80 53
17: 46 53 | 130 90
10: 19 90 | 33 53
13: 53 112 | 90 17
28: 90 128 | 53 110
114: 53 5 | 90 50
78: 49 90 | 51 53
16: 111 53 | 14 90
90: "b"
85: 130 90 | 50 53
80: 38 53 | 16 90
69: 110 53 | 107 90
98: 53 44 | 90 88
94: 5 53 | 46 90
108: 18 53 | 75 90
55: 90 129 | 53 45
128: 90 90
34: 106 90 | 114 53
109: 90 110 | 53 50
96: 36 90 | 116 53
22: 75 53 | 18 90

aaaaaaaabbbbaabaabbbaaba
aaaaaaaaabbaaabbbaabaaaaabbaaabaaabbbbbb
babaabaaabaaabbbaaaabbba
baaaabbbabbabbbbabaababa
aaaaabaabbbabbbabaaabababaabaabbbaaaabba
babababbbaababbabaaaaaab
bbabbbabbabaaabaaaaaaaba
bbaabbaaaababbabbbabbbbb
babbbbbbbbbababaaaabbbab
abbbbbbaaaabbaaaaabbaaababbbbbababbaaaab
aabbaabaaabaabaababbbaaa
baaabaabaaabaabbbbaaaaba
aabababbaabaaaabbaaaabaaabbbbbaa
bbbbbababbaabaaabaababbababbaabababbababbaabbabaaaabbbba
bbbaabbbaababbaaaaaaaabb
aaababbbbbaaababababaabb
bbabaabbababbbaabbababaa
baaabababbbbbaaababbabab
aaaababaaabbaababbaaaabb
ababbabaaabaaaabbbbaaaba
bbaaababbbbababbabbaabba
babbbbbbbbbababababbaaab
babaabbbbababaababbaabaabbabaabb
baaaaabaaaaaabaabbaaabaa
aabbabaaabaaabababbbbaab
bababaabaabbaabbababaaab
babaababbbbbbabababbbaaa
babaaabbaababaaaaaaabbbb
bbbbbabbbbaabaaabbaabbaabaabbaabaababbaa
bbababaaaaaaaababbbaabbabbbaabbabbabbaabaaaaaaaaabbbabbbbaabbaababaaaaabaabbaaaa
abaaabababaaabaabbbaaaaa
baabbbbbabbbabbbbbaababbaababaaabbbbaaaa
abbbabbbabbbaabbbaaaabab
babbabbbabbbbabbaaabbaaabbababbabbbbbbaababaabbb
babaabaaabbaabaaaaabbbbbabaabaaaabbbbaaaaaaababbabbaabbbaaabaaaababaaaba
aabbababbaaaaaaabbbbababbaabbbbaaababbbbaaaabbabbabbbbaaaabbababbbbbabba
bbaaabbaabaabaaabbaaaabb
bbaabaaaabbabbababbbbbabbaaaaaababbaabbb
baaababaabbbabaabbaaaaabaaababab
abababbabbaabaabbaaabbaa
bbbbabbaababaaaabbbbaaaababbabbbabbbbbabbbaaabbabbbbbbbabbbaabababaabbbb
bbabaaaaaaababbababbabaaaaaaabaabbbbbaaabababbaaaaaaaabbbbabaabaaaaaabbbbababaabaabbaababbaaabab
babaaaabbaaabababbaaabbbbaaaaaaa
babbbabbbaabbababbbaaabb
abbbabaaabbabbbbbbabababaaaaabba
baaaaaaaaababaaaabbbbbaabbaaaaba
bbbabbbababbaababaabbabaaabbbabbabaaaababbbaaaab
bbbaabaaabbaaaaabbabaaaa
abababbabaababbaaabaabaaaaababbbbaaabbaabbbababbababaaba
bbbaabbbbbbbbbaababbaabababbaabaabbbbaba
babbaaaaaabaaabaabaabaabbbaaaababaaaaabaabbbaaaabbbabaabbabbbaabbbabaaab
bbabbbbaababaabbababbbbaaaaabaabbaababbbabaabaaaaababaaabbabbbba
abbabaaaaabbbbbabbaaabbb
aababaaaaaaabaaabbababbb
babbbbbbbbbababaaaabaaab
bbbabaabababaaaabaaaabba
aaababbbbabbaabbbabbbabbbbababaa
abbbbaaaabaaaabaabaaaaba
bbabaabbbaabbabbaaaababbbbbaabbaabaaaaaabbabbbbaababaaba
abaaababaaaaaaabbbabbbbaabbababbbbbaababbbbbabbaabbbbbababbabbbb
bababaababbaaaaaaabbabab
baaabbaabbaabaaababbababbbabbbabbbbbbaab
baaaaababaababbaaaababab
abbaabaabbbabbaaaaabaaab
abbbabbaabbaaaaabbbbaaaabaababbabaabbbaa
bbaabbbbbaabbaaaabaabaaaababbaaa
aaabaaaaabbabbabaaababaa
aabaabbaaabbbbbaabbbbbbaabaabbba
aababbaababbbabbabbbabab
bbabbaaaaabbbbbaaabababa
aaabbbbbabbbbbaababaabba
aaaaaaaabbabaaabbbabbbaa
bbbabaaaaaabaaaaaaababaa
aabbbabbbabbabababbbabbbbbbbabba
baababbababbaabaabbbbaba
abbbaabbbabbbabbabbabbaa
aabbaabbabbbbbbabaabbabbabbbbbbbaaabbbbbaaaabbba
bababaabaabaaabaaaabbbaa
bbbabaabbaaababababbbbba
abbbaabbbbbaaaabbabbbbabababbabb
baabaaaabbababbbabbaabbabaaaabab
babaabbabbaabbbabbaabbababbbbabb
aaaaabbbaaabbbbbabbabbbbbbbabaabbbabbbababaaaaaa
babaaaabbababbaaababaababaaaabba
bababaabbbbabababbabaaba
aaabbbbbaabababbababbabb
bbbaabbbbabbbbbbaabaabab
baababbabbbbbabaabaabbbb
abbbabaabbbbaabaababbbaa
aababaaaaabaaabaaaaaaaba
abbbbaaaababaaabbaaaaaaababbaaaababbbaabbaabbbbbaabbababbaaabbbb
bbbbbbaabbbababaabaaaababbbbbaabaabbaaaabbbbaaababababaa
bbbaabbaaaabaaababbabbaaaabbabbabaabbbaaaabaaaaa
bbbabbbabbbbbaababaaabbbaaababbaabaabaaa
abbbabbaabbaaaaaaabababa
baabaabbabaaabbabbbaaabb
aaabaabaabaaabaaababbbaa
babbaabaabaaaabbabbbbaba
bbbbaabbbaabbaabbbabbbbaabaaababaaaaabab
baabaabbaaaaabaaaabbabaabbbbbabaaababbabbbbbababbabaabbbbbabaaba
abaaabbaaabaabbaaaaabbba
ababaaaabbaaaaaaabbbaabbabbbbabb
babaabbababbbabbabaabaabbbbbaabbbabaaabbaaabbbba
baabbbbbbbbabbbbbababbab
ababbababaaaaabbbbbabbbbabaaaabbaaaaabaaabaababb
aaabaabababaabababbababb
aaabbbbaaaaabbbbbbabbabbbabaabaabbaaaaaabaaaaabbbbbabbbabaaaaabaababaaba
bbaabbaaaaaababbbaababaa
aaaaabbbbbaaaaabbaababaa
aaabbbbbabbbbbababbbaabbaaabbabbabaaabbb
baaaaabbbbbbbbbabbbbbabbbaabbbababbbbbaa
abbabababbbbabbabbaabbaabaaaabaabbbbbaaabbbbbbaaabbabbbabbbaaabbbbaaabab
bbabbbabbbbabaaaabbabbabbaaabbab
aabbaaabaabbbabbbbbaaaba
ababbabaabbbaabbaaaaabbbaabaabbbbbbbbbbbbaaabbbbbaabaaabbaaaabba
bbabbbababababaabbaaabbb
babbabbbbbbabbbabbabaabbabbaaabbababbababbabbbbbabababaa
bbaaaaabaabaabaabbbabbbbaabbbbbbaaaaaaba
aaaaababbaaaaababaaabaaaaaaaaaabababbabbabbaaaaa
abaaabbbaaabaabaaabaaaabaaabbbaa
baaaaababbabbbbaaaaaaaaabbbbabba
bbaabbaabbbbbabaaabbbbbabaaabaaaaaabbaba
bbaaabbabaaaaabbaabbaababaaaabaaababbbab
aabbaaababbbbbbbaabbabba
abbabbabbbaaabbababaaaaa
abbaabaabbbbbbbbbbbabbbbbabaabaa
aabbabaaababbabaabbbaaaa
bbabaababbabbaaaaaabbbbbabbaabaabaaabbbbbabbaabbbaaaaababbaababbbbababab
bbabbaabbbabbbbabaaabbaa
aaaabbababbaaabbabbbabaabbbaaababababbab
aaaababbaaabaabbbaabaaab
aabbaabbaaabaaaabbaabbab
babababbaabbbbabbbabbaabbaaaaababaabbabbabbabbbaabababaabbabbbaa
baabbaabbababbbbabaaaaba
aabaaabbababbbaaabbbabaabaaaabbbabaabbaaabbbaabaaaabaaaaabaaabbabbbabbbb
aabbbbbbaabaaabaaabbbbabaaabaabaababbaababbaabab
bbbabbbaaaaabaabbbbbbaaaaabbbbbabbabaaabbbbaabba
aabbbaaaabaaaabbbbbabbab
bbaaaaaaabbbbbbbababbbaa
baaaabbbabbbbbbbbbaababa
abbabaaaaabbbbbaaabbaaaa
bbbbbbbbaabaabbbbaaaabba
aabaaaaaaabbbaababbaabbbbababbabababaaab
aaaabbabaabbabaaaaabbbab
baaabbbbbbbabaabbbaabaabaaaaababbaabbbbababbbbababbbbababbbbbbab
baabbbbbbababbbbabaaaaaa
bbbbbbbbbaaaaababbabbbbbbbbaaabb
abbaaabbaaaabbabbaabbabbbbaababbbbbbbabb
abbabababbaabaaaabbbaaba
abbabaaaaabbbbbbaaaabbbb
bbaabaababababbabbabaaaa
ababbbbbbabbabbababbaababbbabbabbbabbabaaaaaababaaaabaabbbaababa
bbabbabbabbababaaaababaa
baabbaaabaabaaaaabaaaaab
bbbabbaabbaaababbaaaaaab
bbbbaabaababbabababbaaaa
babbbabbabbabbabbbaaabbaaabbaabababbbabb
aaaababbbaaaaababbbbbbaaabaababb
bbbbaaaabbbbaaaaaabaaababbaabaababababaa
baabbbabaaababababbbabab
aaaaaaabbbbbbabaababbabb
aaaaaababbbaaaaabababbab
baaabbbbaaaabababababbba
ababbbabaaaabbabaaaaabababaabbba
abbabbbbbabbaabaabaababb
baaaaababbbaabababbaabab
babbaaaaaabbbbaabbabbbabbbbbbababaabbabbababaaba
bbbbbaaaaabababbaabaabbaabbbaabbabaabbba
bbbbaabaaaabbbbbbabbaaab
baaababaaababbaaaabbbbbbabaaaaaa
aaabbaaaababaabbabbbbabbbbaaaaaaaaabbaaabaabbaabbbbabbabbabbaaabaaabaabb
aabaabbabbbabbbaabaaaaab
abaabaaaaabaabaaabaabbba
aabbbbabaaababbbababbbaa
bbabaaababbabbabaabbaabbbbbbabba
aabbbaaaaabbbbbbbababaaabaabbbaa
abbbbabbaabbabaabaababaaabbabaaabaabaabbaaaaabaabbaaabbabbaaaaab
bbbabaaabbaabbbbaaaaaaba
baaaaabbaaaaabaabbababbb
bbbabbbbbabbbbbbbbbbabab
abbbabaabbaaababbbbbabaa
aaaaabaaaaababbbabaaaabbabaaaaba
abbababbbbbaaabbaaaabbbabaaabbbaaaaabbaababaaaababaaaabb
abaabbbbbbbabaabababbabbbbabaaabbabababbaaabbaabbaababab
baabbababbbabbaaaaaaaaba
aabbbabbaaaabaaaababaaab
abbabaaaaabbbbabbabbbbaaabbbbbabbbaaaabbbbaababb
abbbbbbaaaabaababbaabbaa
bbbbaabaabaaababaaabbabbaabbbabbbbababbbaabbabbabaabaaba
abbbabaaaababaaaababaaab
bbabaaababbaabbababbabaabaababaa
aaaabbbaaaaabbbbabbbbbbabbbabaabbbabbbaabbaabababababaaabbbaabbabbabaaaabbbbbbbbabaaabba
abbaabaabbbabbbbabaaaaab
abbaaaaababbbbbbbabbabbaabbababbaaaaaabbabbaaaabaabbbaba
aababaaaaabaaabbbaabaaab
bbbabababbbabbbbabbabaaababaaaaa
abbbbaaababbaaabbaaaabbabaabaaab
abaabaabbbbabaabaabababa
aaaaaaaaabaaababbbabbabbaaaaaaabaaaabbababababaa
abababbbabababbaaabbabbbbbaabbbbbbaaababbbabbbbaabbabbaa
bbbbbabaaabbbbabaaabbabbabababbaaaaabbbb
aabbbbaaaaababbbaabbabba
baaaaababaaaaababbabbbbaaaaaabaaababbaaabaaaaaaa
abaaaabbabbaaababbabbbbb
bbaabaaabaaaaabbbabbaabaaaabaabbaaaaabba
abbbbbbbbabbbbaabbabaaaaabbabbbabaaabaaa
bbbaabaaabaaaababbbbbabbbbbbbabbbbaaaaba
abbaaabbbaabaabbbbbbaaab
aaabbaaabbabbaabbababbaa
abbbabbbabababbababaaaaa
bbabbbbabaaaaababbaababbbbbaabaabbabbaaaaaaaabbbaaabbaab
abaaababbbaabaaababbabaa
bbaabaabbaaabbbbbaaaaabbaabbbbbbabbabaaabbaabababababbbabaaaabab
abbaaaaaaabbabaababbbbba
bbbababababaaabbabaaaaaa
babbbabbbbbabaabababbabb
abbaaaaaabbabaaabbbbaabbbabababa
abbabbbbbbabaabbbabbabba
baabaaaaaaaabaabbbbababaaaabbaaabbbaaabbbabbbaba
baaabaababbaaabbabbbbabb
abaabaabbbbbaabbababbbaa
bbbbaabaabbababbbbababaabaaabbabbbbbabbabbbabbab
bbabaaababbabaaaaaabaabbaabaaabaaabbaababbaaabbbbbbbabba
bbbabaaaabbabbabbbbabbab
bababaaababbbbbbbaabbbaa
abbbbbbbbbabbaaabbababbb
aabbaaabaabbbaaabbbaaaba
aabbabbbbabaabababbabbaa
abbbabaababaaabbabaabaaaaabbbbababaaabaababbaaaa
aaaaabaabaaababaabaaaaab
bbbaabbbbbaabbaababaabbb
abaaaabbabbabbbbbbbbaaab
aabababbbaaabababbabbabbaaaaabab
bbabbaaaaaaaaaabbaaababb
baaaaabaaaabaaaabbbabbbbaabbbbaaabaabbabbabbbbbababaaaaa
aaababbaaababaaaaaabaababbbabaaa
babbaabbbaaabaababaabbba
abbbabaaabbababaaababbbb
abbbaabbbabbababaabbaaabbabbaaaa
bbbaabababbaaabaaaababab
aaaaaaaaabbabbabababaabbbbaaaabbbbababbaaaabbaaaabababaabaabababbbbaaabaaaabaabb
bbbbbaaabababbabaabbbbaabaaaaabbabbbabbabaabbbbaaabaababbbaabbba
aaabbabbaabbaaabbbaaabbaaabbbbbabaaaaabaaababaaabaabaaab
bbaababbaabbbbbbaabbbaaaabaabbab
bbbbababababaaaaabbbaabbaaababbbababbabaaabbbaaa
bababaaaaabaaabbbbabbababbbbbaaa
babababbaaaaaaababaababb
bbaaaaaaaabababbabbaabab
abbaaaaabbbbbbaaaababaab
babaababaababbaabbbabbbbbabbabbb
aabbbbbbaababaaaababaabb
aaaababbabababbabbabbabbbbaaababbabbbaab
bbabbaaaaabaaababaabbaabaaaaabab
aaaaaaaabbbbbaaaabbaabab
abaaaabbbabbbabbabaabaabbbaaaaabbbbaabbb
babaaabbabababbabbaaaaba
baaababaabbabaabbaababbb
aababaaaabaaabbaabaababa
bbbabaabbabbbabbbbaaabbb
abaaabbabbaabbaabaaabbaa
bbbababbbbbbbaaabababbbaabbbaabbbaabaaabbabbabbabbaabaaaababbbbbbbbbbababbbabbaa
bbbbaaaaaabbbabbabbaabaababbababaabbabaaaaababbbbaababaa
bababbbbbaabbaababababbbabbbaaab
bbaababbabbbaabbbababbab
baabaabbaabbaabbbaaaabab
aaaaabbbbababaabaabaaaaa
bbbabaababbabaaabbbbabab
bbbabaabaaaaaaaabaabbbababbaaabaaaabbabbaaaaabbbabbaaabb
aabbabaabbbbaabaaababaaaabbbabbbbbbaaaaababbbbab
aaaaaaabbabaaabbababaabb
abaaabaabbabbaaabbbbbaab
aabaabbaabbabaaabbabbabbabbbbbbbaaaabbbb
baabaaaabbbabaabaabbaabbaababbaaaabbaaaaaababaab
baabbaaaaabbbbbbabbabbba
aabbbbbbbbaababbaaabaabaabbbabaababbbabaabbababb
bbabaabbbabbaababbababba
bbbbaabbbbaabbaaabbbbaba
aaababbabaabbabbabaaaaab
aaabaabaaaaaabaaabababab
ababbabaabbbbbabbabbaababababbba
abbaaabbbbbabaabaabbbbbababaababaabaabaabbaabbbaabbbbaaa
baabbaabbbaaabbaabaaaabbbbbbbbaaabaaababababbbba
aaaababaaaaabbabaabbaaaababaabaabaabababababbbbaaabbaaaa
aaabaabbbbbaabaaababaaba
bababaabaabbbabbaaaabbababbabbaa
baabaaaaaabbaababaaababb
baaaabaaaaaaaaaabbabbbaa
babbaabbabaaabaaabbaabaabababbbabaababababaaaaaaabaaaaabaaabbbba
abbaaaaabaabbbbbabaaaaaabbbbbbba
aaabbaaaabaaaabbbaababab
baaabbbbaabbbabbaabbbaab
babbaabbbabbabaaababbbababaababbbabbbbbbbbaabaaaabaaabbbbaabbbbbbaaabbbb
bbabbabaaaaaaaabaaaaaabb
ababbbbbababbabaaabbaababababbbbabbbbaaaaaaaaaaaabbbbbbabbbaabba
aaababbaaabababbababaaba
aaaaababbababbabbaaabbbbbbaaaabaaaabbabb
baabbbbbabbbabbbaaabaaab
babaaababaababbbababbbbabbababababbbbaab
abaabaabbabababbbaababbbbabbbbab
baababbababaaaaaaababaababbaabaaaabaaabaabbbbbbabbbbabaabbbababbaaaabbbabaaaaababbbababaabaaabab
bbbbbbaaabbababaabbbbaab
abbaaaaabbabbabaababbaaa
baaabbbbaabaabbbbbbabbbbbaaaabab
bbbbbbaaaabaabaabaaabbaa
aabaabbabbbabbbaabaaabbb
bbaababbaabbbbabbbababbb
bababaaabbabbbabaaaaabbbaaabbaab
babbabbbbbabaabbbbabbbbaaabbbaaabaabbbbaaabbaaaabbbbabbb
babbababbbabbabaabbbbaab
aaaabbabbbabbbbabbbbaabaabbabababaaabaabbbbbbbbabaaaabba
bbbbaaabaaabaaaaabbaabababaaabbbabbabbbb
bbbabababbbbbbaaabbbbbaa
baababbabaabbabbaabaabbbaabbbbbabbabbbaa
bbaabbbbbbabbababaaabbaa
aaaaaababaabbbbbbaabbabbbababaaaaababababaaabbabaaaabbbbaaaabbabbabbbaab
babbbabbbaaabbbbbbaaaaaaaaabaabbbaabbaaaaababaabababaaba
abababbbaaaababbbbaaabaa
ababbabaaaaababbabaaaaaa
bababaaaabbaaabbbababbab
bbaabbbaabbabbbbaabababa
baabbbbbabbabbabbbbbaaab
abbaaaaaaaaabaaabaaaabba
aabbaabbbbbabbaababbababaaabaabb
bbaababbbbbabbbaaaababbabbaababbabababbabbababaabbaaabaaabaabbaa
abbbbbabaaabbabbababbaab
aaaaabaaaabaaaababbbbaaa
aabaaabbbabbabbbabababaa
aabbbabbaaaaabbbaababaab
abababbbbbaabbaaabbbaabbaaaaabaabaaaabaabbbaaababbaababaabaababaababbbbb
babbaabaabababbbaaabbaab
abbbaabbabbbbbbbbaaababababbbaabbababbab
aaaababbabbaaaaabaabaabbbbabbbaaaaaaabba
bababbbbbbbbaabbaaaabbba
bbaabbbaaaaaabbbbabbbbaa
aabbaabaabbbabaabababbbbbbbbabab
babababbabbbabaabbbabaaaabababaa
babaaababbaaaabbbaabbbba
ababaaaaabbbbbbbbaabbabbbabbaabbaaaabababaababaa
bbaaaaabbaaaabbbbabbaabaababaababaabbaabababbbbaabbabbaa
baabbabbaaabaabbbbbbaabaaaaabaabaabaabab
aaababbbbbaababbabbabbaa
aabbaaabaabbaaabbaababab
abbabaaaaababaaaaaaaaaaabaaabaaabbbbabaa
aaabaabaabbbabaabaabbabbaababaaaabaababa
abbabbabbababbbbbaaaaaab
aabaaabbbbbaaaabbbabababbaaaabbbaaabbbab
bababbaaababbabababbabaabababaababbabaaaaaabaaaabbaaaaaabaabaaab
aababaaabaaaaabbabababaa
aabbabaabbabbaaabbbaaaba
aabbabbbabbabaababbaaaaaaabbbabbaaabbaabaaaabbbbaaaabbba
abababbabbbbaaaababbbbab
aaaabbbbbbbbaabbbaababbaaabbbbbaaababbabbbbaaaaaababaabbababbbaabaababba
abaaabbababababbbabababa
abaaabbaabababbbbaaaaaaabbbbabbb
aabababbbbbabaaababbabbbababaabb
abababbaabbbaabbaabbbbbabbbbbbbb
aabaabbbbbaabbbabaaabbbbbbaaaaaabbbbbbbabababbaabaaaabaa
babaaaabaaababbaaabababa
bbaabbbaababbababbbaaaab
bbbaaaababbbbbaabbbbbababbababbaabbaabababbabbbababbbbababbbabaaaabbabaaabaaaababbbbbaaaabaaabbb
baabaabbbaabbabaaababbba
bbbaabbbbbababbbbbbbaababbaabbaabbbbbaababbaabbabbbbaaabaabaabbabaabbbaa
bbbbbbbababbbbbbaabaababaaaaabbbbbbabbbb
aababbaabbbbaabbbbbaabbbaabaabaaaaaaabbbbabababa
abbbabaaabaaabbabbaaaaba
aaaaabbbaabbbbbbaaababbbbabaabbaababaabbbabaaaaabbaaabbb
babbabbbbbabaaabaaaabbaa
bbbbaabbaaaaabaabbabbaaabbabaaaa
aaababbbaabaaabbbbbaabba
aabbaabbababaaaaabbababbbababbaaabbbbaabbbbaaabbbaaabaab
bbabbabaabbabaabababaaab
bbaaababbbbbaabababbbbaa
aaaababaabbaaabbabbbbbaa
bbaabbbaabaabaabbbaaaaababbabaabbbabbabaaabbabbabbbbabaa
babbababaabaaabababbababbbaaababbbabbbbbbabababa
aababbaaaaabaabbbbaaabaaabbbbabb
bbbaaabbabaabbbbaabbabbbbabbaabbbabaababbbbaaaaaaababaabaaaaaaabbababaaa
abbaaabbbbabbaaaabaabbba
aaaaabaaaaaabbabbbaabaaaabaaaaaa
aaabbbbbbaabaabbabbbaaab
abaabaabbabaabbabbababbb
aabbbaaaabababbababbbabbbabbabababbbbaabbaaaaaaa
baababaababbabbbbbbabbbbababbabaabaaaaba
bbaabbaabbaaaaaaaaabbaba
aaaaabbbbaabbababababbbbbaababbaaaabbaab
abbaabbabaaabbbaaaaaaabbaababbbaaabbbbbbabaaaaabbaabaaaabaaaaaababaabaababbbbbbbbaabbabb
baababbabbabbabaabbabaaababbbaaa
baabbaabaababbabbbbbabbb
aabbaaababbbabbbbaabbaabababbbbb
aabbbabbaaabaabaabbbaaab
abbbbbbbbabababbbbaaaaabaabaabbbbababbaa
bbbbbaaabbabaaabaababbababbababababaabbbbabaaaaa
abbabbabaabbbbbbaabbbbbbbabbabbbabbaaaaaabbbaabababbaaaa
aaaababbaababbabaaaaabaaabbbbbbbbbbbbaba
bbbbabbaabaaabbabbaaabbaaababbaabbabbabaababaababbaaabaa
aaabbbbbbaabaabbbbaababa
baabaaaaaaabbabbbabbbabbbabbaaabbaaaabab
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
