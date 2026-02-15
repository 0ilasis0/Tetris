from core.debug import dbg
from core.font.preset import TextID, TextJson
from core.json.manager import json_mg
from core.screen.draw.preset import DrawID
from core.screen.variable import ScreenConfig
from core.tetris_game.variable import GameVar
from core.ui_layout.manager import LayoutManager
from core.ui_layout.name.identifiers import LayoutName
from core.ui_layout.scale.manager import location_config
from core.ui_layout.variable import LayoutItem, PosZLayer
from core.variable import Align, PageTable, Position, Size


# 建立虛擬 Pos Size 的物件
class LayoutCollection:
    def __init__(self, lay_mg: LayoutManager) -> None:
        self.lay_mg = lay_mg
        self.reload_setup()

    def reload_setup(self):
        self.lay_mg.clear_items()
        self.lay_mg.update_screen_size(ScreenConfig.width, ScreenConfig.height)

        self._setup_menu(PageTable.MENU)
        self._setup_single_menu(PageTable.SINGLE_MENU)
        self._setup_single_game(PageTable.SINGLE)
        self._setup_double_game(PageTable.DOUBLE)
        self._setup_endless_game(PageTable.ENDLESS)
        self._setup_sys_config(PageTable.SYS_CONFIG)
        self._setup_help(PageTable.HELP)
        self._setup_rank(PageTable.RANK)

    def check_integrity(self):
        """
        遍歷所有的 DrawID 和 TextID，確保它們參照的 LayoutItem 和 JSON 資料真的存在。
        """
        dbg.log("=== 開始 Layout 完整性檢查 (全域掃描模式) ===")
        error_count = 0

        # --- 檢查 DrawID (Layout 參照) ---
        # 建立「已知 Layout 名稱」的白名單
        all_existing_names = set()
        for page_data in self.lay_mg.items.values():
            for name in page_data.keys():
                all_existing_names.add(name)

        for member in DrawID:
            profile = member.value
            if profile.name is None:
                continue

            if profile.name not in all_existing_names:
                dbg.error(f"[DrawID Integrity] {member.name} 指向的 layout_name='{profile.name}' 在任何頁面都找不到！")
                error_count += 1

        # --- 檢查 TextID (JSON 資料參照) ---
        for member in TextID:
            # 取得映射設定
            path_or_list = TextJson.mapping.get(member)

            # 純動態文字或無 Mapping，跳過
            if not path_or_list: continue

            # 統一轉成 List 處理 (為了同時支援「單一路徑 Tuple」與「多重路徑 List」)
            paths_to_check = []
            if isinstance(path_or_list, list):
                paths_to_check = path_or_list
            else:
                paths_to_check = [path_or_list]

            # 檢查列表中的每一條路徑
            for path_tuple in paths_to_check:

                # 格式防呆: 確保 tuple 至少包含 (FileID, Key...)
                if not path_tuple or len(path_tuple) < 1:
                    dbg.war(f"[TextID Config Error] {member.name} 的路徑格式錯誤: {path_tuple}")
                    error_count += 1
                    continue

                file_id = path_tuple[0]  # 第一個元素是 JsonID (例如 JsonID.DISPLAY)
                keys = path_tuple[1:]    # 剩下的是 Keys (例如 "MENU", "title")

                # 呼叫新版 get_data 進行驗證
                data = json_mg.get_data(file_id, *keys, silent=True)

                if data is None:
                    file_id_str = file_id.name if hasattr(file_id, 'name') else str(file_id)

                    dbg.war(f"[TextID JSON Error] {member.name} 找不到資料 -> File:{file_id_str}, Path:{keys}")
                    error_count += 1

        if error_count == 0:
            dbg.log("=== Layout & JSON 完整性檢查通過！ ===")
        else:
            dbg.war(f"=== 檢查完成，共發現 {error_count} 個錯誤 ===")

    @staticmethod
    def _create_item(category, name, size, pos = None):
        return LayoutItem(
            category = category,
            name = name,
            size = size,
            pos = pos or Position(0, 0, 0),
        )

    def _setup_menu(self, page: PageTable):
        # MENU
        self.menu_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.menu_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.MENU_MAIN,
                location_config.menu.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.menu_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.MENU_USER,
                location_config.menu.user_size
            ),
            target = self.menu_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_CENTER,
            gap_y = location_config.menu.gap_y
        )
        self.menu_bt_board = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.MENU_BT_BOARD,
                location_config.menu.bt_board_size
            ),
            target = self.menu_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.menu.gap_x,
            align = Align.BOTTOM_LEFT
        )

    def _setup_single_menu(self, page: PageTable):
        # SINGLE_MENU
        self.single_menu_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.SINGLE_MENU_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.single_menu_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.SINGLE_MENU_MAIN,
                location_config.single_menu.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.single_menu_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.SINGLE_MENU_USER,
                location_config.single_menu.block_size
            ),
            target = self.single_menu_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_LEFT,
        )

        self.single_menu_rects = []
        self.single_menu_levels = []
        for r in range(GameVar.GAME_LEVEL_ROW):
            for c in range(GameVar.GAME_LEVEL_COL):
                index = r * GameVar.GAME_LEVEL_COL + c

                rect_item = self.lay_mg.add_inner(
                    item = self._create_item(
                        page,
                        LayoutName.SINGLE_MENU_RECT.serial_list[index],
                        location_config.single_menu.block_size
                    ),
                    target = self.single_menu_main,
                    pos_z = PosZLayer.UI_ELEMENT.value,
                    align = Align.TOP_LEFT,
                    gap_x = c * location_config.single_menu.gap,
                    gap_y = r * location_config.single_menu.gap
                )
                self.single_menu_rects.append(rect_item)

                text_item = self.lay_mg.add_center(
                    item = self._create_item(
                        page,
                        LayoutName.SINGLE_MENU_LEVEL.serial_list[index],
                        location_config.single_menu.number_size
                    ),
                    pos_z = PosZLayer.TEXT.value,
                    target = rect_item,
                )
                self.single_menu_levels.append(text_item)

    def _setup_single_game(self, page: PageTable):
        # SINGLE
        self.single_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.SINGLE_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.single_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.GAME_MAIN.serial_list[0],
                location_config.game_s.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )

        self.single_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SLOT.serial_list[0],
                location_config.game_s.slot_size
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.TOP_LEFT
        )
        self.single_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO.serial_list[0],
                location_config.game_s.combo_size,
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.CENTER_LEFT
        )
        self.single_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO_NUMBER.serial_list[0],
                location_config.game_s.combo_number_size,
            ),
            target = self.single_combo,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_s.gap_x,
            align = Align.CENTER_LEFT
        )
        self.single_score = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SCORE.serial_list[0],
                location_config.game_s.score_size,
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.BOTTOM_LEFT
        )
        self.single_score_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.BASE_NUMBER_BIG.serial_list[0],
                location_config.game_s.score_number_size,
            ),
            target = self.single_score,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_s.gap_x,
            align = Align.CENTER_LEFT
        )
        self.single_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_KO.serial_list[0],
                location_config.game_s.ko_size,
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.ko_gap_x * (-1),
            gap_y = location_config.game_s.ko_gap_y,
            align = Align.CENTER_LEFT
        )

        self.single_board = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_BOARD,
                location_config.game_s.board_size
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.board_gap_x,
            gap_y = location_config.game_s.board_gap_y,
            align = Align.BOTTOM_LEFT
        )
        self.single_target_time = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_TARGET_TIME,
                location_config.game_s.target_time_size
            ),
            target = self.single_board,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_s.target_gap_x,
            gap_y = location_config.game_s.target_gap_y,
            align = Align.TOP_LEFT
        )
        self.single_target_score = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.GAME_TARGET_SCORE,
                location_config.game_s.target_score_size
            ),
            target = self.single_target_time,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_CENTER
        )

        self.single_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK,
                location_config.game_s.clock_size,
            ),
            target = self.single_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.gap_x * (-1),
            align = Align.TOP_LEFT
        )
        self.single_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_MIN.serial_list[0],
                location_config.game_s.clock_number_size
            ),
            target = self.single_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_s.gap_x,
            gap_y = location_config.game_s.x2gap_y * (-1),
            align = Align.BOTTOM_LEFT
        )
        self.single_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_SEC.serial_list[0],
                location_config.game_s.clock_number_size
            ),
            target = self.single_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_s.gap_x * (-1),
            gap_y = location_config.game_s.x2gap_y * (-1),
            align = Align.BOTTOM_RIGHT
        )

    def _setup_double_game(self, page: PageTable):
        # DOUBLE - Common
        self.double_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.DOUBLE_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.double_clock = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK,
                location_config.game_d.clock_size,
            ),
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_y = location_config.game_d.gap_y_player1,
        )
        self.double_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_MIN.serial_list[0],
                location_config.game_d.clock_number_size
            ),
            target = self.double_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_d.gap_x,
            gap_y = location_config.game_d.d2x3gap_y * (-1),
            align = Align.BOTTOM_LEFT
        )
        self.double_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_SEC.serial_list[0],
                location_config.game_d.clock_number_size
            ),
            target = self.double_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_d.gap_x * (-1),
            gap_y = location_config.game_d.d2x3gap_y * (-1),
            align = Align.BOTTOM_RIGHT
        )

        # DOUBLE - Player 1
        self.double_1_main = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.GAME_MAIN.serial_list[0],
                location_config.game_d.main_size,
                location_config.game_d.main_pos
            ),
        )
        self.double_1_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SLOT.serial_list[0],
                location_config.game_d.slot_size
            ),
            target = self.double_1_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.TOP_LEFT
        )
        self.double_1_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO.serial_list[0],
                location_config.game_d.combo_size,
            ),
            target = self.double_1_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_1_score = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SCORE.serial_list[0],
                location_config.game_d.score_size,
            ),
            target = self.double_1_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.BOTTOM_LEFT
        )
        self.double_1_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO_NUMBER.serial_list[0],
                location_config.game_d.combo_number_size,
            ),
            target = self.double_1_combo,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_d.gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_1_score_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.BASE_NUMBER_BIG.serial_list[0],
                location_config.game_d.score_number_size,
            ),
            target = self.double_1_score,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_d.gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_1_ko = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_KO.serial_list[0],
                location_config.game_d.ko_size,
            ),
            target = self.double_1_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.ko_gap_x,
            gap_y = location_config.game_d.ko_gap_y,
            align = Align.CENTER_LEFT
        )

        # DOUBLE - Player 2
        self.double_2_main = self.lay_mg.add_symmetric(
            item = self._create_item(
                page,
                LayoutName.GAME_MAIN.serial_list[1],
                location_config.game_d.main_size,
            ),
            target = self.double_1_main,
            pos_z = PosZLayer.MAIN.value,
            axis = 'vertical',
            gap_x = location_config.game_d.gap_x_slot2 * (-1)
        )
        self.double_2_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SLOT.serial_list[1],
                location_config.game_d.slot_size,
            ),
            target = self.double_2_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.TOP_LEFT
        )
        self.double_2_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO.serial_list[1],
                location_config.game_d.combo_size,
            ),
            target = self.double_2_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_2_score = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SCORE.serial_list[1],
                location_config.game_d.score_size,
            ),
            target = self.double_2_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.x2gap_x,
            align = Align.BOTTOM_LEFT
        )
        self.double_2_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO_NUMBER.serial_list[1],
                location_config.game_d.combo_number_size,
            ),
            target = self.double_2_combo,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_d.gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_2_score_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.BASE_NUMBER_BIG.serial_list[1],
                location_config.game_d.score_number_size,
            ),
            target = self.double_2_score,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_d.gap_x,
            align = Align.CENTER_LEFT
        )
        self.double_2_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_KO.serial_list[1],
                location_config.game_d.ko_size,
            ),
            target = self.double_2_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_d.ko_gap_x * (-1),
            gap_y = location_config.game_d.ko_gap_y,
            align = Align.CENTER_LEFT
        )

    def _setup_endless_game(self, page: PageTable):
        # ENDLESS
        self.endless_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.ENDLESS_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.endless_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.GAME_MAIN.serial_list[0],
                location_config.game_s.main_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.endless_slot = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SLOT.serial_list[0],
                location_config.game_s.slot_size
            ),
            target = self.endless_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.TOP_LEFT
        )
        self.endless_combo = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO.serial_list[0],
                location_config.game_s.combo_size,
            ),
            target = self.endless_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.CENTER_LEFT
        )
        self.endless_score = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.GAME_SCORE.serial_list[0],
                location_config.game_s.score_size,
            ),
            target = self.endless_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.x2gap_x,
            align = Align.BOTTOM_LEFT
        )
        self.endless_combo_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.GAME_COMBO_NUMBER.serial_list[0],
                location_config.game_s.combo_number_size,
            ),
            target = self.endless_combo,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_s.gap_x,
            align = Align.CENTER_LEFT
        )
        self.endless_score_number = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.BASE_NUMBER_BIG.serial_list[0],
                location_config.game_s.score_number_size,
            ),
            target = self.endless_score,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.game_s.gap_x,
            align = Align.CENTER_LEFT
        )
        self.endless_clock = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK,
                location_config.game_s.clock_size,
            ),
            target = self.endless_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.gap_x * (-1),
            align = Align.TOP_LEFT
        )
        self.endless_clock_min = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_MIN.serial_list[0],
                location_config.game_s.clock_number_size
            ),
            target = self.endless_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_s.gap_x,
            gap_y = location_config.game_s.x2gap_y * (-1),
            align = Align.BOTTOM_LEFT
        )
        self.endless_clock_sec = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.GAME_CLOCK_SEC.serial_list[0],
                location_config.game_s.clock_number_size
            ),
            target = self.endless_clock,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.game_s.gap_x * (-1),
            gap_y = location_config.game_s.x2gap_y * (-1),
            align = Align.BOTTOM_RIGHT
        )
        self.endless_ko = self.lay_mg.add_left_of(
            item = self._create_item(
                page,
                LayoutName.GAME_KO.serial_list[0],
                location_config.game_s.ko_size,
            ),
            target = self.endless_main,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap_x = location_config.game_s.ko_gap_x * (-1),
            gap_y = location_config.game_s.ko_gap_y,
            align = Align.CENTER_LEFT
        )

    def _setup_sys_config(self, page: PageTable):
        self.song_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.SYS_CONFIG_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.song_main = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_MAIN,
                location_config.sys_config.main_size,
            ),
            pos_z = PosZLayer.MAIN.value,
            gap_x = location_config.sys_config.main_gap_x
        )
        self.song_name = self.lay_mg.add_right_of(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_NAME,
                location_config.sys_config.song_name_size
            ),
            target = self.song_main,
            pos_z = PosZLayer.TEXT.value,
            gap_x = location_config.sys_config.gap_x,
            align = Align.TOP_LEFT
        )
        self.song_block = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_BLOCK,
                location_config.sys_config.song_block_size
            ),
            target = self.song_name,
            pos_z = PosZLayer.UI_ELEMENT.value,
            gap = location_config.sys_config.block_gap_y,
            align = Align.CENTER_LEFT
        )
        self.window_scale_size = self.lay_mg.add_below(
            item = self._create_item(
                page,
                LayoutName.SYS_WINDOW_SCALE,
                location_config.sys_config.window_scale_size
            ),
            target = self.song_block,
            pos_z = PosZLayer.TEXT.value,
            gap = location_config.sys_config.window_scale_gap_y,
            align = Align.CENTER
        )
        self.sys_config_user = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.SYS_SONG_USER,
                location_config.sys_config.user_size,
            ),
            target = self.song_main,
            pos_z = PosZLayer.TOP_OVERLAY.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.sys_config.user_gap_x * (-1),
            gap_y = location_config.sys_config.user_gap_y,
        )

    def _setup_help(self, page: PageTable):
        # HELP
        self.help_bg = self.lay_mg.add_item(
            item = self._create_item(
                page,
                LayoutName.HELP_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.help_panel = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.HELP_PANEL,
                location_config.help.panel_size
            ),
            pos_z = PosZLayer.MAIN.value,
            gap_y = location_config.help.panel_gap_y * (-1)
        )
        self.help_lace = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.HELP_LACE,
                location_config.help.lace_size
            ),
            pos_z = PosZLayer.DECORATION.value,
            gap_y = location_config.help.lace_gap_y
        )
        self.help_option_title = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.HELP_OPTION_TITLE,
                location_config.help.option_title_size,
            ),
            target = self.help_panel,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.help.title_gap_x,
            gap_y = location_config.help.title_gap_y
        )

        self.help_option_desc_sl = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.HELP_OPTION_DESC,
                location_config.help.option_desc_size,
            ),
            target = self.help_lace,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.help.desc_gap_x,
            gap_y = location_config.help.desc_gap_y
        )

    def _setup_rank(self, page: PageTable):
        # RANK
        self.rank_bg = self.lay_mg.add_item(
            self._create_item(
                page,
                LayoutName.RANK_BG,
                Size(ScreenConfig.width, ScreenConfig.height),
                Position(0, 0, PosZLayer.BACKGROUND.value),
            ),
        )
        self.rank_underline = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.RANK_UNDERLINE,
                location_config.rank.under_line_size
            ),
            pos_z = PosZLayer.MAIN.value,
        )
        self.rank_frame = self.lay_mg.add_center(
            item = self._create_item(
                page,
                LayoutName.RANK_FRAME,
                location_config.rank.frame_size
            ),
            pos_z = PosZLayer.DECORATION.value,
        )

        self.rank_ranking = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.RANK_RANKING,
                location_config.rank.ranking_size
            ),
            target = self.rank_underline,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.rank.ranking_gap_x,
            gap_y = location_config.rank.ranking_gap_y * (-1)
        )
        self.rank_min = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.RANK_MIN,
                location_config.rank.min_size,
            ),
            target = self.rank_underline,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.rank.min_gap_x,
            gap_y = location_config.rank.gap_y * (-1)
        )
        self.rank_sec = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.RANK_SEC,
                location_config.rank.sec_size,
            ),
            target = self.rank_underline,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.rank.sec_gap_x,
            gap_y = location_config.rank.gap_y * (-1)
        )
        self.rank_fraction = self.lay_mg.add_inner(
            item = self._create_item(
                page,
                LayoutName.RANK_FRACTION,
                location_config.rank.fraction_size
            ),
            target = self.rank_underline,
            pos_z = PosZLayer.TEXT.value,
            align = Align.TOP_LEFT,
            gap_x = location_config.rank.fraction_gap_x,
            gap_y = location_config.rank.gap_y * (-1)
        )

layout_mg = LayoutManager(ScreenConfig.width, ScreenConfig.height)

layout_collection = LayoutCollection(layout_mg)
