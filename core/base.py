from typing import Generic, List, TypeVar

import pygame

from core.screen.variable import ScreenConfig
from core.variable import SysConfig

# 這個 Stack 是一個容器，它裝的內容型別是不固定的，先用佔位符 T 表示
T = TypeVar('T')

class Stack(Generic[T]):
    def __init__(self, initial_item: T = None):
        self._items: List[T] = []
        if initial_item:
            self._items.append(initial_item)

    def push(self, item: T):
        self._items.append(item)

    def pop(self) -> T | None:
        if not self.is_empty():
            return self._items.pop()
        return None

    def peek(self) -> T | None:
        """ 取得當前頂端元素 (不移除) """
        if not self.is_empty():
            return self._items[-1]
        return None

    def is_empty(self) -> bool:
        return len(self._items) == 0

    def size(self) -> int:
        return len(self._items)

    def clear(self):
        self._items.clear()



class GlobalTimer:
    def __init__(self):
        self.clock = pygame.time.Clock()

        self.raw_dt = 0.0   # 原始 Delta Time (秒)：不受暫停/慢動作影響 (適合用於 UI 動畫)
        self.dt = 0.0       # 遊戲 Delta Time (秒)：受 time_scale 影響 (適合用於角色移動、遊戲計時)

        self.time_scale = 1.0  # 1.0 = 正常速度, 0.5 = 慢動作, 0.0 = 暫停
        self.global_time = 0.0 # 遊戲啟動後的總累計時間 (秒)

    def tick(self, target_fps):
        """ 每一幀呼叫一次，計算時間差 """
        # 回傳的是毫秒 (ms)
        ms = self.clock.tick(target_fps)

        self.raw_dt = ms / 1000
        self.dt = self.raw_dt * self.time_scale

        self.global_time += self.dt

    def get_fps(self):
        return self.clock.get_fps()

    # 一般時間功能
    def sprite_time_change(self, fps, amount):
        '''
        :fps: 為每秒幾張圖
        :amount: 為總共幾張圖
        '''
        return int((self.global_time * fps) % amount)

    def get_dt(self):
        """
        取得經過處理的 '秒數' (float)
        """
        return self.dt

    def get_raw_dt(self):
        """
        取得不受暫停影響的原始秒數
        用於：UI 動畫、滑鼠特效等不應該被暫停的元素
        """
        return self.raw_dt

    # --- 控制功能 ---
    def pause(self):
        """ 全局暫停 (角色停止，但 UI 可繼續跑) """
        self.time_scale = 0.0

    def resume(self):
        """ 恢復正常 """
        self.time_scale = 1.0

    def set_slow_motion(self, scale: float):
        """ 設定慢動作 (例如 0.5) """
        self.time_scale = scale

global_timer = GlobalTimer()


# 碼表
class Stopwatch:
    def __init__(self):
        self.elapsed_time = 0.0  # 累計時間 (秒)
        self.is_running = False

    def reset(self):
        """ 歸零 """
        self.elapsed_time = 0.0

    def start(self):
        """ 開始計時 """
        self.is_running = True

    def stop(self):
        """ 停止計時 """
        self.is_running = False

    def update(self, dt: float):
        """
        在 Game Loop 中呼叫，傳入 game_timer.dt
        這樣這個時鐘就會受到 慢動作/暫停 的影響
        """
        if self.is_running:
            self.elapsed_time += dt

    def get_min_sec(self):
        total_sec = int(self.elapsed_time)
        minutes = total_sec // 60
        seconds = total_sec % 60
        return minutes, seconds

    def get_total_seconds(self) -> float:
        return self.elapsed_time



#
# 遊戲狀態總管理
#
class CentralManager:
    def __init__(self):
        self.running = True
        self.debug_mode = True

        self.current_window = pygame.display.set_mode(
            (ScreenConfig.width, ScreenConfig.height),
            pygame.RESIZABLE
        )
        self.sys_window_scale_pending = None

    def leave_game(self, event):
        if event.type == pygame.QUIT:
            self.running = False

    def update_clock(self, target_fps = SysConfig.FPS.value):
        global_timer.tick(target_fps)

    def get_fps(self):
        return global_timer.get_fps()

central_mg = CentralManager()
