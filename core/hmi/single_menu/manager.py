from typing import TYPE_CHECKING

from core.debug import dbg
from core.hmi.base import HMIBaseManager
from core.hmi.grid import GridManager
from core.page.variable import GridParameter, GridThing
from core.variable import PageTable

if TYPE_CHECKING:
    from core.tetris_game.manager import TetrisCore


class SingleMenuManager(HMIBaseManager):
    """ [View/Controller] 負責業務邏輯：處理按鍵、換頁、存檔路徑 """
    def __init__(self, base_nav, player: "TetrisCore"):
        super().__init__(base_nav, PageTable.SINGLE_MENU)

        self.player = player

        # 初始化 Model
        self.grid_mg = GridManager(
            GridParameter.SINGLE_MENU_LEVEL_ROW,
            GridParameter.SINGLE_MENU_LEVEL_COLS
        )

        self._init_grid_state()

    # --- 初始化流程 ---
    def _init_grid_state(self):
        path = self._save_path
        if path:
            self.grid_mg.load_from_global_storage(path[0], *path[1:])

        # 檢查是否為空 (初次遊玩)
        first_cell = self.grid_mg.get_cell(0, 0)
        if not first_cell or first_cell.is_empty:
            self._setup_default()

    # --- 存檔路徑設定 ---
    @property
    def _save_path(self):
        from core.json.preset import SaveID, SaveJson  # 延遲引入
        path = SaveJson.mapping.get(SaveID.SINGLE_MENU_GRID)
        if not path:
            dbg.error("SaveID.SINGLE_MENU_GRID not found!")
        return path

    def _setup_default(self):
        """ 預設全解鎖 """
        for y in range(self.grid_mg.rows):
            for x in range(self.grid_mg.cols):
                self.grid_mg.set_cell(x, y, merge = False, **{GridThing.LOCK_SWITCH_: GridThing.UNLOCK})

        # 立即存檔
        path = self._save_path
        if path:
            self.grid_mg.save_to_global_storage(path[0], *path[1:])

    def unlock_level(self, level_idx):
        x = level_idx % self.grid_mg.cols
        y = level_idx // self.grid_mg.cols
        self.grid_mg.set_cell(x, y, merge = True, **{GridThing.LOCK_SWITCH_: GridThing.UNLOCK})

        path = self._save_path
        if path:
            self.grid_mg.save_to_global_storage(path[0], *path[1:])
        else:
            dbg.log(f'the {path} is not exisit')

    # --- 事件處理 (被 Keyboard 呼叫) ---
    def _enter_handle(self):
        x, y = self.hook_x, self.hook_y

        cell = self.grid_mg.get_cell(x, y)
        if not cell: return

        # 設定關卡
        self.player.level_mg.current_level = (x + y * self.grid_mg.cols)

        # 判斷解鎖
        if cell.data.get(GridThing.LOCK_SWITCH_) == GridThing.UNLOCK:
            self.base_nav.go_to_page(PageTable.SINGLE_MENU, PageTable.SINGLE)

    def _move_cursor(self, dx, dy):
        """ Grid 專用的游標移動邏輯 (循環移動) """
        # 使用 Base 裡的 self.hook_x/y
        nx = self.hook_x + dx
        ny = self.hook_y + dy

        rows = self.grid_mg.rows
        cols = self.grid_mg.cols

        # 循環邏輯 (Wrap around)
        if nx < 0: nx = cols - 1
        elif nx >= cols: nx = 0

        if ny < 0: ny = rows - 1
        elif ny >= rows: ny = 0

        # 檢查目標格子是否解鎖 ---
        target_cell = self.grid_mg.get_cell(nx, ny)
        if not target_cell: return

        is_unlocked = target_cell.data.get(GridThing.LOCK_SWITCH_) == GridThing.UNLOCK
        if not is_unlocked: return

        # 更新內部狀態
        self.hook_x = nx
        self.hook_y = ny

    def on_up(self):    self._move_cursor(0, -1)
    def on_down(self):  self._move_cursor(0, 1)
    def on_left(self):  self._move_cursor(-1, 0)
    def on_right(self): self._move_cursor(1, 0)
    def on_confirm(self): self._enter_handle()
