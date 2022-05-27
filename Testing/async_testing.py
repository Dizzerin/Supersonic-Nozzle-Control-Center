import trio
import dearpygui.dearpygui as dpg
import numpy


async def run_every_5_sec():
    """
    add text to console window every 5 seconds
    """
    while dpg.is_dearpygui_running():
        frame_counter = dpg.get_frame_count() + 1
        # print('frame count {}'.format(frame_counter))
        if numpy.remainder(frame_counter, 5 * 60) == 0:
            dpg.add_text('hello', parent='console')
        dpg.render_dearpygui_frame()
        await trio.sleep(0)

async def start_app():
    """
    start main window
    :return:
    """

    dpg.create_context()

    # console window
    with dpg.window(label='Console', tag='console', pos=[100, 100], width=500, height=700):
        with dpg.group(horizontal=True):
            dpg.add_text('welcome to console', indent=10)

    dpg.create_viewport(title='Console', width=1024, height=900)
    dpg.setup_dearpygui()
    # dpg.set_primary_window("console", True)
    dpg.show_viewport()

    async with trio.open_nursery() as nursery:
        nursery.start_soon(run_every_5_sec)

    dpg.start_dearpygui()
    dpg.destroy_context()

if __name__ == "__main__":
    trio.run(start_app)