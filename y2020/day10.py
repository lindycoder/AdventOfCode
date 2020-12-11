import sys
from collections import defaultdict

import pytest
from hamcrest import assert_that, is_


def compute(data):
    numbers = prep_numbers(data)

    differences = defaultdict(lambda: 0)
    for a, b in zip(numbers[:-1], numbers[1:]):
        differences[b - a] += 1

    return differences[1] * differences[3]


def prep_numbers(data):
    numbers = sorted(map(int, data.strip().splitlines()))
    return [0] + numbers + [numbers[-1] + 3]


def compute2(data):
    numbers = prep_numbers(data)

    branchings = defaultdict(lambda: 1)

    for number in reversed(numbers[:-1]):
        branches_total = sum(branchings[number + i]
                             for i in range(1, 4)
                             if number + i in numbers)
        branchings[number] = branches_total

    return branchings[0]


@pytest.mark.parametrize('val,expect', [
    ("""\
16
10
15
5
1
11
7
19
6
12
4
""", 35),
    ("""\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""", 220),
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
16
10
15
5
1
11
7
19
6
12
4
""", 8),
    ("""\
28
33
18
42
31
14
46
20
48
47
24
23
49
45
19
38
39
11
1
32
25
35
8
17
7
9
4
2
34
10
3
""", 19208),
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
149
87
67
45
76
29
107
88
4
11
118
160
20
115
130
91
144
152
33
94
53
148
138
47
104
121
112
116
99
105
34
14
44
137
52
2
65
141
140
86
84
81
124
62
15
68
147
27
106
28
69
163
97
111
162
17
159
122
156
127
46
35
128
123
48
38
129
161
3
24
60
58
155
22
55
75
16
8
78
134
30
61
72
54
41
1
59
101
10
85
139
9
98
21
108
117
131
66
23
77
7
100
51
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
