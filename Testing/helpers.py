import dearpygui.dearpygui as dpg
import Testing.window


def change_window(current: Window, new: Window):
    new.show()
    current.hide()
    dpg.set_primary_window(new._name(), True)


