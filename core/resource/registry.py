from enum import Enum
from typing import Any, Callable, Set

from core.debug import dbg


class ResourceRegistry:
    """
    確保 ID 格式統一 (Strategy Pattern)
    確保 ID 曾經被註冊過 (Validation)
    提供檔案路徑搜尋工具 (File IO Helper)
    """
    # 內部儲存：已註冊的 ID 白名單 ---
    _REGISTERED_IDS: Set[str] = set()

    # 策略定義：定義各類型需要的參數順序 ---
    _STRATEGIES: dict[str, Callable] = {

    }

    @classmethod
    def register_key(cls, genre: str | Enum, *args) -> str:
        """
        生成 ID 並標記為「已存在」。
        只有透過此函式生成的 ID，後續才能被 get_key 存取。
        """
        key = cls._generate_internal(genre, *args)

        if key in cls._REGISTERED_IDS:
            dbg.war(f"[ResManager] ID duplicate registration: {key}")

        cls._REGISTERED_IDS.add(key)
        return key

    @classmethod
    def get_key(cls, genre: str | Enum, *args) -> str:
        """
        嘗試取得 ID。
        """
        key = cls._generate_internal(genre, *args)

        # 嚴格檢查
        if key not in cls._REGISTERED_IDS:
            dbg.error(f"[ResManager] Access Denied! ID '{key}' was never registered.")
            return None

        return key

    @classmethod
    def _generate_internal(cls, genre: str | Enum, *args) -> str:
        """ 核心生成邏輯 (不含驗證) """
        genre_val = cls._save_get_enum_value(genre)
        strategy = cls._STRATEGIES.get(genre_val)

        if not strategy:
            return cls._join_id(genre_val, *args)

        try:
            # 執行策略 (參數檢查)
            raw_params = strategy(*args)
            # 標準化參數
            clean_params = [cls._save_get_enum_value(p) for p in raw_params]
            # 組合字串
            return cls._join_id(*clean_params)

        except TypeError as e:
            dbg.error(f"[ResManager] Invalid args for {genre_val}: {e}")
            raise e

    @staticmethod
    def _join_id(*args) -> str:
        """
        [通用 ID 生成器]
        接收任意數量的參數，過濾掉 None，組合成大寫 ID
        例如: generate_id("blue", "castle", 0) -> "BLUE_CASTLE_0"
        """
        valid_args = [str(arg) for arg in args if arg is not None and str(arg) != ""]
        return "_".join(valid_args).upper()

    @staticmethod
    def _save_get_enum_value(val: Any) -> str | int:
        """ Enum 自動轉 value """
        if isinstance(val, Enum):
            return val.value
        return val

