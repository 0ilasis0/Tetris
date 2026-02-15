from abc import ABC, abstractmethod
from typing import Any, Type

from core.debug import dbg
from core.screen.variable import ScreenConfig
from core.ui_layout.scale.preset.base import (ScaleDraw, ScaleFont,
                                              ScaleMapGrid, ScaleZoom)
from core.ui_layout.scale.preset.game import ScaleGameD, ScaleGameS
from core.ui_layout.scale.preset.help import ScaleHelp
from core.ui_layout.scale.preset.menu import ScaleMenu
from core.ui_layout.scale.preset.rank import ScaleRank
from core.ui_layout.scale.preset.single_menu import ScaleSingleMenu
from core.ui_layout.scale.preset.sys_config import ScaleSysConfig
from core.ui_layout.variable import LayoutItem
from core.variable import GridPoint, Position, Size


class IHasLayout(ABC):
    """
    凡是繼承此類的物件，都承諾會提供一個 LayoutItem
    """
    @property
    @abstractmethod
    def layout_ui(self) -> LayoutItem: pass



class LocationConfig:
    # 僅告訴系統有這東西，實際不會用
    menu: ScaleMenu
    single_menu: ScaleSingleMenu
    game_s: ScaleGameS
    game_d: ScaleGameD
    font: ScaleFont
    zoom: ScaleZoom
    map_grid: ScaleMapGrid
    draw: ScaleDraw
    sys_config: ScaleSysConfig
    help: ScaleHelp
    rank: ScaleRank

    def __init__(self) -> None:
        # 建立分類實例
        self._config_registry: list[tuple[str, Type[Any]]] = [
            ("menu", ScaleMenu),
            ("single_menu", ScaleSingleMenu),
            ("game_s", ScaleGameS),
            ("game_d", ScaleGameD),
            ("font", ScaleFont),
            ("zoom", ScaleZoom),
            ("map_grid", ScaleMapGrid),
            ("draw", ScaleDraw),
            ("sys_config", ScaleSysConfig),
            ("help", ScaleHelp),
            ("rank", ScaleRank),
        ]

        # 內部儲存原始設計稿資料 (Source of Truth)
        # 結構: {'menu': ScaleMenu(raw), 'font': ScaleFont(raw)...}
        self._source_data: dict[str, Any] = {}

        for name, cls in self._config_registry:
            # 建立原始資料 (設計稿數值)
            raw_obj = cls()
            self._source_data[name] = raw_obj

            # 建立輸出容器 (預設先給空的或跟原始一樣，稍後會被覆蓋)
            output_obj = cls()

            # 綁定到 self 上，讓外部可以用 self.menu 存取
            setattr(self, name, output_obj)

        # 初次計算
        self.reload_setup()

    def reload_setup(self):
        for name, raw_obj in self._source_data.items():
            # 取得 self 上對應的目標物件
            target_obj = getattr(self, name)
            # 執行縮放計算
            self._update_group(raw_obj, target_obj)

    def _update_group(self, raw_group, target_group):
        """ 將 raw_group 的所有屬性縮放後填入 target_group """
        for key, val in vars(raw_group).items():
            scaled_val = self._scale_any(val)
            setattr(target_group, key, scaled_val)

    def _scale_any(self, val: Any) -> Any:
        """ 遞迴判斷型別並縮放 """
        # 遍歷原始資料的所有屬性
        if isinstance(val, int):
            return self._scale(val)
        elif isinstance(val, float):
            return self._scale(int(val))
        elif isinstance(val, Size):
            return self._scale_size(val)
        elif isinstance(val, Position):
            return self._scale_pos(val)
        elif isinstance(val, list):
            return [self._scale_any(v) for v in val]
        elif isinstance(val, dict):
            return {k: self._scale_any(v) for k, v in val.items()}

        return val

    @staticmethod
    def _scale(val: int) -> int:
        """ 將設計稿數值 (1980x1080) 轉換為當前螢幕數值 """
        return int(val * ScreenConfig.RATIO)

    @staticmethod
    def _scale_size(size: Size) -> Size:
        return Size(size.width * ScreenConfig.RATIO, size.height * ScreenConfig.RATIO)

    @staticmethod
    def _scale_pos(pos: Position) -> Position:
        return Position(pos.x * ScreenConfig.RATIO, pos.y * ScreenConfig.RATIO, pos.z)

location_config = LocationConfig()
