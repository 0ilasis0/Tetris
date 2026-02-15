from core.screen.draw.manager import draw_mg
from core.screen.image.manager.core import img_mg


def submit_static_img():
    # 背景/圖片更新
    img_mg.submit_static()

    # 更新繪圖draw
    draw_mg.submit_static()
