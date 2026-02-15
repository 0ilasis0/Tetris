from copy import deepcopy
from typing import Any

from core.debug import dbg
from core.hmi.base import HMIBaseManager
from core.input.keyboard.variable import UI_LIMITS, UILimitConfig
from core.json.manager import json_mg
from core.path.manager import JsonFileID
from core.variable import PageTable


class ListManager(HMIBaseManager):
    """
    通用 manager：負責 state 管理、hook_x/hook_y 切換邏輯、以及 JSON load/save。
    json_map: dict[state_key] = (FileID, JsonKey)
    """
    def __init__(
            self,
            base_nav,
            page_table: PageTable,
            default_state:  dict[str, Any],
            json_map:       dict[str, tuple] | None = None
        ):
        super().__init__(base_nav, page_table)

        self.state = deepcopy(default_state)
        self._default_state = deepcopy(default_state)
        # Tuple 結構: (JsonID, KeyName)
        self.json_map = json_map or {}

        # 建立索引映射
        self.key_map = dict(enumerate(self.state.keys()))

        # 讀取邊界設定 (取代原本傳入的一堆 min/max)
        self._load_hook_limits()

        # 初始化資料
        self._load_state_from_json()
        self._sync_hook_initial()

    def _load_hook_limits(self):
        """ 從 UI_LIMITS 讀取邊界設定 """
        config: UILimitConfig = UI_LIMITS.get(self.page)

        # 設定邊界
        if config:
            self.min_x = config.min_x
            self.min_y = config.min_y
            self.max_x = config.max_x # 這裡可能是 int 或 dict
            self.max_y = config.max_y

    def _update_cursor(self, dx = 0, dy = 0):
        # 取得目前 hook 狀態
        cur_x = self.hook_x
        cur_y = self.hook_y
        # --- Y 軸移動 (切換行) ---
        if dy != 0:
            cur_y += dy
            # 限制 Y 範圍
            cur_limit_y = self._resolve_limit(self.max_y, cur_x) # 這裡通常依賴 0 或固定值
            if cur_y < 0: cur_y = cur_limit_y
            elif cur_y > cur_limit_y: cur_y = 0

            # 切換行後，X 要變成該行原本儲存的數值 (例如從 音量 切到 視窗大小)
            key = self.key_map.get(cur_y)
            if key:
                cur_x = self.state.get(key, 0)

        # --- X 軸移動 (調整數值) ---
        if dx != 0:
            cur_x += dx
            # 限制 X 範圍 (依賴目前的 Y)
            cur_limit_x = self._resolve_limit(self.max_x, cur_y)

            if cur_x < 0: cur_x = cur_limit_x
            elif cur_x > cur_limit_x: cur_x = 0

            # [重要] 數值改變，寫入 State 並存檔
            key = self.key_map.get(cur_y)
            if key:
                self.state[key] = cur_x
                self._save() # 自動存檔
                self.on_state_change(key, cur_x) # 觸發回呼

        # --- 更新全域 Hook ---
        self.hook_x = cur_x
        self.hook_y = cur_y

    def _resolve_limit(self, limit_obj, check_val):
        """ 解析 int 或 dict 類型的限制 """
        if isinstance(limit_obj, int): return limit_obj
        if isinstance(limit_obj, dict):
            # ... 查字典邏輯 ...
            key_name = self.key_map.get(check_val)
            if key_name and key_name in limit_obj: return limit_obj[key_name]
            if check_val in limit_obj: return limit_obj[check_val]
        return 0

    def _load_state_from_json(self):
        """ 專門負責讀取 JSON 並更新 state """
        for state_key, path_tuple in self.json_map.items():
            if not path_tuple or len(path_tuple) < 2:
                dbg.war(f"json_map path error: {path_tuple}")
                continue

            file_id, *keys = path_tuple

            raw_data = json_mg.get_data(file_id, *keys, silent=True)
            if raw_data is None: continue

            # 處理 List 與 Value 的對應
            val = raw_data
            default_val = self._default_state.get(state_key)

            # 如果預設值不是 list，但讀到 list，則取第一個元素
            if not isinstance(default_val, list) and isinstance(raw_data, list) and len(raw_data) > 0:
                val = raw_data[0]

            if val is None: continue

            # 型別安全轉換
            if isinstance(default_val, int):
                try:
                    self.state[state_key] = int(val)
                except Exception:
                    self.state[state_key] = default_val
            else:
                self.state[state_key] = val

    def _sync_hook_initial(self):
        """ 僅在初始化時呼叫一次，確保 Hook 在正確位置 """
        init_key = self.key_map.get(0)
        if init_key:
            val = self.state.get(init_key, 0)
            self.hook_x = val
            self.hook_y = 0

    def _save(self):
        """
        儲存邏輯：更新記憶體 -> 通知 JsonManager 寫入硬碟
        """
        if not self.json_map: return

        has_changes = False
        target_file_ids = set() # 紀錄哪些檔案被修改了

        for state_key, path_tuple in self.json_map.items():

            if not path_tuple or len(path_tuple) < 2: continue

            file_id = path_tuple[0]
            keys = path_tuple[1:]

            # 只處理 SAVE 類型的資料 (display.json 通常不存檔)
            if file_id == JsonFileID.SAVE:
                current_value = self.state[state_key]

                # 判斷是否為列表模式
                if isinstance(current_value, list):
                    target_index = None
                else:
                    target_index = 0

                # 更新 JsonManager 記憶體
                json_mg.update_data(
                    file_id,
                    *keys,
                    value = current_value,
                    index = target_index
                )

                has_changes = True
                target_file_ids.add(file_id)

        # 如果有變動，通知 JsonManager 寫入硬碟
        if has_changes:
            for file_id in target_file_ids:
                json_mg.save_to_disk(file_id)

    def on_state_change(self, key: str, value: Any):
        """ 子類別覆寫用 """
        pass

    def on_up(self):    self._update_cursor(dy = -1)
    def on_down(self):  self._update_cursor(dy = 1)
    def on_left(self):  self._update_cursor(dx = -1)
    def on_right(self): self._update_cursor(dx = 1)
