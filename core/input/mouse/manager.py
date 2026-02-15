from typing import TYPE_CHECKING

import pygame

from core.debug import dbg
from core.input.mouse.register import MouseRegistry
from core.ui_layout.main import layout_mg
from core.variable import PageTable

if TYPE_CHECKING:
    from core.page.base import PageManager

class MouseManager:
    def __init__(self):
        self.page_mg = None

        # 滑鼠下的 ui,building last 儲存
        self._hovered_ui = None
        self._hovered_building = None

    def setup(self, page_mg: "PageManager"):
        """ 依賴注入 """
        self.page_mg = page_mg

    def handle_event(self, event):
        """ 接收 Pygame 事件的統一入口 """
        if event.type == pygame.MOUSEBUTTONDOWN:
            if event.button == 1: # 左鍵
                self._on_left_click(event.pos)
            elif event.button == 3: # 右鍵
                self._on_right_click(event.pos)
        elif event.type == pygame.MOUSEMOTION:
            self._on_mouse_move(event.pos)

    def _on_left_click(self, pos: tuple[int, int]):
        current_page = self.page_mg.current_page

        # --- UI 攔截 ---
        clicked_ui = layout_mg.get_clicked_item(pos, current_page)

        if clicked_ui:
            # dbg.log(f'{clicked_ui}')
            is_handled = MouseRegistry.execute_ui(clicked_ui.name)
            if is_handled: return

    def _on_right_click(self, pos: tuple[int, int]):
        """ 右鍵邏輯 (例如取消操作) """
        pass

    def _on_mouse_move(self, pos: tuple[int, int]):
        """ 滑鼠移動時的邏輯 """
        pass
        current_page = self.page_mg.current_page
        current_ui = layout_mg.get_clicked_item(pos, current_page)

        if current_ui != self._hovered_ui:
            if self._hovered_ui:
                pass
            if current_ui:
                pass
            self._hovered_ui = current_ui

mouse_mg = MouseManager()
