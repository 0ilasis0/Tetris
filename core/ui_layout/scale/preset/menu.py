from dataclasses import dataclass
from enum import IntEnum

from core.ui_layout.scale.preset.base import ScaleFont
from core.variable import Size


class ScaleMenuVar(IntEnum):
    MAIN_QUANTITY = 7
    BT_BOARD_WH_QUANTITY = 5

@dataclass
class ScaleMenu:
    main_size: Size = Size(ScaleFont.nor * 7, ScaleFont.x2nor * ScaleMenuVar.MAIN_QUANTITY)
    user_size: Size = Size(main_size.width * 1.4, main_size.height // ScaleMenuVar.MAIN_QUANTITY * 1.1)
    bt_board_size: Size = Size(1200 // ScaleMenuVar.BT_BOARD_WH_QUANTITY, 1200 // ScaleMenuVar.BT_BOARD_WH_QUANTITY)
    gap_y: int = 5
    gap_x: int = 50 * (-1)
