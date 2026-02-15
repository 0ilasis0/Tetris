import pygame

from core.debug import dbg
from core.screen.image.variable import ImageProfile  # 假設你的 ImageProfile 在這裡


class SpriteSlicer:
    """
    專門負責將 Sprite Sheet 切割成小圖
    支援兩種模式：
    1. 指定 Size (精確模式): 依據固定長寬切割，自動計算行列。
    2. 指定 Row/Col (網格模式): 依據行列數將原圖均分切割。
    """
    @staticmethod
    def slice(sheet: pygame.Surface, profile: ImageProfile) -> list[pygame.Surface]:
        frames = []
        sheet_w, sheet_h = sheet.get_size()

        # 參數準備
        gap_x = profile.frame_gap_x
        gap_y = profile.frame_gap_y
        fw, fh = 0, 0
        cols, rows = 1, 1

        # 決定單格尺寸 (fw, fh) 與 排版列數 (cols)
        if profile.frame_size:
            ''' 優先使用Size決定單格大小 '''
            fw = profile.frame_size.width
            fh = profile.frame_size.height
            # 防呆
            if fw > 0:
                cols = (sheet_w + gap_x) // (fw + gap_x)
            if fh > 0:
                rows = (sheet_h + gap_y) // (fh + gap_y)

        else:
            ''' 網格均分模式 (User 沒給 Size，依賴 Row/Col) '''
            cols = max(1, profile.frame_col)
            rows = max(1, profile.frame_row)

            # 自動推算單格大小
            fw = (sheet_w - (cols - 1) * gap_x) // cols
            fh = (sheet_h - (rows - 1) * gap_y) // rows

            # 檢查是否整除 (僅供除錯警告，不中斷程式)
            if (fw * cols + (cols - 1) * gap_x) != sheet_w:
                dbg.war(f'SpriteSlicer: {profile.name or "Image"} width indivisible by cols {cols}')
            if (fh * rows + (rows - 1) * gap_y) != sheet_h:
                dbg.war(f'SpriteSlicer: {profile.name or "Image"} height indivisible by rows {rows}')

        # 防呆
        if fw <= 0 or fh <= 0:
            dbg.error(f"SpriteSlicer: Invalid frame size calculated ({fw}x{fh}) for {profile.name}")
            return [sheet] # 回傳原圖避免崩潰

        # 決定總格數
        if profile.frame_count is not None:
            total_count = profile.frame_count
        else:
            total_count = cols * rows

        # 執行切割迴圈
        for i in range(total_count):
            # 計算目前是第幾列、第幾行
            row_idx = i // cols
            col_idx = i % cols

            # 計算像素座標
            x = col_idx * (fw + gap_x)
            y = row_idx * (fh + gap_y)

            # 邊界檢查 (提早終止，避免切到圖片外)
            if x + fw > sheet_w or y + fh > sheet_h:
                dbg.war(f"SpriteSlicer: Frame {i} out of bounds (Sheet: {sheet_w}x{sheet_h}). Stop slicing.")
                break

            rect = pygame.Rect(x, y, fw, fh)

            try:
                frame = sheet.subsurface(rect).copy()
                frames.append(frame)
            except ValueError as e:
                dbg.error(f"SpriteSlicer: Slice error at index {i}: {e}")
                break

        return frames
