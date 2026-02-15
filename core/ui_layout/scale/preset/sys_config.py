from dataclasses import dataclass
from enum import IntEnum

from core.hmi.config.variable import ConfigVar
from core.ui_layout.scale.preset.base import ScaleFont, ScaleZoom
from core.variable import Size


class ScaleSysConfigVar(IntEnum):
    main_quantity = 3

@dataclass
class ScaleSysConfig:
    main_size: Size = Size(ScaleFont.x2nor * 5, ScaleFont.x2nor * ScaleSysConfigVar.main_quantity)
    song_name_size: Size = Size(8 * ScaleZoom.x2nor, ConfigVar.HEIGHT_BLOCK * ScaleZoom.x2nor)
    song_block_size: Size = Size(ConfigVar.WIDTH_BLOCK * ScaleZoom.x2nor, ConfigVar.HEIGHT_BLOCK * ScaleZoom.x2nor)
    window_scale_size: Size = Size(ScaleFont.x2nor * 4, ScaleFont.x2nor)
    user_size: Size = Size(main_size.width, ScaleZoom.x2nor * 1.2)
    window_scale_gap_y: int = 6
    main_gap_x: int = song_name_size.width // 2 * (-1)
    user_gap_x: int = 16
    user_gap_y: int = 8
    block_gap_y: int = 20
    gap_y: int = ScaleZoom.nor
    gap_x: int = ScaleZoom.nor
