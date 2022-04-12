from Testing import gui, cv2_testing


if __name__ == '__main__':
    # Testing
    capture = cv2_testing.initialize_capture()
    gui.run_gui(capture)
    cv2_testing.end_capture(capture)

    # Testing
    # cv2_testing.test_cv2()
    # py_gui_demo.run_demo()

exit()
