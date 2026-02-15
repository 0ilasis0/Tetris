from dataclasses import dataclass
from enum import Enum
from typing import Dict, Union

from core.json.preset import SaveID
from core.variable import PageTable


class NameHookLimit(str, Enum):
    SYS_SONG = "SYS_SONG_LIMITS"


@dataclass
class UILimitConfig:
    max_x: Union[int, Dict[str, int]]
    max_y: int
    min_x: int = 0
    min_y: int = 0


# 定義動態限制字典
DYNAMIC_LIMITS = {
    NameHookLimit.SYS_SONG: {
        SaveID.SYS_SONG:   0,  # 初始值，會在讀取歌曲後更新
        SaveID.SYS_VOLUME: 10,
        SaveID.SYS_SCALE:  0,  # 初始值，會在讀取螢幕數量後更新
    }
}

UI_LIMITS = {
    PageTable.MENU: UILimitConfig(
        max_x = 0,
        max_y = 6
    ),

    PageTable.SINGLE_MENU: UILimitConfig(
        max_x = 4,
        max_y = 1
    ),

    PageTable.SINGLE: UILimitConfig(max_x = 0, max_y = 0),
    PageTable.DOUBLE: UILimitConfig(max_x = 0, max_y = 0),
    PageTable.ENDLESS: UILimitConfig(max_x = 0, max_y = 0),

    PageTable.SYS_CONFIG: UILimitConfig(
        max_x = DYNAMIC_LIMITS[NameHookLimit.SYS_SONG],
        max_y = 2
    ),

    PageTable.RANK: UILimitConfig(max_x = 0, max_y = 0),

    PageTable.HELP: UILimitConfig(
        max_x = 2,
        max_y = 0
    ),
}
