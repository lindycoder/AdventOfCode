import re
import sys
import unittest
from dataclasses import dataclass, field
from datetime import date, timedelta
from textwrap import dedent
from typing import List, DefaultDict

from hamcrest import assert_that, is_


def compute(data):
    sleeps_by_guards = group_sleeps_by_guards(parse(data))

    guard, minutes_sleeping = max(
        ((guard, sum(len(sleep)
                     for sleep in sleeps))
         for guard, sleeps in sleeps_by_guards.items()),
        key=lambda e: e[1]
    )

    minute, times = most_slept_minute(sleeps_by_guards[guard])

    return guard * minute


def compute2(data):
    sleeps_by_guards = group_sleeps_by_guards(parse(data))

    guard, (minute, times) = max(((guard, most_slept_minute(sleeps))
                                  for guard, sleeps in sleeps_by_guards.items()),
                                 key=lambda e: e[1][1])

    return guard * minute


def group_sleeps_by_guards(shifts):
    sleeps_by_guards = DefaultDict(lambda: [])

    for shift in shifts:
        for sleep in shift.sleeps:
            sleeps_by_guards[shift.guard].append(sleep)

    return sleeps_by_guards


def time_asleep_at_minute(minute, sleeps):
    return len(list(filter(lambda sleep: minute in sleep, sleeps)))


def most_slept_minute(sleeps):
    minute, times = max(((minute, time_asleep_at_minute(minute, sleeps))
                         for minute in range(0, 60)),
                        key=lambda e: e[1])

    return minute, times


def parse(input):
    shifts_by_date = DefaultDict(lambda: Shift(), {})
    sleeps_by_date = DefaultDict(lambda: [])

    for line in input.split("\n"):
        y, m, d, h, n, event = re.match(r"\[(\d+)-(\d+)-(\d+) (\d+):(\d+)\] (.*)", line).groups()

        shift_date = date(int(y), int(m), int(d))

        if int(h) >= 1:
            shift_date += timedelta(days=1)

        match = re.match(r"Guard #(\d+) begins shift", event)
        if match:
            if shift_date in shifts_by_date:
                raise Exception("there's already a guard here")
            shifts_by_date[shift_date].guard = int(match.group(1))
        else:
            sleeps_by_date[shift_date].append(int(n))

    shifts = []

    for day, shift in shifts_by_date.items():
        shift.day = day

        events = list(sorted(sleeps_by_date[day]))
        if len(events) % 2 != 0:
            raise Exception("Off number of events")
        shift.sleeps = [Sleep(a, b) for a, b in zip(events[0::2], events[1::2])]

        shifts.append(shift)

    return list(sorted(shifts, key=lambda e: e.day))


@dataclass
class Sleep:
    start: int = None
    stop: int = None

    def __contains__(self, item):
        return self.start <= item < self.stop

    def __len__(self):
        return self.stop - self.start


@dataclass
class Shift:
    day: date = None
    guard: int = None
    sleeps: List[Sleep] = field(default_factory=list)


class ParseTest(unittest.TestCase):
    def test_parse(self):
        input = dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:05] falls asleep
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-02 00:40] falls asleep
            [1518-11-02 00:50] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-03 00:24] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-05 00:55] wakes up""")

        shifts = parse(input)

        assert_that(shifts, is_([
            Shift(day=date(1518, 11, 1), guard=10, sleeps=[Sleep(5, 25), Sleep(30, 55)]),
            Shift(day=date(1518, 11, 2), guard=99, sleeps=[Sleep(40, 50)]),
            Shift(day=date(1518, 11, 3), guard=10, sleeps=[Sleep(24, 29)]),
            Shift(day=date(1518, 11, 4), guard=99, sleeps=[Sleep(36, 46)]),
            Shift(day=date(1518, 11, 5), guard=99, sleeps=[Sleep(45, 55)]),
        ]))

    def test_parse_month_overlap(self):
        input = dedent("""\
            [1518-06-30 23:58] Guard #99 begins shift
            [1518-07-01 00:40] falls asleep
            [1518-07-01 00:50] wakes up""")

        shifts = parse(input)

        assert_that(shifts, is_([
            Shift(day=date(1518, 7, 1), guard=99, sleeps=[Sleep(40, 50)]),
        ]))

    def test_parse_and_order(self):
        input = dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:25] wakes up
            [1518-11-03 00:24] falls asleep
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-01 00:30] falls asleep
            [1518-11-02 00:40] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-02 00:50] wakes up
            [1518-11-04 00:36] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 00:05] falls asleep
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:46] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:55] wakes up""")

        shifts = parse(input)

        assert_that(shifts, is_([
            Shift(day=date(1518, 11, 1), guard=10, sleeps=[Sleep(5, 25), Sleep(30, 55)]),
            Shift(day=date(1518, 11, 2), guard=99, sleeps=[Sleep(40, 50)]),
            Shift(day=date(1518, 11, 3), guard=10, sleeps=[Sleep(24, 29)]),
            Shift(day=date(1518, 11, 4), guard=99, sleeps=[Sleep(36, 46)]),
            Shift(day=date(1518, 11, 5), guard=99, sleeps=[Sleep(45, 55)]),
        ]))


class SleepTest(unittest.TestCase):
    def test_contains(self):
        assert_that(1 in Sleep(30, 55), is_(False))
        assert_that(30 in Sleep(30, 55), is_(True))
        assert_that(38 in Sleep(30, 55), is_(True))
        assert_that(54 in Sleep(30, 55), is_(True))
        assert_that(55 in Sleep(30, 55), is_(False))
        assert_that(56 in Sleep(30, 55), is_(False))

    def test_len(self):
        assert_that(len(Sleep(30, 55)), is_(25))


class ToolsTest(unittest.TestCase):
    def test_time_asleep_at_minute(self):
        assert_that(time_asleep_at_minute(24, [Sleep(5, 25), Sleep(30, 55), Sleep(24, 29)]), is_(2))

    def test_most_slept_minute(self):
        assert_that(most_slept_minute([Sleep(5, 25), Sleep(30, 55), Sleep(24, 29)]), is_((24, 2)))


class DayTest(unittest.TestCase):
    def test_provided(self):
        input = dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:05] falls asleep
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-02 00:40] falls asleep
            [1518-11-02 00:50] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-03 00:24] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-05 00:55] wakes up""")

        assert_that(compute(input), is_(240))

    def test_provided2(self):
        input = dedent("""\
            [1518-11-01 00:00] Guard #10 begins shift
            [1518-11-01 00:05] falls asleep
            [1518-11-01 00:25] wakes up
            [1518-11-01 00:30] falls asleep
            [1518-11-01 00:55] wakes up
            [1518-11-01 23:58] Guard #99 begins shift
            [1518-11-02 00:40] falls asleep
            [1518-11-02 00:50] wakes up
            [1518-11-03 00:05] Guard #10 begins shift
            [1518-11-03 00:24] falls asleep
            [1518-11-03 00:29] wakes up
            [1518-11-04 00:02] Guard #99 begins shift
            [1518-11-04 00:36] falls asleep
            [1518-11-04 00:46] wakes up
            [1518-11-05 00:03] Guard #99 begins shift
            [1518-11-05 00:45] falls asleep
            [1518-11-05 00:55] wakes up""")

        assert_that(compute2(input), is_(4455))


puzzle_input = """\
[1518-08-29 00:24] falls asleep
[1518-08-06 00:20] falls asleep
[1518-03-12 00:21] falls asleep
[1518-06-17 00:45] wakes up
[1518-06-27 00:46] falls asleep
[1518-09-07 00:36] falls asleep
[1518-07-22 00:23] wakes up
[1518-05-18 00:35] falls asleep
[1518-09-27 00:40] wakes up
[1518-04-10 23:52] Guard #3559 begins shift
[1518-03-16 00:44] wakes up
[1518-05-16 00:23] wakes up
[1518-06-18 00:00] Guard #1499 begins shift
[1518-11-21 00:48] wakes up
[1518-05-19 00:29] falls asleep
[1518-03-20 23:58] Guard #73 begins shift
[1518-09-28 00:18] falls asleep
[1518-10-21 00:00] Guard #983 begins shift
[1518-05-19 00:57] wakes up
[1518-10-08 00:47] wakes up
[1518-05-04 00:19] falls asleep
[1518-07-30 00:30] falls asleep
[1518-05-04 00:22] wakes up
[1518-10-01 00:20] wakes up
[1518-03-24 23:47] Guard #2411 begins shift
[1518-06-19 00:00] Guard #1499 begins shift
[1518-09-15 00:38] falls asleep
[1518-07-26 00:50] falls asleep
[1518-06-13 00:00] Guard #3499 begins shift
[1518-08-30 00:03] Guard #983 begins shift
[1518-04-18 00:44] wakes up
[1518-07-09 00:53] falls asleep
[1518-06-09 00:02] falls asleep
[1518-10-09 23:56] Guard #3559 begins shift
[1518-04-15 23:46] Guard #313 begins shift
[1518-10-06 00:03] Guard #3499 begins shift
[1518-10-27 23:59] Guard #2617 begins shift
[1518-10-21 00:33] wakes up
[1518-03-23 00:47] falls asleep
[1518-07-21 00:31] wakes up
[1518-06-05 00:21] falls asleep
[1518-03-11 00:54] wakes up
[1518-05-06 00:11] wakes up
[1518-04-09 00:39] wakes up
[1518-06-10 00:00] Guard #919 begins shift
[1518-11-10 00:57] falls asleep
[1518-09-27 00:27] falls asleep
[1518-07-29 00:53] falls asleep
[1518-07-26 00:38] falls asleep
[1518-08-05 00:01] falls asleep
[1518-06-07 00:59] wakes up
[1518-11-22 00:39] falls asleep
[1518-11-17 00:58] wakes up
[1518-11-04 00:22] falls asleep
[1518-09-10 00:34] wakes up
[1518-04-11 00:25] wakes up
[1518-04-14 23:58] Guard #3203 begins shift
[1518-06-22 00:22] falls asleep
[1518-04-07 00:48] falls asleep
[1518-11-15 00:57] wakes up
[1518-05-24 23:56] Guard #983 begins shift
[1518-07-29 00:59] wakes up
[1518-11-15 00:05] falls asleep
[1518-11-22 00:02] Guard #3499 begins shift
[1518-11-01 00:46] wakes up
[1518-08-31 00:01] Guard #2411 begins shift
[1518-06-30 00:39] falls asleep
[1518-04-29 00:24] wakes up
[1518-04-12 23:54] Guard #2099 begins shift
[1518-05-04 00:48] falls asleep
[1518-09-25 00:49] falls asleep
[1518-09-21 00:28] falls asleep
[1518-04-25 00:44] falls asleep
[1518-04-13 00:43] falls asleep
[1518-08-24 00:16] falls asleep
[1518-07-02 00:43] wakes up
[1518-04-26 00:00] Guard #241 begins shift
[1518-06-26 00:29] falls asleep
[1518-04-17 00:47] wakes up
[1518-11-23 00:28] falls asleep
[1518-10-04 00:53] wakes up
[1518-11-20 00:46] falls asleep
[1518-06-28 00:37] wakes up
[1518-09-12 00:21] falls asleep
[1518-04-20 23:54] Guard #73 begins shift
[1518-03-21 23:57] Guard #1811 begins shift
[1518-07-04 00:48] wakes up
[1518-09-25 00:34] wakes up
[1518-04-13 00:35] wakes up
[1518-08-29 00:02] Guard #2657 begins shift
[1518-03-30 00:03] Guard #1811 begins shift
[1518-11-16 00:22] falls asleep
[1518-08-16 00:29] falls asleep
[1518-08-07 00:27] falls asleep
[1518-03-26 23:57] Guard #1091 begins shift
[1518-09-13 00:21] falls asleep
[1518-11-12 00:42] wakes up
[1518-05-14 00:01] Guard #1291 begins shift
[1518-03-21 00:39] falls asleep
[1518-04-23 00:22] falls asleep
[1518-09-19 00:05] falls asleep
[1518-04-02 00:42] falls asleep
[1518-04-27 00:39] wakes up
[1518-03-24 00:02] Guard #1033 begins shift
[1518-03-16 00:59] wakes up
[1518-05-11 23:50] Guard #3109 begins shift
[1518-04-18 00:06] falls asleep
[1518-08-31 00:33] wakes up
[1518-09-18 23:48] Guard #3559 begins shift
[1518-04-21 00:30] wakes up
[1518-10-07 00:44] wakes up
[1518-09-30 00:57] falls asleep
[1518-10-08 00:56] wakes up
[1518-06-19 00:37] wakes up
[1518-10-22 00:33] falls asleep
[1518-10-20 00:52] falls asleep
[1518-11-13 00:27] wakes up
[1518-07-05 00:11] falls asleep
[1518-08-17 00:48] wakes up
[1518-07-25 00:45] wakes up
[1518-05-01 23:59] Guard #3109 begins shift
[1518-07-31 00:10] falls asleep
[1518-05-26 00:54] falls asleep
[1518-08-10 23:57] Guard #3203 begins shift
[1518-06-26 00:06] falls asleep
[1518-09-24 00:12] falls asleep
[1518-04-11 00:01] falls asleep
[1518-06-01 00:02] Guard #2657 begins shift
[1518-06-30 23:49] Guard #241 begins shift
[1518-10-29 00:49] wakes up
[1518-06-12 00:44] wakes up
[1518-04-16 00:01] falls asleep
[1518-10-13 00:55] wakes up
[1518-05-21 00:28] falls asleep
[1518-06-21 00:17] falls asleep
[1518-06-05 00:47] falls asleep
[1518-05-10 00:19] falls asleep
[1518-09-05 00:04] falls asleep
[1518-04-23 00:12] falls asleep
[1518-07-16 00:56] wakes up
[1518-07-26 00:00] Guard #3499 begins shift
[1518-08-27 00:47] falls asleep
[1518-09-24 00:32] falls asleep
[1518-09-15 00:03] Guard #313 begins shift
[1518-11-21 00:04] Guard #3499 begins shift
[1518-07-11 00:49] wakes up
[1518-06-27 00:35] falls asleep
[1518-07-17 00:59] wakes up
[1518-05-13 00:10] falls asleep
[1518-09-28 00:04] Guard #3559 begins shift
[1518-10-03 00:00] Guard #313 begins shift
[1518-06-15 00:27] falls asleep
[1518-09-24 00:59] wakes up
[1518-10-29 23:50] Guard #983 begins shift
[1518-06-17 00:48] falls asleep
[1518-09-24 00:01] Guard #241 begins shift
[1518-05-28 23:56] Guard #2657 begins shift
[1518-04-17 00:00] Guard #1291 begins shift
[1518-05-29 00:34] wakes up
[1518-03-16 00:48] falls asleep
[1518-05-25 00:59] wakes up
[1518-04-11 00:42] falls asleep
[1518-06-02 23:59] Guard #241 begins shift
[1518-04-13 00:00] falls asleep
[1518-07-22 00:35] falls asleep
[1518-09-19 23:56] Guard #3109 begins shift
[1518-08-05 23:52] Guard #3449 begins shift
[1518-08-25 00:18] wakes up
[1518-07-14 23:57] Guard #2617 begins shift
[1518-05-08 00:19] falls asleep
[1518-10-11 00:02] Guard #2657 begins shift
[1518-03-21 00:22] falls asleep
[1518-06-23 00:10] falls asleep
[1518-05-28 00:41] falls asleep
[1518-09-01 00:02] Guard #3109 begins shift
[1518-09-13 00:43] wakes up
[1518-05-19 00:16] wakes up
[1518-10-03 00:59] wakes up
[1518-05-04 00:59] wakes up
[1518-06-15 00:53] falls asleep
[1518-07-16 00:09] falls asleep
[1518-08-11 00:48] falls asleep
[1518-08-15 00:00] Guard #823 begins shift
[1518-07-31 00:44] wakes up
[1518-04-28 23:51] Guard #73 begins shift
[1518-04-21 00:46] falls asleep
[1518-09-21 00:42] wakes up
[1518-05-27 00:26] falls asleep
[1518-08-23 00:04] Guard #3203 begins shift
[1518-07-13 00:01] falls asleep
[1518-08-14 00:01] falls asleep
[1518-07-10 00:50] wakes up
[1518-11-05 00:37] wakes up
[1518-08-12 00:58] wakes up
[1518-03-11 00:33] falls asleep
[1518-09-20 00:32] falls asleep
[1518-09-03 00:56] wakes up
[1518-03-21 00:40] wakes up
[1518-07-03 00:22] falls asleep
[1518-08-16 23:46] Guard #313 begins shift
[1518-10-31 00:00] Guard #919 begins shift
[1518-08-11 00:32] wakes up
[1518-08-25 23:58] Guard #1033 begins shift
[1518-09-01 23:57] Guard #2617 begins shift
[1518-06-17 00:53] wakes up
[1518-10-18 00:42] falls asleep
[1518-07-11 00:14] falls asleep
[1518-03-13 00:27] falls asleep
[1518-10-28 00:58] wakes up
[1518-07-31 00:01] Guard #3499 begins shift
[1518-04-22 00:49] wakes up
[1518-10-17 00:42] wakes up
[1518-03-14 00:02] Guard #1033 begins shift
[1518-08-09 00:38] falls asleep
[1518-04-26 23:58] Guard #3109 begins shift
[1518-05-09 00:34] falls asleep
[1518-11-09 23:57] Guard #2099 begins shift
[1518-05-22 00:28] falls asleep
[1518-08-08 00:28] wakes up
[1518-11-23 00:42] wakes up
[1518-09-16 00:19] falls asleep
[1518-04-08 00:12] falls asleep
[1518-10-03 00:47] wakes up
[1518-04-10 00:22] falls asleep
[1518-07-30 00:37] wakes up
[1518-11-16 00:47] wakes up
[1518-08-12 00:13] falls asleep
[1518-08-04 00:33] falls asleep
[1518-09-24 00:14] wakes up
[1518-09-13 00:56] wakes up
[1518-10-10 00:25] falls asleep
[1518-04-14 00:01] Guard #3559 begins shift
[1518-06-25 23:59] Guard #241 begins shift
[1518-07-19 00:02] falls asleep
[1518-03-15 00:01] Guard #1033 begins shift
[1518-09-18 00:15] falls asleep
[1518-11-09 00:35] falls asleep
[1518-08-22 00:11] falls asleep
[1518-10-07 23:59] Guard #2411 begins shift
[1518-08-02 23:59] Guard #3361 begins shift
[1518-06-26 00:53] wakes up
[1518-04-01 00:16] falls asleep
[1518-11-08 23:58] Guard #2617 begins shift
[1518-09-02 00:57] wakes up
[1518-07-06 00:46] falls asleep
[1518-07-21 00:17] falls asleep
[1518-05-01 00:58] wakes up
[1518-06-21 00:23] wakes up
[1518-07-01 00:47] wakes up
[1518-09-07 00:41] wakes up
[1518-05-05 00:34] wakes up
[1518-04-02 00:01] Guard #2099 begins shift
[1518-07-03 00:19] wakes up
[1518-06-01 00:39] falls asleep
[1518-04-06 00:08] falls asleep
[1518-08-24 00:01] Guard #2657 begins shift
[1518-07-01 23:51] Guard #3109 begins shift
[1518-08-13 00:04] Guard #2099 begins shift
[1518-08-09 00:34] wakes up
[1518-05-31 00:40] wakes up
[1518-06-26 00:45] falls asleep
[1518-06-26 23:59] Guard #983 begins shift
[1518-07-01 00:36] wakes up
[1518-03-24 00:26] falls asleep
[1518-04-19 00:55] falls asleep
[1518-04-06 00:09] wakes up
[1518-10-15 00:24] falls asleep
[1518-04-30 00:47] falls asleep
[1518-05-08 00:08] falls asleep
[1518-09-24 00:56] falls asleep
[1518-04-24 00:04] Guard #3361 begins shift
[1518-07-06 00:59] wakes up
[1518-06-24 00:28] wakes up
[1518-08-11 00:19] falls asleep
[1518-04-19 23:58] Guard #1291 begins shift
[1518-03-18 00:32] wakes up
[1518-10-23 00:04] falls asleep
[1518-10-19 00:04] Guard #3203 begins shift
[1518-04-05 00:31] wakes up
[1518-03-13 00:04] Guard #3449 begins shift
[1518-06-15 00:22] wakes up
[1518-03-26 00:10] falls asleep
[1518-07-07 00:34] wakes up
[1518-04-27 00:24] falls asleep
[1518-04-30 00:49] wakes up
[1518-04-17 00:18] falls asleep
[1518-09-11 00:20] falls asleep
[1518-05-07 00:56] wakes up
[1518-05-23 00:24] wakes up
[1518-03-28 00:44] wakes up
[1518-08-10 00:12] falls asleep
[1518-06-12 00:13] falls asleep
[1518-09-23 00:58] wakes up
[1518-08-29 00:59] wakes up
[1518-09-04 00:33] falls asleep
[1518-05-29 00:09] falls asleep
[1518-04-25 00:00] Guard #3203 begins shift
[1518-07-30 00:55] wakes up
[1518-10-31 23:57] Guard #983 begins shift
[1518-11-05 00:29] falls asleep
[1518-06-06 00:12] falls asleep
[1518-03-18 00:29] falls asleep
[1518-08-30 00:58] wakes up
[1518-11-08 00:13] wakes up
[1518-08-08 00:11] falls asleep
[1518-07-12 23:50] Guard #2099 begins shift
[1518-03-15 00:56] wakes up
[1518-06-07 00:39] falls asleep
[1518-11-02 00:29] wakes up
[1518-06-13 00:43] wakes up
[1518-07-21 23:47] Guard #2099 begins shift
[1518-10-12 00:38] wakes up
[1518-08-23 00:36] falls asleep
[1518-08-04 23:53] Guard #1091 begins shift
[1518-06-29 00:51] wakes up
[1518-03-28 00:10] falls asleep
[1518-10-20 00:23] falls asleep
[1518-11-12 00:04] Guard #2411 begins shift
[1518-04-17 00:59] wakes up
[1518-10-07 00:32] falls asleep
[1518-09-06 00:39] wakes up
[1518-03-27 00:34] falls asleep
[1518-05-27 00:53] wakes up
[1518-10-05 00:15] falls asleep
[1518-10-02 00:15] falls asleep
[1518-07-12 00:37] wakes up
[1518-07-16 23:57] Guard #983 begins shift
[1518-09-03 00:20] falls asleep
[1518-04-13 00:46] wakes up
[1518-06-14 23:50] Guard #983 begins shift
[1518-09-12 00:48] falls asleep
[1518-09-11 23:57] Guard #73 begins shift
[1518-07-26 00:51] wakes up
[1518-09-01 00:45] falls asleep
[1518-05-30 00:53] wakes up
[1518-08-09 00:28] falls asleep
[1518-10-03 00:29] falls asleep
[1518-09-02 00:49] wakes up
[1518-09-06 00:03] falls asleep
[1518-03-18 23:49] Guard #3449 begins shift
[1518-07-04 00:03] Guard #2411 begins shift
[1518-08-01 00:21] falls asleep
[1518-06-15 00:44] wakes up
[1518-11-22 23:56] Guard #3499 begins shift
[1518-06-14 00:08] falls asleep
[1518-08-01 00:03] Guard #1291 begins shift
[1518-05-26 00:56] wakes up
[1518-07-17 23:47] Guard #1091 begins shift
[1518-11-02 00:03] Guard #3559 begins shift
[1518-04-07 00:51] wakes up
[1518-06-03 00:56] wakes up
[1518-10-15 00:40] wakes up
[1518-07-29 00:40] falls asleep
[1518-06-25 00:18] falls asleep
[1518-08-06 00:51] falls asleep
[1518-05-23 00:11] falls asleep
[1518-09-10 23:59] Guard #2411 begins shift
[1518-08-23 00:59] wakes up
[1518-03-15 00:29] falls asleep
[1518-06-25 00:00] Guard #3499 begins shift
[1518-06-02 00:38] wakes up
[1518-07-25 00:29] falls asleep
[1518-04-19 00:49] wakes up
[1518-04-01 00:46] wakes up
[1518-11-10 23:49] Guard #241 begins shift
[1518-06-06 00:24] wakes up
[1518-07-04 00:22] falls asleep
[1518-05-28 00:54] wakes up
[1518-07-25 00:57] wakes up
[1518-03-30 00:54] falls asleep
[1518-11-10 00:58] wakes up
[1518-06-15 00:58] wakes up
[1518-03-25 23:58] Guard #1033 begins shift
[1518-08-10 00:00] Guard #3109 begins shift
[1518-11-05 23:48] Guard #73 begins shift
[1518-10-25 00:08] falls asleep
[1518-08-25 00:35] falls asleep
[1518-04-25 00:52] wakes up
[1518-04-05 23:57] Guard #2617 begins shift
[1518-09-20 00:55] falls asleep
[1518-08-11 00:52] wakes up
[1518-05-09 00:49] wakes up
[1518-08-02 00:38] wakes up
[1518-07-07 23:57] Guard #983 begins shift
[1518-09-29 00:42] wakes up
[1518-05-31 00:50] falls asleep
[1518-08-04 00:57] falls asleep
[1518-08-20 00:42] wakes up
[1518-10-28 00:57] falls asleep
[1518-11-20 00:54] wakes up
[1518-10-08 00:13] falls asleep
[1518-09-30 00:58] wakes up
[1518-07-18 23:53] Guard #3499 begins shift
[1518-03-15 23:50] Guard #1811 begins shift
[1518-07-23 00:33] falls asleep
[1518-08-26 00:35] wakes up
[1518-11-07 00:17] falls asleep
[1518-07-20 00:30] wakes up
[1518-10-13 23:52] Guard #2657 begins shift
[1518-05-21 00:31] wakes up
[1518-11-01 00:21] falls asleep
[1518-10-24 00:26] falls asleep
[1518-04-28 00:02] Guard #1811 begins shift
[1518-08-02 00:18] falls asleep
[1518-10-26 00:09] falls asleep
[1518-06-26 00:21] wakes up
[1518-11-17 00:48] falls asleep
[1518-08-28 00:45] falls asleep
[1518-09-08 00:26] wakes up
[1518-09-30 00:00] Guard #3499 begins shift
[1518-09-25 00:00] Guard #1091 begins shift
[1518-09-17 00:03] Guard #313 begins shift
[1518-05-11 00:10] falls asleep
[1518-11-18 00:32] wakes up
[1518-06-08 00:48] wakes up
[1518-08-06 00:00] falls asleep
[1518-09-23 00:06] falls asleep
[1518-05-25 00:29] falls asleep
[1518-08-31 00:22] falls asleep
[1518-07-11 00:55] falls asleep
[1518-11-10 00:50] falls asleep
[1518-04-28 00:33] falls asleep
[1518-11-13 00:05] falls asleep
[1518-07-25 00:49] falls asleep
[1518-04-07 00:14] falls asleep
[1518-09-05 23:50] Guard #3559 begins shift
[1518-03-31 23:58] Guard #3203 begins shift
[1518-07-24 00:03] Guard #823 begins shift
[1518-06-07 00:34] wakes up
[1518-05-15 00:19] falls asleep
[1518-04-09 00:05] falls asleep
[1518-07-30 00:06] falls asleep
[1518-10-17 00:01] Guard #3203 begins shift
[1518-06-19 00:45] falls asleep
[1518-05-16 00:20] falls asleep
[1518-08-22 00:33] wakes up
[1518-06-08 00:14] falls asleep
[1518-11-10 00:35] wakes up
[1518-08-19 00:50] wakes up
[1518-03-28 00:03] Guard #241 begins shift
[1518-07-23 00:04] Guard #2617 begins shift
[1518-06-13 00:26] falls asleep
[1518-05-08 23:56] Guard #2099 begins shift
[1518-03-22 23:50] Guard #3361 begins shift
[1518-08-21 23:58] Guard #313 begins shift
[1518-05-18 00:40] wakes up
[1518-04-29 00:01] falls asleep
[1518-08-08 00:54] wakes up
[1518-11-01 00:53] falls asleep
[1518-10-06 00:36] falls asleep
[1518-03-19 00:19] wakes up
[1518-05-28 00:11] falls asleep
[1518-04-03 00:04] Guard #313 begins shift
[1518-11-02 23:59] Guard #73 begins shift
[1518-03-24 00:42] wakes up
[1518-05-31 00:33] falls asleep
[1518-05-17 00:23] wakes up
[1518-08-08 00:41] falls asleep
[1518-09-22 00:08] falls asleep
[1518-11-01 00:31] wakes up
[1518-11-06 00:22] wakes up
[1518-04-08 23:51] Guard #3559 begins shift
[1518-11-11 00:39] wakes up
[1518-08-01 23:56] Guard #1033 begins shift
[1518-05-05 23:58] Guard #3499 begins shift
[1518-10-11 23:58] Guard #2099 begins shift
[1518-06-08 00:54] wakes up
[1518-05-23 00:21] falls asleep
[1518-04-04 00:22] falls asleep
[1518-05-26 00:02] Guard #919 begins shift
[1518-04-14 00:51] wakes up
[1518-07-20 00:13] falls asleep
[1518-07-07 00:02] Guard #2099 begins shift
[1518-10-18 00:15] falls asleep
[1518-09-09 23:58] Guard #241 begins shift
[1518-07-31 00:41] falls asleep
[1518-05-26 00:46] wakes up
[1518-11-09 00:39] wakes up
[1518-09-02 00:27] falls asleep
[1518-10-31 00:49] falls asleep
[1518-06-30 00:56] falls asleep
[1518-08-07 00:55] wakes up
[1518-06-06 23:59] Guard #3499 begins shift
[1518-03-24 00:58] wakes up
[1518-06-11 00:02] Guard #919 begins shift
[1518-06-11 00:14] falls asleep
[1518-07-17 00:41] wakes up
[1518-05-27 00:00] Guard #3499 begins shift
[1518-11-19 00:02] Guard #3109 begins shift
[1518-09-17 00:21] falls asleep
[1518-11-03 00:53] falls asleep
[1518-03-24 00:51] falls asleep
[1518-04-30 00:02] Guard #1499 begins shift
[1518-07-22 00:01] falls asleep
[1518-03-25 00:00] falls asleep
[1518-06-05 00:43] wakes up
[1518-06-05 00:56] falls asleep
[1518-08-24 00:35] wakes up
[1518-06-22 00:02] Guard #2411 begins shift
[1518-09-22 23:59] Guard #2657 begins shift
[1518-06-14 00:48] wakes up
[1518-07-09 00:00] Guard #3361 begins shift
[1518-10-20 00:53] wakes up
[1518-05-03 23:56] Guard #3559 begins shift
[1518-10-09 00:10] falls asleep
[1518-08-25 00:31] wakes up
[1518-06-10 00:57] wakes up
[1518-07-05 23:58] Guard #3361 begins shift
[1518-04-05 00:26] falls asleep
[1518-10-07 00:00] Guard #1811 begins shift
[1518-05-16 00:58] wakes up
[1518-08-25 00:11] falls asleep
[1518-04-24 00:58] wakes up
[1518-03-12 00:29] wakes up
[1518-05-07 00:35] wakes up
[1518-08-14 00:39] wakes up
[1518-08-16 00:36] wakes up
[1518-07-10 00:22] falls asleep
[1518-10-31 00:09] falls asleep
[1518-04-08 00:03] Guard #2411 begins shift
[1518-10-01 00:05] falls asleep
[1518-10-15 00:46] falls asleep
[1518-09-09 00:30] wakes up
[1518-03-14 00:50] wakes up
[1518-08-17 00:02] falls asleep
[1518-08-03 00:59] wakes up
[1518-03-26 00:56] wakes up
[1518-10-28 00:08] falls asleep
[1518-07-23 00:52] wakes up
[1518-05-15 00:49] wakes up
[1518-10-21 00:15] falls asleep
[1518-06-17 00:00] Guard #983 begins shift
[1518-05-07 00:52] falls asleep
[1518-08-31 00:58] wakes up
[1518-07-04 23:59] Guard #2099 begins shift
[1518-04-09 00:46] wakes up
[1518-06-03 00:36] falls asleep
[1518-05-06 00:06] falls asleep
[1518-04-07 00:01] Guard #1291 begins shift
[1518-06-17 00:15] falls asleep
[1518-09-24 00:53] wakes up
[1518-09-13 00:01] Guard #2099 begins shift
[1518-07-14 00:04] Guard #2579 begins shift
[1518-06-28 00:20] falls asleep
[1518-06-27 00:58] wakes up
[1518-05-02 00:19] falls asleep
[1518-04-19 00:44] falls asleep
[1518-08-09 00:45] wakes up
[1518-04-27 00:44] wakes up
[1518-07-15 00:53] wakes up
[1518-10-06 00:55] wakes up
[1518-09-08 00:25] falls asleep
[1518-06-03 00:55] falls asleep
[1518-05-28 00:43] wakes up
[1518-07-11 00:04] Guard #3559 begins shift
[1518-07-09 23:59] Guard #3499 begins shift
[1518-09-18 00:57] wakes up
[1518-11-14 00:01] falls asleep
[1518-10-08 23:58] Guard #1811 begins shift
[1518-04-12 00:50] wakes up
[1518-04-08 00:28] wakes up
[1518-04-10 00:59] wakes up
[1518-10-29 00:16] falls asleep
[1518-11-07 00:29] wakes up
[1518-08-13 23:50] Guard #2099 begins shift
[1518-10-10 00:49] wakes up
[1518-06-02 00:09] falls asleep
[1518-03-25 00:30] wakes up
[1518-09-04 23:46] Guard #2657 begins shift
[1518-03-30 23:58] Guard #1867 begins shift
[1518-05-03 00:04] falls asleep
[1518-11-19 00:50] falls asleep
[1518-07-08 00:37] wakes up
[1518-07-16 00:20] wakes up
[1518-08-27 00:31] falls asleep
[1518-04-15 00:23] wakes up
[1518-08-05 00:27] wakes up
[1518-07-05 00:13] wakes up
[1518-08-06 00:42] wakes up
[1518-05-28 00:03] Guard #3449 begins shift
[1518-04-14 00:13] falls asleep
[1518-10-16 00:45] falls asleep
[1518-07-29 00:00] Guard #1811 begins shift
[1518-05-24 00:57] wakes up
[1518-06-01 00:48] wakes up
[1518-09-12 00:29] wakes up
[1518-04-06 00:15] falls asleep
[1518-06-06 00:03] Guard #2657 begins shift
[1518-07-28 00:41] wakes up
[1518-09-30 00:39] falls asleep
[1518-06-30 00:59] wakes up
[1518-09-01 00:51] wakes up
[1518-08-04 00:59] wakes up
[1518-03-22 00:46] falls asleep
[1518-05-13 00:00] Guard #1499 begins shift
[1518-07-08 00:36] falls asleep
[1518-04-09 00:45] falls asleep
[1518-05-01 00:01] Guard #1499 begins shift
[1518-09-22 00:03] Guard #3559 begins shift
[1518-05-12 00:54] wakes up
[1518-11-04 00:57] wakes up
[1518-04-21 00:00] falls asleep
[1518-11-19 23:56] Guard #2617 begins shift
[1518-07-16 00:42] falls asleep
[1518-04-10 00:00] Guard #1811 begins shift
[1518-11-10 00:34] falls asleep
[1518-08-18 00:01] Guard #241 begins shift
[1518-08-04 00:45] wakes up
[1518-11-21 00:36] falls asleep
[1518-06-07 00:15] falls asleep
[1518-10-28 00:36] wakes up
[1518-07-15 23:57] Guard #2657 begins shift
[1518-06-29 00:46] falls asleep
[1518-03-17 00:54] wakes up
[1518-08-22 00:12] wakes up
[1518-11-20 00:26] wakes up
[1518-10-02 00:23] wakes up
[1518-07-26 00:43] wakes up
[1518-04-23 00:57] wakes up
[1518-04-22 23:57] Guard #2099 begins shift
[1518-03-21 00:46] falls asleep
[1518-04-04 00:30] wakes up
[1518-04-20 00:45] wakes up
[1518-08-31 00:47] falls asleep
[1518-09-16 00:34] wakes up
[1518-10-05 00:03] Guard #3499 begins shift
[1518-04-11 23:57] Guard #3499 begins shift
[1518-08-29 00:29] wakes up
[1518-10-13 00:43] falls asleep
[1518-07-12 00:29] falls asleep
[1518-05-08 00:55] wakes up
[1518-03-29 00:01] Guard #2579 begins shift
[1518-10-31 00:56] wakes up
[1518-11-17 00:49] wakes up
[1518-06-03 23:46] Guard #313 begins shift
[1518-05-02 00:48] wakes up
[1518-05-17 23:58] Guard #3499 begins shift
[1518-03-27 00:30] wakes up
[1518-09-21 00:02] Guard #2099 begins shift
[1518-05-22 00:30] wakes up
[1518-10-04 00:40] wakes up
[1518-03-23 00:49] wakes up
[1518-08-16 00:00] Guard #3361 begins shift
[1518-10-09 00:59] wakes up
[1518-03-30 00:48] wakes up
[1518-11-13 23:49] Guard #1811 begins shift
[1518-06-28 23:59] Guard #2657 begins shift
[1518-04-22 00:11] falls asleep
[1518-05-17 00:15] falls asleep
[1518-09-28 23:56] Guard #1811 begins shift
[1518-07-15 00:59] wakes up
[1518-09-26 23:59] Guard #3109 begins shift
[1518-03-14 00:56] falls asleep
[1518-08-06 00:11] wakes up
[1518-03-23 00:28] wakes up
[1518-11-07 23:52] Guard #3559 begins shift
[1518-10-14 00:44] wakes up
[1518-04-16 00:59] wakes up
[1518-07-20 00:00] Guard #241 begins shift
[1518-09-20 00:58] wakes up
[1518-05-01 00:49] falls asleep
[1518-05-15 00:03] Guard #241 begins shift
[1518-10-24 00:29] wakes up
[1518-10-03 23:59] Guard #2657 begins shift
[1518-10-24 00:47] wakes up
[1518-03-23 00:00] falls asleep
[1518-10-11 00:41] wakes up
[1518-08-28 00:03] Guard #983 begins shift
[1518-10-04 00:49] falls asleep
[1518-09-05 00:51] wakes up
[1518-04-03 00:58] wakes up
[1518-05-24 00:17] falls asleep
[1518-06-16 00:56] wakes up
[1518-06-20 23:57] Guard #3361 begins shift
[1518-06-27 00:37] wakes up
[1518-04-11 00:53] wakes up
[1518-03-24 00:41] falls asleep
[1518-04-05 00:01] Guard #2099 begins shift
[1518-06-14 00:00] Guard #3499 begins shift
[1518-03-27 00:44] wakes up
[1518-11-07 00:01] Guard #73 begins shift
[1518-09-25 00:55] wakes up
[1518-04-24 00:34] falls asleep
[1518-06-15 00:03] falls asleep
[1518-08-25 00:22] falls asleep
[1518-04-20 00:28] falls asleep
[1518-10-30 00:05] falls asleep
[1518-10-19 00:21] falls asleep
[1518-10-03 00:39] falls asleep
[1518-07-01 00:05] falls asleep
[1518-06-30 00:52] wakes up
[1518-04-26 00:40] wakes up
[1518-10-20 00:04] Guard #3203 begins shift
[1518-03-19 00:04] falls asleep
[1518-04-07 00:40] wakes up
[1518-05-05 00:55] wakes up
[1518-05-22 00:04] Guard #313 begins shift
[1518-06-08 23:47] Guard #241 begins shift
[1518-08-17 00:28] wakes up
[1518-06-17 00:25] wakes up
[1518-03-12 00:35] falls asleep
[1518-07-30 00:04] Guard #3109 begins shift
[1518-03-14 00:57] wakes up
[1518-07-11 00:56] wakes up
[1518-04-21 23:56] Guard #1811 begins shift
[1518-08-27 00:36] wakes up
[1518-06-09 00:53] wakes up
[1518-08-08 00:04] Guard #241 begins shift
[1518-03-22 00:58] wakes up
[1518-04-19 00:58] wakes up
[1518-04-18 00:00] Guard #1091 begins shift
[1518-09-28 00:48] wakes up
[1518-08-01 00:52] wakes up
[1518-03-19 00:29] falls asleep
[1518-04-04 00:02] Guard #983 begins shift
[1518-09-22 00:19] wakes up
[1518-06-15 23:59] Guard #1499 begins shift
[1518-05-10 00:29] wakes up
[1518-06-18 00:28] falls asleep
[1518-03-20 00:59] wakes up
[1518-08-26 00:15] falls asleep
[1518-10-24 00:01] Guard #3109 begins shift
[1518-07-15 00:57] falls asleep
[1518-06-05 00:59] wakes up
[1518-11-02 00:14] falls asleep
[1518-05-26 00:11] wakes up
[1518-11-04 23:56] Guard #3499 begins shift
[1518-10-08 00:53] falls asleep
[1518-09-25 00:25] falls asleep
[1518-09-25 23:56] Guard #3361 begins shift
[1518-06-24 00:04] Guard #1033 begins shift
[1518-05-07 00:04] Guard #1091 begins shift
[1518-08-18 00:29] falls asleep
[1518-09-13 00:47] falls asleep
[1518-04-02 00:53] wakes up
[1518-11-08 00:51] wakes up
[1518-09-02 23:56] Guard #3203 begins shift
[1518-08-06 00:55] wakes up
[1518-10-01 23:58] Guard #2411 begins shift
[1518-06-29 23:59] Guard #1811 begins shift
[1518-05-07 00:48] wakes up
[1518-11-12 00:37] falls asleep
[1518-10-16 00:00] Guard #2657 begins shift
[1518-07-07 00:29] falls asleep
[1518-07-17 00:45] falls asleep
[1518-11-01 00:57] wakes up
[1518-10-26 00:02] Guard #1291 begins shift
[1518-11-06 00:04] falls asleep
[1518-09-29 00:22] falls asleep
[1518-08-20 00:03] Guard #3499 begins shift
[1518-07-03 00:47] wakes up
[1518-05-01 00:25] wakes up
[1518-08-10 00:49] wakes up
[1518-03-13 00:55] wakes up
[1518-08-13 00:59] wakes up
[1518-06-08 00:53] falls asleep
[1518-07-17 00:06] falls asleep
[1518-06-25 00:41] wakes up
[1518-10-31 00:11] wakes up
[1518-05-05 00:32] falls asleep
[1518-06-23 00:40] wakes up
[1518-05-13 00:33] wakes up
[1518-04-17 00:53] falls asleep
[1518-05-01 00:09] falls asleep
[1518-03-14 00:22] falls asleep
[1518-10-27 00:01] Guard #1291 begins shift
[1518-06-04 00:01] falls asleep
[1518-10-16 00:50] wakes up
[1518-07-08 00:45] falls asleep
[1518-04-12 00:37] falls asleep
[1518-10-18 00:38] wakes up
[1518-09-14 00:10] falls asleep
[1518-07-01 00:40] falls asleep
[1518-11-08 00:20] falls asleep
[1518-03-30 00:59] wakes up
[1518-06-12 00:00] Guard #3499 begins shift
[1518-08-27 00:00] Guard #1291 begins shift
[1518-03-20 00:37] falls asleep
[1518-09-30 00:44] wakes up
[1518-09-20 00:43] wakes up
[1518-10-27 00:08] falls asleep
[1518-09-09 00:02] Guard #1091 begins shift
[1518-08-13 00:21] falls asleep
[1518-04-21 00:49] wakes up
[1518-11-16 23:56] Guard #919 begins shift
[1518-07-22 00:47] wakes up
[1518-10-03 00:50] falls asleep
[1518-09-26 00:50] wakes up
[1518-06-08 00:02] Guard #1811 begins shift
[1518-05-22 23:59] Guard #2617 begins shift
[1518-07-31 00:34] wakes up
[1518-10-22 23:52] Guard #313 begins shift
[1518-08-03 00:49] falls asleep
[1518-10-24 00:43] falls asleep
[1518-05-08 00:01] Guard #1033 begins shift
[1518-10-19 00:48] wakes up
[1518-10-13 00:04] Guard #1091 begins shift
[1518-07-18 00:18] wakes up
[1518-10-20 00:36] wakes up
[1518-10-04 00:33] falls asleep
[1518-05-08 00:11] wakes up
[1518-05-19 00:04] falls asleep
[1518-04-06 00:55] wakes up
[1518-08-10 00:38] wakes up
[1518-06-10 00:34] falls asleep
[1518-07-15 00:38] falls asleep
[1518-08-18 00:35] wakes up
[1518-03-27 00:18] falls asleep
[1518-08-10 00:45] falls asleep
[1518-07-30 00:22] wakes up
[1518-06-22 23:59] Guard #2657 begins shift
[1518-07-11 23:57] Guard #2617 begins shift
[1518-10-15 00:47] wakes up
[1518-08-25 00:02] Guard #1291 begins shift
[1518-06-24 00:12] falls asleep
[1518-03-16 23:57] Guard #2657 begins shift
[1518-10-18 00:02] Guard #2657 begins shift
[1518-05-11 00:58] wakes up
[1518-03-30 00:37] falls asleep
[1518-08-21 00:53] wakes up
[1518-07-09 00:57] wakes up
[1518-08-07 00:00] Guard #1499 begins shift
[1518-09-02 00:56] falls asleep
[1518-10-14 23:56] Guard #2099 begins shift
[1518-09-19 00:48] wakes up
[1518-05-30 00:04] Guard #1499 begins shift
[1518-11-11 00:04] falls asleep
[1518-03-21 00:57] wakes up
[1518-05-20 23:57] Guard #1811 begins shift
[1518-10-23 00:08] wakes up
[1518-07-02 23:57] Guard #1811 begins shift
[1518-10-28 23:58] Guard #241 begins shift
[1518-05-12 00:05] falls asleep
[1518-11-18 00:26] falls asleep
[1518-03-21 00:27] wakes up
[1518-07-29 00:50] wakes up
[1518-10-24 23:56] Guard #2657 begins shift
[1518-05-14 00:37] wakes up
[1518-08-04 00:00] Guard #1033 begins shift
[1518-06-20 00:52] wakes up
[1518-05-10 00:00] Guard #73 begins shift
[1518-08-19 00:02] Guard #1033 begins shift
[1518-03-16 00:03] falls asleep
[1518-03-12 00:03] Guard #2657 begins shift
[1518-06-22 00:48] wakes up
[1518-08-22 00:31] falls asleep
[1518-05-11 00:02] Guard #1811 begins shift
[1518-03-19 23:58] Guard #241 begins shift
[1518-04-10 00:53] falls asleep
[1518-10-21 23:57] Guard #919 begins shift
[1518-06-28 00:04] Guard #2657 begins shift
[1518-11-17 00:56] falls asleep
[1518-07-09 00:45] wakes up
[1518-06-11 00:44] wakes up
[1518-04-10 00:48] wakes up
[1518-11-01 00:37] falls asleep
[1518-05-20 00:36] falls asleep
[1518-05-23 23:56] Guard #1811 begins shift
[1518-04-18 23:56] Guard #3109 begins shift
[1518-05-31 00:02] Guard #2657 begins shift
[1518-05-17 00:00] Guard #241 begins shift
[1518-05-28 00:52] falls asleep
[1518-10-30 00:07] wakes up
[1518-08-30 00:26] falls asleep
[1518-03-17 23:57] Guard #241 begins shift
[1518-07-19 00:43] wakes up
[1518-08-09 00:03] Guard #3109 begins shift
[1518-09-11 00:41] wakes up
[1518-07-27 23:50] Guard #2099 begins shift
[1518-10-17 00:26] falls asleep
[1518-05-30 00:14] falls asleep
[1518-10-12 00:26] falls asleep
[1518-06-16 00:44] falls asleep
[1518-05-20 00:02] Guard #1033 begins shift
[1518-06-16 00:24] falls asleep
[1518-06-19 23:57] Guard #2411 begins shift
[1518-10-27 00:53] wakes up
[1518-06-10 00:53] falls asleep
[1518-05-05 00:43] falls asleep
[1518-09-04 00:03] Guard #2099 begins shift
[1518-05-23 00:14] wakes up
[1518-09-08 00:04] Guard #1291 begins shift
[1518-05-03 00:52] wakes up
[1518-07-25 00:03] Guard #1033 begins shift
[1518-07-08 00:59] wakes up
[1518-10-25 00:54] wakes up
[1518-11-08 00:00] falls asleep
[1518-06-20 00:47] falls asleep
[1518-05-08 00:49] wakes up
[1518-11-15 23:59] Guard #3109 begins shift
[1518-06-18 00:55] wakes up
[1518-03-11 00:04] Guard #1499 begins shift
[1518-08-29 00:44] falls asleep
[1518-05-16 00:28] falls asleep
[1518-11-03 23:56] Guard #1291 begins shift
[1518-04-26 00:18] falls asleep
[1518-07-21 00:00] Guard #919 begins shift
[1518-08-21 00:04] falls asleep
[1518-10-14 00:05] falls asleep
[1518-06-19 00:57] wakes up
[1518-08-27 00:54] wakes up
[1518-09-13 23:56] Guard #1499 begins shift
[1518-08-20 23:48] Guard #3559 begins shift
[1518-09-30 23:50] Guard #313 begins shift
[1518-08-20 00:37] falls asleep
[1518-07-18 00:03] falls asleep
[1518-04-23 00:17] wakes up
[1518-05-14 00:17] falls asleep
[1518-06-20 00:27] falls asleep
[1518-06-01 23:59] Guard #241 begins shift
[1518-06-05 00:52] wakes up
[1518-06-26 00:37] wakes up
[1518-05-28 00:14] wakes up
[1518-11-12 23:49] Guard #3449 begins shift
[1518-11-10 00:53] wakes up
[1518-06-05 00:00] Guard #983 begins shift
[1518-10-26 00:45] wakes up
[1518-11-03 00:55] wakes up
[1518-09-10 00:31] falls asleep
[1518-05-31 00:56] wakes up
[1518-11-14 00:31] wakes up
[1518-06-20 00:43] wakes up
[1518-06-09 00:45] falls asleep
[1518-10-18 00:48] wakes up
[1518-07-30 00:43] falls asleep
[1518-08-12 00:04] Guard #2657 begins shift
[1518-09-15 00:59] wakes up
[1518-05-07 00:16] falls asleep
[1518-09-14 00:56] wakes up
[1518-08-25 00:45] wakes up
[1518-04-07 00:55] falls asleep
[1518-07-13 00:32] wakes up
[1518-03-24 00:28] wakes up
[1518-11-22 00:40] wakes up
[1518-09-12 00:59] wakes up
[1518-03-12 00:47] wakes up
[1518-09-17 23:59] Guard #1291 begins shift
[1518-05-26 00:40] falls asleep
[1518-04-07 00:57] wakes up
[1518-03-17 00:48] falls asleep
[1518-09-10 00:56] wakes up
[1518-06-16 00:29] wakes up
[1518-09-04 00:41] wakes up
[1518-05-02 23:53] Guard #241 begins shift
[1518-08-17 00:43] falls asleep
[1518-09-17 00:59] wakes up
[1518-09-07 00:01] Guard #3499 begins shift
[1518-10-11 00:29] falls asleep
[1518-05-18 23:53] Guard #3109 begins shift
[1518-07-02 00:00] falls asleep
[1518-04-03 00:06] falls asleep
[1518-05-04 23:58] Guard #2657 begins shift
[1518-06-03 00:48] wakes up
[1518-06-10 00:48] wakes up
[1518-09-09 00:06] falls asleep
[1518-06-04 00:32] wakes up
[1518-08-19 00:32] falls asleep
[1518-06-17 00:31] falls asleep
[1518-11-17 23:59] Guard #1811 begins shift
[1518-04-27 00:43] falls asleep
[1518-05-26 00:06] falls asleep
[1518-07-03 00:07] falls asleep
[1518-05-16 00:00] Guard #983 begins shift
[1518-07-26 23:57] Guard #1867 begins shift
[1518-10-22 00:36] wakes up
[1518-09-10 00:39] falls asleep
[1518-05-20 00:59] wakes up
[1518-09-26 00:20] falls asleep
[1518-05-07 00:38] falls asleep
[1518-10-05 00:53] wakes up
[1518-07-05 00:39] falls asleep
[1518-11-20 00:09] falls asleep
[1518-03-19 00:34] wakes up
[1518-11-14 23:47] Guard #1291 begins shift
[1518-06-19 00:14] falls asleep
[1518-09-15 23:58] Guard #2617 begins shift
[1518-08-28 00:46] wakes up
[1518-07-28 00:04] falls asleep
[1518-11-19 00:57] wakes up
[1518-04-15 00:17] falls asleep
[1518-05-08 00:52] falls asleep
[1518-10-03 00:32] wakes up
[1518-07-05 00:51] wakes up
[1518-06-09 00:16] wakes up
[1518-04-28 00:43] wakes up
[1518-07-09 00:38] falls asleep"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
