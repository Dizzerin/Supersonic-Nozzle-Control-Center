import cv2 as cv
import numpy as np
import dearpygui.dearpygui as dpg


def test_cv2():
    # Create a capture from camera
    camera_index = 1
    cap = cv.VideoCapture(camera_index)

    # Check if camera stream could be opened/obtained
    if not cap.isOpened():
        print("Cannot open camera")
        exit()

    # Continuously capture
    while True:
        # Capture frame-by-frame
        successful_capture, frame = cap.read()
        # if frame is read correctly ret is True
        if not successful_capture:
            print("Can't receive frame (stream end?). Exiting ...")
            break
        # Display the resulting frame
        cv.imshow('frame', frame)
        if cv.waitKey(1) == ord('q'):
            break
    # When everything done, release the capture
    cap.release()
    cv.destroyAllWindows()


def print_lots_o_stuff(capture):
    print()
    print()
    print("AutoFocus: " + str(capture.get(cv.CAP_PROP_AUTOFOCUS)))
    print("Focus: " + str(capture.get(cv.CAP_PROP_FOCUS)))
    # print("AutoExposure: " + str(capture.get(cv.CAP_PROP_AUTO_EXPOSURE)))
    # print("Exposure: " + str(capture.get(cv.CAP_PROP_EXPOSURE)))
    # print("Exposure Program: " + str(capture.get(cv.CAP_PROP_EXPOSUREPROGRAM)))
    # print("XI Exposure: " + str(capture.get(cv.CAP_PROP_XI_EXPOSURE)))
    # print("Brightness: " + str(capture.get(cv.CAP_PROP_BRIGHTNESS)))
    # print("Aperture: " + str(capture.get(cv.CAP_PROP_APERTURE)))
    # print("Iris: " + str(capture.get(cv.CAP_PROP_IRIS)))
    # print("Gain: " + str(capture.get(cv.CAP_PROP_GAIN)))
    # print("FPS: " + str(capture.get(cv.CAP_PROP_FPS)))
    # print("Format: " + str(capture.get(cv.CAP_PROP_FORMAT)))
    # print("Contrast: " + str(capture.get(cv.CAP_PROP_CONTRAST)))
    # print("Height: " + str(capture.get(cv.CAP_PROP_FRAME_HEIGHT)))
    # print("Width: " + str(capture.get(cv.CAP_PROP_FRAME_WIDTH)))
    # print("Backlight: " + str(capture.get(cv.CAP_PROP_BACKLIGHT)))
    # print("Backend: " + str(capture.get(cv.CAP_PROP_BACKEND)))
    # print("Zoom: " + str(capture.get(cv.CAP_PROP_ZOOM)))
    # print("Temperature: " + str(capture.get(cv.CAP_PROP_TEMPERATURE)))
    # print("Saturation: " + str(capture.get(cv.CAP_PROP_SATURATION)))
    # input("hit key")
