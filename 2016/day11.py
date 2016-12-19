import logging
import re
import sys
import unittest
from copy import deepcopy
from itertools import combinations
from textwrap import dedent

from hamcrest import assert_that, is_, has_length, is_not, greater_than, less_than
from sortedcontainers import SortedList
from sortedcontainers import SortedSet

UP = 1
DOWN = -1
MAX_MOVE_RATE_LIMITING = 900
NEW_SEQUENCES_TO_CONSIDER = 0.5

class Directive(object):
    def __init__(self, direction, microchips, generators):
        self.direction = direction
        self.microchips = microchips
        self.generators = generators


DIRECTIVES = [
    Directive(direction=UP, microchips=1, generators=1),
    Directive(direction=UP, microchips=2, generators=0),
    Directive(direction=UP, microchips=0, generators=2),
    Directive(direction=UP, microchips=1, generators=0),
    Directive(direction=UP, microchips=0, generators=1),
    Directive(direction=DOWN, microchips=1, generators=1),
    Directive(direction=DOWN, microchips=2, generators=0),
    Directive(direction=DOWN, microchips=0, generators=2),
    Directive(direction=DOWN, microchips=1, generators=0),
    Directive(direction=DOWN, microchips=0, generators=1),
]


def djikstra(data):
    system = System()
    system.set_up(data)

    # sequences = SortedSet([Sequence(system)], key=lambda s: (len(s.moves), s.system))

    floor_cleared = 0

    new_steps = [Sequence([], system)]
    known_states = []
    while new_steps:
        # sequences = list(sorted(filter(lambda e: not e.dead_end, new_steps), key=lambda s: s.system, reverse=True))
        # sequences = sequences[:math.ceil(len(sequences) * NEW_SEQUENCES_TO_CONSIDER)]
        # sequences = list(filter(lambda e: all(len(e.system.floors[i].microchips) == len(e.system.floors[i].generators) == 0 for i in range(0, floor_cleared)), new_steps))
        sequences = new_steps[:]
        # known_states = {}
        new_steps = []
        while sequences:
            sequence = sequences.pop(0)
            floor = sequence.system.current_floor()
            for directive in DIRECTIVES:
                if sequence.system.can_move(directive.direction):
                    for variation in variations(floor, directive, sequence.system.elements_worth_moving()):
                        new_seq = sequence.give_birth()

                        if new_seq.add_move(variation):
                            state_id = new_seq.system.state_id()
                            # if state_id not in known_states or known_states[state_id] < len(new_seq.moves):
                            if new_seq.system.is_winning():
                                print("WINNING")
                                print("WINNING at {} moves : \n{}".format(len(new_seq.moves), "\n".join(repr(m) for m in new_seq.moves)))
                                new_seq.system.show()
                                return len(new_seq.moves)
                            elif new_seq.system.is_valid() and state_id not in known_states:
                                known_states.append(state_id)
                                print("moves={}, ks={}, seq={}".format(len(new_seq.moves), len(known_states), new_seq))
                                new_seq.system.show()
                                new_steps.append(new_seq)
                            else:
                                sequence.kill_offspring(new_seq)
                        else:
                            sequence.kill_offspring(new_seq)

            sequence.mark_as_dead_end_if_necessary()
            # # sequences = SortedSet(filter(lambda e: not e.dead_end, sequences), key=lambda s: (len(s.moves), s.system))
            # sequences = list()
        #
        # for seq in new_steps:
        #     all_cleared = all(len(seq.system.floors[i].microchips) == len(seq.system.floors[i].generators) == 0 for i in range(0, floor_cleared + 1))
        #
        #     if all_cleared:
        #         floor_cleared += 1
        #         known_states = {}

    return "COULDN'T COMPUTE"


def astar(data):
    system = System()
    system.set_up(data)

    sequences = []

    sequences = SortedSet()
    sequences.add(Sequence([], system, full_sequence=sequences))
    known_states = {}

    best_sequences = []
    while sequences:
        sequence = sequences.pop()
        floor = sequence.system.current_floor()
        for directive in DIRECTIVES:
            if sequence.system.can_move(directive.direction):
                for variation in variations(floor, directive, sequence.system.elements_worth_moving()):
                    new_seq = sequence.give_birth()

                    if new_seq.add_move(variation):
                        if new_seq.system.is_winning():
                            new_seq.system.show()
                            best_sequences.append(new_seq)

                            if len(best_sequences) >= 1:
                                for s in best_sequences:
                                    print("WINNING at {} moves : \n{}".format(len(s.moves), "\n".join(repr(m) for m in s.moves)))

                                return min([len(s.moves) for s in best_sequences])
                        elif new_seq.system.is_valid():
                            state_id = new_seq.system.state_id()
                            if state_id not in known_states or len(new_seq.moves) < known_states[state_id]:
                                known_states[state_id] = len(new_seq.moves)
                                print("moves={}, seqs={}, ks={}, rating={}, seq={}".format(len(new_seq.moves), len(sequences), len(known_states), sequence.rating(), new_seq))
                                # new_seq.system.show()
                                sequences.add(new_seq)
                            else:
                                sequence.kill_offspring(new_seq)
                        else:
                            sequence.kill_offspring(new_seq)
                    else:
                        sequence.kill_offspring(new_seq)

        seq_list = list(sequences[::-1])
        sequence.mark_as_dead_end_if_necessary()

    return min([len(s.moves) for s in best_sequences])

class Error(Exception):
    pass

def play(data):
    sequence = Sequence([], System(), full_sequence=[])
    sequence.system.set_up(data)

    while True:
        try:
            available_microchips = [e for e in sequence.system.distinct_elements if e in sequence.system.floors[sequence.system.elevator].microchips]
            available_generators = [e for e in sequence.system.distinct_elements if e in sequence.system.floors[sequence.system.elevator].generators]
            print("Controls:")
            print(" - Microchips : {}".format(", ".join("({}) {}".format(i + 1, sequence.system.distinct_elements[i])
                                                        for i in range(0, len(sequence.system.distinct_elements)) if sequence.system.distinct_elements[i] in available_microchips)))
            print(" - Generators : {}".format(", ".join("({}) {}".format(chr(ord('A') + i), sequence.system.distinct_elements[i])
                                                        for i in range(0, len(sequence.system.distinct_elements)) if sequence.system.distinct_elements[i] in available_generators)))

            print()
            sequence.system.show()
            print()

            command = input("Move #{} :: (u/d # [#]) / UNDO: ".format(len(sequence.moves)))

            if command == "UNDO":
                sequence = sequence.parent
            else:
                match = re.match("(u|d) (.)\s?(.)?", command)
                if match:
                    matched = match.groups()
                    move = dict(
                        direction={"u": UP, "d": DOWN}[matched[0]],
                        microchips=[],
                        generators=[],
                    )
                    for i in range(1, len(matched)):
                        if matched[i] is not None:
                            try:
                                microchip = sequence.system.distinct_elements[int(matched[i]) - 1]
                                if microchip not in available_microchips:
                                    raise Error("microchip not on this floor : {}".format(microchip))
                                else:
                                    move["microchips"].append(microchip)
                            except ValueError:
                                try:
                                    generator = sequence.system.distinct_elements[ord(matched[i]) - ord("A")]
                                    if generator not in available_generators:
                                        raise Error("generator not on this floor : {}".format(generator))
                                    else:
                                        move["generators"].append(generator)
                                except IndexError:
                                    raise Error("Unknown generator : {}".format(matched[i]))

                    sequence = sequence.give_birth()
                    sequence.add_move(move)
                    if sequence.system.is_winning():
                        print("Bravo!")
                        return

                else:
                    raise Error("Wat?")
        except Error as e:
            print()
            print(e)
            print()

class Sequence(object):
    def __init__(self, id, system, moves=None, known_states=None, full_sequence=None):
        self.id = id
        self.system = system
        self.moves = moves or []
        self.known_states = known_states or []
        self.parent = None
        self.children = []
        self.dead_end = False
        self.full_sequence = full_sequence

    def add_move(self, move):
        self.system.move(**move)
        state_id = self.system.state_id()
        if state_id in self.known_states:
            return False
        self.moves.append(move)
        self.known_states.append(state_id)
        return True

    def mark_as_dead_end_if_necessary(self):
        if all(c.dead_end for c in self.children):
            self.dead_end = True
            if self.parent:
                self.parent.mark_as_dead_end_if_necessary()

    def give_birth(self):
        offspring = Sequence(self.id + [len(self.children)], self.system.copy(), deepcopy(self.moves), deepcopy(self.known_states), full_sequence=self.full_sequence)
        offspring.parent = self
        self.children.append(offspring)

        return offspring

    def kill_offspring(self, offspring):
        self.children.remove(offspring)

    def rating(self):
        return (len(self.system.floors[-1].generators) + len(self.system.floors[-1].microchips)) * 2 - len(self.moves)

    # def rating(self):
    #     total = 100
    #     for i in range(0, len(self.system.floors)):
    #         floor = self.system.floors[i]
    #         score = len(floor.microchips) + len(floor.generators)
    #         if self.system.elevator <= i:
    #             score += len(set(floor.microchips).intersection(floor.generators)) * 2
    #         floor_total = (2 ** (i + 1)) * score * 2
    #         logging.info("Floor={} elevator={} score={}, total={}".format(i, self.system.elevator, score, floor_total))
    #         total += floor_total
    #
    #     less_moves_modifier = (len(self.full_sequence[-1].moves) if len(self.full_sequence) > 1 else 0) - len(self.moves)
    #     return total - 2 ** self.system.elevator + less_moves_modifier * 5

    def __lt__(self, other):
        return self.rating() < other.rating()

    def __str__(self):
        return "{} : {}".format("-".join(str(e) for e in self.id), self.rating())

class System(object):
    def __init__(self, distinct_elements=None, elevator=0, floors=None):
        self.distinct_elements = SortedList(distinct_elements or [])
        self.elevator = elevator
        self.floors = floors or []

    def current_floor(self):
        return self.floors[self.elevator]

    def can_move(self, direction):
        target = self.elevator + direction
        all_cleared = all(len(self.floors[i].microchips) == len(self.floors[i].generators) == 0 for i in range(0, target + 1))
        return 0 <= self.elevator + direction < len(self.floors) and not all_cleared

    def set_up(self, input):
        def next_item(string, offset):
            string = string[offset:]
            return string, re.match(".*?a (\w+)(-compatible microchip| generator)", string)

        lines = input.strip().split("\n")
        for i in range(0, len(lines)):
            floor = Floor(i)
            remain, match = next_item(lines[i], 0)
            while match:
                if match.group(2) == "-compatible microchip":
                    floor.microchips.add(match.group(1))
                    self.distinct_elements.add(match.group(1))
                else:
                    floor.generators.add(match.group(1))

                remain, match = next_item(remain, len(match.group(0)))

            self.floors.append(floor)

    def is_valid(self):
        for floor in self.floors:
            if len(floor.generators) > 0:
                for microchip in floor.microchips:
                    if microchip not in floor.generators:
                        return False

        return True

    def is_winning(self):
        last_floor = self.floors[-1]
        return len(self.distinct_elements) == len(last_floor.microchips) == len(last_floor.generators)

    def move(self, direction, microchips=None, generators=None):
        from_floor = self.floors[self.elevator]
        self.elevator += direction
        to_floor = self.floors[self.elevator]
        for microchip in microchips or []:
            from_floor.microchips.remove(microchip)
            to_floor.microchips.add(microchip)
        for generator in generators or []:
            from_floor.generators.remove(generator)
            to_floor.generators.add(generator)

    def state_id(self):
        return str(self)

    def __str__(self):
        return "{}-{}".format(self.elevator, "-".join(str(f) for f in self.floors))

    def show(self):
        for i in range(len(self.floors) -1, -1, -1):
            cols = []
            for e in self.distinct_elements:
                cols.append("M:{}".format(e[:2]) if e in self.floors[i].microchips else " -- ")
                cols.append("G:{}".format(e[:2]) if e in self.floors[i].generators else " -- ")

            print("F{} {} {}".format(
                i + 1,
                "E" if self.elevator == i else " ",
                " ".join(cols)
            ))

    def copy(self):
        return deepcopy(self)

    def __lt__(self, other):
        for i in range(len(self.floors) - 1, -1, -1):
            if self.floors[i].count_elements() < other.floors[i].count_elements():
                return True
            elif self.floors[i].count_elements() > other.floors[i].count_elements():
                return False
        return False

    def __hash__(self, *args, **kwargs):
        return hash(self.state_id())

    def __eq__(self, other):
        return self.state_id() == other.state_id()

    def elements_worth_moving(self):
        states = {}
        microchip_level = None
        generator_level = None
        for element in self.distinct_elements:
            for floor in self.floors:
                if element in floor.microchips:
                    microchip_level = floor.number
                if element in floor.generators:
                    generator_level = floor.number

            state = (microchip_level, generator_level)
            if list(states.values()).count(state) < 2:
                states[element] = state

        return sorted(states.keys())


def variations(floor, directive, elements):
    result = []
    microchips = list(filter(lambda e: e in elements, floor.microchips))
    generators = list(filter(lambda e: e in elements, floor.generators))
    if len(microchips) < directive.microchips or len(generators) < directive.generators:
        return result

    m_permutations = list(filter(lambda e: e, list(combinations(microchips, directive.microchips))))
    g_permutations = list(filter(lambda e: e, list(combinations(generators, directive.generators))))

    if m_permutations:
        for m_permutation in m_permutations:
            microchips = [e for e in m_permutation if e is not None]
            if g_permutations:
                for g_permutation in g_permutations:
                    generators = [e for e in g_permutation if e is not None]
                    result.append(dict(direction=directive.direction, microchips=microchips, generators=generators))
            else:
                result.append(dict(direction=directive.direction, microchips=microchips, generators=[]))
    elif g_permutations:
        for g_permutation in g_permutations:
            generators = [e for e in g_permutation if e is not None]
            result.append(dict(direction=directive.direction, microchips=[], generators=generators))


    return result


class Floor(object):
    def __init__(self, number, microchips=None, generators=None):
        self.number = number
        self.microchips = SortedList(microchips or [])
        self.generators = SortedList(generators or [])

    def __str__(self):
        return "{}:{}:{}".format(
            self.number,
            ",".join("M{}".format(e[:2]) for e in self.microchips),
            ",".join("G{}".format(e[:2]) for e in self.generators),
        )

    def count_elements(self):
        return len(self.microchips) + len(self.generators) + len(set(self.microchips).intersection(self.generators))

class ReadDataTest(unittest.TestCase):
    def test_reads_data(self):
        system = System()
        system.set_up(dedent("""
            The first floor contains a lithium-compatible microchip and a hydrogen-compatible microchip.
            The second floor contains a hydrogen generator.
            The third floor contains a lithium generator.
            The fourth floor contains nothing relevant."""))

        assert_that(system.distinct_elements, has_length(2))
        assert_that(system.elevator, is_(0))

        assert_that(system.floors, has_length(4))
        assert_that(system.floors[0].number, is_(0))
        assert_that(system.floors[0].microchips, has_length(2))
        assert_that(system.floors[0].microchips[0], is_("hydrogen"))
        assert_that(system.floors[0].microchips[1], is_("lithium"))
        assert_that(system.floors[0].generators, has_length(0))

        assert_that(system.floors[1].number, is_(1))
        assert_that(system.floors[1].microchips, has_length(0))
        assert_that(system.floors[1].generators, has_length(1))
        assert_that(system.floors[1].generators[0], is_("hydrogen"))

        assert_that(system.floors[2].number, is_(2))
        assert_that(system.floors[2].microchips, has_length(0))
        assert_that(system.floors[2].generators, has_length(1))
        assert_that(system.floors[2].generators[0], is_("lithium"))

        assert_that(system.floors[3].number, is_(3))
        assert_that(system.floors[3].microchips, has_length(0))
        assert_that(system.floors[3].generators, has_length(0))


class ValidateSystem(unittest.TestCase):
    def test_empty_configuration_is_valid(self):
        assert_that(System(floors=[
            Floor(0, microchips=[], generators=[])
        ]).is_valid(), is_(True))

    def test_one_chip_is_valid(self):
        assert_that(System(floors=[
            Floor(0, microchips=["a"], generators=[])
        ]).is_valid(), is_(True))

    def test_one_generator_is_valid(self):
        assert_that(System(floors=[
            Floor(0, microchips=[], generators=["a"])
        ]).is_valid(), is_(True))

    def test_one_chip_with_its_generator_is_valid(self):
        assert_that(System(floors=[
            Floor(0, microchips=["a"], generators=["a"])
        ]).is_valid(), is_(True))

    def test_one_chip_with_its_generator_and_another_generator_is_valid(self):
        assert_that(System(floors=[
            Floor(0, microchips=["a"], generators=["a", "b"])
        ]).is_valid(), is_(True))

    def test_one_chip_without_its_generator_and_another_generator_is_invalid(self):
        assert_that(System(floors=[
            Floor(0, microchips=["a", "b"], generators=["a"])
        ]).is_valid(), is_(False))

    def test_is_done_for_all_floors(self):
        assert_that(System(floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=[]),
            Floor(2, microchips=[], generators=[]),
            Floor(3, microchips=["a"], generators=["b"])
        ]).is_valid(), is_(False))


class CheckForWin(unittest.TestCase):
    def test_winning_if_last_floor_has_all_items(self):
        assert_that(System(distinct_elements=["a", "b"], floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "b"], generators=["a", "b"])
        ]).is_winning(), is_(True))

    def test_fails_if_last_floor_hasnt_all_items(self):
        assert_that(System(distinct_elements=["a", "b"], floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"])
        ]).is_winning(), is_(False))


class MoveTest(unittest.TestCase):
    def test_move_one_chip(self):
        system = System(elevator=0, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=[], generators=[])
        ])

        system.move(UP, microchips=["a"])

        assert_that(system.elevator, is_(1))
        assert_that(system.floors[0].microchips, is_([]))
        assert_that(system.floors[1].microchips, is_(["a"]))

    def test_move_two_chip(self):
        system = System(elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "b"], generators=["a", "b"])
        ])

        system.move(DOWN, microchips=["a", "b"])

        assert_that(system.elevator, is_(0))
        assert_that(system.floors[0].microchips, is_(["a", "b"]))
        assert_that(system.floors[1].microchips, is_([]))

    def test_move_two_generators(self):
        system = System(elevator=0, floors=[
            Floor(0, microchips=["a", "b"], generators=["a", "b"]),
            Floor(1, microchips=[], generators=[])
        ])

        system.move(UP, generators=["a", "b"])

        assert_that(system.elevator, is_(1))
        assert_that(system.floors[0].generators, is_([]))
        assert_that(system.floors[1].generators, is_(["a", "b"]))

    def test_move_one_of_each(self):
        system = System(elevator=0, floors=[
            Floor(0, microchips=["a", "b"], generators=["a", "b"]),
            Floor(1, microchips=[], generators=[])
        ])

        system.move(UP, microchips=["a"], generators=["a"])

        assert_that(system.floors[0].microchips, is_(["b"]))
        assert_that(system.floors[1].microchips, is_(["a"]))

        assert_that(system.floors[0].generators, is_(["b"]))
        assert_that(system.floors[1].generators, is_(["a"]))

    def test_moving_keeps_element_in_a_sorted_manner(self):
        system = System(elevator=0, floors=[
            Floor(0, microchips=["a", "b"], generators=["a", "b"]),
            Floor(1, microchips=["c"], generators=["c"])
        ])

        system.move(UP, microchips=["a"], generators=["a"])

        assert_that(system.floors[1].microchips, is_(["a", "c"]))
        assert_that(system.floors[1].generators, is_(["a", "c"]))


class SystemState(unittest.TestCase):
    def test_can_give_a_small_state_identifier(self):
        system1 = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a", "b"]),
            Floor(1, microchips=["b"], generators=[])
        ])
        system2 = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a", "b"]),
            Floor(1, microchips=["b"], generators=[])
        ])

        assert_that(system1.state_id(), is_(system2.state_id()))


class SystemCanMove(unittest.TestCase):
    def test_says_if_can_move(self):
        system = System(elevator=0, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"])
        ])

        assert_that(system.can_move(DOWN), is_(False))
        assert_that(system.can_move(UP), is_(True))

    def test_says_if_can_move2(self):
        system = System(elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"])
        ])

        assert_that(system.can_move(DOWN), is_(True))
        assert_that(system.can_move(UP), is_(False))

    def test_says_you_cant_move_down_if_all_floors_under_are_empty(self):
        system = System(elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["b"], generators=["b"])
        ])

        assert_that(system.can_move(DOWN), is_(False))

        system = System(elevator=2, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=[]),
            Floor(2, microchips=["b"], generators=["b"])
        ])

        assert_that(system.can_move(DOWN), is_(False))

class SystemCanCopy(unittest.TestCase):
    def test_a_copy_is_100_percent_independent(self):
        system = System(distinct_elements=["a"], elevator=0, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
        ])

        copy = system.copy()

        copy.distinct_elements.append("b")
        copy.elevator = 1
        copy.floors.append(Floor(1, microchips=["b"], generators=["b"]))
        copy.floors[0].number = 24
        copy.floors[0].microchips.add("c")
        copy.floors[0].generators.add("c")

        assert_that(system.distinct_elements, is_(["a"]))
        assert_that(system.elevator, is_(0))
        assert_that(system.floors, has_length(1))
        assert_that(system.floors[0].number, is_(0))
        assert_that(system.floors[0].microchips, is_(["a"]))
        assert_that(system.floors[0].generators, is_(["a"]))


class SystemCanBeComparedTest(unittest.TestCase):
    def test_sorting_a_list_of_systems(self):
        winning = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "b"], generators=["a", "b"]),
        ])
        almost = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=[]),
            Floor(1, microchips=["b"], generators=["a", "b"]),
        ])
        getting_there = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"]),
        ])
        not_quite = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a", "b"]),
            Floor(1, microchips=["b"], generators=[]),
        ])
        nope = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a", "b"], generators=["a", "b"]),
            Floor(1, microchips=[], generators=[]),
        ])

        output = sorted([winning, getting_there, nope, almost, not_quite])

        assert_that(output, is_([nope, not_quite, getting_there, almost, winning]))

    def test_a_floor_with_a_microchip_and_a_generator_of_same_element_is_better(self):

        winning = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["b"], generators=["b"]),
            Floor(1, microchips=["a"], generators=["a"]),
        ])
        losing = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["b"]),
            Floor(1, microchips=["b"], generators=["a"]),
        ])

        assert_that(losing < winning)

    def test_2_equivalent_system_in_the_same_set_should_not_coexists(self):
        system1 = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"]),
        ])
        system2 = System(distinct_elements=["a", "b"], elevator=1, floors=[
            Floor(0, microchips=["a"], generators=["a"]),
            Floor(1, microchips=["b"], generators=["b"]),
        ])
        myset = SortedSet([system1])
        myset.add(system2)
        assert_that(myset, has_length(1))


class SequenceWinningRating(unittest.TestCase):
    def test_higher_floor_is_better(self):
        sequence_a = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["c"], generators=["c"]),
            Floor(2, microchips=["a", "b"], generators=["a", "b"]),
        ]), moves=[])

        sequence_b = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=["c"], generators=["c"]),
            Floor(1, microchips=[], generators=[]),
            Floor(2, microchips=["a", "b"], generators=["a", "b"]),
        ]), moves=[])

        assert_that(sequence_a.rating(), greater_than(sequence_b.rating()))

    def test_less_moves_is_better(self):
        sequence_a = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["c"], generators=["b", "c"]),
            Floor(2, microchips=["a", "b"], generators=["a"]),
        ]), moves=["one", "one"])

        sequence_b = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "c"], generators=["c"]),
            Floor(2, microchips=["b"], generators=["a", "b"]),
        ]), moves=["one"])

        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_pairs_up_are_better(self):
        sequence_a = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "c"], generators=["b", "c"]),
            Floor(2, microchips=["b"], generators=["a"]),
        ]), moves=["one", "one"])

        sequence_b = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["b", "c"], generators=["b", "c"]),
            Floor(2, microchips=["a"], generators=["a"]),
        ]), moves=["one", "one"])

        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_pairs_on_a_floor_is_better(self):
        sequence_a = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["b", "c"], generators=[]),
            Floor(2, microchips=["a"], generators=["a", "b", "c"]),
        ]), moves=["one", "one"])

        sequence_b = Sequence([0], System(distinct_elements=["a", "b", "c"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["c"], generators=["c"]),
            Floor(2, microchips=["a", "b"], generators=["a", "b"]),
        ]), moves=["one", "one"])

        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_pairs_on_a_floor_is_better2(self):
        sequence_a = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["co", "cu"], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["pl", "pr", "ru"], generators=[]),
            Floor(3, microchips=[], generators=[]),
        ]), moves=["1", "2", "3"])

        sequence_b = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=2, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["pl", "pr", "ru"], generators=[]),
            Floor(3, microchips=["co", "cu"], generators=[]),
        ]), moves=["1", "2", "3"])

        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_lower_elevator_is_better_than_less_moves(self):
        sequence_a = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=3, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["cu", "pr", "ru"], generators=[]),
            Floor(3, microchips=["co", "pl"], generators=[]),
        ]), moves=["1", "2", "3", "4", "5"])
        sequence_b = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=2, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["cu", "pr", "ru"], generators=[]),
            Floor(3, microchips=["co", "pl"], generators=[]),
        ]), moves=["1", "2", "3", "4", "5", "6"])
        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_unknown(self):
        sequence_a = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=3, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["ru"], generators=[]),
            Floor(3, microchips=["co", "cu", "pl", "pr"], generators=[]),
        ]), moves=list(range(0, 7)))
        sequence_b = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["cu", "pr"], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["ru"], generators=[]),
            Floor(3, microchips=["co", "pl"], generators=[]),
        ]), moves=list(range(0, 7)))
        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

    def test_unknown2(self):
        sequence_a = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=1, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["co", "cu"], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["pl", "pr", "ru"], generators=[]),
            Floor(3, microchips=[], generators=[]),
        ]), moves=list(range(0, 3)))
        sequence_b = Sequence([0], System(distinct_elements=["co", "cu", "pl", "pr", "ru"], elevator=3, floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=[], generators=["co", "cu", "pl", "pr", "ru"]),
            Floor(2, microchips=["pl", "pr", "ru"], generators=[]),
            Floor(3, microchips=["co", "cu"], generators=[]),
        ]), moves=list(range(0, 3)))
        assert_that(sequence_a.rating(), less_than(sequence_b.rating()))

class Variants(unittest.TestCase):
    def test_all_variants_directives_for_0_items(self):
        floor = Floor(0, microchips=[], generators=[])

        assert_that(variations(floor, DIRECTIVES[0], []), is_([]))
        assert_that(variations(floor, DIRECTIVES[1], []), is_([]))
        assert_that(variations(floor, DIRECTIVES[2], []), is_([]))
        assert_that(variations(floor, DIRECTIVES[3], []), is_([]))

    def test_all_variants_directives_for_1_items(self):
        floor = Floor(0, microchips=["a"], generators=[])

        assert_that(variations(floor, DIRECTIVES[0], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[1], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[2], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[3], ["a"]), is_([
            dict(direction=UP, microchips=["a"], generators=[])
        ]))

    def test_all_variants_directives_for_1_generator(self):
        floor = Floor(0, microchips=[], generators=["a"])

        assert_that(variations(floor, DIRECTIVES[0], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[1], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[2], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[3], ["a"]), is_([]))

    def test_all_variants_directives_for_1_of_each(self):
        floor = Floor(0, microchips=["a"], generators=["a"])

        assert_that(variations(floor, DIRECTIVES[0], ["a"]), is_([
            dict(direction=UP, microchips=["a"], generators=["a"])
        ]))
        assert_that(variations(floor, DIRECTIVES[1], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[2], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[3], ["a"]), is_([
            dict(direction=UP, microchips=["a"], generators=[])
        ]))

    def test_all_variants_directives_for_3_of_each(self):
        floor = Floor(0, microchips=["a", "b", "c"], generators=["a", "b", "c"])

        assert_that(variations(floor, DIRECTIVES[0], ["a", "b", "c"]), is_([
            dict(direction=UP, microchips=["a"], generators=["a"]),
            dict(direction=UP, microchips=["a"], generators=["b"]),
            dict(direction=UP, microchips=["a"], generators=["c"]),
            dict(direction=UP, microchips=["b"], generators=["a"]),
            dict(direction=UP, microchips=["b"], generators=["b"]),
            dict(direction=UP, microchips=["b"], generators=["c"]),
            dict(direction=UP, microchips=["c"], generators=["a"]),
            dict(direction=UP, microchips=["c"], generators=["b"]),
            dict(direction=UP, microchips=["c"], generators=["c"]),
        ]))
        assert_that(variations(floor, DIRECTIVES[1], ["a", "b", "c"]), is_([
            dict(direction=UP, microchips=["a", "b"], generators=[]),
            dict(direction=UP, microchips=["a", "c"], generators=[]),
            dict(direction=UP, microchips=["b", "c"], generators=[])
        ]))
        assert_that(variations(floor, DIRECTIVES[2], ["a", "b", "c"]), is_([
            dict(direction=UP, microchips=[], generators=["a", "b"]),
            dict(direction=UP, microchips=[], generators=["a", "c"]),
            dict(direction=UP, microchips=[], generators=["b", "c"]),
        ]))
        assert_that(variations(floor, DIRECTIVES[3], ["a", "b", "c"]), is_([
            dict(direction=UP, microchips=["a"], generators=[]),
            dict(direction=UP, microchips=["b"], generators=[]),
            dict(direction=UP, microchips=["c"], generators=[]),
        ]))

    def test_variations_should_only_consider_given_elements(self):
        floor = Floor(0, microchips=["a", "b", "c"], generators=["a", "b", "c"])

        assert_that(variations(floor, DIRECTIVES[0], ["a"]), is_([
            dict(direction=UP, microchips=["a"], generators=["a"])
        ]))
        assert_that(variations(floor, DIRECTIVES[1], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[2], ["a"]), is_([]))
        assert_that(variations(floor, DIRECTIVES[3], ["a"]), is_([
            dict(direction=UP, microchips=["a"], generators=[])
        ]))


class EquivalenceOfElements(unittest.TestCase):
    def test_return_a_list_elements_with_up_to_2_duplicates(self):
        system = System(distinct_elements=["a", "b"], floors=[
            Floor(0, microchips=["a", "b"], generators=["a", "b"]),
            Floor(1, microchips=[], generators=[]),
        ])

        assert_that(system.elements_worth_moving(), is_(["a", "b"]))

    def test_return_a_list_elements_that_without_duplicates_multi_level(self):
        system = System(distinct_elements=["a", "b"], floors=[
            Floor(0, microchips=["a", "b"], generators=[]),
            Floor(1, microchips=[], generators=[]),
            Floor(2, microchips=[], generators=["a", "b"]),
        ])

        assert_that(system.elements_worth_moving(), is_(["a", "b"]))

    def test_return_a_list_elements_that_without_duplicates_all_non_equivalent(self):
        system = System(distinct_elements=["a", "b", "c"], floors=[
            Floor(0, microchips=["a", "b", "c"], generators=[]),
            Floor(1, microchips=[], generators=["c"]),
            Floor(2, microchips=[], generators=["a", "b"]),
        ])

        assert_that(system.elements_worth_moving(), is_(["a", "b", "c"]))

    def test_return_a_list_elements_that_without_duplicates_multi_pair(self):
        system = System(distinct_elements=["a", "b", "c"], floors=[
            Floor(0, microchips=[], generators=[]),
            Floor(1, microchips=["a", "b", "c"], generators=[]),
            Floor(2, microchips=[], generators=["a", "b", "c"]),
        ])

        assert_that(system.elements_worth_moving(), is_(["a", "b"]))

    def test_return_a_list_elements_that_without_duplicates_multi_pair2(self):
        system = System(distinct_elements=["a", "b", "c", "d", "e", "f"], floors=[
            Floor(0, microchips=[], generators=["d", "e", "f"]),
            Floor(1, microchips=["a", "b", "c"], generators=[]),
            Floor(2, microchips=["d", "e", "f"], generators=["a", "b", "c"]),
        ])

        assert_that(system.elements_worth_moving(), is_(["a", "b", "d", "e"]))


def invert(variation):
    return dict(direction=variation["direction"] * -1, microchips=variation["microchips"], generators=variation["generators"])


class Invert(unittest.TestCase):
    def test_inverts_a_variation(self):
        variation = dict(direction=UP, microchips=["a"], generators=["b"])
        inverted = invert(variation)

        assert_that(inverted, is_(dict(direction=DOWN, microchips=["a"], generators=["b"])))
        assert_that(variation, is_not(inverted))

        inverted = invert(inverted)

        assert_that(variation, is_(inverted))


class DjikstraTest(unittest.TestCase):
    def setUp(self):
        self.method = djikstra

    def test_very_simple(self):
        result = self.method(dedent("""
            The first floor contains a hydrogen-compatible microchip and a hydrogen generator.
            The second floor contains nothing relevant."""))
        assert_that(result, is_(1))
    def test_2_floors(self):
        result = self.method(dedent("""
            The first floor contains a hydrogen-compatible microchip and a hydrogen generator.
            The second floor contains nothing relevant.
            The third floor contains nothing relevant."""))
        assert_that(result, is_(2))
    def test_official(self):
        result = self.method(dedent("""
            The first floor contains a hydrogen-compatible microchip and a lithium-compatible microchip.
            The second floor contains a hydrogen generator.
            The third floor contains a lithium generator.
            The fourth floor contains nothing relevant."""))
        assert_that(result, is_(11))


class AstarTest(DjikstraTest):
    def setUp(self):
        self.method = astar



if __name__ == '__main__':
    compute = astar

    if len(sys.argv) < 2 or sys.argv[1] == "1":
        print("Result is {}".format(compute(dedent("""
            The first floor contains a promethium generator and a promethium-compatible microchip.
            The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
            The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
            The fourth floor contains nothing relevant."""))))
    elif sys.argv[1] == "2":
        print("Result is {}".format(compute(dedent("""
            The first floor contains a promethium generator, a promethium-compatible microchip, a elerium generator, a elerium-compatible microchip, a dilithium generator, and a dilithium-compatible microchip.
            The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
            The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
            The fourth floor contains nothing relevant."""))))
    elif sys.argv[1] == "play":
        play(dedent("""
            The first floor contains a promethium generator and a promethium-compatible microchip.
            The second floor contains a cobalt generator, a curium generator, a ruthenium generator, and a plutonium generator.
            The third floor contains a cobalt-compatible microchip, a curium-compatible microchip, a ruthenium-compatible microchip, and a plutonium-compatible microchip.
            The fourth floor contains nothing relevant."""))


"""
WINNING at 33 moves :
{'direction': 1, 'generators': ['promethium'], 'microchips': ['promethium']}
{'direction': 1, 'microchips': ['promethium'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['cobalt', 'curium']}
{'direction': -1, 'microchips': ['cobalt'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['cobalt', 'plutonium']}
{'direction': -1, 'microchips': ['cobalt'], 'generators': []}
{'direction': -1, 'generators': [], 'microchips': ['cobalt', 'promethium']}
{'direction': 1, 'microchips': [], 'generators': ['curium', 'ruthenium']}
{'direction': -1, 'generators': ['curium'], 'microchips': []}
{'direction': 1, 'microchips': [], 'generators': ['curium', 'plutonium']}
{'direction': 1, 'generators': ['curium', 'plutonium'], 'microchips': []}
{'direction': -1, 'microchips': ['curium'], 'generators': ['curium']}
{'direction': 1, 'generators': ['curium', 'ruthenium'], 'microchips': []}
{'direction': -1, 'microchips': ['plutonium'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['curium', 'plutonium']}
{'direction': -1, 'microchips': [], 'generators': ['ruthenium']}
{'direction': -1, 'generators': ['ruthenium'], 'microchips': []}
{'direction': 1, 'microchips': ['cobalt', 'promethium'], 'generators': []}
{'direction': -1, 'generators': [], 'microchips': ['cobalt']}
{'direction': 1, 'microchips': [], 'generators': ['promethium', 'ruthenium']}
{'direction': 1, 'generators': ['promethium', 'ruthenium'], 'microchips': []}
{'direction': -1, 'microchips': ['curium'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['curium', 'promethium']}
{'direction': -1, 'microchips': [], 'generators': ['ruthenium']}
{'direction': -1, 'generators': ['ruthenium'], 'microchips': []}
{'direction': 1, 'microchips': [], 'generators': ['cobalt', 'ruthenium']}
{'direction': 1, 'generators': ['cobalt', 'ruthenium'], 'microchips': []}
{'direction': -1, 'microchips': ['curium'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['curium', 'ruthenium']}
{'direction': -1, 'microchips': ['curium'], 'generators': []}
{'direction': -1, 'generators': [], 'microchips': ['curium']}
{'direction': 1, 'microchips': ['cobalt', 'curium'], 'generators': []}
{'direction': 1, 'generators': [], 'microchips': ['cobalt', 'curium']}
"""
