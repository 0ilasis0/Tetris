from core.input.keyboard.variable import DYNAMIC_LIMITS, NameHookLimit
from core.json.preset import SaveID


class ConfigVar:
    WIDTH_BLOCK     = DYNAMIC_LIMITS[NameHookLimit.SYS_SONG].get(SaveID.SYS_VOLUME, 10)
    HEIGHT_BLOCK    = 1

    # 最後的歌名顯示
    SYS_SHUFFLE = "隨機播放"
    # 因為加入隨機播放所以歌的實際長度+1
    RANDOM_SPACE    = 1

    # WINDOW_SCALE
    FULLSCREEN_RATIO = 0.773
    window_scale_list = [FULLSCREEN_RATIO, 0.73, 0.67, 0.5]
