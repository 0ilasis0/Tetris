from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from core.path.manager import PathConfig


@dataclass(frozen = True)
class TextProfile:
    """ 文字設定檔：包含定位、內容與樣式 """
    name: str                          # 對應 LayoutItem 的名稱
    content: str                       # 文字內容 (支援 {} 格式化)
    color: tuple                       # 顏色
    font: Path = PathConfig.font_base  # 字體
    direction: str = 'horizontal'      # 可填 horizontal / vertical 來決定是否直立或橫書寫
    spacing: float = 1.0               # 行距(橫式) / 字距(直立)(為單個字的倍率)

class TextContent(list, Enum):
    SYS_WINDOW_SCALE_NUMBER = [
        "全視窗(1980X1080)",
        "視窗(1451X788)",
        "略小(1320X720)",
        "迷你(990X540)",
    ]
