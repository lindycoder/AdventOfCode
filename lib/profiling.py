import logging
import time
from functools import partial
from typing import Iterable, Callable

_default_reporter = partial(logging.warn,
                            'Looped %s times; avg %s loops / seconds')


def reporting(iterator: Iterable,
              every: int = 100,
              reporter: Callable[[int, int], None] = _default_reporter):
    loops = 0
    start = time.time()
    for item in iterator:
        yield item

        loops += 1
        if loops % every == 0:
            seconds = time.time() - start

            reporter(loops, int(loops / seconds))
