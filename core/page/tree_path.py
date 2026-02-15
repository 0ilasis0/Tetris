from typing import Dict, List

from core.debug import dbg
from core.variable import PageTable


class PageTree:
    def __init__(self, name: PageTable):
        self.name = name                                # 節點名稱（PageTable Enum）
        self.children: List['PageTree'] = []            # 子節點物件列表
        self.parent: 'PageTree | None' = None        # 父節點物件
        self.family_table: Dict[int, PageTable] = {}    # 索引對照表 {index: 子頁名稱}

    def add_child(self, child_node: 'PageTree'):
        child_node.parent = self
        self.children.append(child_node)
        # 自動更新索引表
        self.family_table[len(self.children) - 1] = child_node.name

    def get_child_by_index(self, index: int) -> PageTable:
        return self.family_table.get(index)

    def is_leaf(self) -> bool:
        return len(self.children) == 0


def create_page_tree() -> Dict[PageTable, PageTree]:
    """
    回傳一個字典，包含所有頁面的 Node，方便快速查找
    """
    # 先建立所有節點
    nodes = {page: PageTree(page) for page in PageTable}

    # 定義結構 (父 -> 子列表)
    structure = {
        PageTable.MENU: [
            PageTable.SINGLE_MENU,
            PageTable.DOUBLE,
            PageTable.ENDLESS,
            PageTable.SYS_CONFIG,
            PageTable.HELP,
            PageTable.RANK,
            PageTable.EXIT
        ],
        PageTable.SINGLE_MENU: [
            PageTable.SINGLE
        ],
    }

    # 自動組裝樹
    for parent_enum, child_enums in structure.items():
        parent_node = nodes[parent_enum]
        for child_enum in child_enums:
            if child_enum in nodes:
                parent_node.add_child(nodes[child_enum])
            else:
                dbg.error(f"Page {child_enum} not defined in PageTable nodes!")

    return nodes



# 建立查找表
tree_path_table = create_page_tree()

# 為了 Debug 方便，如果你還是需要那個 genealogy_table
def build_genealogy_dict(root_node: PageTree) -> dict:
    result = {}
    if root_node.children:
        result[root_node.name] = root_node.family_table
        for child in root_node.children:
            # 遞迴合併子字典
            result.update(build_genealogy_dict(child))
    return result

genealogy_table = build_genealogy_dict(tree_path_table[PageTable.MENU])

# 驗證
dbg.dump(genealogy_table)
