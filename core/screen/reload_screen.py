import os

import pygame

from core.base import central_mg
from core.page.base import BootMode, page_mg
from core.page.variable import RankConfig
from core.screen.image.manager.core import img_mg
from core.screen.variable import ScreenConfig
from core.ui_layout.main import layout_collection
from core.ui_layout.scale.manager import location_config
from core.variable import PageTable


def reload_sys_window_scale():
    if central_mg.sys_window_scale_pending is not None:
        # 將螢幕移回正中間，已顯示右上角符號
        os.environ['SDL_VIDEO_CENTERED'] = '1'
        # 需要從新進入boot一次
        page_mg.switch_boot(page_mg.current_page, BootMode.RELOAD)

        ScreenConfig.set_resolution_ratio(central_mg.sys_window_scale_pending)
        location_config.reload_setup()
        layout_collection.reload_setup()

        RankConfig.reload_setup()
        img_mg.reload_setup()

        # 更新螢幕大小
        central_mg.current_window = pygame.display.set_mode((ScreenConfig.width, ScreenConfig.height), pygame.RESIZABLE)

        central_mg.sys_window_scale_pending = None
