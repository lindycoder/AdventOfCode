import logging
import re
import sys
from dataclasses import dataclass, asdict
from itertools import combinations

import pytest
from hamcrest import assert_that, is_

from y2019.lcm import lcm
from y2019.point3d import Point3d


def compute(data, steps=1000):
    moons = parse(data)

    simulate(moons, steps)

    return sum(moon.energy for moon in moons)


def compute2_lcm(data):
    start = parse(data)
    moons = parse(data)
    orbits = []
    orbits_pending = [0, 1, 2, 3]

    steps = 0
    while True:
        simulate(moons, 1)
        steps += 1

        for i in orbits_pending[:]:
            if start[i] == moons[i]:
                logging.info(f'Orbit of moon {i} == {steps} steps')
                orbits.append(steps)
                orbits_pending.remove(i) # impacting loop

        if len(orbits_pending) == 0:
            break

    return lcm(*orbits)


def compute2(data):
    start = parse(data)
    logging.info("".join([f'{s.energy:<10}' for s in start]))
    moons = parse(data)

    steps = 0
    while True:
        simulate(moons, 1)
        steps += 1
        if all(s.energy == 0 for s in moons):
            return steps
        # logging.info(f"Step {steps}: " + "".join([f'{s.energy:<10}' for s in moons]))


def simulate(moons, steps):
    for i in range(steps):
        update_velocities(moons)
        apply_velocities(moons)


def update_velocities(moons):
    for moon1, moon2 in combinations(moons, 2):
        for axis in ['x', 'y', 'z']:
            pos1, pos2 = getattr(moon1.position, axis), getattr(moon2.position,
                                                                axis)
            if pos1 > pos2:
                v1, v2 = -1, 1
            elif pos1 < pos2:
                v1, v2 = 1, -1
            else:
                v1, v2 = 0, 0

            setattr(moon1.velocity, axis, getattr(moon1.velocity, axis) + v1)
            setattr(moon2.velocity, axis, getattr(moon2.velocity, axis) + v2)


def apply_velocities(moons):
    for moon in moons:
        moon.position += moon.velocity


def parse(data):
    return [
        Moon(Point3d.from_string(line), Point3d(0,0,0))
        for line in data.strip().splitlines()
    ]

@dataclass
class Moon:
    position: Point3d
    velocity: Point3d

    @property
    def energy(self):
        return sum(map(abs, asdict(self.position).values())) * sum(map(abs, asdict(self.velocity).values()))

    def __str__(self):
        return f'pos={self.position}, vel={self.velocity}'


@pytest.mark.parametrize('scenario', [
    ("""\
After 0 steps:
pos=<x=-1, y=0, z=2>, vel=<x=0, y=0, z=0>
pos=<x=2, y=-10, z=-7>, vel=<x=0, y=0, z=0>
pos=<x=4, y=-8, z=8>, vel=<x=0, y=0, z=0>
pos=<x=3, y=5, z=-1>, vel=<x=0, y=0, z=0>
"""), ("""\
After 1 steps:
pos=<x=2, y=-1, z=1>, vel=<x=3, y=-1, z=-1>
pos=<x=3, y=-7, z=-4>, vel=<x=1, y=3, z=3>
pos=<x=1, y=-7, z=5>, vel=<x=-3, y=1, z=-3>
pos=<x=2, y=2, z=0>, vel=<x=-1, y=-3, z=1>
"""), ("""\
After 2 steps:
pos=<x=5, y=-3, z=-1>, vel=<x=3, y=-2, z=-2>
pos=<x=1, y=-2, z=2>, vel=<x=-2, y=5, z=6>
pos=<x=1, y=-4, z=-1>, vel=<x=0, y=3, z=-6>
pos=<x=1, y=-4, z=2>, vel=<x=-1, y=-6, z=2>
"""), ("""\
After 3 steps:
pos=<x=5, y=-6, z=-1>, vel=<x=0, y=-3, z=0>
pos=<x=0, y=0, z=6>, vel=<x=-1, y=2, z=4>
pos=<x=2, y=1, z=-5>, vel=<x=1, y=5, z=-4>
pos=<x=1, y=-8, z=2>, vel=<x=0, y=-4, z=0>
"""), ("""\
After 4 steps:
pos=<x=2, y=-8, z=0>, vel=<x=-3, y=-2, z=1>
pos=<x=2, y=1, z=7>, vel=<x=2, y=1, z=1>
pos=<x=2, y=3, z=-6>, vel=<x=0, y=2, z=-1>
pos=<x=2, y=-9, z=1>, vel=<x=1, y=-1, z=-1>
"""), ("""\
After 5 steps:
pos=<x=-1, y=-9, z=2>, vel=<x=-3, y=-1, z=2>
pos=<x=4, y=1, z=5>, vel=<x=2, y=0, z=-2>
pos=<x=2, y=2, z=-4>, vel=<x=0, y=-1, z=2>
pos=<x=3, y=-7, z=-1>, vel=<x=1, y=2, z=-2>
"""), ("""\
After 6 steps:
pos=<x=-1, y=-7, z=3>, vel=<x=0, y=2, z=1>
pos=<x=3, y=0, z=0>, vel=<x=-1, y=-1, z=-5>
pos=<x=3, y=-2, z=1>, vel=<x=1, y=-4, z=5>
pos=<x=3, y=-4, z=-2>, vel=<x=0, y=3, z=-1>
"""), ("""\
After 7 steps:
pos=<x=2, y=-2, z=1>, vel=<x=3, y=5, z=-2>
pos=<x=1, y=-4, z=-4>, vel=<x=-2, y=-4, z=-4>
pos=<x=3, y=-7, z=5>, vel=<x=0, y=-5, z=4>
pos=<x=2, y=0, z=0>, vel=<x=-1, y=4, z=2>
"""), ("""\
After 8 steps:
pos=<x=5, y=2, z=-2>, vel=<x=3, y=4, z=-3>
pos=<x=2, y=-7, z=-5>, vel=<x=1, y=-3, z=-1>
pos=<x=0, y=-9, z=6>, vel=<x=-3, y=-2, z=1>
pos=<x=1, y=1, z=3>, vel=<x=-1, y=1, z=3>
"""), ("""\
After 9 steps:
pos=<x=5, y=3, z=-4>, vel=<x=0, y=1, z=-2>
pos=<x=2, y=-9, z=-3>, vel=<x=0, y=-2, z=2>
pos=<x=0, y=-8, z=4>, vel=<x=0, y=1, z=-2>
pos=<x=1, y=1, z=5>, vel=<x=0, y=0, z=2>
"""), ("""\
After 10 steps:
pos=<x=2, y=1, z=-3>, vel=<x=-3, y=-2, z=1>
pos=<x=1, y=-8, z=0>, vel=<x=-1, y=1, z=3>
pos=<x=3, y=-6, z=1>, vel=<x=3, y=2, z=-3>
pos=<x=2, y=0, z=4>, vel=<x=1, y=-1, z=-1>
""")
])
def test_v(scenario):
    initial = """\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>"""

    steps, moon1, moon2, moon3, moon4 = scenario.strip().splitlines()

    steps = int(re.match('After (\d+) steps:', steps).group(1))

    moons = parse(initial)
    simulate(moons, steps=steps)
    assert_that(str(moons[0]), is_(moon1))
    assert_that(str(moons[1]), is_(moon2))
    assert_that(str(moons[2]), is_(moon3))
    assert_that(str(moons[3]), is_(moon4))


@pytest.mark.parametrize('initial,steps,value', [
    ("""\
<x=-1, y=0, z=2>
<x=2, y=-10, z=-7>
<x=4, y=-8, z=8>
<x=3, y=5, z=-1>""", 10, 179),
    ("""\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""", 100, 1940),
])
def test_compute(initial, steps, value):
    assert_that(compute(initial, steps=steps), is_(value))


@pytest.mark.parametrize('initial,value', [
#     ("""\
# <x=-1, y=0, z=2>
# <x=2, y=-10, z=-7>
# <x=4, y=-8, z=8>
# <x=3, y=5, z=-1>""", 2772),
    ("""\
<x=-8, y=-10, z=0>
<x=5, y=5, z=10>
<x=2, y=-7, z=3>
<x=9, y=-8, z=-3>""", 4686774924),
])
def test_compute2(initial, value):
    assert_that(compute2(initial), is_(value))


puzzle_input = """\
<x=-16, y=-1, z=-12>
<x=0, y=-4, z=-17>
<x=-11, y=11, z=0>
<x=2, y=2, z=-6>
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
