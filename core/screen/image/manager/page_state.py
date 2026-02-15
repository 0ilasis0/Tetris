import pygame

from core.screen.image.variable import ImageProfile
from core.ui_layout.variable import LayoutItem
from core.variable import PageTable


class PageStateManager:
    """負責管理各頁面的圖片引用與渲染隊列 (Context Management)"""
    def __init__(self):
        self.current_page: PageTable = None # 需由 Manager 初始化

        # 頁面圖片引用：{ layout_name: surface }
        self.page_images: dict[PageTable, dict[str, pygame.Surface]] = {p: {} for p in PageTable}

        # 渲染隊列：LayoutItem list
        self.render_queues: dict[PageTable, list[LayoutItem]] = {p: [] for p in PageTable}

        # 多圖資源狀態緩存
        self.multi_state_resources: dict[tuple[PageTable, str], ImageProfile] = {}

    def set_current_page(self, page: PageTable):
        self.current_page = page

    def is_page_loaded(self, page: PageTable) -> bool:
        return len(self.render_queues[page]) > 0

    def clear_page_data(self, page: PageTable):
        self.page_images[page].clear()
        self.render_queues[page].clear()

        # 清除該頁面的 multi_state 記錄
        keys_to_remove = [k for k in self.multi_state_resources.keys() if k[0] == page]
        for k in keys_to_remove:
            del self.multi_state_resources[k]

    def register_image(self, page: PageTable, name: str, surface: pygame.Surface):
        self.page_images[page][name] = surface

    def register_render_item(self, page: PageTable, item: LayoutItem):
        self.render_queues[page].append(item)

    def sort_render_queue(self, page: PageTable):
        self.render_queues[page].sort(key=lambda x: x.pos.z)

    def get_render_queue(self, page: PageTable) -> list[LayoutItem]:
        return self.render_queues.get(page, [])

    def get_image(self, page: PageTable, name: str) -> pygame.Surface | None:
        return self.page_images.get(page, {}).get(name)
