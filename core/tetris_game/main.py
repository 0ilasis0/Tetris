from core.base import Stopwatch, global_timer
from core.page.navigation import base_nav
from core.tetris_game.manager import TetrisCore, player0
from core.tetris_game.mode.double import main_double
from core.tetris_game.mode.endless import main_endless
from core.tetris_game.mode.single import main_single
from core.tetris_game.variable import GameState
from core.variable import PageTable

game_watch = Stopwatch()

def main_tetris_game(player: TetrisCore, current_page: PageTable):
    # 若是 STATE_GAMEOVER 自動跳回前一頁面
    if player.state == GameState.GAMEOVER:
        base_nav.back_to_prev(current_page)
    if player.state == GameState.WIN and current_page == PageTable.SINGLE:
        if player.level_mg.current_level <= player.level_mg.max_level:
            base_nav.single_menu_mg.unlock_level(player.level_mg.current_level + 1)
        base_nav.back_to_prev(current_page)

    # 遊戲FPS依據
    dt = global_timer.get_dt()
    player.drop_timer += dt

    # 一般機制(掉落、方塊碰撞、分數更新...)
    if player.drop_timer > player.drop_clock:
        if not player.field.check_collision(player.current_tetromino, 0, 1):
            player.current_tetromino.y += 1
        else:
            player.freeze()
        player.drop_timer = 0



class IndividualTetris:
    def __init__(self) -> None:
        # 建立PageTable對TetrisGame映射表map
        self.mode_map = {}
        self._set()

        self.player: TetrisCore = player0
        self.min = 0
        self.sec = 0

    def _set(self):
        for table in PageTable:
            method_name = table.name
            if hasattr(self, method_name):
                self.mode_map[table] = getattr(self, method_name)

    def main_process(self, category, player, min, sec) -> None:
        self.player = player
        self.min = min
        self.sec = sec

        func = self.mode_map.get(category)
        if func:
            func()
        else:
            raise ValueError(f"未知的 category 模式: {category}")

    def SINGLE(self):
        main_single(self.player, self.sec, self.min)

    def DOUBLE(self):
        main_double()

    def ENDLESS(self):
        main_endless(self.player, self.sec, self.min)

        # 遊戲結束進行排名計算
        if self.player.state == GameState.GAMEOVER:
            base_nav.rank_mg.add_score(self.min, int(self.sec), self.player.score)

individual_tetris = IndividualTetris()
