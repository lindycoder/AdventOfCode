from collections import defaultdict
from dataclasses import dataclass
from enum import Enum
from operator import itemgetter
from typing import Generator, Union

import pytest
import sys
from hamcrest import assert_that, is_


@dataclass(frozen=True)
class HexPoint:
    """https://www.redblobgames.com/grids/hexagons/"""
    x: int
    z: int
    y: int

    def __add__(self, other: Union['HexPoint', 'HexDir']):
        if isinstance(other, HexDir):
            other = other.value
        return HexPoint(self.x + other.x, self.z + other.z, self.y + other.y)


@dataclass(frozen=True)
class HexDir(Enum):
    W = HexPoint(-1, 0, 1)
    NW = HexPoint(0, -1, 1)
    NE = HexPoint(1, -1, 0)
    E = HexPoint(1, 0, -1)
    SE = HexPoint(0, 1, -1)
    SW = HexPoint(-1, 1, 0)


@pytest.mark.parametrize('hp,hdir,matches', [
    (HexPoint(0, 0, 0), HexDir.NE, HexPoint(1, -1, 0)),
    (HexPoint(2, -1, -1), HexDir.NE, HexPoint(3, -2, -1)),
])
def test_hex_point_add(hp, hdir, matches):
    assert_that(hp + hdir, is_(matches))


def compute(data):
    tiles = flip_by_path(data)

    return len(list(find_black_tiles(tiles)))


def find_black_tiles(tiles):
    return map(itemgetter(0), filter(lambda e: e[1], tiles.items()))


def flip_by_path(data):
    origin = HexPoint(0, 0, 0)
    tiles = defaultdict(lambda: False)
    for line in data.strip().splitlines():
        new_tile = origin
        for hex_dir in parse_dirs(line):
            new_tile += hex_dir
        tiles[new_tile] = not tiles[new_tile]
    return tiles


def compute2(data):
    new_black_tiles = set(find_black_tiles(flip_by_path(data)))

    for _ in range(100):
        black_tiles = new_black_tiles.copy()

        white_tiles = set()
        for tile in black_tiles:
            white_tiles.update(tile + d for d in HexDir)
        white_tiles -= black_tiles

        new_black_tiles = set()
        for tile in black_tiles:
            near = sum(1 for d in HexDir if (tile + d) in black_tiles)
            if near in (1, 2):
                new_black_tiles.add(tile)
        for tile in white_tiles:
            near = sum(1 for d in HexDir if (tile + d) in black_tiles)
            if near == 2:
                new_black_tiles.add(tile)

    return len(new_black_tiles)


def parse_dirs(data: str) -> Generator[HexDir, None, None]:
    chars = list(data)
    while len(chars):
        dir_name = chars.pop(0)
        if dir_name in ('s', 'n'):
            dir_name += chars.pop(0)
        yield HexDir[dir_name.upper()]


def test_parse_dirs():
    assert_that(list(parse_dirs('esenee')),
                is_([HexDir.E, HexDir.SE, HexDir.NE, HexDir.E]))


@pytest.mark.parametrize('val,expect', [
    ("""\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""", 10)
])
def test_compute(val, expect):
    assert_that(compute(val), is_(expect))


@pytest.mark.parametrize('val,expect', [
    ("""\
sesenwnenenewseeswwswswwnenewsewsw
neeenesenwnwwswnenewnwwsewnenwseswesw
seswneswswsenwwnwse
nwnwneseeswswnenewneswwnewseswneseene
swweswneswnenwsewnwneneseenw
eesenwseswswnenwswnwnwsewwnwsene
sewnenenenesenwsewnenwwwse
wenwwweseeeweswwwnwwe
wsweesenenewnwwnwsenewsenwwsesesenwne
neeswseenwwswnwswswnw
nenwswwsewswnenenewsenwsenwnesesenew
enewnwewneswsewnwswenweswnenwsenwsw
sweneswneswneneenwnewenewwneswswnese
swwesenesewenwneswnwwneseswwne
enesenwswwswneneswsenwnewswseenwsese
wnwnesenesenenwwnenwsewesewsesesew
nenewswnwewswnenesenwnesewesw
eneswnwswnwsenenwnwnwwseeswneewsenese
neswnwewnwnwseenwseesewsenwsweewe
wseweeenwnesenwwwswnew
""", 2208)
])
def test_compute2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
ewnwnwsenwnwnwwnweswnwnenwnwesenwwnww
wswwswwnwwswswswswnewswwwewsew
seseeseswwneseseseseseenenesewsesesew
nwwnwnenenwneseseenewnenenenenenwnenenene
enwnenwwnwwwswswseewnwenwwnw
nwsenwsenwewnwewwwwnwnenwwnwswwe
seseseeseeseneseseseeseseesesw
nwsweswsenwnenesweseenenwswnenwenwwe
nwswnwnwneenwnenwnwnwnwnwwnwswswnwwenwnw
nwwnwnwnwenwnwnwnwwnwnwnwswwwnwnwe
neswseseseeewnwsenwswsweseswwswsesw
swnenenwneeneeeeeneeneee
wesewseseseseswnesewseseseenwsenenwse
eneeseswswswswnwsewseenwnwswseswswnwsw
seswsweswneeswswnewwswnwnwnewnesesesese
enenweeneeeeewneeneswese
eneeneeeneeneneenwseeswnenenewsee
enwnwenwsenwnwnwnwnwnwnwwnwnwswnwnwnwnwsw
wwwwnwwwnwwsewwnwnwwnwwsenenww
eeneswneeneeeeesesewenwswnwenenwsw
seneswsewsewneneeeneeeeswwnwee
nwwwswwsewswewwwwswnewswwwwsew
senwseseseseswswseseseswseesesesese
wwswseswwswswswseswenwswwnenwswswswsw
seseneswswseswswneswneseswwswwswwneswwsw
nwswwswswseswswswwnwsweeswnwsweswsw
seseesesesenwseeseseseseseswse
neenesweswnwnwwwnwsenewnwnewwswwnw
senwseswseseseswnewsesweswswsweswse
wwnwwnwswwnwwwwwnwne
sesesesenenewsesesweseseswsewsewse
seswneseseswsewnenweswseswsenweswneswsesw
eneswnewneneneeneneneeneneneeneene
weseswwwwnwnwwwseswwneeswwww
seeeenwseenwnwswseeeseseeseeeee
sesesenwseswneseeenwseseseswswwswesenw
nwnwenwnwnwwswnwnwnwnwwenwsenwnwnww
nwnwnwneneswwnenwnenenwnwsenwnenwnwnenwne
senewnwneenwwswwnwnwneenenwsw
neneneneneenenwnenenesenenwnesenwswnene
neswswsweswswswswnenwswwswswewneswsw
sesesesesesenwswswsesesesesewswnese
eneseeseeeseeswsesese
wwseseseswswseseseeswwseswnewseenesw
eeeeeeeeswnewwenweewwnwswse
nwwswenwnwswenwnwnwwnwewnwnwwnwwnw
nwnwsewnwwnwenwnwnwnwwnwswnwnwnwnww
nwnwwswswnwneeneswnwnwenwenwnwnwnwwnw
neswneneneneneneenenesw
newenwswseeweseesweweseneewnesee
enwwswwwnwwnwseswwwwwnenwnenesw
seswnwseseneneseeswswswnewwswswew
wnwsewwnwwenwseeeww
swswswswswnwswswswnesenwswsesweswswwswsw
wneweswswswswswswswwwswwsewswnwsw
swwswswneswswswwswwneswswswswswswswesw
seeseseeeenwenweeenwsenweswswnwse
swswswswswswswswwneswneseswwswwsww
neeneneseneewsenenenenewnenenenenene
nwwnwseeneswswnwneswneeswseenwnwnesww
wneswseswswnwswwswwswwswwnewenese
seewesesesesewseseseeseseseneseesese
sesenwnwswneswswseswwsewneswneseenenww
swswewseseswnwswseseseswsewswnenwsesese
swwswswswswswwnewswewwswswwswswe
wsesesewneneeswsweeneswwnwswsw
neswswswswseswseseswswseswswneswsw
enwseewsweseeeeeeesesweneseenw
wewnewwwwwwnewwwswwwwsww
eswnwwswsenwwwenwswwswwsenenesw
ewnwnwswsenwnwnwnwwwnwenwwnwnwnwnw
wnwenenwenwnwsenwnwswnenwnewnenenese
sewwenwwwnwnwwwnwnesenwnwnw
eeeeeeeneeeeweeeseesw
wswsewnenwwwnwnwnwnwnwnwnwneswnwww
swenweeseeeewneneeeenenweese
neeesweswwneeeeeneeeneesenee
swwwneseswswswwwswsewswswnw
eswenenwnwswnwwnwwnwsewnwneswnwneswnwne
nenwneneneesenenwnesenwwnenenenenwnww
wwenwswswwswwnwsenwwwseewwswwww
swwswwwswwnwnwswweswswwswswswwe
eeneeseneseeeesweeeesesw
nweesewnewneseneneneneneseeeneenene
enwweswwseseenwswweee
wwwnwnwnenwwnwswnwnwwwswwnwenwwnw
nwseneneneeneneeeeneewswswwne
nesesesesweseeseseseeesenwse
eseesenwnwswseneswseseeese
nwseswneswnewnwsene
eeeeeeweseseweeneeeeesee
nenesewnesenwewwwsewwwewwnesesew
wwnwswseswsenesewsenwseeee
seseseswseswnwseseneseseswsenewswswsesw
seenwenweeseseesweswesenewewee
swneenenenenenwnwnenwnenenwnwnenwnwne
sewwwwwwsenewsewnwenwswswnenwnwnw
seseseswsewseseseewnewsesenwnesenene
nwnwnesenweswswnweswnwnenenwnewnwnwwnwne
swenenwseswnewweswnenenwewnwnewnw
nenenenesenewenenenenwneneswnwneenwwne
nesewwnwnwswseenenwnwwewnesenwnwswsw
eeewenwseeeseesesweseenwnwee
nwwswnenwsenwwswneewwwwwnwwswnwsenw
nwnwwnenenewnenenenenwnwnenwneneseenene
nwswswswswswswswswswswswseswswseswesw
swswseseseeseseseseneesesesewsenwnwseswse
wswwnewwwswwswwewswwwseneswww
wwwwwwwswwew
ewewnwswnwwswnwwwwnwewwwnwwnwnw
nesenwneneeneneeneeneeeneneeewne
seseseseseswwsesesesesenese
seswsweneswseeswswwseswnewseswnwsw
swweneswneneeeneeeeneeeenw
wnwnenweswewnwwwwnwswsewnwnwnwwwnw
swseneeeneswseewwneseweesewwese
nwwnwwnwwnwnwwnwwnewwnwnwwnwsesese
senenwswseswseesesenesesesewwsesenesesese
nwnwnwnenwnenwnwewnwneswwnwenenwnwnw
nwenwnweseswwwnwnwnwnwnenenenwnwnwnwnw
nwneneneenenenwneswnenenenenwnenenene
swsweswwswneswswswswswwwsww
wwsewwwnewwwwswnewwwwwww
nenweeewswneneswneeeseesweseswewne
sesesweeeenweeeeenwswwnwwee
neeewwnewesewwwnesewwewseenww
enwwwswnwwenwwnwwwenwwswwww
newnwsenwwswwswnwsewnenenwnwneesenwsew
nenenewneeneneneeneneeswnenenwswnee
neenewsenenwneneneswsenenenenwneneswnw
eswneesesenwwseseeeseeewnesesesese
eeswnwnwnwnwnenewnwnwsenwnwnwnwnwnwnwnw
seswsesesweneseswswwswwseswswseseseswsw
swnwsesenwwnewnwwwwnwnwwenwneneswnwnw
wsenwseeseseseweneseeesese
nwsenwnwwnwewenwnwsw
seeswseneeneswsesewseswneseseseseeenw
nwswswswswseeswswneswseseseseswswseseswswne
swnwnwswenwsenwswewwneewwswwnwne
wnwwsenwenwswnwnwnwnwnwnwnwnwnwenene
wwnwswnwwnwwwnwwnwwnwnwwenwnwwse
nwneswenenwnenenenenenenwneswneswnwnwnene
neneenenwneneeeswnenewneeseneewene
ewwswsenwwnwsenwnwnwnwwwnwnwwnwwse
eeeeneseeeeeenweeweseeneee
nwnwnwnesenwnwwnwneswnwnwnwnw
seseseseewesenewneseseseneesweesesw
weswnesweswwnenwswseneswseneswwswwsw
nwneeswnenenwnewnenenwneswswneneesenwne
swnewweewswwswswwnwewwwswswnwsww
swswswsenwswswswswsweswswwseswswneswse
weeeseeeeewneeeeneeseseewse
newseneneneswnenwneneeseseewneewsee
neneenwnewnweseswwneeswnwnwswnenwnwnw
neesenweneenweenesesweswenweeew
eeseseneseeseseseeeewenwseeesee
weseseswswswswswswseseseseswse
eewswwseseseseseseeeseseenenw
swwnwsenwnewswnwswsweeswwwwswsenese
neneewneeeeeeseeneeeneeeenw
swseswsweswswswwswnwenwswswswswswnew
swswswswswswnesewswseseenwseswswswswswsesw
wnenesweesenweeswwnwseenwnesweswee
nenwnwnwswswnwnwsenwwnwnenwesesenwnewswe
swsenwesesewswenwwseneswswseneswne
nwnwnenwnwenenenenwswnwnwnw
eeneneneeswnweneeswswneeneeneeene
nwswswewwnwswwwswwenewseswwww
senwseseswwseesenesweswnwseseseeenwe
eweneeeeseneeeeee
wwwswwwwesewnewwww
nwnwnwnwnwnwswnwnwnwnwnwnwenwswnwnwneenwnw
eeeseenweeeeeeeseewnesesewe
swswewswswswswswswswseswenwseswswnesw
nweswenwnwesweseseseeeeee
nwenenenewswwsenenwnwnwnenenwnenw
nwneneneswneneneneseneneneneneneneneene
swswnwwswwwswsweswsweneswswswswwswsww
swswneenenwwnwwsewswenenewwseseswnw
nenenesweneeswneeeeneneswenenenenee
nenwseenwnwneswnenenweeneswnwnewsenesw
swwwswwsewwwswswnewwwwwswswne
weesesenwenwneswneeesweweneswnew
nwenenesenwneneneneswswnwwneswnwnwenwne
senwnwwnwnwnwwsenwnenwnwswseneww
senwseseseseseseneneseseswesenwswsesesesw
wenweneeseeseweeeweeneeeenee
seseswewneseseseesese
seeseeewseeeeseewe
eeswnweeeeneeeneeee
eneweeeeeeeenee
sweseswswswswswswswwswswseseswnwswsesw
nwwsewnewwenwnwnwswswnw
weseswsewseswnwswnwsesesenwneseswsenese
newnwneeenewsenwswnwnwnenwnewnenenw
nwsenwnwnwnwnwnwsenenenwnwnwnwwnenenewne
wneswnwwwwsewwsewwwwwwenwe
wwswswswnenewswwswewwsenwweww
enenesweeneneeneeseeneeneeewnwe
neneneneneswnenwnewenwnenenwneneenenwne
nwnweeeswneseseswnwsesweseeseenwewe
ewnwnwswnwnwnwwswnwnwnewnwneseewww
wenwwsenwswwnenwnwnwwenwwnwnwseww
enwswnwnwnwsenwnwswnwnwnwnenwnwnenwnwnw
nwnwenwwwnwnwnwwsenwnwnwnwnwnwnw
nwswswnwnwenenwnwnwnwnwenwnenenwnenwnenw
nwwswwswswneneswsewwseswwwsewswnesw
nwsewwwwwwswwnwenwwwwwwnew
nwnwnwnwnwnwneneswnenwnenwnwnwne
nenenenenesesenenenenenenenenwnwnenenenew
swswwewswwnenwnewwwsewsw
nwnwnwnenwsewsewnwnewwneswnwnw
swswswswswseswseseseneswwswseneseswsesw
nwnwnwnwnwnwenwnwnwwnwnwnwnwwwenwnwsw
eneeeeeeeeeenesenenenenewewne
eneewewwseewenwsweeneeeesene
sewseseswswswseswseseseneseswseneswsesesw
ewwnwwswswnwnesesewnweesweseeenene
wswnewsenwwwwwnwnwenwwwwwwwwnw
eeseeneeweneeeeeeweeeseee
wswswswswswswwswswswnwswewswwnwswewsw
wseseeesenwseseeeeenwsesesesw
eseesewnweeswneeeewese
sweswswswnwswswwswwnwswwewewnewsew
eeeneeeneeneenwenwsweneswneeenee
swenwseneweseneneneeewswewnwneeese
wwnwnwsweeeneswnewseswneswswneese
seswsesesenwseseseseswswesenwseseswsese
senenenenweeeneeneeweeneeeesw
seseseneswseseswwswseseneswswseneeswse
wwswwwenwswwwswseswww
sweswswseseswswnwswseswsw
eeeweeeneneweneweseeneee
seswwseseneneswswseswneeseswwswwsesw
nwenenewneswnewwnewnesenwenwnesenwne
nwnenwwnwnenwseswsenesenenenenwesenwne
neswswwswwswwsww
nwwsewwwsewenewwswwnewwwswwse
nwsenwnwsenenwnwnwnwnwnwnwnwnwnwwnwnwnwnw
nwsenwwnwnesenenenwnwnwnwnwnwenwnwnenene
seseseswnewseseswwneneseswe
neswwswswswswsweseswsesesesenwseswnwsese
eseesweeeneeseseseenwseneseseswse
wswwsewewwwwwwwwwswwwwnew
newnwwswnewwswwwwswswsesewwsweswsw
eeeneneneneneseneswnwneenenenenenwne
nwswnwenenenenenwnenenewnesenenwnwnwne
wsenwwwwewwnewwnwsewwswwnwww
neseseewneeesenweswneeesesewesese
nwnwnenenwnwnwnwnwnwnwnwnwnwnesenw
nwwwnwswnwwnwnwenwwnwwewwwwse
neseswswswseswswswswswsesw
sweeneneeenewnwswneeeneneeenee
nwswenwenwswnenenenwseesenwwswswese
eeeswseeeneneeewseesesweeeee
nenenwnesenwsenenenenwnwneseneneswnenese
enwnwnenwnenwnenenewnwswnwnenwnenwnwnesw
eeeeewseeenwsw
nesenenenwwenwnwnenwnwswnenesenwnwnenw
sewswneneswsewww
weswswswswswnwwswwewwwwswswwswsw
nwswnweswnenwnenwnwnwnwseene
enwenwnenesewneeeswnewseenenwnee
eeeeseenwneenenenenwnenweeeseswse
nwseswseswswnwswesenwesesene
wnwwnwwewnwnwnwwwwnewwswnewwnwse
eswseswswswwswswswswswswswnwsw
wwneswwwewnwswewwwswwwwsew
seseseseseswsewneswseseseneswseseswswnesese
nwneswswswsweswewswswswwseswswnwswswesw
neswnenenewswnwswsenwnwenwnenenenwnwnwswne
swnwneseneeeneneeeeneneneswneene
eseeeenweeeeesweese
seseeseseseseseseswwseseseneesesesese
eseseeseenwseseseenweseeseenwesee
nwswneneneneneneeneneeneeneesenenwse
nesewnenenenenenewnenenenenenenenesene
nenwnwwsenwwnwswsewnwnwseeswenwwnww
swseswswsenwseseswsweseswswswsw
neswswnwnwneswnwswnweneswnwweenwnwswne
swswsweswswswswwswnwswwwswwswseeswnw
nwnwnwnwnwswnwwnwnwnwenwnwnwsesenenwnw
nwseneseswseseswswnwseseswenewswsesese
neneeeswnenwneneeseswneneeneswwnene
seneswswswswswnwseneseseswswswseesewsee
neesenenenweeesweenwww
wseswwswewswwwswwwswwwwwnwnewsw
swnwswneswswswswswseswswswseseswsweswsw
seswseswswswsesweseswwenwswsesw
sewseseseseseeseseenewsesesesesesesene
sewsesesesesenesenesewseseseeswsesesese
enenenenenenenenenenenenenewnenesene
sewwnesewwwnweneeewnwwww
enwswewswwnwnwnwnwwnwswwnwnwenwnwenw
wwwweeswnwwsenwsenwnwwswnwenwwnw
nwnwneneeneseenenwwneswnenwwswnenwneenw
nwnwwwnwswnwwnwwweneswew
wnwnwwwsesenwnwwwnwnwnwwnwnwnenwnwne
seswswwsewswneswswnwswsenwneswseswswesw
nwnwnwnenesweswnwnwnenenenenwnwneeswnwnw
newnwsewsewwswswwswwswneewwnew
wwwnwwnwwwsenwwnwwwwewnwwew
seneneswwnewsenwswnesesewnenwsee
wnwnwnenwnenwswnwnwnenweswnwnwnwsenwne
nesenwswneseswnwneswswswsewse
nenenwneseneneeeswnw
eeeweeeeesenweeesenw
wswsenwnweeeswnesenwsesenwwswesww
nenenwsewneswnwnwneenewnenwenenenwne
eeeseeeseeseeeewewseeeee
neeseewseeeeewneeeeeeesenwesw
swewseeneswswswswwnwswswwswswswwnw
swswswswswnwenenewswswseswswswnesw
wneswseneneneenenewnenenene
nwnwswswnwenenwnene
eeeeswneneswwsenweneseeenweene
seseneswswnweswswsenesesew
eesenwnweseeeseeseeeeeseseese
wwwsewnwewwwswswwswwwwwswneww
neseeneneesesesesweeesesewsewsee
nwnwnenwwwnwesenwwnwnwwnwwnwwwnwnw
newseseswseswwesesese
sweenwnewsenwnwwwwwwswe
wnwswneswnewnwwnewnwwwwwwswww
eeeseseseseeeseneeeswweenwnwse
neswswswswnenwswswswwswswswswswseswsww
eeeneseeswneenewnweseeneeeneene
enesenwsesesewseseseseweseseseseseee
wswseenwwnwwnwnwnwwnewenwwwwnw
wnwwwwsewswwswenwwwswwwwsww
nwnwnwnwnwnwnenwnwnwwsenwwsenwnwnwnwnw
seseeswswnwswsenwnesw
swsesesesewseseneswswseeseswsewsesesw
nenewwswewswwnwwsesweswwwswwwsenw
swswswswswseswseseseseswsenweneseswsesesw
wswnewwwwwwnwneseswnewswsewwww
wswnwsweseneseseesesesesesesesesesww
neneneneewneswnenenenenenenenenenenese
wnwnwnwnwneneesenwnwewnwnewsenwnwnw
neneneeneseswenenwneneeenweneene
neeneneneswneneeeswneenenwneeneene
nwnenwnwnwnwnwnwnwsenwnwnwnwnwneswnwnwnese
swwenwnwnwnwswwnwnwnenwnwnwenwweww
wweneeneeneneneneneenene
enwseeswesenwseswee
sewnwswwwsenenenweswswnwnweeeeee
swenwsenenwnwnwwwnwwnwnweenwnwwnwnw
newseneswnwwwwswwwwwwewnwswnw
wwsenwsweesweseeenewsenwnwseee
neneswenwnwneneneneneneneneneneswneswne
seweeesenweeseneesweeeeseseee
nwwwnwwwnwnewwwswwnwsewnwwwwew
nwnenwsenwnwnwnwnwnwwnwnwenwnwnwnwswnwnw
neneweswnenenenene
eeeeseeewenweeeeeneneeee
senenenweswneneneswnee
swnenwswnwnwsenwwnwnwwnwwwwnwewnwenw
eswnwnenenwnenenenwnenwneswnwnenenw
nesenwnwnwnenenenenewwnenwsenenenwswne
wweseswwwenenewnwseeeswenewnwsw
swsesweeeseswnesewnwenwseseneenenwesw
swwswesenwsweswswswswseswseswwswswneswse
ewwnwnwswwwwsenwwnwnwwwnwnewseww
nwnwswswseneswseseseswseewswwseseneswse
newswsweswswneseswswswswswswnenwseswsesew
ewseenwswnwwnwnenwnwneneneeswswenene
seseswswwseseseswswswseswneswswneseswsese
wswesewwwwnewwnwnwesewnwwsesw
nesesesweseeseeeseswesenwenwewse
neneneswnwnenwwsenenenwnwnenwsenwenee
eeeweeeeeeeeweneeeewese
nenwnwwnwwwnwnwwsesewwnwnwnwnwwnww
seseeseesweesesesenweesenweesese
eweenwseeeeeeeeweeeewe
nwneewneneneneneswnewnenenenenenwenene
swswneswwswwwnwwseneseswwsw
neneenwewnwswesesene
seseseswswnwswseswsesesesesewneeswnwse
wswnewnwwnwnwwnwwwwwnwwewswnew
wnenwnwnenenenwneenwnenenenenenesewnesw
nweswenenwwnenwnenenwneseswnenww
swwnwnwswnwseneswsesesweseswneee
seewnwwneseneswseswewnwnwnewwnwwnw
enwseseeenweeseseseee
seswseswseswnenwsenwseswswseswwseseswswsw
seesesesesesesesewsesenenwseseseneesesw
eeeseenwseeeseesewesesesenesese
swsweswswswswswswweswswswswnwseswswswsw
wwnwsweswswwnewwswwswswseswswwww
swswswseneewwswnwwwseeswnwnwswnwswse
ewseeeeeenweeeeeeseeesese
ewwwwswsewwnwswnwwwswwwsenesww
wwswswwnwwwwswwwswewswwwswse
esenwsesesewsesesenweswseseswseeesee
nwnenenenwswnwnwewneseneenenenenenenene
esesesenwwseseseeseenweseseswswe
wwnwwsewwwwwswnwseewwnwww
seneneseenenwwewneneneenewneeneee
nwneenenenwnwneswswnwnenwwneenwnwsene
seseeeweseseseseeneweeeseeesese
nwwnwnwnwnwnwenwnwenwnwwnwswwwsenw
swnwnwenwnwnwnwnwnwsenwnenw
swwseswswswswnenwswswswswswswswswswswsw
newwwnwsewewnwnwsewwnwnwww
eeeeeseenweeeeeene
swwnwnwsenwwnwnwwewewwswnwseew
ewnwnwnenwsesenwnwwswwnewwnwwnewsw
eseswnesewsesenweneseenwweseseese
nwnenwnwswwnwenwwswwwnwnwnwwnwwne
neneeeeeeenweswnee
nwnweswnwswnewswnwsenwweswenenwesw
neenewneewenenenwsee
nenwnenwwnwnenwenwnenwnwnenwnwnesenesew
swswswswnwswswwswswseneswswwswswswswsw
newseeswwseeneeeeeneneneneneswwe
neneneneneswneeewenwwsewnenwnwswswne
eneeneeneneeneeseeeewnesweene
nwnwneswwseswswswneeweenesewnwseswswsw
nwseseswnwseenwsenwwsenwnwnwnwenwwnenew
enenwwswsewwwneeswnewswsewnew
nenwnwnwnwenweswsenwenwnwswnwswswse
eenwwnesesenesesesewsesesewsesew
nwwnwsenwneseneneswneneneswenwsw
nenwnenesenwnenenwnwnwsenesenenenwnenenwnw
seeeewswnwewseneewne
wswwswsweswswswsweswsw
enesenwseseswesenwsenenwswenwsweswsesw
eeswnenwnenenenenwneneweseswne
wwnewwwwwnwewsewwwwwwew
newseseneswnwnwnenwneneweseseewnesw
seeewsenesesweseweeseenwnwesene
nwnwnenenwnwnwnwsenenwnesenenenwnenwnwne
nwwnweswwwwnwenwwnwnwwwweswe
wsewwwwwnwwwsewsenenewwwwwswsw
swneneeneeneswnesewnenewseenesewe
nenwswswswswswswswswswseswwswswswswsw
seseewesweseseeseenweeseseseesenwsw
esewneseseneseseswseswwswseswseseswsese
nwnwnwnwneeweswnenenenwnwenwswseew
wnwenwneenwwnwnwwnwenwsenwwnwnwnw
swswneswswswseswswneswswwswnwswswwew
nwnenesweneeeeneeswnweeeeene
nwswswwswswseseneswswwnewsweswswswsw
wswwwwwewwwe
nenenenesewnenenenenwnenenenwwswnwsene
eeseseenweeeesweeeeewee
wswnwneswnwwsewwswswswwweswseswswew
wsesesewenwswseswseweeswswesesw
senwswseswswseswswnwswnwnesweweenesewse
weneneneeneneswneeeenenwneswswnee
nwnwnwnenwnwenwnenenwwnwsewsewenenwnw
nenenenenewneneneneneneneneneene
eswseswwwwwwwnwswsewweswnewe
wseweenweeneewseeseswesese
wnewenwsweeneenesenesweneeneee
nwnwwnwnwwwnwnwsenwwnewwenwsenww
swneseswswswsenwwenwswwwswswneswwwnew
esenwenwswwswenwswsewnwswswswenw
swnwewneeswswswswswswswnwseseseseesesw
nenewnwnenesenenenesweneneeneneneneenene
neswsewnewswswswwseswswneswwswseswswsw
nwswwnwnwenwnwnwnwnwnwnwnwwnwwnwnw
seseneswnwneswsesenwswnewnwnwsenwewnenene
neneeesesenwneneeeneneeswneeenww
eeesweeswseeseweeeneseeeeenw
seseseeeswwswwneswswwnwnwseeswese
swnwnwenwnenenwnwneenenwnenwnwnenenwswsene
wwsenewnwwnwwwwwwwsenwswnwwww
enenewnwswseeneseewneseseswesesee
nwwwswsewwnwwnwwwwswswswseswswe
wseswwseswnwseeseseeseseseseeswne
enwsesweeeeeneeeeeeeeeenw
seseeseseseeseswsesenwweeseenesenwsesw
senwneseseseswseswseswseswnwsesesewsesesese
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
