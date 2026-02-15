import pygame

from core.base import central_mg
from core.debug import dbg
from core.font.preset import TextID, TextJson
from core.font.variable import TextProfile
from core.json.manager import json_mg
from core.path.manager import PathConfig
from core.rendering.manager import render_mg
from core.ui_layout.main import layout_mg
from core.ui_layout.scale.preset.base import ScaleFont
from core.ui_layout.variable import LayoutItem
from core.variable import BOOT_PAGE, Align, PageTable, Position


class FontManager:
    def __init__(self):
        self._font_cache = {}    # 存字體物件
        self._surface_cache = {} # 存渲染好的圖

        self.current_page: PageTable = BOOT_PAGE

    def draw_json_text(
            self,
            text_id: TextID,
            index: int = None,
            override_color = None,
            alpha = None,
            align: Align = Align.CENTER,
            offset_pos: Position = Position(0, 0, 0),
            override_pos: Position = None
        ):
        """
        根據 TextID 自動去 JSON 抓資料並繪製
        :param index: 如果 TextJson 中的對應值是 List，則使用此 index 取值
        :index: 如果只有單一路徑無list，不用填
        """
        # 查表
        json_path_or_list = TextJson.mapping.get(text_id)
        if json_path_or_list is None: return

        target_path_tuple = None

        # 判斷是否為列表模式 (多路徑)
        if isinstance(json_path_or_list, list):
            # 如果有指定 index 且合法
            if index is not None and 0 <= index < len(json_path_or_list):
                target_path_tuple = json_path_or_list[index]
            else:
                # 錯誤處理：預設取第 0 個
                dbg.war(f"TextID {text_id} requires valid index, got {index}")
                target_path_tuple = json_path_or_list[0]
        else:
            # 單一路徑模式
            target_path_tuple = json_path_or_list

        # 拆解 Tuple 為 (FileID, *Keys)
        if not target_path_tuple or len(target_path_tuple) < 1:
            return

        file_id = target_path_tuple[0]  # 第一個元素是 JsonID
        keys = target_path_tuple[1:]    # 剩下的是路徑 Keys

        # 去 JsonManager 抓資料
        content = json_mg.get_data(file_id, *keys, silent = True)

        # 防呆與渲染
        if content:
            self.draw_text(
                text_id,
                content,
                override_color = override_color,
                alpha = alpha,
                align = align,
                offset_pos = offset_pos,
                override_pos = override_pos
            )

    def draw_text(
            self,
            text_id,
            *args,
            target_layout = None,
            alpha = None,
            align: Align = Align.CENTER,
            offset_pos: Position = Position(0, 0, 0),
            override_pos: Position = None,
            override_color = None,
        ):
        """
        :text_id: TextID Enum (包含 TextProfile)
        "target_layout: 允許使用 TextID 定義好的文字樣式與內容，但強制將其繪製在另一個指定的 LayoutItem
        """
        # 取得設定檔
        profile: TextProfile = text_id.value

        final_color = override_color if override_color is not None else profile.color

        # 防止 List 被 format 轉成字串(直接把 List 當作最終內容，不要轉成字串)
        if args and profile.content == "{}" and isinstance(args[0], list):
             final_content = args[0]

        else:
            # 正常格式化流程 (處理 "Score: {}" 這種情況)
            try:
                final_content = profile.content.format(*args) if args else profile.content
            except IndexError:
                final_content = profile.content

        self._draw_inner(
            name = profile.name,
            content = final_content,
            color = final_color,
            alpha = alpha,
            font_path = profile.font,
            direction = profile.direction,
            line_spacing = profile.spacing,
            target_layout = target_layout,
            align = align,
            offset_pos = offset_pos,
            override_pos = override_pos
        )

    def _draw_inner(
            self,
            name,
            content,
            color,
            alpha,
            font_path = PathConfig.font_base,
            direction = 'horizontal',
            line_spacing: float = 1.0,
            target_layout = None,
            align: Align = Align.CENTER,
            offset_pos: Position = Position(0, 0, 0),
            override_pos: Position | None = None
        ):
        # 不管是否有 override_pos，我們都先嘗試取得 item (為了計算字體大小參考)
        item = self._resolve_target_item(target_layout, name)

        container_rect = None
        z_index = 0

        # index_z 單獨處理
        if item:
            z_index = item.pos.z
        elif override_pos is not None:
            z_index = override_pos.z
        else: return

        # 情境 A: 強制覆蓋座標
        if override_pos is not None:
            container_rect = pygame.Rect(
                round(override_pos.x),
                round(override_pos.y),
                0, 0 # Override 時通常只當作基準點，長寬設為 0
            )
        # 情境 B: 跟隨 Item 座標
        elif item:
            container_rect = pygame.Rect(
                round(item.pos.x),
                round(item.pos.y),
                round(item.size.width),
                round(item.size.height)
            )

        # 處理文字內容 (標準化為 List 與 String)
        if isinstance(content, list):
            lines_for_horizontal = content
            text_for_vertical = "".join(str(x) for x in content)
            num_lines = len(content)
        else:
            str_content = str(content)
            lines_for_horizontal = [str_content]
            text_for_vertical = str_content
            num_lines = 1

        #  計算字體大小
        if item:
            layout_h = item.size.height
            if num_lines > 1:
                font_size = int(layout_h / num_lines)
            else:
                font_size = int(layout_h)
        else:
            dbg.error(f'because haven\'t {item}, font_size is not exisit')
            font_size = ScaleFont.nor

        # 分流繪製
        if direction == 'vertical':
            self._render_vertical(
                text_for_vertical, z_index,
                font_size, color, alpha, font_path,
                container_rect, line_spacing, align,
                offset_pos
            )
        elif direction == 'horizontal':
            self._render_horizontal(
                lines_for_horizontal, z_index,
                font_size, color, alpha, font_path,
                container_rect, line_spacing, align, offset_pos
            )
        else:
            dbg.error(f"{self.current_page}->{name} direction input error: {direction}")

    def _resolve_target_item(self, target_layout, name) -> LayoutItem | None:
        """
        解析並回傳目標 LayoutItem
        """
        # 優先看 target_layout (可能是物件本身或名稱字串)
        if target_layout:
            if isinstance(target_layout, str):
                return self._get_item_safely(target_layout)
            return target_layout

        # 其次看 name (TextProfile 的名稱)
        if name:
            return self._get_item_safely(name)

        return None

    def _render_horizontal(
            self,
            lines, z_index, font_size,
            color, alpha, font_path,
            container_rect: pygame.Rect,
            line_spacing, align,
            offset_pos: Position
        ):
        """ 橫書模式 (接收 List[str]) """
        target_window = central_mg.current_window
        if target_window is None: return

        # 生成所有 Surface，以便計算總尺寸
        surfaces = [self._get_text_surface(line, font_size, color, font_path) for line in lines]
        if not surfaces: return

        # 計算整個 文字區塊 的總寬高
        max_line_width = max(s.get_width() for s in surfaces)
        step_y = int(font_size * line_spacing)
        total_height = (len(surfaces) - 1) * step_y + surfaces[-1].get_height()

        # 建立文字區塊的虛擬 Rect(先假設它在 (0,0)，寬高確定)
        text_block_rect = pygame.Rect(0, 0, max_line_width, total_height)

        attr_name = align.value
        setattr(text_block_rect, attr_name, getattr(container_rect, attr_name))
        text_block_rect.x += offset_pos.x
        text_block_rect.y += offset_pos.y

        # 開始繪製每一行，計算起始 Y (第一行的 top)
        current_y = text_block_rect.top

        for surf in surfaces:
            line_rect = surf.get_rect()
            line_rect.top = current_y

            # 判斷 Enum 名稱中是否包含方位，決定每一行的對齊
            if 'LEFT' in align.name:
                line_rect.left = text_block_rect.left
            elif 'RIGHT' in align.name:
                line_rect.right = text_block_rect.right
            else:
                # CENTER 或沒有左右關鍵字的，一律水平置中
                line_rect.centerx = text_block_rect.centerx

            # 處理透明度
            target_surf = surf
            original_alpha = surf.get_alpha()
            if alpha is not None and alpha < 100:
                # 如果有透明度，必須 copy 一份新的 Surface
                target_surf = surf.copy()
                target_surf.set_alpha(int(alpha * 2.55))

            # 發送繪圖任務
            render_mg.add_task(z_index, target_window.blit, target_surf, line_rect)

            # 還原透明度
            if alpha is not None:
                surf.set_alpha(original_alpha if original_alpha is not None else 255)

            current_y += step_y

    def _render_vertical(
            self,
            content, z_index, font_size,
            color, alpha, font_path,
            container_rect: pygame.Rect,
            line_spacing, align,
            offset_pos: Position
        ):
        """ 直書模式 (不支援 \n，\n 會被視為一般字元處理，或您可以自行擴充直書換行邏輯) """
        target_window = central_mg.current_window
        if target_window is None: return

        chars = list(str(content))
        surfaces = [self._get_text_surface(char, font_size, color, font_path) for char in chars]
        if not surfaces: return

        # 計算尺寸
        max_char_width = max(s.get_width() for s in surfaces)
        step_y = int(font_size * line_spacing)
        total_height = (len(surfaces) - 1) * step_y + surfaces[-1].get_height()

        # 建立文字區塊的虛擬 Rect(先假設它在 (0,0)，寬高確定)
        text_block_rect = pygame.Rect(0, 0, max_char_width, total_height)

        attr_name = align.value
        setattr(text_block_rect, attr_name, getattr(container_rect, attr_name))
        text_block_rect.x += offset_pos.x
        text_block_rect.y += offset_pos.y

        current_y = text_block_rect.top

        for surf in surfaces:
            char_rect = surf.get_rect()
            char_rect.top = current_y

            # 直書時，字元一律水平置中於該行，這樣看起來才像一條直線
            char_rect.centerx = text_block_rect.centerx

            target_surf = surf
            original_alpha = surf.get_alpha()
            if alpha is not None and alpha < 100:
                target_surf = surf.copy()
                target_surf.set_alpha(int(alpha * 2.55))

            # 發送繪圖任務
            render_mg.add_task(z_index, target_window.blit, target_surf, char_rect)

            if alpha is not None:
                surf.set_alpha(original_alpha if original_alpha is not None else 255)

            current_y += step_y

    def _get_font(self, font_path, size):
        key = (font_path, size)
        if key not in self._font_cache:
            try:
                self._font_cache[key] = pygame.font.Font(str(font_path), size)
            except Exception as e:
                dbg.error(f"Font load error: {e}")
                return pygame.font.SysFont("No Find Font", size)
        return self._font_cache[key]

    def _get_text_surface(self, content: str, size: int, color: tuple, font_path = PathConfig.font_base):
        """ 取得文字 Surface (含快取機制) """
        # 轉成 tuple 確保可 hash
        color_tuple = tuple(color) if isinstance(color, list) else color
        key = (content, font_path, size, color_tuple)

        if key in self._surface_cache:
            return self._surface_cache[key]

        font = self._get_font(font_path, size)
        surface = font.render(str(content), True, color)

        # 存入快取
        self._surface_cache[key] = surface
        return surface

    def _get_item_safely(self, target_name):
        # 嘗試從當前頁面找
        item = layout_mg.get_item(
            page = self.current_page,
            name = target_name,
            silent = True
        )
        if item: return item

        return None

    ''' 其他工具 '''
    def switch_page(self, page: PageTable):
        self.current_page = page

    def clear_cache(self):
        self._font_cache.clear()
        self._surface_cache.clear()

font_mg = FontManager()
