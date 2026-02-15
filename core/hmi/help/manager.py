from core.hmi.list import ListManager
from core.variable import PageTable


class HelpManager(ListManager):
    def __init__(self, base_nav):
        # 因為主選單不需要存檔，也沒有數值要調整，
        # 所以傳入空的 state 和 None 的 json_map 即可。
        super().__init__(
            base_nav,
            PageTable.HELP,
            default_state = {},
            json_map = None
        )
