from core.ui_layout.main import layout_mg
from core.ui_layout.name.identifiers import LayoutName
from core.variable import PageTable, Position


class GridParameter:
    SINGLE_MENU_LEVEL_ROW = 2
    SINGLE_MENU_LEVEL_COLS = 5

class GridThing:
    LOCK_SWITCH_ = 'lock_switch'
    LOCK = 'lock'
    UNLOCK = 'unlock'

class HelpConfig:
    # hook_x 透明度矩陣
    # 例：title_alpha[hook_x][item_index] 表示對應透明度
    title_alpha = [
        [100, 20, 20],
        [20, 100, 30],
        [20, 20, 100],
    ]

class RankConfig:
    @classmethod
    def reload_setup(cls):
        cls.rank_underline = layout_mg.get_item_size(PageTable.RANK, LayoutName.RANK_UNDERLINE)

        cls.extra_pos = {
            0: Position(0, 0, 0),
            1: Position(cls.rank_underline.width * 12 // 44, cls.rank_underline.height * 19 // 49, 0),
            2: Position(cls.rank_underline.width * 26 // 46, cls.rank_underline.height * 21 // 26, 0),
        }
