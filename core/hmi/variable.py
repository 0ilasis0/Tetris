from copy import deepcopy


class Cell:
    """每個格子的資料結構"""
    def __init__(self, **kwargs):
        # 這裡直接存 kwargs，保持彈性
        self.data = kwargs

    @property
    def is_empty(self):
        """ 判斷是否為空 (無資料) """
        return not bool(self.data)

    def clear(self):
        self.data.clear()

    def update(self, **kwargs):
        """ 更新資料 (而不是建立新物件) """
        self.data.update(kwargs)

    def copy(self):
        """ 複製一個新的 Cell 物件 (深拷貝) """
        # 使用 deepcopy 確保字典內如果有嵌套物件也能被獨立複製
        return Cell(**deepcopy(self.data))

    def to_dict(self):
        """ 轉成純字典，供 JSON 存檔使用 """
        return self.data

    @staticmethod
    def from_dict(data: dict):
        """ 從字典還原成 Cell 物件 """
        # 如果 data 是 None 或空，回傳空 Cell
        if not data:
            return Cell()
        return Cell(**data)

    def __repr__(self):
        return f"Cell({self.data})"