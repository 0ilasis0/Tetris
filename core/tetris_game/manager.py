from core.tetris_game.attack.base import Attack
from core.tetris_game.base import Field, Tetromino
from core.tetris_game.level.manager import LevelManager
from core.tetris_game.variable import GameState, GameVar


class StoreSlot:
    def __init__(self):
        self.current_slot: Tetromino | None = None

    def swap(self, current_tetromino: Tetromino) -> Tetromino:
        """
        傳入當前方塊
        return: 新的當前方塊（可能是原本暫存槽的方塊）
        """
        if self.current_slot is None:
            self.current_slot = current_tetromino.clone()
            return Tetromino()  # 返回新生成的方塊
        else:
            # 交換方塊
            temp = self.current_slot
            self.current_slot = current_tetromino.clone()
            # 回傳暫存槽方塊作為新的當前方塊
            temp.x = current_tetromino.x
            temp.y = current_tetromino.y
            return temp

    def simulation_swap(self, current_tetromino: Tetromino) -> Tetromino:
        """
        回傳交換後玩家會得到的方塊的一個複製（但不修改 slot）。
        - 若 slot 為空，回傳一個新生成的 Tetromino（代表玩家會拿到新方塊）。
        - 若 slot 有東西，回傳該 slot 的 clone 並把位置設為 current 的位置（方便 collision 檢查）。
        """
        if self.current_slot is None:
            return Tetromino()
        else:
            temp = self.current_slot.clone()
            temp.x = current_tetromino.x
            temp.y = current_tetromino.y
            return temp



class TetrisCore:
    def __init__(
            self,
            suffix_index,
            width_block = GameVar.WIDTH_BLOCK,
            height_block = GameVar.HEIGHT_BLOCK
        ):
        # 目前玩家為誰
        self.suffix_index = suffix_index
        # 場地
        self.field = Field(
            width_block = width_block,
            height_block = height_block
        )

        # 當前方塊
        self.current_tetromino = Tetromino()

        # 難度等級(LevelSystem管理)
        self.level_mg = LevelManager()

        # 攻擊/連擊（Attack 管理）
        self.attack_mg = Attack()

        # 管理暫存方塊
        self.store_slot = StoreSlot()
        self.slot_can_hold = True

        # 消行數combo、分數、墜落時間
        self.score = 0
        self.combo = 0
        self.drop_timer = 0
        self.drop_clock = GameVar.DROP_CLOCK
        # 遊戲狀態
        self.state = GameState.START

        # 生成第一個方塊
        self.new_figure()

    '''----------------- 內部運行 -----------------'''
    def new_figure(self):
        ''' 生成新方塊並檢查是否立刻碰撞，決定是否結束遊戲 '''
        # 允許玩家再次存放方塊
        self.slot_can_hold = True
        self.current_tetromino = Tetromino()

        if self.field.check_collision(self.current_tetromino):
            # KO 結算
            self.attack_mg.check_ko(self.field)
            # 遊戲 結算
            if self.attack_mg.ko_counter >= GameVar.MAX_KO_COUNT:
                self.state = GameState.GAMEOVER

    def freeze(self):
        '''
         將玩家方塊變成地圖方塊
         並且計算連擊/分數與攻擊模式
         最後生成新方塊並決定遊戲是否GAMEOVER
        '''
        # 將方塊固定到格子
        self.field.freeze(self.current_tetromino)

        # 消除行
        cleared_lines = self.field.clear_lines()

        # 地雷判斷觸發
        mine_triggered = self.attack_mg.check_mine_collision(self.current_tetromino, self.field)
        if mine_triggered:
            cleared_lines += 1

        # 分數/連擊計算
        if cleared_lines > 0:
            self.combo += 1
            self.score += int(cleared_lines * 1.5) + round(min(self.combo, 8) * 0.5)
        else:
            self.combo = 0  # 確保 lines 不會殘留

        # 攻擊模式（由 Attack 管理）
        self.attack_mg.attack_enable = True
        if self.attack_mg.enabled:
            self.attack_mg.update(self, cleared_lines)

        # 生成新方塊
        self.new_figure()

    '''----------------- 人機操作 -----------------'''
    def move_down(self):
        if not self.field.check_collision(self.current_tetromino, 0, 1):
            self.current_tetromino.y += 1
        else:
            self.freeze()

        self.drop_timer = 0

    def move_side(self, dx):
        if not self.field.check_collision(self.current_tetromino, dx, 0):
            self.current_tetromino.x += dx

    def rotate(self):
        '''自動嘗試右移，直到方塊不碰牆，如果碰到的是其他方塊（非牆）就還原旋轉'''
        old_rot = self.current_tetromino.rotation
        old_x   = self.current_tetromino.x

        self.current_tetromino.rotate()

        # 嘗試最多往右移 4 次（因為 tetromino 寬度最大為 4）
        for _ in range(GameVar.CELL_BLOCK):
            if not self.field.check_collision(self.current_tetromino):
                break  # 無碰撞就結束
            # 如果碰到左邊界，右移
            if self.current_tetromino.x < 0:
                self.current_tetromino.x += 1
            # 如果碰到右邊界，左移
            elif self.current_tetromino.x + GameVar.CELL_BLOCK > self.field.width_block:
                self.current_tetromino.x -= 1
            else:
                # 碰撞到其他方塊，還原旋轉與位置
                self.current_tetromino.rotation = old_rot
                self.current_tetromino.x = old_x
                break

    def go_space(self):
        ''' 直接落下到底部，直到碰撞 '''
        while not self.field.check_collision(self.current_tetromino):
            self.current_tetromino.y += 1
        self.current_tetromino.y -= 1
        self.freeze()

    def store_action(self):
        """
        安全的 hold/交換流程：
        1) 檢查 slot_can_hold，若 False 直接返回。
        2) 若 slot 為空，直接 swap。
        3) 暫存 current 方塊，暫時移除。
        4) 嘗試將 incoming 放在 current 原位 + kicks。
        - 如果放不下，再嘗試小幅微調。
        5) 如果仍然放不下，回復暫存的 current，取消交換。
        """
        if not self.slot_can_hold:
            return

        # slot 為空，直接交換
        if self.store_slot.current_slot is None:
            self.current_tetromino = self.store_slot.swap(self.current_tetromino)
            self.slot_can_hold = False
            return

        # 模擬 incoming（不真正 swap）
        incoming = self.store_slot.simulation_swap(self.current_tetromino)

        # 暫存 current
        saved_current = self.current_tetromino.clone()
        orig_x, orig_y = self.current_tetromino.x, self.current_tetromino.y

        kicks = [(0,0), (0,-1), (-1,0), (1,0), (0,-2), (-1,-1), (1,-1), (-1,-2), (1,-2)]

        # 嘗試放 incoming
        placed = False
        for dx, dy in kicks:
            incoming.x, incoming.y = orig_x + dx, orig_y + dy
            if not self.field.check_collision(incoming):
                placed = True
                break

        # 如果 kicks 失敗，再嘗試微調
        if not placed:
            shifts = [(0,-1), (-1,0), (1,0), (-1,-1), (1,-1)]
            for sdx, sdy in shifts:
                tmp_x, tmp_y = orig_x + sdx, orig_y + sdy
                for dx, dy in kicks:
                    incoming.x, incoming.y = tmp_x + dx, tmp_y + dy
                    if not self.field.check_collision(incoming):
                        placed = True
                        orig_x, orig_y = tmp_x, tmp_y  # 更新 current 位置
                        break
                if placed:
                    break

        # 成功放入 incoming → 真正 swap 並設定位置
        if placed:
            self.current_tetromino = self.store_slot.swap(saved_current)
            self.current_tetromino.x, self.current_tetromino.y = incoming.x, incoming.y
            self.slot_can_hold = False
            return

        # 全部失敗 → 回復暫存的 current，不做 swap
        self.current_tetromino = saved_current
        return

    def suffix_key(self, base: str):
        """
        產生對應玩家的 LayoutName key
        回傳例如 game_main_0, game_main_1
        """
        return f"{base.value}_{self.suffix_index}"

    '''----------------- reset -----------------'''
    def reset(self, attack_sw: bool = True, level_sw: bool = True):
        # 重置grid格子
        for y in range(self.field.height_block):
            for x in range(self.field.width_block):
                self.field.grid[y][x] = GameVar.EMPTY_COLOR

        # 攻擊模組初始化
        if attack_sw:
            self.attack_mg.reset()

        # 等級模組初始化
        if level_sw:
            self.level_mg.reset(self)

        self.level_mg.last_time = None

        # 重置當前方塊
        self.current_tetromino = Tetromino()
        # 重製當前下落時間
        self.drop_timer = 0
        # 重置暫存槽
        self.store_slot.current_slot = None
        self.slot_can_hold = True
        # 重置分數 / combo / state
        self.score = 0
        self.combo = 0
        self.state = GameState.START
        # 生成新方塊
        self.new_figure()


# 生成具遊戲管理系統的玩家
player0 = TetrisCore(suffix_index = 0)
player1 = TetrisCore(suffix_index = 1)
