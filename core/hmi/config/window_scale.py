from core.base import central_mg
from core.hmi.config.variable import ConfigVar
from core.input.keyboard.variable import DYNAMIC_LIMITS, NameHookLimit
from core.json.preset import SaveID


class SysWindowManager:
    """
    Mixin: 視窗縮放邏輯
    """
    def __init__(self) -> None:
        pass

    def init_window_setup(self):
        """ 初始化：只負責設定按鍵邊界限制 (Dynamic Limits) """
        # 計算選項數量
        total_options = len(ConfigVar.window_scale_list)
        limit_val = total_options - 1 if total_options > 0 else 0

        # 更新動態限制字典
        # ListManager 會讀取這個字典來決定 SaveID.SYS_SCALE 這一行的 max_x
        key = SaveID.SYS_SCALE
        limit_dict = DYNAMIC_LIMITS[NameHookLimit.SYS_SONG] # 這裡共用同一個字典

        if limit_dict.get(key) != limit_val:
            limit_dict[key] = limit_val

    def apply_window_logic(self, value):
        """
        處理視窗改變的邏輯 (由 SysConfigManager 呼叫)
        value: int (ConfigVar.window_scale_list 的 index)
        """
        try:
            idx = int(value)
        except (ValueError, TypeError):
            return

        # 檢查範圍
        if 0 <= idx < len(ConfigVar.window_scale_list):
            target_ratio = ConfigVar.window_scale_list[idx]

            # 通知 CentralManager 視窗大小需要改變
            if hasattr(central_mg, 'sys_window_scale_pending'):
                central_mg.sys_window_scale_pending = target_ratio
