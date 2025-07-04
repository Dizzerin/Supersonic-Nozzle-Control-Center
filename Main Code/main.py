import sys
import threading
import time
from datetime import datetime
from queue import Queue

from Custom_Types.custom_types import DataStore
from Hardware_Interfaces.ADC_data_provider_interface import IADCDataProvider
from Hardware_Libraries.camera_PCB_cam import PCBCamera
from Hardware_Libraries.ADC_labjack import Ue9LabJackADC
from Software_Libraries.ADC_data_writer import ADCDataFileWriter
from Software_Libraries.config_file_handler import ConfigHandler
from os import path
from GUI import GUI_manager

running = True
sampling_thread_exception_q = Queue()

def do_sampling(sample_period_s: float, ADC_data_provider: IADCDataProvider, data_store: DataStore):
    global running
    global sampling_thread_exception_q

    while running:
        try:
            sample_start_time = datetime.now()
            # Take new sample
            data_store.add_sensor_data(ADC_data_provider.get_next_data_row())
            sample_end_time = datetime.now()
            # Sleep this thread until time to take next sample
            sleep_duration = sample_period_s-(sample_end_time-sample_start_time).total_seconds()
            # Ensure we don't try sleeping for negative time (in the rare event a sample takes longer than the sample period)
            if sleep_duration < 0:
                sleep_duration = 0
            time.sleep(sleep_duration)

            # Max sample time under 10ms it seems
            # print(f"sample time: {(sample_end_time-sample_start_time).total_seconds()}")
        except Exception as e:
            sampling_thread_exception_q.put(e)
            running = False

if __name__ == '__main__':

    config_file_path = path.join(path.dirname(__file__), 'config.cfg')

    # Instantiate data providers
    try:
        camera_data_provider = PCBCamera(1024, 768) # TODO (skip) get these values from the config file (also maybe make it update live whenever config file settings are changed?  In reality, we probably shouldn't have this configurable...)
        ADC_data_provider = Ue9LabJackADC()
        ADC_data_writer = ADCDataFileWriter
        config_handler = ConfigHandler(config_file_path)
    except Exception as e:
        GUI_manager.display_pre_init_error_GUI(e)

    data_store = DataStore()
    sample_period_s = 0.02
    my_thread = threading.Thread(target=do_sampling, args=(sample_period_s, ADC_data_provider, data_store))

    # Initialize GUI
    GUI_manager.init_GUI(camera_data_provider=camera_data_provider, ADC_data_provider=ADC_data_provider,
                         ADC_data_writer=ADC_data_writer, config_handler=config_handler, data_store=data_store, sample_thread=my_thread)
    # Display Main Window
    GUI_manager.run_GUI(sampling_thread_exception_q)
    # Perform teardown actions after user closes the GUI
    running = False
    GUI_manager.teardown_GUI()

    # Wait for sampling thread to quit if its running
    if my_thread.is_alive():
        my_thread.join()
