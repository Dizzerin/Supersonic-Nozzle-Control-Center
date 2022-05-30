from Hardware_Libraries.camera_PCB_cam import PCBCamera
from Hardware_Libraries.ADC_labjack import Ue9LabjackADC
from GUI import GUI_manager

if __name__ == '__main__':

    # Instantiate data providers
    camera_data_provider = PCBCamera()
    ADC_data_provider = Ue9LabjackADC()

    # Initialize GUI
    GUI_manager.init_GUI(camera_data_provider=camera_data_provider, ADC_data_provider=ADC_data_provider)
    # Display Welcome Window
    GUI_manager.run_GUI()
    # Perform teardown actions after user closing the GUI
    GUI_manager.teardown_GUI()
