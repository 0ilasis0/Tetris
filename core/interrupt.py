import pygame

from core.hmi.config.variable import ConfigVar
from core.json.preset import SaveID
from core.page.navigation import base_nav
from core.screen.variable import ScreenConfig


def main_interrupt(event):
    # 音樂播放完畢
    if event.type == pygame.USEREVENT:
        base_nav.sys_config_mg.on_song_end()

    # 偵測右上角螢幕縮放標籤是否被按下
    elif event.type == pygame.VIDEORESIZE:
        raw_ratio = event.h / ScreenConfig.DESIGN_HEIGHT

        # 者出最接近的現有螢幕倍率的數值
        renew_index = min(
                range(len(ConfigVar.window_scale_list)),
                key = lambda i: abs(ConfigVar.window_scale_list[i] - raw_ratio)
            )

        current_idx = base_nav.sys_config_mg.state.get(SaveID.SYS_SCALE, 0)

        if renew_index != current_idx:
            base_nav.sys_config_mg.interrupt_window_scale(renew_index)


