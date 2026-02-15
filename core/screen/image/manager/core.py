from enum import Enum
from pathlib import Path

import pygame

from core.base import central_mg
from core.debug import dbg
from core.path.manager import PathBase
from core.rendering.manager import render_mg
from core.screen.image.manager.page_state import PageStateManager
from core.screen.image.manager.pipeline import ImagePipeline
from core.screen.image.manager.store import ImageStore
from core.screen.image.preset import IMAGE_RESOURCE_MAP
from core.screen.image.variable import ImageProfile
from core.screen.variable import ScreenConfig
from core.ui_layout.main import layout_mg
from core.variable import BOOT_PAGE, PageTable, Position, Size


class ImgManager:
    def __init__(self):
        # 組件初始化
        self.store = ImageStore()
        self.state = PageStateManager()
        self.state.set_current_page(BOOT_PAGE)

    @property
    def current_page(self):
        return self.state.current_page

    def reload_setup(self):
        """ 視窗初始化設定 """
        if central_mg.current_window is not None:
            self.store.clear_processed_only()
            # 必須同時清除頁面引用，因為 Surface 已經失效
            for page in PageTable:
                self.state.clear_page_data(page)

        pygame.display.set_caption(ScreenConfig.title_name)

        try:
            icon_surface = pygame.image.load(str(PathBase.icon)).convert_alpha()
            pygame.display.set_icon(icon_surface)
        except Exception as e:
            dbg.war(f"Icon load failed: {e}")

        # 重新綁定當前頁面
        self._bind_images_from_layout(self.current_page)

    # =========================================================================
    # 公開介面 (Public Interface)
    # =========================================================================
    def switch_page(self, page: PageTable):
        if self.state.current_page != page:
            self.state.set_current_page(page)
            if not self.state.is_page_loaded(page):
                self._bind_images_from_layout(page)

    def switch_image_idx(self, name: str, index: int):
        current_p = self.state.current_page
        profile = self.state.multi_state_resources.get((current_p, name))
        if not profile: return

        size = layout_mg.get_item_size(current_p, name)
        surface = self.get_processed_surface(profile, size, sprite_index = index)
        self.state.register_image(current_p, name, surface)

    def clear_cache(self):
        self.store.clear_all()
        for page in PageTable:
            self.state.clear_page_data(page)
        self._bind_images_from_layout(self.state.current_page)

    def submit_static(self):
        """ 提交靜態渲染工作 """
        if central_mg.current_window is None: return

        queue = self.state.get_render_queue(self.current_page)

        for item in queue:
            surface = self.state.get_image(self.current_page, item.name)
            if surface:
                # 計算中心點對齊
                # 取得 LayoutItem 預期的中心點座標
                target_center_x = item.pos.x + item.size.width / 2
                target_center_y = item.pos.y + item.size.height / 2

                # 取得圖片的 Rect，並將其中心移到預期位置
                rect = surface.get_rect()
                rect.center = (target_center_x, target_center_y)

                # 使用修正後的 rect.topleft 進行繪製
                render_mg.add_task(
                    item.pos.z,
                    central_mg.current_window.blit,
                    surface,
                    rect.topleft
                )

    def draw_image_dynamic(
            self,
            image_id: str | Enum,
            pos: Position,
            offset_pos: Position = Position(0, 0, 0),
            size: Size | None = None,
            sprite_index: int = 0
        ):
        if central_mg.current_window is None: return

        search_key = image_id.value if isinstance(image_id, Enum) else image_id
        profile = IMAGE_RESOURCE_MAP.get(search_key)

        if not profile:
            dbg.war(f"[ImgManager] Dynamic draw failed: ID '{image_id} KEY '{search_key}' not registered.")
            return

        if size is None:
            size = layout_mg.get_item_size(self.current_page, image_id)
            if size is None: return

        surface = self.get_processed_surface(profile, size, sprite_index=sprite_index)

        # 計算中心點對齊
        base_x = pos.x + offset_pos.x
        base_y = pos.y + offset_pos.y

        # 計算目標的中心點
        center_x = base_x + size.width / 2
        center_y = base_y + size.height / 2

        # 取得圖片 Rect 並校正中心
        rect = surface.get_rect()
        rect.center = (center_x, center_y)

        render_mg.add_task(
            pos.z,
            central_mg.current_window.blit,
            surface,
            rect.topleft
        )

    # =========================================================================
    # 核心邏輯 - 資源綁定 (Core - Resource Binding)
    # =========================================================================
    def _bind_images_from_layout(self, page: PageTable):
        items = layout_mg.get_items_by_category(page)
        if items is None: return

        self.state.clear_page_data(page)

        for item in items:
            profile = IMAGE_RESOURCE_MAP.get(item.name) or IMAGE_RESOURCE_MAP.get(item.img_id)
            if not profile: continue

            # 根據 Profile 類型準備資源
            surface = None

            if profile.is_sprite_sheet:
                self.state.multi_state_resources[(page, item.name)] = profile
                self._ensure_sprite_sliced(profile)
                surface = self.get_processed_surface(profile, item.size, sprite_index=0)

            elif isinstance(profile.path, list):
                self.state.multi_state_resources[(page, item.name)] = profile
                surface = self.get_processed_surface(profile, item.size, sprite_index=0)

            else:
                surface = self.get_processed_surface(profile, item.size)

            if surface:
                self.state.register_image(page, item.name, surface)
                if profile.is_static:
                    self.state.register_render_item(page, item)

        self.state.sort_render_queue(page)

    # =========================================================================
    # 核心邏輯 - 獲取與管線 (Core - Pipeline Integration)
    # =========================================================================
    def get_processed_surface(self, profile: ImageProfile, size: Size | None, sprite_index: int | None = None) -> pygame.Surface:
        # 決定身分 (Identity)
        if profile.is_sprite_sheet:
            idx = sprite_index if sprite_index is not None else 0
            image_identity = self.store.make_raw_sprite_key(profile.path, idx)
        elif isinstance(profile.path, list):
            idx = sprite_index if sprite_index is not None else 0
            path = profile.path[idx]
            image_identity = path
        else:
            image_identity = profile.path

        # 產生快取 Key 並查表
        size_tuple = (size.width, size.height) if size else None
        full_key = self.store.make_processed_key(image_identity, size_tuple, profile)

        cached = self.store.get(full_key)
        if cached: return cached

        # Cache Miss -> 取得原始圖
        raw_surface = self._get_raw_source(image_identity)
        if raw_surface is None:
            return pygame.Surface((10, 10))

        # 執行變換
        processed = ImagePipeline.apply_transform(raw_surface, profile, size_tuple)

        # 存回 Cache
        self.store.set(full_key, processed)
        return processed

    def _get_raw_source(self, identity) -> pygame.Surface | None:
        """ 從 Store 獲取原始資源，若無則呼叫 Pipeline 讀取 """

        # 若是 Sprite 切片 Key (tuple) -> 必須在 Cache 中 (預期已由 ensure_sprite_sliced 載入)
        if isinstance(identity, tuple):
             return self.store.get(identity)

        # 若是檔案路徑 -> 嘗試從 Cache 取 RAW_FILE，若無則讀取
        file_key = self.store.make_raw_file_key(identity)
        cached_file = self.store.get(file_key)
        if cached_file: return cached_file

        # IO 讀取
        surf = ImagePipeline.load_raw_file(identity)
        if surf:
            self.store.set(file_key, surf)
        return surf

    def _ensure_sprite_sliced(self, profile: ImageProfile):
        """ 協調 Pipeline 切割並存入 Store """
        # 檢查第 0 張是否存在
        check_key = self.store.make_raw_sprite_key(profile.path, 0)
        if self.store.get(check_key): return

        # 讀取大圖
        raw_sheet = self._get_raw_source(profile.path)
        if not raw_sheet: return

        # 執行切割
        frames = ImagePipeline.slice_sprite(raw_sheet, profile)

        # 存入 Store
        for idx, frame in enumerate(frames):
            key = self.store.make_raw_sprite_key(profile.path, idx)
            self.store.set(key, frame)

img_mg = ImgManager()
