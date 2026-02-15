from enum import Enum

import pygame

from core.variable import Color

#  0 0 0 0
#  0 0 0 0
#  0 0 0 0
#  0 0 0 0

figures = {
    "I": {
        "rotations": [[2, 6, 10, 14], [4, 5, 6, 7]],
        "color": Color.DEEP_GREEN.value
    },
    "Z": {
        "rotations": [[1, 2, 6, 7], [2, 5, 6, 9]],
        "color": Color.DEEP_BLUE.value
    },
    "S": {
        "rotations": [[6, 7, 9, 10], [2, 6, 7, 11]],
        "color": Color.PURPLE.value
    },
    "J": {
        "rotations": [[2, 3, 6, 10], [5, 6, 7, 11], [3, 7, 10, 11], [1, 5, 6, 7]],
        "color": Color.DARK_BROWN.value
    },
    "L": {
        "rotations": [[2, 3, 7, 11], [3, 5, 6, 7], [2, 6, 10, 11], [5, 6, 7, 9]],
        "color": Color.CYAN.value
    },
    "T": {
        "rotations": [[2, 5, 6, 7], [2, 6, 7, 10], [5, 6, 7, 10], [3, 6, 7, 11]],
        "color": Color.MAGENTA.value
    },
    "O": {
        "rotations": [[2, 3, 6, 7]],
        "color": Color.SKY_BLUE.value
    },
}



class BaseVar:
    NUMBER_MAX = 1000

class GameState(Enum):
    START       = 'start'
    KO          = 'ko'
    GAMEOVER    = 'gameover'
    WIN         = 'win'

class GameVar:
    GAME_LEVEL_COL = 5
    GAME_LEVEL_ROW = 2
    GAME_LEVEL_PAGE = 1
    GAME_LEVEL_ALL = GAME_LEVEL_COL * GAME_LEVEL_ROW * GAME_LEVEL_PAGE

    # SIZE AND BOLCK
    WIDTH_BLOCK     = 10
    HEIGHT_BLOCK    = 20
    CELL_BLOCK      = 4

    # COLORS
    EMPTY_COLOR = Color.WHITE.value
    RAISE_COLOR = Color.GREY.value
    MINE_COLOR  = Color.GOLD.value
    GRID_COLOR  = Color.BLACK.value

    # GAME
    MAX_KO_COUNT    = 3
    MAX_COMBO       = 20
    MAX_SCORE       = BaseVar.NUMBER_MAX

    # SYS_BASE
    DROP_CLOCK  = 0.5

    # OTHER
    SINGLE_MENU_WIDTH_BLOCK     = 5
    SINGLE_MENU_HEIGHT_BLOCK    = 2


class RankVar:
    RANK_TOTAL = 3
    DATA_TOTAL = 4

# 設定遊戲 FPS
clock = pygame.time.Clock()
