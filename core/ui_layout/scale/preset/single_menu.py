from dataclasses import dataclass

from core.tetris_game.variable import GameVar
from core.variable import Size


@dataclass
class ScaleSingleMenu:
    block_size: Size = Size(128, 128)
    main_size: Size = Size(
        block_size.width * (GameVar.SINGLE_MENU_WIDTH_BLOCK * 2 - 1),
        block_size.height * (GameVar.SINGLE_MENU_HEIGHT_BLOCK * 2 - 1)
    )
    number_size: Size = Size(60, 60)
    gap: int = block_size.width * 2
