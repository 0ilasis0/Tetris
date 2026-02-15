from core.hmi.config.song import SysSongManager
from core.hmi.config.window_scale import SysWindowManager
from core.hmi.list import ListManager
from core.json.preset import SaveID, SaveJson
from core.variable import PageTable


class SysConfigManager(ListManager, SysSongManager, SysWindowManager):
    def __init__(self, base_nav):
        # 準備預設狀態與映射表
        default_state = {
            SaveID.SYS_SONG:   0,
            SaveID.SYS_VOLUME: 5,
            SaveID.SYS_SCALE:  0,
        }

        json_map = {
            SaveID.SYS_SONG:   SaveJson.mapping[SaveID.SYS_SONG],
            SaveID.SYS_VOLUME: SaveJson.mapping[SaveID.SYS_VOLUME],
            SaveID.SYS_SCALE:  SaveJson.mapping[SaveID.SYS_SCALE],
        }

        # 這會執行：_load_hook_limits (讀取剛更新的 Limit) -> _load_state_from_json (讀檔)
        ListManager.__init__(
            self,
            base_nav,
            PageTable.SYS_CONFIG,
            default_state,
            json_map
        )
        SysSongManager.__init__(self)
        SysWindowManager.__init__(self)

        # 載入歌曲與更新 Limits
        self.init_song_setup()
        self.init_window_setup()

        # 應用讀取到的設定(因為 ListManager 只是把值讀進 self.state，還沒真正去設音量或視窗大小)
        self._apply_initial_settings()

    def _apply_initial_settings(self):
        """ 程式啟動時，應用讀取到的 JSON 設定 """
        # 應用音量
        vol = self.state.get(SaveID.SYS_VOLUME, 5)
        self.apply_song_logic(SaveID.SYS_VOLUME, vol)

        # 應用視窗大小
        scale = self.state.get(SaveID.SYS_SCALE, 0)
        self.apply_window_logic(scale)

        # 一啟動就播歌
        song_idx = self.state.get(SaveID.SYS_SONG, 0)
        self.apply_song_logic(SaveID.SYS_SONG, song_idx)

    def on_state_change(self, key: str, value: any):
        """ [覆寫] 總路由：當 ListManager 改變數值時觸發 """
        if key == SaveID.SYS_SCALE:
            self.apply_window_logic(value)

        elif key in [SaveID.SYS_VOLUME, SaveID.SYS_SONG]:
            self.apply_song_logic(key, value)

    def interrupt_window_scale(self, index: int):
        """ 外部事件強制修改 """
        key = SaveID.SYS_SCALE

        # 更新 state
        self.state[key] = index

        # 觸發邏輯
        self.on_state_change(key, index)

        # 如果游標剛好停在「縮放」這一行，也要同步更新 Hook 顯示
        scale_row_index = -1
        for idx, k in self.key_map.items():
            if k == key:
                scale_row_index = idx
                break

        if scale_row_index != -1 and self.hook_y == scale_row_index:
            self.hook_x = index

        # 存檔
        self._save()
