from pathlib import Path

import pygame

from core.debug import dbg
from core.screen.image.processor import SpriteSlicer
from core.screen.image.variable import ImageProfile, ScaleMode


class ImagePipeline:
    """負責圖片的 IO 讀取、數學變換、切割運算 (Stateless)"""

    @staticmethod
    def load_raw_file(path: str | Path) -> pygame.Surface | None:
        try:
            return pygame.image.load(str(path)).convert_alpha()
        except Exception as e:
            dbg.war(f"Load image failed: {path}, {e}")
            return None

    @staticmethod
    def slice_sprite(raw_sheet: pygame.Surface, profile: ImageProfile) -> list[pygame.Surface]:
        return SpriteSlicer.slice(raw_sheet, profile)

    @staticmethod
    def apply_transform(surface: pygame.Surface, profile: ImageProfile, size_tuple: tuple | None) -> pygame.Surface:
        p = surface

        # 縮放
        if size_tuple:
            if profile.scale_mode == ScaleMode.STRETCH:
                p = pygame.transform.smoothscale(p, size_tuple)

        # 翻轉
        if profile.flip_x or profile.flip_y:
            p = pygame.transform.flip(p, profile.flip_x, profile.flip_y)

        # 旋轉
        if profile.angle != 0:
            p = pygame.transform.rotate(p, profile.angle)

        # 透明度
        if profile.alpha < 255:
            p = p.copy()
            p.set_alpha(profile.alpha)

        return p

    @staticmethod
    def get_mask(surface: pygame.Surface) -> pygame.mask.Mask:
        """
        取得圖片的遮罩 (用於精確碰撞檢測)
        這可以用來偵測「斜的」圖片範圍
        """
        return pygame.mask.from_surface(surface)
