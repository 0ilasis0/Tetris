from core.hmi.base import HMIBaseManager
from core.variable import PageTable


class GameHmiManager(HMIBaseManager):
    """
    [Controller] 遊戲頁面的控制器
    職責：接收鍵盤指令，轉發給 TetrisCore (Player) 執行動作
    """
    def __init__(self, base_nav, player, page: PageTable):
        # 繼承 Base，這樣 KeyboardManager 才能通用地呼叫 on_up/on_down...
        super().__init__(base_nav, page)
        self.player = player

    def on_up(self): self.player.rotate()
    def on_down(self): self.player.move_down()
    def on_left(self): self.player.move_side(-1)
    def on_right(self): self.player.move_side(1)
    def on_space(self): self.player.go_space()
    def on_crtl_l(self): self.player.store_action()
