from operator import itemgetter

from core.base import central_mg


class RenderManager:
    def __init__(self):
        # 佇列結構: [{"z": int, "func": callable, "args": tuple, "kwargs": dict}, ...]
        self._render_queue = []

    def add_task(
            self,
            z_index: int,
            func,
            *args,
            **kwargs
        ):
        """
        加入一個繪圖任務到隊列中
        :param z_index: Z 軸層級 (越大越上層)
        :param func: 要執行的繪圖函式 (例如 window.blit 或 pygame.draw.rect)
        :param args: 函式的位置參數
        :param kwargs: 函式的關鍵字參數
        """
        self._render_queue.append({
            "z": z_index,
            "func": func,
            "args": args,
            "kwargs": kwargs
        })

    def render_all(self):
        """ 執行所有繪圖任務 (每一幀最後呼叫) """
        # 初始化畫面
        central_mg.current_window.fill((0, 0, 0))

        if not self._render_queue: return

        # 根據 Z 軸排序 (從小到大，這樣大的會蓋在小的上面)
        self._render_queue.sort(key = itemgetter("z"))

        # 執行
        for task in self._render_queue:
            task["func"](*task["args"], **task["kwargs"])

        # 清空
        self._render_queue.clear()

render_mg = RenderManager()