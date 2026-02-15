from core.base import central_mg, global_timer
from core.debug import dbg
from core.font.manager import font_mg
from core.font.preset import TextID
from core.font.variable import TextContent
from core.hmi.config.variable import ConfigVar
from core.json.preset import SaveID
from core.page.base import BootMode, page_mg
from core.page.navigation import BasePageNavigation, base_nav
from core.page.variable import HelpConfig, RankConfig
from core.screen.draw.manager import draw_mg
from core.screen.draw.preset import DrawID
from core.screen.image.manager.core import img_mg
from core.tetris_game.level.manager import single_level_mg
from core.tetris_game.level.variable import LevelVar
from core.tetris_game.main import (TetrisCore, game_watch, individual_tetris,
                                   main_tetris_game)
from core.tetris_game.manager import player0, player1
from core.ui_layout.main import layout_mg
from core.ui_layout.name.identifiers import LayoutName
from core.ui_layout.scale.manager import location_config
from core.ui_layout.scale.preset.menu import ScaleMenuVar
from core.ui_layout.scale.preset.sys_config import ScaleSysConfigVar
from core.variable import Align, PageTable, Position, Size


def main_page():
    page_function = page_mg.keymaps[page_mg.current_page]

    # 決定是否載入當前boot
    if page_mg.current_boot == page_mg.current_page:
        page_mg.load_page_boot(page_mg.current_boot)
        page_mg.switch_boot(None)

    # 執行當前頁面主循環
    if page_function is not None:
        page_function()
    else:
        dbg.error(f"no load {page_mg.current_page}")



class PageNavigation:
    def __init__(self, base_nav) -> None:
        self.base_nav: BasePageNavigation = base_nav

    def MENU(self):
        font_mg.draw_json_text(TextID.MENU_MAIN)

        # 畫玩家選擇方塊
        rect_pos: Position = layout_mg.get_item_pos(PageTable.MENU, LayoutName.MENU_USER)
        main_size: Size = layout_mg.get_item_size(PageTable.MENU, LayoutName.MENU_MAIN)
        main_one_height = main_size.height // ScaleMenuVar.MAIN_QUANTITY

        draw_mg.add_form(
            draw_id = DrawID.MENU_USER,
            override_pos = Position(
                rect_pos.x,
                rect_pos.y + main_one_height * self.base_nav.menu_mg.hook_y,
                rect_pos.z
            )
        )

        # 黑塔轉圈圈gif
        amount = ScaleMenuVar.BT_BOARD_WH_QUANTITY * ScaleMenuVar.BT_BOARD_WH_QUANTITY - 1
        time = global_timer.sprite_time_change(amount, amount)
        img_mg.switch_image_idx(LayoutName.MENU_BT_BOARD, time)

    def SINGLE_MENU(self):
        # 畫基本關卡方塊
        for level_item in LayoutName.SINGLE_MENU_RECT.serial_list:
            draw_mg.add_form(
                draw_id = DrawID.SINGLE_MENU_RECT,
                layout_name = level_item
            )

        # 畫關卡數字
        for index, level_item in enumerate(LayoutName.SINGLE_MENU_LEVEL.serial_list):
            level_number = index + 1
            font_mg.draw_text(
                TextID.SINGLE_MENU_LEVEL_STYLE,
                str(level_number),
                target_layout = level_item
            )

        # 畫玩家選擇關卡方塊
        user_pos: Position = layout_mg.get_item_pos(PageTable.SINGLE_MENU, LayoutName.SINGLE_MENU_USER)
        
        draw_mg.add_form(
            draw_id = DrawID.SINGLE_MENU_USER,
            override_pos = Position(
                user_pos.x + location_config.single_menu.gap * self.base_nav.single_menu_mg.hook_x,
                user_pos.y + location_config.single_menu.gap * self.base_nav.single_menu_mg.hook_y,
                user_pos.z
            )
        )

    def SINGLE(self):
        self.game_common(PageTable.SINGLE, player0)

        # 顯示通關方式的 分 秒 分數
        target_min = single_level_mg.current_display.get(LevelVar.MIN)
        target_sec = single_level_mg.current_display.get(LevelVar.SEC)
        target_fraction = single_level_mg.current_display.get(LevelVar.FRACTION)
        font_mg.draw_text(TextID.GAME_TARGET_TIME, target_min, target_sec)
        font_mg.draw_text(TextID.GAME_TARGET_SCORE, target_fraction)

    def DOUBLE(self):
        self.game_common(PageTable.DOUBLE, player0)
        self.game_common(PageTable.DOUBLE, player1)

    def ENDLESS(self):
        self.game_common(PageTable.ENDLESS, player0)

    def SYS_CONFIG(self):
        # 選項
        font_mg.draw_json_text(TextID.SYS_SONG_MAIN)

        # 音量大小方塊
        current_vol = self.base_nav.sys_config_mg.state.get(SaveID.SYS_VOLUME)
        song_block_size: Size = layout_mg.get_item_size(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_BLOCK)
        draw_mg.add_form(
            draw_id = DrawID.SYS_SONG_BLOCK_CELL,
            override_size = Size(
                (song_block_size.width // ConfigVar.WIDTH_BLOCK) * current_vol,
                (song_block_size.height // ConfigVar.HEIGHT_BLOCK)
            )
        )

        # 玩家選擇方塊
        user_pos: Position = layout_mg.get_item_pos(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_USER)
        main_size: Size = layout_mg.get_item_size(PageTable.SYS_CONFIG, LayoutName.SYS_SONG_MAIN)
        main_one_height = main_size.height // ScaleSysConfigVar.main_quantity
        draw_mg.add_form(
            draw_id = DrawID.SYS_SONG_USER,
            override_pos = Position(
                user_pos.x,
                user_pos.y + self.base_nav.sys_config_mg.hook_y * main_one_height,
                user_pos.z
            )
        )

        # 歌曲名稱
        index = self.base_nav.sys_config_mg.state.get(SaveID.SYS_SONG)
        font_mg.draw_text(TextID.SYS_SONG_NAME, self.base_nav.sys_config_mg.files_name[index])

        # 調整視窗大小數值顯示
        index = self.base_nav.sys_config_mg.state.get(SaveID.SYS_SCALE)
        font_mg.draw_text(TextID.SYS_WINDOW_SCALE, TextContent.SYS_WINDOW_SCALE_NUMBER[index])

    def HELP(self):
        # 玩家選擇 img_panel
        img_mg.switch_image_idx(LayoutName.HELP_PANEL, self.base_nav.help_mg.hook_x)

        # 標題文字
        for idx in range(3):
            alpha_percent = HelpConfig.title_alpha[self.base_nav.help_mg.hook_x][idx]
            font_mg.draw_json_text(
                TextID.HELP_DYNAMIC_TITLE,
                index = idx,
                alpha = alpha_percent,
                align = Align.CENTER,
                offset_pos = Position(location_config.help.title_gap_y_plus * idx, 0, 0)
            )

        # 遊戲說明文字
        font_mg.draw_json_text(
            text_id = TextID.HELP_DYNAMIC_DESC,
            index = self.base_nav.help_mg.hook_x,
            align = Align.BOTTOM_LEFT
        )

    def RANK(self):
        rank_data = self.base_nav.rank_mg.get_rank()

        for i, offset_pos in RankConfig.extra_pos.items():
            number = i + 1
            # 名次 分 秒 分數
            font_mg.draw_text(
                TextID.RANK_RANKING,
                number,
                offset_pos = offset_pos
            )
            font_mg.draw_text(
                TextID.RANK_MIN,
                rank_data[i][0],
                offset_pos = offset_pos
            )
            font_mg.draw_text(
                TextID.RANK_SEC,
                rank_data[i][1],
                offset_pos = offset_pos
            )
            font_mg.draw_text(
                TextID.RANK_FRACTION,
                rank_data[i][2],
                offset_pos = offset_pos
            )

    def EXIT(self):
        central_mg.running = False

    def game_common(self, page: PageTable, player: TetrisCore = player0):
        ''' 統一使用SINGLE '''
        if   player == player0: player_number = 0
        elif player == player1: player_number = 1

        # 共同核心
        main_tetris_game(player = player, current_page = page)
        # timer
        game_watch.update(dt = global_timer.get_dt())
        min, sec = game_watch.get_min_sec()
        # 不同mode的核心
        individual_tetris.main_process(page, player, min, sec)


        # 畫場地內固定方塊
        draw_mg.add_cells(
            draw_id = DrawID.GAME_MAIN_CELLS,
            cells = player.field.grid,
            grid = player.field.grid,
            target_layout = LayoutName.GAME_MAIN.serial_list[player_number]
        )
        # 畫player移動方塊
        draw_mg.add_cells(
            draw_id = DrawID.GAME_MAIN_CELLS,
            cells = player.current_tetromino.tetromino_to_matrix(player.current_tetromino),
            grid = player.field.grid,
            other_x = player.current_tetromino.x,
            other_y = player.current_tetromino.y,
            target_layout = LayoutName.GAME_MAIN.serial_list[player_number]
        )
        # 畫player暫存方塊
        draw_mg.add_cells(
            draw_id = DrawID.GAME_SLOT_CELLS,
            cells = player.current_tetromino.tetromino_to_matrix(player.store_slot.current_slot),
            grid = player.field.grid,
            target_layout = LayoutName.GAME_SLOT.serial_list[player_number]
        )

        # score
        font_mg.draw_text(
            TextID.GAME_SCORE,
            player.score,
            target_layout = LayoutName.GAME_SCORE.serial_list[player_number]
        )
        # combo
        if player.combo > 0:
            font_mg.draw_text(
                TextID.GAME_COMBO,
                player.combo,
                target_layout = LayoutName.GAME_COMBO.serial_list[player_number]
            )
        # ko
        if player.attack_mg.ko_counter > 0:
            font_mg.draw_text(
                TextID.GAME_KO,
                player.attack_mg.ko_counter,
                target_layout = LayoutName.GAME_KO.serial_list[player_number]
            )

        # timer_clock
        if player == player0:
            font_mg.draw_text(
                TextID.GAME_CLOCK_SEC,
                int(sec),
                target_layout = LayoutName.GAME_CLOCK_SEC.serial_list[player_number]
            )
            font_mg.draw_text(
                TextID.GAME_CLOCK_MIN,
                min,
                target_layout = LayoutName.GAME_CLOCK_MIN.serial_list[player_number]
            )

page_navigation = PageNavigation(base_nav)



class PageBoot():
    ''' 只會在初次進入當前頁面時載入一次下次刷屏不會進來，但下次進入頁面又會進來 '''
    def MENU(self):
        pass

    def SINGLE_MENU(self):
        pass

    def SINGLE(self):
        self.game_common_draw(PageTable.SINGLE, player0)

        if page_mg.boot_mode == BootMode.FULL:
            game_watch.reset()
            game_watch.start()
            player0.reset(attack_sw = True, level_sw = False)
            player0.level_mg.update_level(player = player0, level = player0.level_mg.current_level)

    def DOUBLE(self):
        self.game_common_draw(PageTable.DOUBLE, player0)
        self.game_common_draw(PageTable.DOUBLE, player1)

        if page_mg.boot_mode == BootMode.FULL:
            game_watch.reset()
            game_watch.start()
            player0.reset()
            player1.reset()
            player0.attack_mg.enabled = True
            player1.attack_mg.enabled = True

    def ENDLESS(self):
        self.game_common_draw(PageTable.ENDLESS, player0)

        if page_mg.boot_mode == BootMode.FULL:
            player0.reset()
            game_watch.reset()
            game_watch.start()

    def SYS_CONFIG(self):
        draw_mg.clear_map(PageTable.SYS_CONFIG)
        # 音量網格線
        draw_mg.add_grid(draw_id = DrawID.SYS_SONG_BLOCK_GRID, fixed = True)

    def HELP(self):
        pass

    def RANK(self):
        pass

    def EXIT(self):
        pass

    def game_common_draw(self, page: PageTable, player: TetrisCore = player0):
        if player == player0:
            draw_mg.clear_map(page)
            player_number = 0
        else:
            player_number = 1

        # 主體網格線
        draw_mg.add_grid(
            draw_id = DrawID.GAME_MAIN,
            fixed = True,
            layout_name = LayoutName.GAME_MAIN.serial_list[player_number]
        )
        # 暫存格網格線
        draw_mg.add_grid(
            draw_id = DrawID.GAME_SLOT,
            fixed = True,
            layout_name = LayoutName.GAME_SLOT.serial_list[player_number]
        )

page_boot = PageBoot()
