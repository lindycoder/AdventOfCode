import sys
import unittest
from textwrap import dedent

from hamcrest import assert_that, is_
import pytest

def compute(data):
    return sum(fuel(int(m)) for m in data.strip().split())


def compute2(data):
    return sum(rec_fuel(int(m)) for m in data.strip().split())


def fuel(val):
    return int(val / 3) - 2


def rec_fuel(val):
    total = fuel(val)
    val = total
    while True:
        new_fuel = fuel(val)
        if new_fuel <= 0:
            return total
        total += new_fuel
        val = new_fuel


@pytest.mark.parametrize('val,expect',[
(12, 2),
(14, 2),
(1969,  654),
(100756, 33583),
] )
def test_fuel(val,expect):
    assert_that(fuel(val), is_(expect))

@pytest.mark.parametrize('val,expect',[
(14, 2),
(1969,  966),
(100756, 50346),
] )
def test_rec_fuel(val,expect):
    assert_that(rec_fuel(val), is_(expect))


puzzle_input = """\
124846
99745
110203
140165
110228
65706
128481
75921
57331
72951
133413
99524
79546
54653
55166
66215
147696
91054
64752
76311
139572
61110
65846
121489
147534
66591
109963
83412
138965
70102
128844
141002
77655
68539
128687
70559
140747
51397
117550
91515
60960
133280
83244
106644
100333
67608
118120
60024
115547
136229
108403
128776
109599
111189
98538
129715
116630
120772
80105
52489
130247
144003
85226
83769
137921
54737
126406
108756
149633
138201
78980
126909
125768
86214
54873
97723
92677
120405
143317
102981
142668
100398
67258
126583
114611
102525
115205
78329
140703
136978
94465
129510
81039
141997
120643
55377
89966
113672
112665
51323
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
