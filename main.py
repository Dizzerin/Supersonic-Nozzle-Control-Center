from Testing import gui, cv2_testing, GUI_manager_test_1, GUI_manager_test_2


if __name__ == '__main__':

    # Start GUI and Display Welcome Window

    # GUI and window switching using method/organizational structure 1
    GUI_manager_test_2.init_GUI()
    GUI_manager_test_2.run_GUI()
    GUI_manager_test_2.teardown_GUI()
    exit()

    # GUI and window switching using method/organizational structure 2
    GUI = GUI_manager_test_1.UI()
    GUI.run()
    GUI.teardown()

    # TODO Camera selection (if multiple cameras, or use defaults etc. and settings/config files.)

    """ Initialize Hardware """
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
