import sys
from pathlib import Path

if getattr(sys, 'frozen', False):
    ext_path = str(Path(sys.executable).parent)
    if ext_path not in sys.path:
        sys.path.insert(0, ext_path)

import pygame

import core.init
import core.input.mouse.interaction
from core.base import central_mg
from core.debug import dbg, simple_pro
from core.input.keyboard.manager import keyboard_mg
from core.input.mouse.manager import mouse_mg
from core.interrupt import main_interrupt
from core.page.main import main_page
from core.rendering.manager import render_mg
from core.screen.main import submit_static_img
from core.screen.reload_screen import reload_sys_window_scale

while central_mg.running:
    # 觀看fps
    if dbg.enable:
        simple_pro.start_frame()
        simple_pro.end_frame_and_report()

    # 事件處理，包含鍵盤中斷以及內部設定中斷
    for event in pygame.event.get():
        central_mg.leave_game(event)    # 檢查全局退出
        keyboard_mg.execute_key(event)  # 鍵盤按鍵檢查
        mouse_mg.handle_event(event)    # 滑鼠觸發檢查
        main_interrupt(event)

    # 更新時間
    central_mg.update_clock()
    # 決定是否載入新比例的螢幕
    reload_sys_window_scale()

    main_page()

    submit_static_img()

    render_mg.render_all()

    pygame.display.flip()  # 更新整個畫面

pygame.quit()
sys.exit()
