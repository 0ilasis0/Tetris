import sys
from dataclasses import dataclass
from pathlib import Path

from core.path.variable import JsonFileID, MixPath

PATH_ROOT = Path(__file__).resolve().parent.parent.parent

def resource_path(*paths):
    """
    取得外部資源路徑：
    - 打包成 exe 時：使用 exe 同目錄
    - 開發模式：使用專案根目錄
    """
    if getattr(sys, "frozen", False):
        # exe 打包後使用的路徑
        base_path = Path(sys.executable).parent
    else:
        # 開發環境使用的路徑
        base_path = PATH_ROOT
    return base_path.joinpath(*paths)

@dataclass(frozen = True)
class PathBase:
    background = resource_path("background")
    img        = resource_path("img")
    sprite     = resource_path("sprite")
    pattern    = resource_path("img", "pattern")
    icon       = resource_path("images.ico")
    json       = resource_path("data")
    song       = resource_path("song")
    font       = resource_path("font")
    core       = resource_path("core")



@dataclass(frozen = True)
class PathConfig:
    bg1         = PathBase.background / "bg_menu.jpg"
    img_clock   = PathBase.img / "clock.jpg"
    img_panel   = [
        PathBase.img / "panel1.png",
        PathBase.img / "panel2.png",
        PathBase.img / "panel3.png"
    ]
    img_lace        = PathBase.img / "lace.png"
    img_ranking     = PathBase.img / "ranking.png"
    img_frame       = PathBase.img / "frame.png"
    img_square      = PathBase.img / "square.png"
    img_board       = PathBase.img / "board.png"

    progress_bar    = PathBase.img / "progress_bar.png"
    faction_bar     = PathBase.img / "faction_bar.png"

    sprite_bt_board = PathBase.sprite / "black_tower_billboard.png"

    font_base       = PathBase.font / 'NotoSansTC-VariableFont_wght.ttf'
    font_eng1       = PathBase.font / 'PressStart2P-Regular.ttf'
    font_eng2       = PathBase.font / 'Audiowide-Regular.ttf'

    json_save       = (PathBase.json / JsonFileID.SAVE).with_suffix(".json")
    json_display    = (PathBase.json / JsonFileID.DISPLAY).with_suffix(".json")
    a_star          = MixPath(
        (PathBase.core / "c_src" / "a_star" / "main.c", PathBase.core / "c_src" / "a_star" / "base.c"),
        PathBase.core / "dll" / "a_star.dll"
    )
