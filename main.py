from Hardware_Libraries.camera_PCB_cam import PCBCamera
from Hardware_Libraries.ADC_labjack import Ue9LabJackADC
from Software_Libraries.config_file_handler import ConfigHandler
from os import path
from GUI import GUI_manager

if __name__ == '__main__':

    config_file_path = path.join(path.dirname(__file__), 'config2.cfg')

    # Instantiate data providers
    camera_data_provider = PCBCamera(1024, 768)
    ADC_data_provider = Ue9LabJackADC()
    config_handler = ConfigHandler(config_file_path)

    # Initialize GUI
    GUI_manager.init_GUI(camera_data_provider=camera_data_provider, ADC_data_provider=ADC_data_provider,
                         config_handler=config_handler)
    # Display Welcome Window
    GUI_manager.run_GUI()
    # Perform teardown actions after user closing the GUI
    GUI_manager.teardown_GUI()
