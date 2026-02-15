from typing import List

from core.debug import dbg
from core.ui_layout.variable import LayoutItem, PosZLayer
from core.variable import Align, PageTable, Position, Size


class LayoutManager:
    def __init__(self, screen_width, screen_height):
        self.screen_size = Size(screen_width, screen_height)
        self.items = {}

    def add_item(
            self,
            item: LayoutItem,
            x = None,
            y = None,
            z = PosZLayer.DEFAULT.value
        ):
        ''' 加入 item，可選位置 '''
        # 如果沒有傳入 x, y → 使用 item 原本的座標
        if (x is None or y is None):
            if (item.pos.x is not None) and (item.pos.y is not None):
                (x, y) = (item.pos.x, item.pos.y)
            else:
                dbg.error(f"[add_item] No position for item '{item.category}.{item.name}'")
                return None

        # 如果 z 是預設，則使用item的z
        if z is PosZLayer.DEFAULT.value: z = item.pos.z

        if item.category not in self.items:
            self.items[item.category] = {}

        item.pos = Position(x, y, z)

        if item.name in self.items[item.category]:
            dbg.war(f"[add_item] Overwriting item '{item.category}.{item.name}'")

        # 存入 dict
        self.items[item.category][item.name] = item
        return item

    def add_center(
            self,
            item: LayoutItem,
            pos_z: int,
            target = None,
            gap_x = 0,
            gap_y = 0,
        ):
        ''' 置中 '''
        if target == None:
            item.pos = Position(
                x = (self.screen_size.width - item.size.width + gap_x) // 2,
                y = (self.screen_size.height - item.size.height + gap_y) // 2,
                z = pos_z
            )
        else:
            item.pos = Position(
                x = target.pos.x + (target.size.width - item.size.width) // 2 + gap_x,
                y = target.pos.y + (target.size.height - item.size.height) // 2 + gap_y,
                z = pos_z
            )

        return self.add_item(item = item, z = pos_z)

    def add_symmetric(
            self,
            item: LayoutItem,
            target: LayoutItem,
            pos_z: int,
            axis: str = "vertical",
            gap_x = 0,
            gap_y = 0,
        ):
        """
        讓 item 根據 target 對稱
        "vertical"   → 左右對稱 (以畫面中心垂直線為對稱軸)
        "horizontal" → 上下對稱 (以畫面中心水平線為對稱軸)
        """
        center_x = self.screen_size.width // 2
        center_y = self.screen_size.height // 2

        if axis == "vertical":
            # 左右對稱：X 翻轉，Y 不變
            dx = target.pos.x - center_x
            item_x = center_x - dx - item.size.width
            item_y = target.pos.y
        elif axis == "horizontal":
            # 上下對稱：Y 翻轉，X 不變
            dy = target.pos.y - center_y
            item_y = center_y - dy - item.size.height
            item_x = target.pos.x
        else:
            raise ValueError("axis 只能是 'vertical' 或 'horizontal'")

        item.pos = Position(round(item_x + gap_x), round(item_y + gap_y), pos_z)
        return self.add_item(item = item, z = pos_z)

    def add_below(
            self,
            item: LayoutItem,
            target: LayoutItem,
            pos_z: int,
            gap = 0,
            align: Align = Align.TOP_LEFT
        ):
        """
        垂直堆疊 (放在 target 下方)
        align: 決定水平對齊方式 (LEFT, CENTER, RIGHT)
        """
        val = align.value

        # 水平對齊邏輯
        if 'left' in val:
            x = target.pos.x
        elif 'right' in val:
            x = target.pos.x + target.size.width - item.size.width
        else:
            x = target.pos.x + (target.size.width - item.size.width) // 2

        y = target.pos.y + target.size.height + gap

        item.pos = Position(round(x), round(y), pos_z)
        return self.add_item(item = item, z = pos_z)

    def add_right_of(
            self,
            item: LayoutItem,
            target: LayoutItem,
            pos_z: int,
            gap_x = 0,
            gap_y = 0,
            align: Align = Align.TOP_LEFT
        ):
        """
        水平排列 (放在 target 右邊)
        align: 決定垂直對齊方式 (TOP, CENTER, BOTTOM)
        """
        val = align.value

        if 'top' in val:
            y = target.pos.y
        elif 'bottom' in val:
            y = target.pos.y + target.size.height - item.size.height
        else:
            y = target.pos.y + (target.size.height - item.size.height) // 2

        x = target.pos.x + target.size.width + gap_x

        item.pos = Position(round(x), round(y + gap_y), pos_z)
        return self.add_item(item = item, z = pos_z)

    def add_left_of(
            self,
            item: LayoutItem,
            target: LayoutItem,
            pos_z: int,
            gap_y = 0,
            gap_x = 0,
            align: Align = Align.TOP_LEFT
        ):
        """
        水平排列 (放在 target 左邊)
        align: 決定垂直對齊方式 (TOP, CENTER, BOTTOM)
        """
        val = align.value

        if 'top' in val:
            y = target.pos.y
        elif 'bottom' in val:
            y = target.pos.y + target.size.height - item.size.height
        else:
            y = target.pos.y + (target.size.height - item.size.height) // 2

        x = target.pos.x + gap_x - item.size.width

        item.pos = Position(round(x), round(y + gap_y), pos_z)
        return self.add_item(item = item, z = pos_z)

    def add_inner(
            self,
            item: LayoutItem,
            target: LayoutItem,
            pos_z: int,
            gap_x = 0,
            gap_y = 0,
            align: Align = Align.TOP_LEFT,
    ):
        """
        內部重疊 (將 item 放在 target 內部)
        align: 決定九宮格位置
        """
        if (item.pos is None) or (target.pos is None):
            dbg.error(f'{item.name}->{item.pos} or {target.name}->{target.pos} pos is None')
            return None

        val = align.value

        # --- 水平計算 ---
        if 'left' in val:
            x = target.pos.x
        elif 'right' in val:
            x = target.pos.x + target.size.width - item.size.width
        else:
            x = target.pos.x + (target.size.width - item.size.width) // 2

        # --- 垂直計算 ---
        if 'top' in val:
            y = target.pos.y
        elif 'bottom' in val:
            y = target.pos.y + target.size.height - item.size.height
        else:
            y = target.pos.y + (target.size.height - item.size.height) // 2

        item.pos = Position(round(x + gap_x), round(y + gap_y), pos_z)
        return self.add_item(item = item, z = pos_z)

    def update_item_pos(self, page, name, pos: Position, offset_pos: Position = Position(0, 0, 0)):
        item: LayoutItem = self.get_item(page, name)
        item.pos.x = pos.x + offset_pos.x
        item.pos.y = pos.y + offset_pos.y

    def get_item_pos(
            self,
            category,
            name = None,
            index = None,
            extra_x = 0,
            extra_y = 0
        ) -> Position:
        """
        透過 category + name 取得 item 的 (x, y) 座標
        如果不存在，回傳 None
          """
        item = self.get_item(category, name, index)

        if item is None:
            dbg.error(f'{category}->{name} get_item is error')
            return None

        item_x, item_y = item.pos.x, item.pos.y

        return Position(item_x + extra_x, item_y + extra_y, item.pos.z)

    def get_item_size(self, category, name = None, index = None) -> Size:
        """
        透過 category + name 取得 item 的 (width, height)
        如果不存在，回傳 None
        """
        item = self.get_item(category, name, index)

        if item is None:
            dbg.war(f'{category}->{name} has no size label')
            return None

        return Size(item.size.width, item.size.height)

    def get_item(self, page, name = None, index = None, silent = False) -> LayoutItem:
        """
        取得 LayoutItem
        - 支援用 name 或 index 查
        - 不存在則回傳 None
        - silent 用於不想抱錯的情況
        """
        if page not in self.items:
            if silent: return None
            dbg.error(f"{page} 不存在")
            return None

        if name is not None:
            item = self.items.get(page, {}).get(name)
            if not item:
                if silent: return None
                dbg.error(f"{page} -> {name} 不存在")
                return None
            return item

        elif index is not None:
            items = list(self.items[page].values())
            if not (0 <= index < len(items)):
                if silent: return None
                dbg.error(f"{page} index {index} 超出範圍")
                return None
            return items[index]

        else:
            dbg.error("get_item 必須提供 name 或 index")
            return None

    def get_items_by_category(
            self,
            category,
            start_index = None,
            end_index = None
        ) -> List[LayoutItem]:
        ''' 透過 category 取得 items，可指定範圍 '''
        items_in_category = list(self.items.get(category, {}).values())

        if not items_in_category: return []

        if (start_index is not None) or (end_index is not None):
            items_in_category = items_in_category[start_index:end_index]

        return items_in_category

    def clear_items(self):
        self.items = {}

    def remove_item(self, item: LayoutItem):
        """ 從列表中移除特定 UI 物件 """
        category_dict = self.items.get(item.category)

        if category_dict and item.name in category_dict:
            del category_dict[item.name]

    def update_screen_size(self, width, height):
        self.screen_size = Size(width, height)

    def get_clicked_item(self, mouse_pos: tuple[int, int], page: PageTable) -> LayoutItem | None:
        """
        檢查該頁面所有的 UI Item，回傳被點擊的那一個 (Z-index 高的優先)
        """
        page_items = self.items.get(page)

        if not page_items: return None

        # 準備變數紀錄目前「最高層」的物件
        target_item = None
        highest_z = float('-inf')

        for item in page_items.values():
            if item.rect.collidepoint(mouse_pos):
                # 如果有點到，再檢查是否比目前記錄的還高
                if item.pos.z > highest_z:
                    highest_z = item.pos.z
                    target_item = item

        return target_item
