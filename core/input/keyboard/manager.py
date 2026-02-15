import pygame

from core.debug import dbg
from core.input.keyboard.base import KeyboardBase
from core.variable import BOOT_PAGE, PageTable


class KeyboardManager:
    def __init__(self) -> None:
        self.keymaps_base = {}
        self.current_keyboard = BOOT_PAGE

    def setup(
            self,
            game_mg_S, game_mg_D1, game_mg_D2,  game_mg_E,
            menu_mg, single_menu_mg,
            sys_config_mg, help_mg, rank_mg
        ):
        # 為每個 HMI Manager 裝上通用的鍵盤轉接頭
        menu_key    = KeyboardBase(menu_mg)
        single_key  = KeyboardBase(single_menu_mg)
        sys_config_key  = KeyboardBase(sys_config_mg)
        help_key    = KeyboardBase(help_mg)
        rank_key    = KeyboardBase(rank_mg)

        game_S_key = KeyboardBase(game_mg_S)
        game_D1_key = KeyboardBase(game_mg_D1)
        game_D2_key = KeyboardBase(game_mg_D2)
        game_E_key = KeyboardBase(game_mg_E)



        self.keymaps_base = {
            PageTable.MENU: {
                pygame.K_UP:        menu_key.move_up,
                pygame.K_DOWN:      menu_key.move_down,
                pygame.K_BACKSPACE: menu_key.move_backspace,
                pygame.K_RETURN:    menu_key.move_enter,
            },
            PageTable.SINGLE_MENU: {
                pygame.K_UP:        single_key.move_up,
                pygame.K_DOWN:      single_key.move_down,
                pygame.K_LEFT:      single_key.move_left,
                pygame.K_RIGHT:     single_key.move_right,
                pygame.K_BACKSPACE: single_key.move_backspace,
                pygame.K_RETURN:    single_key.move_enter,
            },
            PageTable.SINGLE: {
                pygame.K_UP:        game_S_key.move_up,
                pygame.K_DOWN:      game_S_key.move_down,
                pygame.K_LEFT:      game_S_key.move_left,
                pygame.K_RIGHT:     game_S_key.move_right,
                pygame.K_SPACE:     game_S_key.move_space,
                pygame.K_LCTRL:     game_S_key.move_crtl_left,
                pygame.K_BACKSPACE: game_S_key.move_backspace,
            },
            PageTable.DOUBLE: {
                # 玩家1
                pygame.K_w:         game_D1_key.move_up,
                pygame.K_s:         game_D1_key.move_down,
                pygame.K_a:         game_D1_key.move_left,
                pygame.K_d:         game_D1_key.move_right,
                pygame.K_LSHIFT:    game_D1_key.move_space,
                pygame.K_LCTRL:     game_D1_key.move_crtl_left,
                # 玩家2
                pygame.K_UP:        game_D2_key.move_up,
                pygame.K_DOWN:      game_D2_key.move_down,
                pygame.K_LEFT:      game_D2_key.move_left,
                pygame.K_RIGHT:     game_D2_key.move_right,
                pygame.K_RSHIFT:    game_D2_key.move_space,
                pygame.K_RCTRL:     game_D2_key.move_crtl_left,
                # 共用
                pygame.K_BACKSPACE: game_D1_key.move_backspace,
            },
            PageTable.ENDLESS: {
                pygame.K_UP:        game_E_key.move_up,
                pygame.K_DOWN:      game_E_key.move_down,
                pygame.K_LEFT:      game_E_key.move_left,
                pygame.K_RIGHT:     game_E_key.move_right,
                pygame.K_SPACE:     game_E_key.move_space,
                pygame.K_LCTRL:     game_E_key.move_crtl_left,
                pygame.K_BACKSPACE: game_E_key.move_backspace,
            },
            PageTable.SYS_CONFIG: {
                pygame.K_UP:        sys_config_key.move_up,
                pygame.K_DOWN:      sys_config_key.move_down,
                pygame.K_LEFT:      sys_config_key.move_left,
                pygame.K_RIGHT:     sys_config_key.move_right,
                pygame.K_BACKSPACE: sys_config_key.move_backspace,
            },
            PageTable.HELP: {
                pygame.K_UP:        help_key.move_up,
                pygame.K_DOWN:      help_key.move_down,
                pygame.K_LEFT:      help_key.move_left,
                pygame.K_RIGHT:     help_key.move_right,
                pygame.K_BACKSPACE: help_key.move_backspace,
            },
            PageTable.RANK: {
                pygame.K_BACKSPACE: rank_key.move_backspace,
            }
        }

    def execute_key(self, event):
        """
        接收按鍵碼，查找當前頁面的對應功能並執行
        """
        if event.type != pygame.KEYDOWN: return

        # 取得當前頁面的按鍵表 (由 BasePageNavigation.switch_page 自動更新)
        current_page_map = self.keymaps_base.get(self.current_keyboard)

        # 如果這一頁沒有設定任何按鍵 (例如過場動畫)，直接忽略
        if not current_page_map: return

        # 查找按鍵對應的函式
        action = current_page_map.get(event.key)
        if action:
            action() # 呼叫綁定的 KeyboardBase.move_xxx -> HMI.on_xxx
        else:
            if event.key != 1073742050:
                try:
                    key_name = pygame.key.name(event.key)
                except:
                    key_name = str(event.key)
                dbg.log(f"[Keyboard] Unmapped key: {event.key} ({key_name}) on page {self.current_keyboard}")

    def switch_page(self, page: PageTable):
        self.current_keyboard = page

keyboard_mg = KeyboardManager()
