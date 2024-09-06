import dearpygui.dearpygui as dpg
# Below centering functions are for use with DPG, but they don't work perfectly for text since
# text always has a width of 0 according to DPG


def center_x_y(dpg_item):
    # Guarantee these commands happen in the same frame
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        viewport_height = dpg.get_viewport_client_height()
        width = dpg.get_item_width(dpg_item)
        height = dpg.get_item_height(dpg_item)
        dpg.set_item_pos(dpg_item, [viewport_width // 2 - width // 2, viewport_height // 2 - height // 2])


def center_y(dpg_item):
    # Guarantee these commands happen in the same frame
    with dpg.mutex():
        viewport_height = dpg.get_viewport_client_height()
        height = dpg.get_item_height(dpg_item)
        current_pos = dpg.get_item_pos(dpg_item)
        dpg.set_item_pos(dpg_item, [current_pos[0], viewport_height // 2 - height // 2])


def center_x(dpg_item):
    # Guarantee these commands happen in the same frame
    with dpg.mutex():
        viewport_width = dpg.get_viewport_client_width()
        width = dpg.get_item_width(dpg_item)
        current_pos = dpg.get_item_pos(dpg_item)
        dpg.set_item_pos(dpg_item, [viewport_width // 2 - width // 2, current_pos[1]])


