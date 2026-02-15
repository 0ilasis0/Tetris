from core.debug import dbg
from core.path.manager import PathBase
from core.path.uility import PathUtility
from core.resource.registry import ResourceRegistry
from core.screen.image.variable import ImageProfile


class ResourceAutoLoader:
    """
    負責自動遍歷 GameTypeMap 並加載資源至 IMAGE_RESOURCE_MAP
    """
    def __init__(self, target_map: dict):
        self.target_map = target_map


    def load_all(self):
        """ 一鍵加載所有動態資源 """
        pass

    def _process_entry(self, args: list, path_kwargs: dict | None = None):
        """
        向 ResourceRegistry 註冊 Key
        向 PathUtility 取得路徑
        存入 target_map
        """
        if path_kwargs is None:
            path_kwargs = {}

        # 註冊 ID
        key = ResourceRegistry.register_key(*args)

        # 生成路徑
        # PathUtility 需要基底路徑 (PathBase.img) + 識別參數
        paths = PathUtility.get_sequential_paths(PathBase.img, *args, **path_kwargs)

        # 存入 Map
        if paths:
            self.target_map[key] = ImageProfile(path = paths)
        else:
            dbg.war(f"Resource path not found for args: {args}")
