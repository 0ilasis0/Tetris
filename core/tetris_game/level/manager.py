from core.debug import dbg
from core.tetris_game.level.variable import LevelConfig, LevelVar
from core.tetris_game.variable import GameState, GameVar


class LevelManager:
    def __init__(
            self,
            difficult_table: dict = LevelConfig.difficult_table,
            max_level: int = LevelConfig.MAX_LEVEL
        ):
        self.difficult_table = difficult_table
        self.max_level = max_level
        self.current_level = -1
        self.last_time = None
        # 初始時同步 current_difficult
        self.current_difficult = self.difficult_table.get(self.current_level, self.difficult_table[self.max_level])

    def update_level(self, player, score = None, level = None):
        """
        根據分數更新等級
        可以用線性、權重或分數門檻決定升級
        """
        if score is not None:
            new_level = max(lvl for s, lvl in LevelConfig.level_table_endless.items() if score >= s)
        elif level is not None:
            new_level = min(level, self.max_level)
        else:
            dbg.error('score and level is None')
            return

        if new_level > self.current_level or level is not None:
            self.current_level = new_level

            # 同步 current_difficult
            self.current_difficult = self.difficult_table.get(self.current_level, self.difficult_table[self.max_level])
            player.drop_clock = self._get_drop_clock()

    def _get_drop_clock(self):
        return self.current_difficult[LevelVar.DROP_CLOCK]

    def get_raise_lines(self):
        return self.current_difficult[LevelVar.RAISE_LINE]

    def get_raise_interval(self):
        return self.current_difficult[LevelVar.RAISE_INTERVAL]

    def reset(self, player):
        player.drop_clock = GameVar.DROP_CLOCK
        self.current_level = -1



class SingleLevelManager:
    def __init__(self) -> None:
        self.current_display = {
           LevelVar.FRACTION: None,
            LevelVar.MIN: None,
            LevelVar.SEC: None
        }
        self.current_limit_time: int = None

    def update_single_mode_targets(self, current_level):
        """ 更新單人遊戲的 分 秒 分數 與目標 """
        if current_level not in LevelConfig.level_table_single:
            dbg.error(f"Level {current_level} not found in single mode table")
            return False

        cfg = LevelConfig.level_table_single[current_level]
        self.current_display.update(cfg)
        self.current_limit_time = cfg[LevelVar.MIN] * 60 + cfg[LevelVar.SEC]

        return True

    def check_single_clear_status(self, current_score, elapsed_min, elapsed_sec):
        """
        檢查單人模式狀態
        """
        elapsed_time = elapsed_min * 60 + elapsed_sec

        # 檢查時間 分數，改變遊戲狀態
        if current_score >= self.current_display.get(LevelVar.FRACTION):
            if elapsed_time <= self.current_limit_time:
                return GameState.WIN
            else:
                return GameState.GAMEOVER

        # 檢查：是否超時
        if elapsed_time > self.current_limit_time:
            return GameState.GAMEOVER

        return None

single_level_mg = SingleLevelManager()
