from enum import Enum

from core.hmi.config.variable import ConfigVar
from core.screen.draw.variable import DrawProfile, DrawShape
from core.tetris_game.variable import GameVar
from core.ui_layout.name.identifiers import LayoutName
from core.ui_layout.scale.manager import location_config
from core.variable import Color


class DrawID(Enum):
    # MENU
    MENU_USER = DrawProfile(
        name = LayoutName.MENU_USER,
        color = Color.DEEP_RED.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )

    # SINGLE_MENU
    SINGLE_MENU_USER = DrawProfile(
        name = LayoutName.SINGLE_MENU_USER,
        color = Color.HOT_PINK.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )

    # SYS_CONFIG
    SYS_SONG_USER = DrawProfile(
        name = LayoutName.SYS_SONG_USER,
        color = Color.DEEP_RED.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow,
    )
    SYS_SONG_BLOCK_CELL = DrawProfile(
        name = LayoutName.SYS_SONG_BLOCK,
        color = Color.DEEP_BLUE.value,
    )
    SYS_SONG_BLOCK_GRID = DrawProfile(
        name = LayoutName.SYS_SONG_BLOCK,
        color = Color.BLACK.value,
        width_block = ConfigVar.WIDTH_BLOCK,
        height_block = ConfigVar.HEIGHT_BLOCK,
        zoom_factory = lambda: location_config.sys_config.song_block_size.width // ConfigVar.WIDTH_BLOCK
    )



    ''' 需動態自行導入物件 '''
    # SINGLE_MENU
    SINGLE_MENU_RECT = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        shape = DrawShape.RECT,
        hollow_factory = lambda: location_config.draw.hollow
    )

    # GAME
    GAME_MAIN_CELLS = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        zoom_factory = lambda: location_config.zoom.nor
    )
    GAME_SLOT_CELLS = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        zoom_factory = lambda: location_config.zoom.nor
    )
    GAME_MAIN = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        width_block = GameVar.WIDTH_BLOCK,
        height_block = GameVar.HEIGHT_BLOCK,
        zoom_factory = lambda: location_config.zoom.nor
    )
    GAME_SLOT = DrawProfile(
        name = None,
        color = Color.BLACK.value,
        width_block = GameVar.CELL_BLOCK,
        height_block = GameVar.CELL_BLOCK,
        zoom_factory = lambda: location_config.zoom.nor
    )

