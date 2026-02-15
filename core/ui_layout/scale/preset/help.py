from dataclasses import dataclass

from core.ui_layout.scale.preset.base import ScaleFont
from core.variable import Size


@dataclass
class ScaleHelp:
    panel_size: Size = Size(1457, 136)
    panel_gap_y: int = 648
    lace_size: Size = Size(1188, 632)
    lace_gap_y: int = 180
    option_title_size: Size = Size(ScaleFont.nor * 4, ScaleFont.nor)
    option_desc_size: Size = Size(ScaleFont.nor * 20, ScaleFont.nor * 10)
    desc_gap_x: int = 90
    desc_gap_y: int = desc_gap_x
    title_gap_x: int = panel_size.width // 6 - option_title_size.width // 2 - 4
    title_gap_y: int = 24
    title_gap_y_plus: int = panel_size.width // 3 + 8
