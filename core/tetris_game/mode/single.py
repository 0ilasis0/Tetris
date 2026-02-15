from core.tetris_game.level.manager import single_level_mg
from core.tetris_game.manager import TetrisCore


def main_single(player: TetrisCore, sec: int, min: int,):
    total_time = sec + min * 60

    # 第一次觸發初始化
    if not getattr(player.level_mg, "last_time", -1):
        _init_single(player, total_time)

    # 垃圾方塊機制
    if player.level_mg.last_time is not None:
        interval = player.level_mg.get_raise_interval()
        if total_time - player.level_mg.last_time >= interval:
            lines = player.level_mg.get_raise_lines()
            player.attack_mg.raise_bottom(player, lines)
            player.level_mg.last_time = total_time   # 更新觸發時間

    # 檢查通關
    state = single_level_mg.check_single_clear_status(player.score, min, sec)
    if state:
        player.state = state

def _init_single(player: TetrisCore, total_time: int):
    player.level_mg.last_time = total_time
    single_level_mg.update_single_mode_targets(player.level_mg.current_level)
