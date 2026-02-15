from abc import ABC, abstractmethod
from enum import Enum, auto
from typing import Any


class IHoverHandler(ABC):
    """
    [Hover 行為介面]
    所有滑鼠懸停的邏輯都必須繼承此類別，並實作 on_enter 與 on_exit。
    """
    @abstractmethod
    def on_enter(self, target: Any):
        """ 當滑鼠移入時觸發 """
        pass
    @abstractmethod
    def on_exit(self, target: Any):
        """ 當滑鼠移出時觸發 """
        pass


class InterState(Enum):
    NORMAL = auto()      # 一般選取
    TARGETING = auto()   # 瞄準模式 (技能、指定攻擊)
