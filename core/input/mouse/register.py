from typing import Any, Callable

from core.debug import dbg
from core.input.mouse.variable import IHoverHandler
from core.ui_layout.name.identifiers import LayoutName


class MouseRegistry:
    """
    負責儲存 UI 名稱與對應函式 (Callback) 的關係。
    """
    # 儲存 UI 點擊事件
    _UI_CLICK_MAP: dict[LayoutName, Callable] = {}

    @classmethod
    def register_ui(cls, layout_name: LayoutName):
        """ [裝飾器] 用來將函式註冊到特定的 UI 按鈕上 """
        def decorator(func: Callable):
            if layout_name in cls._UI_CLICK_MAP:
                dbg.war(f"[MouseRegistry] Overwriting handler for {layout_name}")

            cls._UI_CLICK_MAP[layout_name] = func
            return func
        return decorator

    @classmethod
    def execute_ui(cls, layout_name: LayoutName) -> bool:
        """ 執行 UI 對應的函式，若有執行回傳 True """
        handlers = cls._UI_CLICK_MAP.get(layout_name, None)

        if not handlers: return False

        try:
            handlers()
            return True
        except Exception as e:
            dbg.error(f"[MouseRegistry] Error executing {layout_name}: {e}")
        return False
    