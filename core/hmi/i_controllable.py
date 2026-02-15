from abc import ABC, abstractmethod


class IControllable(ABC):
    """
    [介面] 所有可被鍵盤控制的物件都必須繼承此類別
    這樣 Keyboard 只要呼叫這些標準名稱即可
    """
    # --- 方向鍵 (預設不做任何事) ---
    def on_up(self): pass
    def on_down(self): pass
    def on_left(self): pass
    def on_right(self): pass
    def on_space(self): pass
    def on_crtl_l(self): pass
    def on_crtl_r(self): pass


    # --- 功能鍵 ---
    def on_confirm(self): pass  # Enter
    @abstractmethod
    def on_cancel(self): pass   # Backspace
    def on_special(self): pass
