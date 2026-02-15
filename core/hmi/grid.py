from copy import deepcopy

from core.debug import dbg
from core.hmi.variable import Cell
from core.json.manager import json_mg
from core.page.variable import GridThing
from core.path.manager import JsonFileID


class GridManager:
    """通用二維格子管理器"""
    def __init__(self, rows: int, cols: int):
        self.rows = rows
        self.cols = cols
        # 初始化為空格子
        self.grid = [[Cell() for _ in range(cols)] for _ in range(rows)]

        # 記憶體快照 (例如：切換不同的櫃子頁面)
        self.storage: dict[str, list[list[Cell]]] = {}

    def set_cell(self, x: int, y: int, merge: bool = True, **kwargs):
        """
        設定格子內容
        :param merge: True = 合併現有屬性(update), False = 完全覆蓋
        :param kwargs: 要設定的屬性，例如 lock ="unlock"
        """
        if not self._is_valid(x, y): return

        cell = self.grid[y][x]

         # 如果不是合併模式，先清空
        if not merge:
             cell.clear()
        # 使用 Cell 內部的 update
        if hasattr(cell, 'update'):
            cell.update(**kwargs)
        else:
            cell.data.update(kwargs)

    def get_cell(self, x: int, y: int) -> Cell | None:
        if self._is_valid(x, y):
            return self.grid[y][x]
        return None

    def load_from_global_storage(self, file_id: JsonFileID, *keys):
        """
        [讀取] 從 JsonManager 獲取資料並還原網格
        :param file_id: 例如 JsonFileID.SAVE
        :param keys: 路徑，例如 "SINGLE_MENU", "level_grid"
        """
        # 向 JsonManager 要資料
        raw_data = json_mg.get_data(file_id, *keys, silent = True)

        # 如果資料存在，執行還原
        if raw_data:
            self._import_from_json(raw_data)
        else:
            dbg.war(f"GridManager: 找不到資料 {keys}，維持預設狀態")
            pass

    def save_to_global_storage(self, file_id: JsonFileID, *keys, auto_save: bool = True):
        """
        [存檔] 將網格導出並寫入 JsonManager (會立即寫入硬碟)
        :param file_id: 例如 JsonFileID.SAVE
        :param keys: 路徑，例如 "SINGLE_MENU", "level_grid"
        """
        # 導出資料
        grid_data = self._export_to_json()

        # 更新記憶體
        json_mg.update_data(
            file_id,
            *keys,
            value = grid_data,
            index = None
        )

        if auto_save:
            json_mg.save_to_disk(file_id)

    def _is_valid(self, x, y):
        return 0 <= y < self.rows and 0 <= x < self.cols

    # ------------------ 記憶體暫存用 ------------------ #
    def _import_from_json(self, json_data: list[int]):
        """
        從一維整數陣列 [1, 1, 0...] 還原回 2D Grid
        """
        # (防呆)確保是列表
        if not json_data or not isinstance(json_data, list):
            self._clear_grid()
            return

        # 遍歷 1D 陣列，轉換座標
        for i, val in enumerate(json_data):
            # 計算 2D 座標
            y = i // self.cols
            x = i % self.cols

            # 超出範圍則停止
            if y >= self.rows:
                dbg.error(f"{json_data} is load error,its y length is over row")
                break

            # 將數值包裝回字典格式，再轉為 Cell
            data_dict = {GridThing.LOCK_SWITCH_: val}

            # 更新格子
            if self._is_valid(x, y):
                self.grid[y][x] = Cell.from_dict(data_dict)

    def _export_to_json(self) -> list[int]:
        """
        只提取 GridThing.LOCK_SWITCH_ 的數值
        """
        flat_list = []
        for row in self.grid:
            for cell in row:
                # 從 Cell 的字典中提取數值，如果沒有則預設為 0 (LOCK)
                val = cell.data.get(GridThing.LOCK_SWITCH_, GridThing.LOCK)
                flat_list.append(val)

        return flat_list

    def _clear_grid(self):
        """ 清理整個工作檯所有格子 """
        for row in self.grid:
            for cell in row:
                cell.clear()

    # ------------------ 記憶體快照 ------------------ #
    def save_snapshot(self, key: str):
        """ 將當前狀態存入快照 """
        self.storage[key] = deepcopy(self.grid)

    def load_snapshot(self, key: str):
        """ 從快照載入 """
        if key in self.storage:
            self.grid = deepcopy(self.storage[key])
        else:
            self._clear_grid()

    def clear_storage(self, key: str):
        """ 清理指定快照 """
        if key in self.storage:
            self.storage[key] = [[Cell() for _ in range(self.cols)] for _ in range(self.rows)]

    # ------------------ 顯示 / debug ------------------ #
    def print_grid(self, cur_x = None, cur_y = None):
        for y, row in enumerate(self.grid):
            line = []
            for x, cell in enumerate(row):
                content = str(cell.data) if not cell.is_empty else " "
                if cur_x == x and cur_y == y:
                    line.append(f"[{content}]")
                else:
                    line.append(f" {content} ")
            print(" ".join(line))
