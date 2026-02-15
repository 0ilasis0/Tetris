from dataclasses import dataclass


@dataclass
class ScaleMapGrid:
    start_x: int = 0
    start_y: int = 0
    cell_w: int = 15
    cell_h: int = 15
    x2cell_w: int = cell_w * 2
    x2cell_h: int = cell_h * 2

@dataclass
class ScaleFont:
    plus: int = 57
    nor: int = 38
    x2nor: int = nor * 2
    mini: int = 19

@dataclass
class ScaleZoom:
    plus: int = 128
    mini: int = 16
    nor: int = 32
    x2nor: int = nor * 2

@dataclass
class ScaleDraw:
    hollow: int = 5
