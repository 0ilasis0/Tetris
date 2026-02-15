from enum import Enum

from core.tetris_game.variable import GameVar


class LevelVar(Enum):
    DROP_CLOCK = "drop_clock"
    RAISE_LINE = "raise_lines"
    RAISE_INTERVAL = "raise_interval"
    MIN = "min"
    SEC = "sec"
    FRACTION = "fraction"

class LevelConfig:
    MAX_LEVEL = 10 - 1
    LEVEL_INTERVAL = 20

    # ENDLESS
    difficult_table = {
        0:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 1.0,     LevelVar.RAISE_LINE: 0,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 14},
        1:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.9,     LevelVar.RAISE_LINE: 0,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 14},
        2:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.9,     LevelVar.RAISE_LINE: 1,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 14},
        3:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.8,     LevelVar.RAISE_LINE: 1,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 12},
        4:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.7,     LevelVar.RAISE_LINE: 1,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 12},
        5:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.6,     LevelVar.RAISE_LINE: 1,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 10},
        6:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.8,     LevelVar.RAISE_LINE: 2,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 14},
        7:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.8,     LevelVar.RAISE_LINE: 2,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 12},
        8:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.6,     LevelVar.RAISE_LINE: 2,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 12},
        9:  {LevelVar.DROP_CLOCK: GameVar.DROP_CLOCK * 0.5,     LevelVar.RAISE_LINE: 2,     LevelVar.RAISE_INTERVAL: GameVar.DROP_CLOCK * 10},
    }

    level_table_endless = {
        0: 0,
        30: 1,
        60: 2,
        90: 3,
        120: 4,
        150: 5,
        180: 6,
        210: 7,
        240: 8,
        270: 9,
    }


    # SINGLE
    level_table_single = {
        0:  {LevelVar.FRACTION: 10,     LevelVar.MIN: 3,     LevelVar.SEC: 0},
        1:  {LevelVar.FRACTION: 20,     LevelVar.MIN: 2,     LevelVar.SEC: 40},
        2:  {LevelVar.FRACTION: 30,     LevelVar.MIN: 2,     LevelVar.SEC: 20},
        3:  {LevelVar.FRACTION: 40,     LevelVar.MIN: 2,     LevelVar.SEC: 0},
        4:  {LevelVar.FRACTION: 50,     LevelVar.MIN: 1,     LevelVar.SEC: 40},
        5:  {LevelVar.FRACTION: 50,     LevelVar.MIN: 1,     LevelVar.SEC: 30},
        6:  {LevelVar.FRACTION: 30,     LevelVar.MIN: 0,     LevelVar.SEC: 50},
        7:  {LevelVar.FRACTION: 50,     LevelVar.MIN: 1,     LevelVar.SEC: 20},
        8:  {LevelVar.FRACTION: 60,     LevelVar.MIN: 1,     LevelVar.SEC: 20},
        9:  {LevelVar.FRACTION: 300,     LevelVar.MIN: 30,     LevelVar.SEC: 0},
    }
