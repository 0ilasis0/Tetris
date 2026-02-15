from core.ui_layout.name.identifiers import LayoutName
from core.ui_layout.name.registry import LayoutNameRegistry
from core.ui_layout.name.variable import STATIC_NAME


def layout_name_init_static_names():
    for member in LayoutName:
        # 如果有序列清單 (count > 1 的)
        if hasattr(member, 'serial_list') and member.serial_list:
            for name in member.serial_list:
                LayoutNameRegistry.register(name, STATIC_NAME)
        else:
            # 單一名稱
            LayoutNameRegistry.register(member.value, STATIC_NAME)
