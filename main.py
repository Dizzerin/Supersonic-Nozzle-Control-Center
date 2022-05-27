from Testing import gui, cv2_testing
from GUI import GUI_manager

if __name__ == '__main__':
    # Initialize GUI
    GUI_manager.init_GUI()
    # Display Welcome Window
    GUI_manager.run_GUI()
    # Perform teardown actions after user closing the GUI
    GUI_manager.teardown_GUI()
    exit()

    """ Initialize Hardware """
    # TODO Camera selection (if multiple cameras, or use defaults etc. and settings/config files.)
    # Initialize Camera Capture
    capture = cv2_testing.initialize_capture(camera_index=0)
    # Initialize ADC

    # Testing
    # cv2_testing.test_cv2()
    gui.run_gui(capture)

    """ Teardown """
    # Stop Camera Capture
    cv2_testing.end_capture(capture)

exit()
