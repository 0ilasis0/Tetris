from enum import Enum

from core.font.variable import TextProfile
from core.path.manager import JsonFileID, PathConfig
from core.ui_layout.name.identifiers import LayoutName
from core.variable import Color, PageTable


class TextID(Enum):
    ''' 靜態物件使用 '''
    # SYS_CONFIG
    SYS_SONG_NAME = TextProfile(
        name        = LayoutName.SYS_SONG_NAME,
        content     = "{}",
        color       = Color.BLACK.value,
    )
    SYS_WINDOW_SCALE = TextProfile(
        name        = LayoutName.SYS_WINDOW_SCALE,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # SINGLE
    GAME_TARGET_TIME = TextProfile(
        name        = LayoutName.GAME_TARGET_TIME,
        content     = "在時間內{}:{}完成",
        color       = Color.BLACK.value,
    )
    GAME_TARGET_SCORE = TextProfile(
        name        = LayoutName.GAME_TARGET_SCORE,
        content     = "分數達到{}以上",
        color       = Color.BLACK.value,
    )

    # RANK
    RANK_RANKING = TextProfile(
        name        = LayoutName.RANK_RANKING,
        content     = "第{}名",
        color       = Color.ORANGE.value,
    )
    RANK_MIN = TextProfile(
        name        = LayoutName.RANK_MIN,
        content     = "分：{}",
        color       = Color.BLACK.value,
    )
    RANK_SEC = TextProfile(
        name        = LayoutName.RANK_SEC,
        content     = "秒：{}",
        color       = Color.BLACK.value,
    )
    RANK_FRACTION = TextProfile(
        name        = LayoutName.RANK_FRACTION,
        content     = "分數： {}",
        color       = Color.BLACK.value,
    )



    ''' 需動態自行導入物件 '''
    # SINGLE_MENU
    SINGLE_MENU_LEVEL_STYLE = TextProfile(
        name    = None,
        content = "{}",
        color   = Color.BLACK.value,
    )

    # GAME
    GAME_SCORE = TextProfile(
        name        = None,
        content     = "SCORE: {}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_COMBO = TextProfile(
        name        = None,
        content     = "COMBO: {}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng1
    )
    GAME_KO = TextProfile(
        name        = None,
        content     = "KO {}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_CLOCK_SEC = TextProfile(
        name        = None,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )
    GAME_CLOCK_MIN = TextProfile(
        name        = None,
        content     = "{}",
        color       = Color.BLACK.value,
        font        = PathConfig.font_eng2
    )


    ''' JSON提取區 '''
    # MENU
    MENU_MAIN = TextProfile(
        name        = LayoutName.MENU_MAIN,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # SYS_CONFIG
    SYS_SONG_MAIN = TextProfile(
        name        = LayoutName.SYS_SONG_MAIN,
        content     = "{}",
        color       = Color.BLACK.value,
    )

    # HELP
    HELP_DYNAMIC_TITLE = TextProfile(
        name    = LayoutName.HELP_OPTION_TITLE,
        content = "{}",
        color   = Color.BLACK.value,
    )
    HELP_DYNAMIC_DESC = TextProfile(
        name    = LayoutName.HELP_OPTION_DESC,
        content = "{}",
        color   = Color.BLACK.value,
    )


# 改這邊的路徑，必須同步JSON裡面的dict路徑喔
class TextJson:
    """
    建立 TextID 到 JSON 路徑的直接映射
    Key: TextID
    Value: (JSON_Key_Layer1, JSON_Key_Layer2...)
    """
    mapping = {
        # MENU
        TextID.MENU_MAIN: (JsonFileID.DISPLAY, PageTable.MENU.value, "title"),

        TextID.SYS_SONG_MAIN: (JsonFileID.DISPLAY, PageTable.SYS_CONFIG.value, "title"),

        TextID.HELP_DYNAMIC_TITLE: [
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.SINGLE.value, "title"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.DOUBLE.value, "title"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.ENDLESS.value, "title")
        ],
        TextID.HELP_DYNAMIC_DESC: [
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.SINGLE.value, "description"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.DOUBLE.value, "description"),
            (JsonFileID.DISPLAY, PageTable.HELP.value, PageTable.ENDLESS.value, "description")
        ],
    }
