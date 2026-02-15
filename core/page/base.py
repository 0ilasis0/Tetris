from enum import Enum, auto
from typing import Callable, Dict

from core.debug import dbg
from core.variable import BOOT_PAGE, PageTable


class BootMode(Enum):
    FULL = auto()   # 全新進入 (重置遊戲 Logic + 重繪 UI)
    RELOAD = auto() # 重新載入 (只重繪 UI，保留遊戲狀態)


class PageManager:
    def __init__(self):
        self.keymaps: Dict[PageTable, Callable] = {} # 存儲頁面的 Main Loop 函數

        # 狀態控制
        self.current_page: PageTable = BOOT_PAGE
        self.current_boot: PageTable = BOOT_PAGE
        self.boot_mode: BootMode = BootMode.FULL

        # 初始化回呼函數表 (PageBoot 裡面的函式)
        self.callbacks: Dict[PageTable, Callable] = {}

    def setup(self, keymaps: dict):
        """ 初始化注入 (通常在 main.py 或 base_nav setup 時呼叫) """
        self.keymaps = keymaps

    def load_page_boot(self, page_name: PageTable):
        '''
        執行頁面的初始/刷新函式
        (具體是 Full 還是 Reload，由被呼叫的 callback 內部檢查 self.boot_mode 決定)
        '''
        if page_name in self.callbacks:
            # 執行 PageBoot 對應的函式 (例如 PageBoot.SINGLE)
            self.callbacks[page_name]()
        else:
            dbg.war(f"PageBoot callback not found for {page_name}")

    def register_init_fcn(self, page_name: PageTable, fcn: Callable):
        """ 註冊頁面初始化函式 (由 PageBoot 在初始化時註冊進來) """
        self.callbacks[page_name] = fcn

    def switch_page(self, page: PageTable):
        """ 切換當前頁面指標 """
        self.current_page = page

    def switch_boot(self, page: PageTable, mode: BootMode = BootMode.FULL):
        """
        設定下一次的 Boot 目標與模式
        :param page: 要 Boot 的頁面 (通常是 next_page)，或是 None (表示 Boot 結束)
        :param mode: FULL=重置, RELOAD=只刷畫面
        """
        self.current_boot = page
        self.boot_mode = mode

page_mg = PageManager()
