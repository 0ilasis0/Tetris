from dataclasses import dataclass

from core.ui_layout.scale.preset.base import ScaleFont
from core.variable import Size


@dataclass
class ScaleRank:
    under_line_size: Size = Size(1483, 618)
    frame_size: Size = Size(1492, 804)
    ranking_size: Size = Size(int(ScaleFont.nor * 3 * 1.5), int(ScaleFont.nor * 1.5))
    min_size: Size = Size(ScaleFont.nor * 2, ScaleFont.nor)
    sec_size: Size = min_size
    fraction_size: Size = Size(ScaleFont.nor * 3, ScaleFont.nor)

    gap_y: Size = 35
    ranking_gap_x: int = 8
    ranking_gap_y: int = gap_y * 1.2
    min_gap_x: int = 185
    sec_gap_x: int = 315
    fraction_gap_x: int = 495
