from dataclasses import dataclass
from enum import Enum
from pathlib import Path

from core.variable import Size


# "stretch"(拉伸), "fit"(等比), "original"(原圖)
class ScaleMode(str, Enum):
    STRETCH = "stretch"
    ORIGINAL = "original"
    # FIT = "fit"

@dataclass(frozen = True)
class ImageProfile:
    path: Path | list[Path]             # 支援單圖或多圖
    name: str | None = None             # 對應 LayoutItem 的名稱
    is_static: bool = True              # 設為 False 則只載入不自動渲染

    alpha: int = 255                    # 透明度 (0~255)
    angle: int = 0                      # 旋轉角度
    flip_x: bool = False                # 水平翻轉
    flip_y: bool = False                # 垂直翻轉
    offset: tuple[int, int] = (0,0)     # 位置微調 (x, y)
    scale_mode: str = ScaleMode.STRETCH

    # --- Sprite Sheet 相關參數 ---
    is_sprite_sheet: bool = False       # 是否為 Sprite Sheet
    frame_size: Size | None = None      # 單格大小 (應用無法直接使用長寬Size/長寬數量)
    frame_count: int | None = None      # 總格數 (若為 0 則自動計算為 row * col)
    frame_row: int = 1                  # 行數
    frame_col: int = 1                  # 列數
    frame_gap_x: int = 0                # 格子間距
    frame_gap_y: int = 0                # 格子間距
