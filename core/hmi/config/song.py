import random

import pygame

from core.debug import dbg
from core.hmi.config.variable import ConfigVar
from core.input.keyboard.variable import DYNAMIC_LIMITS, NameHookLimit
from core.json.preset import SaveID
from core.path.manager import PathBase


class SysSongManager:
    def __init__(self) -> None:
        self.files          = []
        self.files_name     = []
        self.files_amount   = 0

        self.loop = -1
        self.shuffle_list = []
        self.shuffle_index = 0

    def init_song_setup(self):
        # [修改] 使用 SaveID 讀取音量
        vol = self.state.get(SaveID.SYS_VOLUME, 5)
        pygame.mixer.music.set_volume(vol * 0.1)

        self._load_files()

        self.files_name = [file.stem for file in self.files]
        self.files_name.append(ConfigVar.SYS_SHUFFLE)

        self.files_amount = len(self.files)

        # 播放
        self.play_current_song()

        key_song = SaveID.SYS_SONG
        if key_song in DYNAMIC_LIMITS[NameHookLimit.SYS_SONG]:
            DYNAMIC_LIMITS[NameHookLimit.SYS_SONG][key_song] = self.files_amount

    def apply_song_logic(self, key, value):
        if key == SaveID.SYS_VOLUME:
            try:
                volume = float(value)
            except:
                volume = 0.0
            pygame.mixer.music.set_volume(max(0.0, min(1.0, volume * 0.1)))

        elif key == SaveID.SYS_SONG:
            self.play_current_song()

    def play_current_song(self):
        if not self.files: return

        try:
            # 使用 SaveID 讀取當前選擇
            raw_idx = int(self.state.get(SaveID.SYS_SONG, 0))
        except Exception:
            raw_idx = 0

        real_idx = self._resolve_song_index(raw_idx)

        if 0 <= real_idx < len(self.files):
            path = self.files[real_idx]
            try:
                pygame.mixer.music.load(str(path))
                pygame.mixer.music.play(loops = self.loop, start = 0.0)
            except Exception as e:
                dbg.error(f"[SongManager] play error: {path} - {e}")

    def _load_files(self):
        try:
            self.files = list(PathBase.song.glob("*.mp3"))
            self.files.sort()
        except Exception as e:
            dbg.error(f"Load songs error: {e}")
            self.files = []

    def _resolve_song_index(self, raw_idx):
        '''
        決定要播哪一個檔案
        raw_idx: UI 上選擇的 index
        return: 實際 files list 中的 index
        '''
        # 如果選到了最後一個選項 (隨機播放)
        if raw_idx == self.files_amount:
            # 設定播放結束事件 (為了自動切下一首)
            pygame.mixer.music.set_endevent(pygame.USEREVENT)
            self.loop = 0 # 不單曲循環，播完觸發事件

            # 初始化隨機列表
            self.shuffle_list = list(range(self.files_amount))
            random.shuffle(self.shuffle_list)
            self.shuffle_index = 0

            # 這同樣是 初始化隨機列表 ，但是他能夠強制沒有播完此單曲循環前，不換歌的順序
            # if not self.shuffle_list:
            #     self.shuffle_list = list(range(self.files_amount))
            #     random.shuffle(self.shuffle_list)
            #     self.shuffle_index = 0

            # 防呆
            if self.shuffle_index >= len(self.shuffle_list):
                 self.shuffle_index = 0
                 random.shuffle(self.shuffle_list)

            return self.shuffle_list[self.shuffle_index]

        else:
            # 一般模式：單曲循環，不觸發結束事件
            pygame.mixer.music.set_endevent(0)
            self.loop = -1
            return (raw_idx % self.files_amount) if (self.files_amount > 0) else 0

    def on_song_end(self):
        """
        當一首歌播完時呼叫
        """
        # 只有在隨機播放模式 (loop=0) 才需要切下一首
        if self.loop == 0:
            self.shuffle_index += 1
            if self.shuffle_index >= len(self.shuffle_list):
                self.shuffle_index = 0
                random.shuffle(self.shuffle_list)

            # 播放下一首
            self.play_current_song()
