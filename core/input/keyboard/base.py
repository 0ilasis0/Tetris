# 基礎鍵盤操作
class KeyboardBase():
    def __init__(self, manager) -> None:
        self.mg = manager
    def move_backspace(self): self.mg.on_cancel()
    def move_enter(self): self.mg.on_confirm()
    def move_up(self): self.mg.on_up()
    def move_down(self): self.mg.on_down()
    def move_left(self): self.mg.on_left()
    def move_right(self): self.mg.on_right()
    def move_space(self): self.mg.on_space()
    def move_crtl_left(self): self.mg.on_crtl_l()
