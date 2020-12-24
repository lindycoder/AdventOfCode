from dataclasses import dataclass, field
from functools import wraps
from typing import Dict, Generic, Iterable, Iterator, Optional, \
    TypeVar

import pytest
from hamcrest import assert_that, has_properties, is_

T = TypeVar('T')


def _set_first(fn):
    @wraps(fn)
    def wrapper(self, value: T) -> 'Circle':
        if self._current is None:
            self._current = Circle._Link(value)
            self._current.before = self._current
            self._current.after = self._current
            self._value_cache[value] = self._current
            return self

        return fn(self, value)

    return wrapper


@dataclass
class Circle(Iterable[T]):
    _current: Optional['_Link'] = None
    _value_cache: Dict[T, '_Link'] = field(default_factory=dict)

    @property
    def current(self):
        return self._current.value

    @classmethod
    def from_iterable(cls, iterable: Iterable[T]) -> 'Circle':
        circle = cls()
        for e in iterable:
            circle.insert_before(e)
        return circle

    @_set_first
    def insert_before(self, value: T) -> 'Circle':
        return self._insert(value, self._current.before, self._current)

    @_set_first
    def insert_after(self, value: T) -> 'Circle':
        return self._insert(value, self._current, self._current.after)

    def _insert(self, value: T, before: '_Link', after: '_Link') -> 'Circle':
        new = Circle._Link(value, before=before, after=after)
        self._value_cache[value] = new
        before.after = new
        after.before = new
        return self

    def pop(self) -> T:
        current = self._current

        current.before.after = current.after
        current.after.before = current.before

        self._current = current.after
        self._value_cache.pop(current.value)
        return current.value

    def turn_cw(self):
        self._current = self._current.after

    def turn_ccw(self):
        self._current = self._current.before

    def seek(self, value: T) -> 'Circle':
        self._current = self._value_cache[value]
        return self

    def __iter__(self) -> Iterator[T]:
        start_at = self._current
        stop_at = self._current

        def iteration():
            current = start_at
            while True:
                yield current.value
                current = current.after
                if current is stop_at:
                    return

        return iteration()

    @dataclass
    class _Link(Generic[T]):
        value: T
        before: Optional['Circle._Link'] = None
        after: Optional['Circle._Link'] = None

        def __repr__(self):
            return f'({self.before.value}) ' \
                   f'-> ({self.value}) ' \
                   f'-> ({self.after.value})'


def test_insert_before():
    circle = Circle().insert_before('a')
    assert_that(list(iter(circle)), is_(['a']))

    circle.insert_before('b')
    circle.insert_before('c')
    circle.insert_before('d')

    assert_that(list(iter(circle)), is_(['a', 'b', 'c', 'd']))


def test_insert_after():
    circle = Circle().insert_before('a')
    assert_that(list(iter(circle)), is_(['a']))

    circle.insert_after('b')
    circle.insert_after('c')
    circle.insert_after('d')

    assert_that(list(iter(circle)), is_(['a', 'd', 'c', 'b']))


@pytest.mark.parametrize('iterable,matches', [
    ([1], [1]),
    ([1, 2], [1, 2]),
    (['a', 'b'], ['a', 'b']),
    (list(range(10)), list(range(10))),
])
def test_from_iterable(iterable, matches):
    assert_that(list(Circle.from_iterable(iterable)), is_(matches))


def test_seek():
    circle = Circle.from_iterable(range(10))
    circle.seek(5)
    assert_that(circle, has_properties(current=5))
    circle.seek(5)
    assert_that(circle, has_properties(current=5))


def test_seek_notfound():
    circle = Circle.from_iterable(range(10))
    with pytest.raises(KeyError):
        circle.seek('A')
