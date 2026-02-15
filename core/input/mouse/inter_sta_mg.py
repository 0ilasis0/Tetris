from typing import Any, Callable

from core.input.mouse.variable import InterState


class InteractionStateManager:
    def __init__(self):
        self.state = InterState.NORMAL

        # 存 "當玩家點擊有效目標時，要執行的函式"
        self._on_target_confirm: Callable[[Any], bool] | None = None
        self._on_cancel: Callable[[], None] | None = None

    def enter_targeting_mode(self, on_confirm_callback: Callable[[Any], bool], on_cancel_callback: Callable = None):
        """
        通用瞄準接口
        :param on_confirm_callback: 接收 (target_entity) 並回傳 bool (成功與否)
        """
        self.state = InterState.TARGETING
        self._on_target_confirm = on_confirm_callback
        self._on_cancel = on_cancel_callback

    def handle_map_click(self, clicked_entity):
        """ 統一處理地圖點擊 """
        # --- [一般模式]：處理 選取 與 發兵 ---
        if self.state == InterState.NORMAL:
            self._handle_normal_interaction(clicked_entity)

        # --- [瞄準模式]：執行 技能 ---
        elif self.state == InterState.TARGETING:
            if self._on_target_confirm:
                success = self._on_target_confirm(clicked_entity)
                if success:
                    self.to_normal_mode()

    def cancel(self):
        """ 取消 """
        if self.state != InterState.NORMAL:
            if self._on_cancel:
                self._on_cancel()
            self.to_normal_mode()
            return True
        return False

    def to_normal_mode(self):
        ''' 回到未點選狀態 '''
        self.state = InterState.NORMAL
        self._on_target_confirm = None
        self._on_cancel = None

    def _handle_normal_interaction(self, target_building: "BuildingEntity | None"):
        """
        統一處理所有建築的點擊邏輯
        """
        pass

inter_sta_mg = InteractionStateManager()
