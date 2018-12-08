import re
import sys
import unittest
from dataclasses import dataclass, field
from functools import partial
from textwrap import dedent
from typing import DefaultDict, Callable

from hamcrest import assert_that, is_


def compute(data):
    return "".join(step.complete() for step in run_steps(parse_dependencies(data)))


def compute2(data, workers_count=5, base_task_time=60):
    Step.base_length = base_task_time

    workers = [Worker(i) for i in range(0, workers_count)]
    dependencies = parse_dependencies(data)
    steps_allocator = run_steps(dependencies)

    second = 0
    has_more_tasks = True
    while True:
        for worker in workers:
            if worker.task is None and has_more_tasks:
                try:
                    worker.task = next(steps_allocator)
                except StopIteration:
                    has_more_tasks = False

        print(second, " ".join(w.task.name if w.task is not None else "." for w in workers))

        for worker in workers:
            if worker.task is not None:
                worker.tick()

        if not has_more_tasks and all(worker.task is None for worker in workers):
            return second

        second += 1


def run_steps(dependencies):
    steps = list(sorted(dependencies.keys()))

    upcoming = set()

    def add_ready_steps():
        for step in steps:
            unresolved_dependencies = list(filter(lambda d: d in steps, dependencies[step]))
            if len(unresolved_dependencies) == 0 and step.complete_callback is None:
                upcoming.add(step)

    def step_done(step):
        steps.remove(step)
        add_ready_steps()

    add_ready_steps()

    while len(steps) > 0:
        if len(upcoming) > 0:
            processing_step = min(upcoming)
            upcoming.remove(processing_step)

            processing_step.complete_callback = partial(step_done, processing_step)

            yield processing_step
        else:
            yield None

        if len(steps) == 0:
            return


def parse_dependencies(data):
    dependencies = DefaultDict(lambda: set())

    for line in data.split("\n"):
        dependency, step = map(lambda e: Step(e),
                               re.match(r"Step (\w) must be finished before step (\w) can begin.", line).groups())

        dependencies[dependency]  # Ensure all present even if it has no dependencies
        dependencies[step].add(dependency)

    return dependencies


@dataclass(unsafe_hash=True)
class Step:
    name: str
    complete_callback: Callable = field(init=False, hash=False, compare=False, default=None)

    base_length = 60

    def __lt__(self, other):
        return self.name < other.name

    def complete(self):
        self.complete_callback()
        return self.name

    def __len__(self):
        return Step.base_length + ord(self.name) - ord("A") + 1


@dataclass
class Worker:
    id: int
    task: Step = None
    spent: int = 0

    def tick(self):
        self.spent += 1
        if self.spent == len(self.task):
            self.task.complete_callback()
            self.task = None
            self.spent = 0


class ParseTest(unittest.TestCase):
    def test_parse(self):
        data = dedent("""\
            Step C must be finished before step A can begin.
            Step C must be finished before step F can begin.
            Step A must be finished before step B can begin.
            Step A must be finished before step D can begin.
            Step B must be finished before step E can begin.
            Step D must be finished before step E can begin.
            Step F must be finished before step E can begin.""")

        assert_that(parse_dependencies(data), is_({
            Step("A"): {Step("C")},
            Step("B"): {Step("A")},
            Step("C"): set(),
            Step("D"): {Step("A")},
            Step("E"): {Step("B"), Step("D"), Step("F")},
            Step("F"): {Step("C")},
        }))


class StepTest(unittest.TestCase):
    def test_len(self):
        Step.base_length = 60
        assert_that(len(Step("A")), is_(61))
        assert_that(len(Step("Z")), is_(86))

    def test_compare(self):
        assert_that(Step("A"), is_(Step("A")))

        step = Step("A")
        step.complete_callback = lambda: 0
        assert_that(step, is_(Step("A")))


class ProvidedTest(unittest.TestCase):
    input = dedent("""\
        Step C must be finished before step A can begin.
        Step C must be finished before step F can begin.
        Step A must be finished before step B can begin.
        Step A must be finished before step D can begin.
        Step B must be finished before step E can begin.
        Step D must be finished before step E can begin.
        Step F must be finished before step E can begin.""")

    def test_part_1(self):
        assert_that(compute(self.input), is_("CABDFE"))

    def test_part_2(self):
        assert_that(compute2(self.input, workers_count=2, base_task_time=0), is_(15))


puzzle_input = """\
Step R must be finished before step Y can begin.
Step N must be finished before step T can begin.
Step C must be finished before step L can begin.
Step F must be finished before step B can begin.
Step L must be finished before step D can begin.
Step T must be finished before step D can begin.
Step O must be finished before step E can begin.
Step M must be finished before step Z can begin.
Step A must be finished before step V can begin.
Step K must be finished before step D can begin.
Step W must be finished before step I can begin.
Step B must be finished before step J can begin.
Step H must be finished before step D can begin.
Step P must be finished before step J can begin.
Step J must be finished before step Z can begin.
Step S must be finished before step X can begin.
Step Z must be finished before step U can begin.
Step Y must be finished before step E can begin.
Step V must be finished before step I can begin.
Step U must be finished before step Q can begin.
Step Q must be finished before step D can begin.
Step X must be finished before step I can begin.
Step G must be finished before step E can begin.
Step I must be finished before step D can begin.
Step D must be finished before step E can begin.
Step B must be finished before step S can begin.
Step U must be finished before step E can begin.
Step J must be finished before step G can begin.
Step I must be finished before step E can begin.
Step N must be finished before step G can begin.
Step P must be finished before step Z can begin.
Step X must be finished before step D can begin.
Step H must be finished before step V can begin.
Step Q must be finished before step E can begin.
Step Z must be finished before step D can begin.
Step V must be finished before step D can begin.
Step S must be finished before step Q can begin.
Step F must be finished before step O can begin.
Step F must be finished before step M can begin.
Step W must be finished before step B can begin.
Step J must be finished before step X can begin.
Step G must be finished before step D can begin.
Step R must be finished before step K can begin.
Step L must be finished before step Y can begin.
Step J must be finished before step Q can begin.
Step Z must be finished before step E can begin.
Step Y must be finished before step Q can begin.
Step K must be finished before step P can begin.
Step N must be finished before step B can begin.
Step Q must be finished before step I can begin.
Step P must be finished before step U can begin.
Step F must be finished before step J can begin.
Step L must be finished before step G can begin.
Step Q must be finished before step X can begin.
Step H must be finished before step G can begin.
Step C must be finished before step O can begin.
Step V must be finished before step G can begin.
Step M must be finished before step G can begin.
Step A must be finished before step Z can begin.
Step C must be finished before step A can begin.
Step N must be finished before step P can begin.
Step N must be finished before step L can begin.
Step W must be finished before step E can begin.
Step N must be finished before step U can begin.
Step A must be finished before step U can begin.
Step O must be finished before step G can begin.
Step Y must be finished before step X can begin.
Step P must be finished before step S can begin.
Step Z must be finished before step Q can begin.
Step K must be finished before step S can begin.
Step N must be finished before step Z can begin.
Step Z must be finished before step V can begin.
Step P must be finished before step Y can begin.
Step L must be finished before step I can begin.
Step O must be finished before step P can begin.
Step N must be finished before step A can begin.
Step F must be finished before step A can begin.
Step P must be finished before step E can begin.
Step Z must be finished before step X can begin.
Step O must be finished before step A can begin.
Step F must be finished before step K can begin.
Step T must be finished before step U can begin.
Step Z must be finished before step I can begin.
Step N must be finished before step O can begin.
Step K must be finished before step U can begin.
Step M must be finished before step W can begin.
Step O must be finished before step U can begin.
Step S must be finished before step I can begin.
Step N must be finished before step K can begin.
Step O must be finished before step J can begin.
Step C must be finished before step J can begin.
Step W must be finished before step S can begin.
Step W must be finished before step J can begin.
Step H must be finished before step J can begin.
Step G must be finished before step I can begin.
Step V must be finished before step U can begin.
Step O must be finished before step H can begin.
Step F must be finished before step Y can begin.
Step U must be finished before step D can begin.
Step N must be finished before step E can begin.
Step H must be finished before step P can begin."""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
