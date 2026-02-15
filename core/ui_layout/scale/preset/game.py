from dataclasses import dataclass

from core.tetris_game.variable import GameVar
from core.ui_layout.scale.preset.base import ScaleFont, ScaleZoom
from core.ui_layout.variable import PosZLayer
from core.variable import PosField, Position, Size

@dataclass
class ScaleGameS:
    main_size: Size = Size(GameVar.WIDTH_BLOCK * ScaleZoom.nor, GameVar.HEIGHT_BLOCK * ScaleZoom.nor)
    slot_size: Size = Size(GameVar.CELL_BLOCK * ScaleZoom.nor, GameVar.CELL_BLOCK * ScaleZoom.nor)

    combo_size: Size = Size(304, ScaleFont.nor)
    score_size: Size = Size(304, ScaleFont.nor)
    combo_number_size: Size = Size(ScaleFont.nor * 2, ScaleFont.nor)
    score_number_size: Size = Size(ScaleFont.nor * 2, ScaleFont.nor)
    ko_size: Size = Size(ScaleFont.nor, ScaleFont.nor)
    board_size: Size = Size(470, 476)
    clock_size: Size = Size(240, 216)
    clock_number_size: Size = Size(ScaleFont.x2nor, ScaleFont.x2nor)
    target_time_size: Size = Size(ScaleFont.plus * 10, ScaleFont.plus)
    target_score_size: Size = Size(ScaleFont.plus * 7, ScaleFont.plus)

    gap_x: int = 25
    gap_y: int = 32
    x2gap_x: int = gap_x * 2
    x2gap_y: int = gap_x * 2
    ko_gap_x: int = 44
    ko_gap_y: int = 32
    board_gap_x: int = 250 * (-1)
    board_gap_y: int = 120
    target_gap_x: int = 50 * (-1)
    target_gap_y: int = 50

@dataclass
class ScaleGameD:
    main_size: Size = ScaleGameS.main_size
    main_pos: Position = PosField(200, 180, PosZLayer.MAIN.value)

    combo_size: Size = ScaleGameS.combo_size
    score_size: Size = ScaleGameS.score_size
    combo_number_size: Size = ScaleGameS.combo_number_size
    score_number_size: Size = ScaleGameS.score_number_size
    ko_size: Size = ScaleGameS.ko_size
    slot_size: Size = ScaleGameS.slot_size
    clock_size: Size = ScaleGameS.clock_size
    clock_number_size: Size = ScaleGameS.clock_number_size

    gap_x: int = ScaleGameS.gap_x
    gap_y: int = ScaleGameS.gap_y
    d2x3gap_y: int = ScaleGameS.gap_y // 2 * 3
    x2gap_x: int = gap_x * 2
    x2gap_y: int = gap_y * 2
    ko_gap_x: int = 44
    ko_gap_y: int = 32
    gap_y_player1: int = 320
    gap_x_slot2: int = 260
