from pathlib import Path

import pygame

from core.screen.image.manager.variable import ImageKeyType
from core.screen.image.variable import ImageProfile


class ImageStore:
    """負責全域圖片快取管理 (Memory Management)"""
    def __init__(self):
        # Key 結構: (Identity, Size, Angle, FlipX, FlipY, Alpha, ScaleMode)
        self._cache: dict[tuple, pygame.Surface] = {}

    def get(self, key: tuple) -> pygame.Surface | None:
        return self._cache.get(key)

    def set(self, key: tuple, surface: pygame.Surface):
        self._cache[key] = surface

    def clear_all(self):
        self._cache.clear()

    def clear_processed_only(self):
        """清除加工後的圖片，保留 RAW 資源"""
        # 邏輯：Raw Key 長度最多為 3，Processed Key 長度為 7
        keys_to_remove = [k for k in self._cache.keys() if len(k) > 3]
        for k in keys_to_remove:
            del self._cache[k]

    def make_processed_key(self, identity, size_tuple, profile: ImageProfile) -> tuple:
        """生成加工後圖片的快取 Key"""
        return (
            identity,
            size_tuple,
            profile.angle,
            profile.flip_x,
            profile.flip_y,
            profile.alpha,
            profile.scale_mode
        )

    def make_raw_file_key(self, path: Path | str) -> tuple:
        return (path, ImageKeyType.RAW_FILE)

    def make_raw_sprite_key(self, path: Path | str, index: int) -> tuple:
        return (path, index, ImageKeyType.RAW_SPRITE)
