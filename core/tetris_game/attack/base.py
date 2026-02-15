import random

from core.debug import dbg
from core.tetris_game.base import Field, Tetromino
from core.tetris_game.variable import GameVar


class Attack:
    def __init__(self, enabled: bool = False):
        self.enabled = enabled    # 是否啟用攻擊模式
        self.attack = 0           # 攻擊點數
        self.attack_enable = False# 確定現在已經有attack_mgr.attack的值能準備攻擊
        self.ko_counter = 0       # KO 次數
        self.player = None

    def update(self ,player ,cleared_lines: int):
        if cleared_lines > 0 or (player.combo != 0):
            self.attack += max(int((cleared_lines - 1) * 1.5), 0) + round(min(player.combo, 8) * 0.5)

    def raise_bottom(self, player, lines_to_raise: int):
        """
        將場地底部上升多行，每行都檢查 KO
        lines_to_raise: 根據此參數決定上升幾格
        """
        for _ in range(lines_to_raise):
            # 先檢查 KO
            if not self.check_ko(player.field):
                return self.ko_counter, False  # 玩家被 KO

            # 準備要新增的垃圾列
            new_row = [GameVar.RAISE_COLOR] * player.field.width_block
            mine_position = random.randint(0, player.field.width_block - 1)
            new_row[mine_position] = GameVar.MINE_COLOR

            # 檢查是否會撞擊玩家當前方塊
            if self.check_raise_collision(player.field, player.current_tetromino):
                try:
                    player.freeze()
                except Exception as e:
                    dbg.error(f"raise_bottom: freeze error {e}")

            # --- 安全地上升一行 ---
            player.field.grid.pop(0)
            player.field.grid.append(new_row)

        # 全部上升成功
        return self.ko_counter, True # 玩家還能繼續

    def check_raise_collision(self, field: Field, tetromino: Tetromino):
        """
        模擬場地上升一行，檢查玩家方塊是否會撞擊垃圾列或最底部。
        """
        shape = tetromino.get_shape()
        bottom_cells = {}

        # 找出每個 x 的最底格
        for i in range(GameVar.CELL_BLOCK):
            for j in range(GameVar.CELL_BLOCK):
                idx = i * GameVar.CELL_BLOCK + j
                if idx in shape:
                    x = int(tetromino.x + j)
                    y = int(tetromino.y + i)
                    bottom_cells[x] = max(bottom_cells.get(x, -1), y)
        # 檢查是否會撞擊垃圾列或場地底部
        for x, y in bottom_cells.items():
            # 如果玩家方塊已經在最底部 → 撞擊
            if y >= field.height_block - 1:
                return True
            # 下方一格是垃圾列 → 撞擊
            if field.grid[y + 1][x] in (GameVar.RAISE_COLOR, GameVar.MINE_COLOR):
                return True

        return False


    def check_ko(self, field: Field):
        """
        檢查最上方是否有方塊阻塞，並更新 KO 次數
        """
        top_row = field.grid[0]

        if any(cell != GameVar.EMPTY_COLOR for cell in top_row):
            self.ko_counter += 1
            # 消除 RAISE_COLOR 方塊並讓剩餘方塊沉底
            field.grid = self.collapse_raise(field)
            if self.ko_counter >= GameVar.MAX_KO_COUNT:
                return False  # 玩家被 KO
        return True

    def check_mine_collision(self, tetromino: Tetromino, field: Field) -> bool:
        triggered = False
        for i in range(4):
            x, y = tetromino.get_cell_position(i)

            # 下一步要往下落的位置
            next_y = y + 1

            # 確認沒有超出邊界
            if 0 <= next_y < field.height_block and 0 <= x < field.width_block:
                if field.grid[next_y][x] == GameVar.MINE_COLOR:
                    triggered = True

                    # 引爆效果：消掉該行 + 補空行
                    field.grid.pop(next_y)
                    field.grid.insert(0, [GameVar.EMPTY_COLOR] * field.width_block)
                    break
        return triggered

    def collapse_raise(self, field: Field):
        """
        將場地中所有 RAISE_COLOR 和 MINE_COLOR 方塊消除，
        剩餘方塊沉到底部，空格補到上方，左右位置保持不變
        """
        new_grid = [[GameVar.EMPTY_COLOR]*field.width_block for _ in range(field.height_block)]
        # 從底部開始放
        target_row = field.height_block - 1

        # 從下往上掃描原始格子
        for row in reversed(field.grid):
            filtered_row = []
            for cell in row:
                if cell in (GameVar.RAISE_COLOR, GameVar.MINE_COLOR):
                    filtered_row.append(GameVar.EMPTY_COLOR)
                else:
                    filtered_row.append(cell)
            # 如果這行有方塊，就放到 target_row
            if any(cell != GameVar.EMPTY_COLOR for cell in filtered_row):
                new_grid[target_row] = filtered_row
                target_row -= 1  # 往上移一行準備下一次放

        return new_grid

    def clear_attack(self):
        self.attack_enable = False
        self.attack = 0

    def reset(self):
        self.enabled = False
        self.clear_attack()
        self.ko_counter = 0
