from enum import Enum
from pathlib import Path

from core.debug import dbg


class PathUtility:
    # 支援的圖片副檔名 (依優先順序檢查)
    SUPPORT_EXTS = ["png", "jpg", "jpeg", "bmp"]

    @staticmethod
    def get_sequential_paths(base_root: Path, *folders, count: int = 1) -> list[Path]:
        """
        [通用路徑生成器]
        自動進入層層資料夾，並尋找 0 ~ count-1 的檔案
        特色：自動判斷副檔名 (png/jpg...)

        Args:
            base_root:起始根目錄 (例如 PathBase.img)
            *folders: 任意數量的資料夾層級 (例如 "arch", "blue", "castle", 0)
            count: 要抓幾張圖 (預設 1)
        """
        # 自動轉字串，讓呼叫者可以隨意傳 Enum 或 Str
        folder_strs = [
            str(f.value) if isinstance(f, Enum) else str(f)
            for f in folders
        ]
        target_dir = base_root.joinpath(*folder_strs)

        result_paths = []

        # 遍歷索引 (0, 1, 2...)
        for i in range(count):
            found_file = None

            # 自動檢查支援的副檔名
            for ext in PathUtility.SUPPORT_EXTS:
                temp_path = target_dir / f"{i}.{ext}"

                if temp_path.exists():
                    found_file = temp_path
                    break

            if found_file:
                result_paths.append(found_file)
            else:
                # 報錯並選擇用第一順位 png 當作路徑回傳
                dbg.war(f"File not found: {target_dir / f'{i}.*'}")
                result_paths.append(target_dir / f"{i}.png")

        return result_paths
