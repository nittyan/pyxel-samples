import random

from typing import Dict
from typing import Tuple

import pyxel

from core.color import Color

WINDOW_WIDTH = 200
WINDOW_HEIGHT = 200


class App:
    """
    see http://amagame.blog12.fc2.com/blog-entry-1989.html
    """

    def __init__(self):
        pyxel.init(WINDOW_WIDTH, WINDOW_HEIGHT, caption='crate_random_2d_map', fps=2)
        self._count = 0
        self._map = dict()
        self._color_map: Dict[int, Color] = {0: Color.AQUA, 1: Color.FLESH, 2: Color.GREEN, 3: Color.BROWN, 4: Color.GRAY}
        self._init_map()

        pyxel.mouse(True)
        pyxel.run(self.update, self.draw)

    def _init_map(self):
        for x in range(0, WINDOW_WIDTH - 1, 2):
            for y in range(0, WINDOW_HEIGHT - 1, 2):
                color = random.randint(0, 4)
                self._map[(x, y)] = self._color_map[color]
                if x == 0 or x == 198 or y == 0 or y == 198:
                    self._map[(x, y)] = Color.AQUA

    def update(self):
        if self._count < 200:
            self._map = self._copy()
            self._map = self._encroachment()
            self._count += 1

    def _copy(self) -> Dict[Tuple[int, int], int]:
        next_frame = dict()
        for x in range(0, WINDOW_WIDTH - 1, 2):
            for y in range(0, WINDOW_HEIGHT - 1, 2):
                if x == 0 or x == 198 or y == 0 or y == 198:
                    next_frame[(x, y)] = Color.AQUA
                    continue

                candidates = []
                if (x - 2, y) in self._map:
                    # 左
                    candidates.append(self._map[(x - 2, y)])
                if (x + 2, y) in self._map:
                    # 右
                    candidates.append(self._map[(x + 2, y)])
                if (x, y - 2) in self._map:
                    # 上
                    candidates.append(self._map[(x, y - 2)])
                if (x, y + 2) in self._map:
                    # 下
                    candidates.append(self._map[(x, y + 2)])
                next_frame[(x, y)] = random.choice(candidates)
        return next_frame

    def _encroachment(self) -> Dict[Tuple[int, int], int]:

        next_frame = dict()
        for x in range(0, WINDOW_WIDTH - 1, 2):
            for y in range(0, WINDOW_HEIGHT - 1, 2):
                if x == 0 or x == 198 or y == 0 or y == 198:
                    next_frame[(x, y)] = Color.AQUA
                    continue

                candidates = []
                if (x - 2, y) in self._map:
                    # 左
                    candidates.append(self._map[(x - 2, y)])
                if (x + 2, y) in self._map:
                    # 右
                    candidates.append(self._map[(x + 2, y)])
                if (x, y - 2) in self._map:
                    # 上
                    candidates.append(self._map[(x, y - 2)])
                if (x, y + 2) in self._map:
                    # 下
                    candidates.append(self._map[(x, y + 2)])

                compressed = set(candidates)
                if len(compressed) == 1:
                    next_frame[(x, y)] = list(compressed)[0]
                else:
                    next_frame[(x, y)] = self._map[(x, y)]

        return next_frame

    def draw(self):
        for x in range(0, WINDOW_WIDTH - 1, 2):
            for y in range(0, WINDOW_HEIGHT - 1, 2):
                color = self._map[(x, y)]
                pyxel.rect(x, y, x + 1, y + 1, color.value)


App()
