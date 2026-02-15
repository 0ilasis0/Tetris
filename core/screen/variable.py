class ScreenConfig:
    title_name = 'Tetris'

    # 縮放倍率 (ScreenRatio可變動)
    RATIO = 1

    # 設計稿基準解析度 (固定不動)
    DESIGN_WIDTH  = 1980
    DESIGN_HEIGHT = 1080

    # 實際執行時的解析度
    width  = DESIGN_WIDTH * RATIO
    height = DESIGN_HEIGHT * RATIO

    @classmethod
    def set_resolution_ratio(cls, new_ratio: float):
        """ 設定新的倍率並更新寬高 """
        cls.RATIO = new_ratio
        cls.width = int(cls.DESIGN_WIDTH * new_ratio)
        cls.height = int(cls.DESIGN_HEIGHT * new_ratio)
