import hashlib
import re
import sys
import unittest

from hamcrest import assert_that, is_, contains_string, starts_with


def simple_hash(input):
    return hashlib.md5(bytes(input, "UTF-8")).hexdigest()


def stretched_hash(input):
    result = simple_hash(input)
    for i in range(0, 2016):
        result = simple_hash(result)

    return result


def compute(salt, hashing=simple_hash):
    pending_keys = []
    confirmed_keys = []

    index = 0
    while len(confirmed_keys) < 64:
        hash = hashing(salt + str(index))

        fives = get_fives(hash)
        if fives:
            for key in pending_keys[:]:
                if index - key.start_index > 1000:
                    pending_keys.remove(key)
                elif key.character in fives:
                    pending_keys.remove(key)
                    confirmed_keys.append(key)

        triple = get_triple(hash)
        if triple:
            pending_keys.append(Key(index, triple))

        index += 1

    return confirmed_keys[63].start_index

class Key(object):
    def __init__(self, start_index, character):
        self.start_index = start_index
        self.character = character


def get_triple(input):
    match = re.match(".*?(.)\\1\\1.*", input)
    if match:
        return match.group(1)
    return None


def get_fives(input):
    return list(set(re.findall("(.)\\1\\1\\1\\1", input)))


class GetTripleTest(unittest.TestCase):
    def test_get_triple(self):
        assert_that(get_triple("aaa"), is_("a"))
        assert_that(get_triple("baaab"), is_("a"))
        assert_that(get_triple("bbaaa"), is_("a"))
        assert_that(get_triple("aaabb"), is_("a"))

    def test_triple_not_found(self):
        assert_that(get_triple("aa"), is_(None))
        assert_that(get_triple("baab"), is_(None))
        assert_that(get_triple("bbaa"), is_(None))
        assert_that(get_triple("aabb"), is_(None))

    def test_get_first_triple(self):
        assert_that(get_triple("bbbaaa"), is_("b"))
        assert_that(get_triple("aabbbaaa"), is_("b"))
        assert_that(get_triple("aabbbffaaa"), is_("b"))
        assert_that(get_triple("aabbbbbaaa"), is_("b"))
        assert_that(get_triple("bbbcdefaaa"), is_("b"))



class HasFiveTest(unittest.TestCase):
    def test_has_five(self):
        assert_that(get_fives("aaaaa"), is_(["a"]))
        assert_that(get_fives("baaaaab"), is_(["a"]))
        assert_that(get_fives("bbaaaaa"), is_(["a"]))
        assert_that(get_fives("aaaaabb"), is_(["a"]))

    def test_has_not_five(self):
        assert_that(get_fives("aaaa"), is_([]))
        assert_that(get_fives("baaaab"), is_([]))
        assert_that(get_fives("bbaaaa"), is_([]))
        assert_that(get_fives("aaaabb"), is_([]))

    def test_get_multiple_fives(self):
        assert_that(set(get_fives("aaaaabbbbb")), is_({"a", "b"}))
        assert_that(set(get_fives("faaaaabbbbb")), is_({"a", "b"}))
        assert_that(set(get_fives("faaaaafbbbbb")), is_({"a", "b"}))
        assert_that(set(get_fives("faaaaafbbbbbf")), is_({"a", "b"}))
        assert_that(set(get_fives("faaaaaaaaafbbbbbbbbbf")), is_({"a", "b"}))



class HashTest(unittest.TestCase):
    def test_simple_hash(self):
        assert_that(simple_hash("abc18"), contains_string("cc38887a5"))

    def test_stretched_hash(self):
        assert_that(stretched_hash("abc0"), starts_with("a107ff"))


class ComputeTest(unittest.TestCase):
    def test_official(self):
        assert_that(compute("abc"), is_(22728))

    def test_official2(self):
        assert_that(compute("abc", hashing=stretched_hash), is_(22551))


if __name__ == '__main__':
    puzzle_input = "jlmsuwbz"

    if sys.argv[1] == "1":
        result = compute(puzzle_input)
    else:
        result = compute(puzzle_input, hashing=stretched_hash)

    print("Result is {}".format(result))
