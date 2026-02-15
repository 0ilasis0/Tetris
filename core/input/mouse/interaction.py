from typing import TYPE_CHECKING

from core.input.mouse.register import MouseRegistry
from core.ui_layout.name.identifiers import LayoutName

# --- UI 行為註冊 ---

@MouseRegistry.register_ui(LayoutName.MENU_BT_BOARD)
def text_bt():
    print(">> 黑塔轉轉轉 ")
