from enum import Enum

from core.debug import dbg
from core.ui_layout.scale.manager import IHasLayout
from core.ui_layout.variable import LayoutItem
from core.variable import PageTable


class LayoutNameRegistry:
    """
    負責記錄所有目前場上「已存活」的物件名稱
    提供快速查找、驗證功能
    """
    _active_names: set[str] = set()       # 快速查找用
    _group_map: dict[str, set[str]] = {} # 群組索引用
    _name_to_group: dict[str, str] = {}

    @classmethod
    def register(cls, name: str, group_key: str):
        """ 寫入資料 """
        if name in cls._active_names: return

        cls._active_names.add(name)
        if group_key:
            if group_key not in cls._group_map:
                cls._group_map[group_key] = set()

            cls._group_map[group_key].add(name)
            cls._name_to_group[name] = group_key

    @classmethod
    def unregister(cls, name: str):
        """ 移除單一物件名稱 """
        if name not in cls._active_names: return

        cls._active_names.remove(name)

        # 從群組移除 (利用反向索引快速找到群組)
        group_key = cls._name_to_group.pop(name, None)
        if group_key and group_key in cls._group_map:
            cls._group_map[group_key].discard(name)

    @classmethod
    def clear_all(cls):
        """ 清空資料 """
        cls._active_names.clear()
        cls._group_map.clear()
        cls._name_to_group.clear()

    @classmethod
    def exists(cls, name: str) -> bool:
        """ 查詢是否存在 """
        return name in cls._active_names

    @classmethod
    def get_group(cls, group_key: str) -> list[str]:
        """ 查詢群組 """
        return cls._group_map.get(group_key, [])



class LayoutNameLoader:
    '''
    負責解析巢狀字典結構，自動為物件命名並載入至 LayoutManager
    '''
    def __init__(self, lay_mg):
        self.lay_mg = lay_mg

    def load_from_root(self, page: PageTable, root_data: dict):
        """
        root_data: 輸入整個 object 字典
        """
        self._recursive_walk(page, root_data, [])

    def _recursive_walk(self, page: PageTable, current_data: any, path_parts: list[str]):
        """
        path_parts: 目前累積的路徑，例如 ['1', 'ARCH']
        """
        # 遇到 dict (繼續往下鑽)
        if isinstance(current_data, dict):
            for key, data in current_data.items():
                # 處理 Key 的轉換邏輯
                if isinstance(key, Enum):
                    part_name = key.value
                else:
                    part_name = str(key)

                self._recursive_walk(page, data, path_parts + [part_name])

            return

        # 遇到list (終止並生成)
        if isinstance(current_data, list):
            combined_name = "_".join(path_parts)

            for index, item in enumerate(current_data):
                # 無論是 LayoutItem 還是 BuildingEntity 都能被抓到
                target_ui = self._extract_ui(item)

                if target_ui:
                    self._finalize_item(page, combined_name, index, target_ui)
                else:
                    dbg.war(f"Item {index} in {combined_name} is not a valid UI object: {item}")
            return

        # 遇到單個物件 (終止並生成)
        target_ui = self._extract_ui(current_data)
        if target_ui:
            combined_name = "_".join(path_parts)
            self._finalize_item(page, combined_name, 0, target_ui)
            return

        dbg.war(f"current data {current_data} is not limit form in {page}")

    def _extract_ui(self, item) -> LayoutItem | None:
        """
        安全地提取 UI
        """
        # 它本身就是 LayoutItem
        if isinstance(item, LayoutItem):
            return item

        # 它是一個有 Layout 的實體
        if isinstance(item, IHasLayout):
            return item.layout_ui

        return None

    def _finalize_item(self, page, combined_name, index, item: LayoutItem):
        """
        直接修改傳入的 item ，並加入 LayoutCollection(位在main中)
        """
        name = self.create_name(page, (combined_name, index))
        LayoutNameRegistry.register(name, combined_name)

        item.update(
            category = page,
            name = name,
            size = item.size,
            pos = item.pos
        )

        self.lay_mg.add_item(item)

    @staticmethod
    def create_name(page: PageTable, *layers: tuple[str, int]) -> str:
        """
        layers: (名稱, 索引) 的元組序列
        """
        parts = [page.name]

        # 遍歷所有層級
        for layer_data in layers:
            # 支援直接傳入 Enum，自動轉字串
            if isinstance(layer_data, tuple) and len(layer_data) == 2:
                name_key, number = layer_data

                # 處理 Enum 轉值
                if isinstance(name_key, Enum):
                    name_key = name_key.value

                parts.append(f"{name_key}_{number}")
            else:
                dbg.error(f"{layer_data} is not tuple or is not double character")

        return "_".join(parts)
