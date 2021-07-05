import numpy as np
import cv2
from _config import Config
from _spectrum import Spectrum

class Capturer:
    def __init__(self, spectrum):
        self.config = Config()
        self.spectrum = spectrum
        self.spectrum.setCalibration(self.config.calibration)

    def readFromFile(self, name):
        img = cv2.imread(name)
        img = img[self.config.bottomh:self.config.toph, self.config.bottomw:self.config.topw]

        cv2.imshow('image', img)
        if self.spectrum.getSpectrumimg() is None:
            self.spectrum.setSpectrumimg(img)
        else:
            self.spectrum.mergeSpectrumimg(img)

    def capture(self, nr = 1):
        for dev in range(1, 10):
            cap = cv2.VideoCapture(dev)
            if cap.isOpened():
                break
        if not cap.isOpened():
            raise ValueError("Webcam not found")

        cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
        cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

        # wait for correct picture
        while (True):
            # Capture frame-by-frame
            ret, frame = cap.read()
            if frame is None:
                raise ValueError("Error reading from webcam")
            height, width = frame.shape[:2]
            if (height != self.config.height or width != self.config.width):
                raise ValueError("Resolution of camera does not match configfile")

            img = frame[self.config.bottomh:self.config.toph, self.config.bottomw:self.config.topw]
            cv2.imshow('Capture? push 1 to accept!', img)
            if cv2.waitKey(1) & 0xFF == ord('1'):
                cv2.destroyAllWindows()
                break

        print("Taking " + str(nr) + " shots")
        for nrcap in range(0, nr):
            # Capture frame-by-frame
            ret, frame = cap.read()
            print("Shot " + str(nrcap + 1))
            if frame is None:
                raise ValueError("Error reading from webcam")
            img = frame[self.config.bottomh:self.config.toph, self.config.bottomw:self.config.topw]

            if self.spectrum.getSpectrumimg() is None:
                self.spectrum.setSpectrumimg(img)
            else:
                self.spectrum.mergeSpectrumimg(img)
        print("Done!")

        cap.release()