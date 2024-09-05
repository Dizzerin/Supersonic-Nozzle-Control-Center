import dearpygui.dearpygui as dpg
import dearpygui.demo as demo

dpg.create_context()
dpg.show_documentation()
dpg.show_style_editor()
dpg.show_debug()
dpg.show_about()
dpg.show_metrics()
dpg.show_font_manager()
dpg.show_item_registry()
dpg.create_viewport(title='Custom Title', width=1920, height=1080)

demo.show_demo()

dpg.setup_dearpygui()
dpg.show_viewport()
dpg.maximize_viewport()
dpg.start_dearpygui()
dpg.destroy_context()
