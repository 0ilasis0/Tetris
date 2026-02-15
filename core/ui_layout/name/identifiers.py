from enum import Enum
from typing import TYPE_CHECKING

from core.debug import dbg
from core.ui_layout.name.registry import LayoutNameLoader, LayoutNameRegistry
from core.variable import PageTable


class LayoutName(str, Enum):
    '''
    一般 static_name ： 直接用 LayoutName.name 取出名稱
    大量dynaic_name ： 使用 get_name 取出名稱
    '''
    # 這段 '給 VS Code 看的' 宣告，實際不會跑
    if TYPE_CHECKING:
        serial_list: list[str]
        count: int

    def __new__(cls, content, count = 1):
        '''
        自定義的 Enum，支援自動產生序列名稱
        定義格式: 名稱 = ('字串值', 數量)
        如果沒有寫數量，預設為 1
        '''
        # 建立字串物件 (這一步保證了它依然是 str)
        obj = str.__new__(cls, content)

        # 設定 Enum 的實際值 (必須是字串)
        obj._value_ = content

        # 將數量存為這個成員的屬性
        obj.count = count

        # 順便直接生成 list 存起來，這樣以後直接讀屬性就好，不用再運算
        if count > 1:
            obj.serial_list = [f'{content}_{i}' for i in range(count)]
        else:
            obj.serial_list = [content]

        return obj

    @staticmethod
    def get_name(page: PageTable, index: int = 0, *path_parts) -> str | None:
        '''
        單一名稱尋找(用於非static_name)
        自動拼字 + 自動去 Registry 查證
        '''
        # 處理參數 (把 Enum 轉字串，組合成 Group Key)
        # 例如: 1, ARCH -> '1_ARCH'
        str_parts = [p.value if isinstance(p, Enum) else str(p) for p in path_parts]
        cat_name = '_'.join(str_parts)

        # 呼叫自己的拼字邏輯
        # 產生 'SINGLE_1_ARCH_0'
        target_name = LayoutNameLoader.create_name(page, (cat_name, index))

        # 去 Registry 確認
        if LayoutNameRegistry.exists(target_name):
            return target_name

        dbg.war(f'the {target_name} is not registered.')
        return None


    ''' --- 定義區域 ---  '''
    # BASE
    BASE_NUMBER_BIG         = ('BASE_NUMBER_BIG', 2)

    # BACKGROUND
    MENU_BG                 = 'MENU_BG'
    SINGLE_BG               = 'SINGLE_BG'
    SINGLE_MENU_BG          = 'SINGLE_MENU_BG'
    DOUBLE_BG               = 'DOUBLE_BG'
    ENDLESS_BG              = 'ENDLESS_BG'
    SYS_CONFIG_BG           = 'SYS_CONFIG_BG'
    HELP_BG                 = 'HELP_BG'
    RANK_BG                 = 'RANK_BG'

    # MENU
    MENU_BT_BOARD           = 'MENU_BT_BOARD'
    MENU_MAIN               = 'MENU_MAIN'
    MENU_USER               = 'MENU_RECT'

    # GAME
    SINGLE_MENU_MAIN        = 'SINGLE_MENU_MAIN'
    SINGLE_MENU_USER        = 'SINGLE_MENU_USER'
    SINGLE_MENU_RECT        = ('SINGLE_MENU_RECT', 10)
    SINGLE_MENU_LEVEL       = ('SINGLE_MENU_LEVEL', 10)

    GAME_MAIN               = ('GAME_MAIN', 2)
    GAME_SLOT               = ('GAME_SLOT', 2)
    GAME_COMBO              = ('GAME_COMBO', 2)
    GAME_SCORE              = ('GAME_SCORE', 2)
    GAME_COMBO_NUMBER       = ('GAME_COMBO_NUMBER', 2)
    GAME_CLOCK              = 'GAME_CLOCK'
    GAME_CLOCK_MIN          = ('GAME_CLOCK_MIN', 2)
    GAME_CLOCK_SEC          = ('GAME_CLOCK_SEC', 2)
    GAME_KO                 = ('GAME_KO', 2)
    GAME_BOARD              = 'GAME_BOARD'
    GAME_TARGET_TIME        = 'GAME_TARGET_TIME'
    GAME_TARGET_SCORE       = 'GAME_TARGET_SCORE'

    # SYS_CONFIG
    SYS_SONG_MAIN           = 'SYS_SONG_MAIN'
    SYS_SONG_USER           = 'SYS_SONG_RECT'
    SYS_SONG_NAME           = 'SYS_SONG_NAME'
    SYS_SONG_BLOCK          = 'SYS_SONG_BLOCK'
    SYS_WINDOW_SCALE        = 'SYS_WINDOW_SCALE'

    # HELP
    HELP_PANEL              = 'HELP_PANEL'
    HELP_LACE               = 'HELP_LACE'
    HELP_OPTION_TITLE       = 'HELP_OPTION_TITLE'
    HELP_OPTION_DESC        = 'HELP_OPTION_DESC'

    # RANK
    RANK_UNDERLINE          = 'RANK_UNDERLINE'
    RANK_FRAME              = 'RANK_FRAME'
    RANK_RANKING            = 'RANK_RANKING'
    RANK_SEC                = 'RANK_SEC'
    RANK_MIN                = 'RANK_MIN'
    RANK_FRACTION           = 'RANK_FRACTION'
