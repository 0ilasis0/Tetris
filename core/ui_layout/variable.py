from dataclasses import dataclass, field
from enum import IntEnum

import pygame

from core.variable import Position, Size


@dataclass
class LayoutItem:
    category: str = None       # 分類，例如 'MENU', 'SINGLE' 等
    name: str = None           # 唯一名稱
    img_id: str = None
    size: Size = None
    pos: Position = field(default_factory = Position.zero)

    def update(self, **changes):
        """
        解包 dict 並將其內容結合舊物件整合成新物件回傳
        用法：
            item.update(
                name = name,
                category = page
            )
        """
        for key, value in changes.items():
            # 檢查屬性是否存在 (防呆)
            if not hasattr(self, key):
                raise ValueError(f"LayoutItem 沒有屬性 '{key}'，無法修改。")

            setattr(self, key, value)

        return self

    def __hash__(self):
        # 使用物件的記憶體位址作為 ID
        # 這樣即使修改 pos 或 size，Hash 值也不會變，不會破壞 set 結構
        return id(self)

    def __eq__(self, other):
        # 只有當兩個變數指向同一個記憶體物件時，才視為相等
        return self is other

    @property
    def rect(self) -> pygame.Rect:
        """
        當外界呼叫 item.rect 時，自動根據當下的 pos 和 size
        產生一個 pygame.Rect 物件回傳。
        """
        return pygame.Rect(
            int(self.pos.x),
            int(self.pos.y),
            int(self.size.width),
            int(self.size.height)
        )


class PosZLayer(IntEnum):
    """ 全局圖層管理 (Z-Index) """
    BACKGROUND      = 0     # 最底層背景
    MAIN            = 10    # 主要容器 (如遊戲盤面、主面板、Underline)
    DECORATION      = 20    # 裝飾層 (如邊框 Frame、蕾絲 Lace)
    CASTLE_RANGE    = 30
    UI_ELEMENT      = 40    # UI 圖片元件 (如 Slot, Combo bar, Clock, Song Block)
    UI_ELEMENT_1    = 40 + 1
    UI_ELEMENT_2    = 40 + 2
    PROJECTILE      = 40 + 3
    TEXT            = 50    # 文字與數字 (必須疊在 UI 圖片之上)
    TOP_OVERLAY     = 100   # 最上層覆蓋 (如選單游標 Rect、高亮特效)

    DEFAULT         = 999
