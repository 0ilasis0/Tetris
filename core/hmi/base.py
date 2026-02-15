from typing import TYPE_CHECKING

from core.hmi.i_controllable import IControllable

if TYPE_CHECKING:
    from core.page.navigation import BasePageNavigation

class HMIBaseManager(IControllable):
    """
    所有 HMI Manager 的基類
    """
    def __init__(self, base_nav: "BasePageNavigation", page):
        # 游標管理
        self.hook_x = 0
        self.hook_y = 0

        self.base_nav = base_nav
        self.page = page

    def on_cancel(self):
        """ 通用的返回邏輯 """
        self.base_nav.back_to_prev(self.page)

    def on_confirm(self):
        """ 通用的前進邏輯 """
        self.base_nav.handle_tree_navigation(
            self.page,
            self.hook_y
        )

    def reset_hook(self):
        self.hook_x = 0
        self.hook_y = 0
