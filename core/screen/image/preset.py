from core.path.manager import PathConfig
from core.resource.loader import ResourceAutoLoader
from core.screen.image.variable import ImageProfile
from core.ui_layout.name.identifiers import LayoutName
from core.ui_layout.scale.preset.menu import ScaleMenuVar


def P(path, **kwargs):
    return ImageProfile(path = path, **kwargs)

IMAGE_RESOURCE_MAP = {
    # --- 背景類 ---
    LayoutName.MENU_BG:          P(PathConfig.bg1),
    LayoutName.SINGLE_BG:        P(PathConfig.bg1),
    LayoutName.SINGLE_MENU_BG:   P(PathConfig.bg1),
    LayoutName.DOUBLE_BG:        P(PathConfig.bg1),
    LayoutName.ENDLESS_BG:       P(PathConfig.bg1),
    LayoutName.SYS_CONFIG_BG:    P(PathConfig.bg1),
    LayoutName.HELP_BG:          P(PathConfig.bg1),
    LayoutName.RANK_BG:          P(PathConfig.bg1),

    # --- UI 類 ---
    LayoutName.MENU_BT_BOARD:    P(
        PathConfig.sprite_bt_board,
        is_sprite_sheet = True,
        frame_count = ScaleMenuVar.BT_BOARD_WH_QUANTITY * ScaleMenuVar.BT_BOARD_WH_QUANTITY - 1,
        frame_row = ScaleMenuVar.BT_BOARD_WH_QUANTITY,
        frame_col = ScaleMenuVar.BT_BOARD_WH_QUANTITY
    ),

    LayoutName.GAME_CLOCK:       P(PathConfig.img_clock),
    LayoutName.GAME_BOARD:       P(PathConfig.img_board),
    LayoutName.RANK_UNDERLINE:   P(PathConfig.img_ranking),
    LayoutName.RANK_FRAME:       P(PathConfig.img_frame),
    LayoutName.HELP_LACE:        P(PathConfig.img_lace),
    LayoutName.HELP_PANEL:       P(PathConfig.img_panel),
}


# 執行自動加載(將 IMAGE_RESOURCE_MAP 傳進去，Loader 會直接修改這個字典)
loader = ResourceAutoLoader(IMAGE_RESOURCE_MAP)
loader.load_all()
