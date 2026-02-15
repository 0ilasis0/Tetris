from core.debug import dbg
from core.hmi.base import HMIBaseManager
from core.json.manager import json_mg
from core.json.preset import SaveID, SaveJson
from core.path.manager import JsonFileID
from core.variable import PageTable


class RankManager(HMIBaseManager):
    def __init__(self, base_nav):
        super().__init__(base_nav, PageTable.RANK)

        # 定義排行榜對應的 ID 順序 (第1名, 第2名, 第3名)
        self.rank_id_map = [SaveID.RANK_1ST, SaveID.RANK_2ND, SaveID.RANK_3RD]

        # 這是我們的 Model (資料)
        self.rank_list: list[list[int]] = []

        self.load_rank()

    def get_rank(self) -> list[list[int]]:
        """
        回傳: [[分, 秒, 分數], [分, 秒, 分數], ...]
        """
        return self.rank_list

    def load_rank(self):
        """ 從 JsonManager 讀取前三名資料 """
        self.rank_list.clear()

        for save_id in self.rank_id_map:
            # 查表取得路徑
            path = SaveJson.mapping.get(save_id)
            if not path: continue

            # 抓取資料 (path[0]=FileID, path[1:]=Keys)
            data = json_mg.get_data(path[0], *path[1:], silent = True)

            # 驗證資料格式 (必須是 list 且長度 >= 3: [分, 秒, 分數])
            if isinstance(data, list) and len(data) >= 3:
                self.rank_list.append(data)
            else:
                self.rank_list.append([0, 0, 0]) # 預設空資料

    def add_score(self, min_val: int, sec_val: int, score: int):
        """ 加入新成績並存檔 """
        new_entry = [min_val, sec_val, score]

        # 避免完全重複
        if new_entry in self.rank_list: return

        # 加入列表 (先過濾掉全是 0 的空資料，再加新的)
        valid_ranks = [r for r in self.rank_list if r[2] > 0]
        valid_ranks.append(new_entry)

        # 排序 (分數大優先，時間小優先)
        valid_ranks.sort(key=lambda x: (-x[2], x[0]*60 + x[1]))

        # 只取前三名
        self.rank_list = valid_ranks[:3]

        # 如果不足 3 名，補 0
        while len(self.rank_list) < 3:
            self.rank_list.append([0, 0, 0])

        self._save_to_disk()

    def _save_to_disk(self):
        """ 將 rank_list 分配回對應的 SaveID """
        has_change = False

        for i, entry in enumerate(self.rank_list):
            if i >= len(self.rank_id_map): break

            save_id = self.rank_id_map[i]
            path = SaveJson.mapping.get(save_id)

            if path:
                # 更新記憶體
                json_mg.update_data(
                    path[0],    # JsonID.SAVE
                    *path[1:],  # Keys
                    value=entry,
                    index=None  # 覆蓋整個 List
                )
                has_change = True

        # 統一寫入硬碟
        if has_change:
            json_mg.save_to_disk(JsonFileID.SAVE)
