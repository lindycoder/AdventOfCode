import sys
from pprint import pprint
from typing import List, Tuple

import pytest
from hamcrest import assert_that, is_


def compute(data, target=2020):
    n1, n2 = find_adders(parse_input(data), target)
    return n1 * n2


def parse_input(data):
    numbers = sorted(map(int, data.strip().splitlines()))
    return numbers


def find_adders(numbers: List[int], target: int) -> Tuple[int, int]:
    low_nums = iter(numbers)
    low = next(low_nums)
    high_nums = iter(reversed(numbers))
    high = next(high_nums)
    while True:
        if low + high == target:
            return low, high
        elif low + high > target:
            high = next(high_nums)
        else:
            low = next(low_nums)


def compute2(data, target=2020):
    numbers = parse_input(data)

    for number in numbers:
        try:
            adders = find_adders(numbers, target - number)
        except StopIteration:
            pass
        else:
            n1, n2 = adders
            return number * n1 * n2




@pytest.mark.parametrize('val,expect', [
    ("""\
1721
979
366
299
675
1456
""",
     514579)
])
def test_v1(val, expect):
    assert_that(compute(val), is_(expect))

@pytest.mark.parametrize('val,expect', [
    ("""\
1721
979
366
299
675
1456
""",
     241861950)
])
def test_v2(val, expect):
    assert_that(compute2(val), is_(expect))


puzzle_input = """\
261
1773
1839
1551
1781
1276
1372
1668
1823
1870
1672
1821
1327
1902
1949
1389
1720
1437
1716
1360
1893
1410
1881
1927
1639
1514
1753
1625
1249
1696
1698
1699
2004
1742
1903
473
1948
1830
1973
2005
1468
1824
1809
1493
2009
1848
1306
1519
1618
1905
1402
1705
1910
1609
1571
1557
1420
608
1471
1383
1442
1447
1985
1486
1629
1450
1767
1407
1626
1623
1467
1224
1269
1325
1674
1945
1733
1913
1451
1853
1875
405
1500
1634
1570
1868
1510
1069
1296
1852
1287
1274
832
1373
1142
1838
1854
1480
1628
1632
1597
1761
1717
1684
1956
1351
1622
1941
1704
1926
1873
1393
1850
1898
1960
1673
1736
1901
1806
1768
1670
1989
1214
1851
1715
1461
1277
951
1482
1464
1883
1976
1602
1606
1258
1801
1593
1332
1386
1309
1388
1762
1533
1805
1462
375
1555
1357
1578
1552
1473
1834
1262
1466
1925
1955
1575
1975
1964
1440
1667
1922
1454
1813
1968
1836
1982
1326
1811
900
1588
1529
1997
1345
1859
1458
1764
1509
1397
1237
1627
1564
1814
1842
1679
1289
1957
1819
801
1350
1841
1803
1718
1966
1272
1636
1352
1496
1455
1488
"""

if __name__ == '__main__':
    if sys.argv[1] == "2":
        result = compute2(puzzle_input)
    else:
        result = compute(puzzle_input)

    print(f"Result is {result}")
