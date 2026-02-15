from dataclasses import dataclass
from enum import Enum


class DrawShape(str, Enum):
    RECT = "rect"
    CIRCLE = "circle"

@dataclass
class DrawProfile:
    """ 繪圖設定檔：包含定位、形狀與樣式 """
    name: str                       # 對應 LayoutItem 的名稱

    color: tuple
    shape: str = DrawShape.RECT     # "rect" 或 "circle"
    # 如果不傳則預設回傳 0(0為填滿, > 0 為調整邊框粗細)
    hollow_factory: callable = lambda: 0

    # --- Grid 專用屬性 (預設為 0，一般圖形用不到) ---
    width_block: int = 0            # 橫向格子數 (cols)
    height_block: int = 0           # 縱向格子數 (rows)
    zoom_factory: callable = lambda: None

    @property
    def hollow(self):
        return round(self.hollow_factory())

    @property
    def zoom(self):
        value = self.zoom_factory()
        return None if value is None else round(value)
