import sys
import unittest
from dataclasses import dataclass
from textwrap import dedent
from typing import Dict, List, Callable, TypeVar

from hamcrest import assert_that, is_, has_key, not_
from pypaths import astar

from y2018 import Point, Directions


def compute(data):
    grid, fighters = parse(data)

    game = Game(
        grid=grid,
        fighters=fighters
    )

    return game.play()



def compute2(data):
    def try_it(value):
        print(f"Trying with {value}")
        grid, fighters = parse(data)

        game = Game(
            grid=grid,
            fighters=fighters
        )

        for f in fighters:
            if f.team == "E":
                f.attack_power = value

        game.report_death = lambda e: game.stop() if e.team == "E" else None

        return game.play()

    return dichotomic_search(
        start=4,
        end=200,
        test=try_it,
        until=lambda result: result is not None
    )


T = TypeVar('T')

def dichotomic_search(start: int,
                      end: int,
                      test: Callable[[int], T],
                      until: Callable[[T], bool]):

    if start == end:
        return test(start)
    half = start + int((end - start) / 2)

    result = test(half)
    if until(result):
        if half == start:
            return result
        else:
            return dichotomic_search(start, half, test, until)
    else:
        if half == end:
            return result
        else:
            return dichotomic_search(half + 1, end, test, until)


@dataclass
class Game:
    grid: Dict
    fighters: List

    report_death = lambda self, e: None
    keep_going = True

    def __post_init__(self):
        for f in self.fighters:
            f.game = self

    def play(self):
        turn = 0
        while self.keep_going:

            playing = self.tick()
            if not playing:
                return turn * sum(f.hp for f in self.fighters)

            turn += 1

        return None

    def stop(self):
        self.keep_going = False

    def tick(self):
        for fighter in self.sorted_fighters():
            try:
                if fighter.is_alive:
                    fighter.act()
            except NoMoreEnemies:
                return False

        return True

    def sorted_fighters(self):
        return sorted(self.fighters, key=lambda f: (f.pos.y, f.pos.x))

    def get_neighbors(self, point: Point):
        for x, y in neighbors:
            pos = Point(point.x + x, point.y + y)
            if pos.tuple() in self.grid:
                yield pos

    def move(self, fighter, new_pos):
        # print(f"{fighter} moves to {new_pos}")
        self.grid[fighter.pos.tuple()] = None
        self.grid[new_pos.tuple()] = fighter
        fighter.pos = new_pos

    def hit(self, attacker, defender):
        # print(f"{attacker} attacks {defender}")
        defender.hp -= attacker.attack_power
        if defender.hp <= 0:
            self.grid[defender.pos.tuple()] = None
            self.fighters.remove(defender)
            defender.is_alive = False
            self.report_death(defender)


neighbors = ((0, -1), (-1, 0), (1, 0), (0, 1))


class NoMoreEnemies(Exception):
    pass


@dataclass
class Fighter:
    team: str
    pos: Point
    hp: int = 200
    attack_power: int = 3
    is_alive: bool = True

    game: Game = None

    def act(self):
        self.attack() or \
        (self.move() and self.attack())

    def attack(self):
        possible_targets = []
        for pos in self.game.get_neighbors(self.pos):
            target = self.game.grid[pos.tuple()]
            if isinstance(target, Fighter) and target.team != self.team:
                possible_targets.append(target)

        if len(possible_targets) > 0:
            target = sorted(possible_targets, key=lambda e: e.hp)[0]
            self.game.hit(self, target)
            return True

        return False

    def move(self):
        start = self.pos

        def reading_order_cost(current, neighbor):
            if current == start:
                try:
                    if current.direction_to(neighbor) == Directions.UP:
                        return 1
                    elif current.direction_to(neighbor) == Directions.LEFT:
                        return 2
                    elif current.direction_to(neighbor) == Directions.RIGHT:
                        return 3
                    elif current.direction_to(neighbor) == Directions.DOWN:
                        return 4
                except ValueError:
                    pass

            return 10

        targets = []
        has_an_enemy = False
        for fighter in self.game.fighters:
            if fighter.team != self.team:
                has_an_enemy = True

                def get_free_neighbors(point):
                    for neighbor in self.game.get_neighbors(point):
                        if neighbor == fighter.pos or self.game.grid[neighbor.tuple()] is None:
                            yield neighbor

                find_path = astar.pathfinder(
                    neighbors=get_free_neighbors,
                    distance=lambda start, end: start.manhattan_dist(end),
                    cost=reading_order_cost
                )

                length, path = find_path(self.pos, fighter.pos)
                if length is not None:
                    targets.append((length, path))

        if len(targets) > 0:
            targets = sorted(targets)
            length, path = targets[0]
            self.game.move(self, path[1])

        if not has_an_enemy:
            raise NoMoreEnemies

        return True

    def __str__(self):
        return f"[{self.team}({self.pos}); hp={self.hp}]"


def parse(data):
    fighters = []
    grid = {}
    for y, line in enumerate(data.split("\n")):
        for x, char in enumerate(line):
            if char == ".":
                grid[x, y] = None
            elif char in ["E", "G"]:
                fighter = Fighter(char, Point(x, y))
                grid[x, y] = fighter
                fighters.append(fighter)

    return grid, fighters


class ParseTest(unittest.TestCase):
    def test_parse(self):
        grid, fighters = parse(dedent("""\
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######"""))

        assert_that(fighters, is_([
            Fighter("G", Point(2, 1)),
            Fighter("E", Point(4, 2)),
            Fighter("G", Point(5, 2)),
            Fighter("G", Point(5, 3)),
            Fighter("G", Point(3, 4)),
            Fighter("E", Point(5, 4)),
        ]))

        assert_that(grid[2, 1], is_(fighters[0]))
        assert_that(grid[3, 1], is_(None))
        assert_that(grid, not_(has_key((2, 3))))


class ProvidedTest(unittest.TestCase):
    def test_part_1_1(self):
        input = dedent("""\
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######""")
        assert_that(compute(input), is_(27730))

    def test_part_1_2(self):
        input = dedent("""\
        #######
        #G..#E#
        #E#E.E#
        #G.##.#
        #...#E#
        #...E.#
        #######""")
        assert_that(compute(input), is_(36334))

    def test_part_1_3(self):
        input = dedent("""\
        #######
        #E..EG#
        #.#G.E#
        #E.##E#
        #G..#.#
        #..E#.#
        #######""")
        assert_that(compute(input), is_(39514))

    def test_part_1_4(self):
        input = dedent("""\
        #######
        #E.G#.#
        #.#G..#
        #G.#.G#
        #G..#.#
        #...E.#
        #######""")
        assert_that(compute(input), is_(27755))

    def test_part_1_5(self):
        input = dedent("""\
        #######
        #.E...#
        #.#..G#
        #.###.#
        #E#G#G#
        #...#G#
        #######""")
        assert_that(compute(input), is_(28944))

    def test_part_1_6(self):
        input = dedent("""\
        #########
        #G......#
        #.E.#...#
        #..##..G#
        #...##..#
        #...#...#
        #.G...G.#
        #.....G.#
        #########""")
        assert_that(compute(input), is_(18740))

    def test_part_2_1(self):
        input = dedent("""\
        #######
        #.G...#
        #...EG#
        #.#.#G#
        #..G#E#
        #.....#
        #######""")
        assert_that(compute2(input), is_(4988))

    def test_part_2_3(self):
        input = dedent("""\
        #######
        #E..EG#
        #.#G.E#
        #E.##E#
        #G..#.#
        #..E#.#
        #######""")
        assert_that(compute2(input), is_(31284))

    def test_part_2_4(self):
        input = dedent("""\
        #######
        #E.G#.#
        #.#G..#
        #G.#.G#
        #G..#.#
        #...E.#
        #######""")
        assert_that(compute2(input), is_(3478))

    def test_part_2_5(self):
        input = dedent("""\
        #######
        #.E...#
        #.#..G#
        #.###.#
        #E#G#G#
        #...#G#
        #######""")
        assert_that(compute2(input), is_(6474))

    def test_part_2_6(self):
        input = dedent("""\
        #########
        #G......#
        #.E.#...#
        #..##..G#
        #...##..#
        #...#...#
        #.G...G.#
        #.....G.#
        #########""")
        assert_that(compute2(input), is_(1140))

    puzzle_input = """\
################################
####.#######..G..########.....##
##...........G#..#######.......#
#...#...G.....#######..#......##
########.......######..##.E...##
########......G..####..###....##
#...###.#.....##..G##.....#...##
##....#.G#....####..##........##
##..#....#..#######...........##
#####...G.G..#######...G......##
#########.GG..G####...###......#
#########.G....EG.....###.....##
########......#####...##########
#########....#######..##########
#########G..#########.##########
#########...#########.##########
######...G..#########.##########
#G###......G#########.##########
#.##.....G..#########..#########
#............#######...#########
#...#.........#####....#########
#####.G..................#######
####.....................#######
####.........E..........########
#####..........E....E....#######
####....#.......#...#....#######
####.......##.....E.#E...#######
#####..E...####.......##########
########....###.E..E############
#########.....##################
#############.##################
################################"""

    if __name__ == '__main__':
        if sys.argv[1] == "2":
            result = compute2(puzzle_input)
        else:
            result = compute(puzzle_input)

        print(f"Result is {result}")
