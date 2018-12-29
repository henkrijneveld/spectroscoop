import sys
import numpy as np

class Spectrum:
    def __init__(self, name = "test", spectrumimg = None, rawspectrum = None, calib = None):
        self.spectrumimg = spectrumimg   # imahe of a spectrum in rgb values
        self.rawspectrum = rawspectrum   # numpy array of ints with uncalibrated wavelength in x-axis
                                # not-normalized intensity in y-axis
        self.wavelengths = []   # numpy array of floats, with the wavelength value in nm of the corresponding
                                # x-axis indices of the rawspectrum
        self.intensity = []     # numpy array of floats, normalized between 0 and 1 of the y-axis in rawspectrum
        self.zoomedIntensity = []  # Like the intensity, but mimumum of raw spectrum set to 0
        self.calibration = calib   # calibration of the x-axis: dictionary with pixel -> wavelength pairs
        self.dirty = True       # wavelengths and intentisity are not computed at the moment
        self.name = name
        self.mergers = 0        # number of merged spectra

    def setName(self, name):
        self.name = name

    def getName(self):
        return self.name

    def setSpectrumimg(self, img):
        self.dirty = True
        self.mergers += 1
        height, width = img.shape[:2]
        self.spectrumimg = np.zeros((height, width, 3), dtype = int)
#        for i in range(0, 4):
#            self.spectrumimg[:,215+i,:] = 10
#            self.spectrumimg[:,587+i,:] = 10

        self.spectrumimg += img

    def mergeSpectrumimg(self, img):
        self.dirty = True
        self.mergers += 1
        if self.spectrumimg is None:
            raise ValueError("Trying to merge to uninitialized image")
        self.spectrumimg += img

    def getSpectrumimg(self):
        return(self.spectrumimg)

    def setRawSpectrum(self, spectrum):
        self.dirty = True
        self.rawspectrum = spectrum

    def setCalibration(self, calib):
        self.dirty = True
        if (len(calib) < 2):
            raise ValueError("Calibration dictionary should contain at least 2 entries")
        self.calibration = calib

    def getRawSpectrum(self):
        return self.rawspectrum

    def getCookedSpectrum(self):
        if (self.dirty):
            self._makeWavelengths()
            self._normalizeIntensity()
            self._zoomIntensity()
            self.dirty = False
        return(self.wavelengths, self.intensity, self.zoomedIntensity)

    def _normalizeIntensity(self):
        if (self.rawspectrum is None):
            raise ValueError("No spectrum specified")
        m = max(self.rawspectrum)
        if (m == 0):
            self.intensity = np.zeros(len(self.rawspectrum), dtype=float)
            return
        self.intensity = np.array([i / m for i in self.rawspectrum])

    def _zoomIntensity(self):
        if (self.rawspectrum is None):
            raise ValueError("No spectrum specified")
        m = max(self.rawspectrum)
        mn = min(self.rawspectrum)
        if (mn < 0):
            raise ValueError("Raw spectrum contains negative values")
        if (m == mn):
            self.zoomedIntensity = np.zeros(len(self.rawspectrum), dtype=float)
            return
        self.zoomedIntensity = np.array([(i - mn) / (m - mn) for i in self.rawspectrum])

    def _makeWavelengths(self):
        if (self.calibration is None):
            raise  ValueError("Calibration not specified")
        keys = list(self.calibration.keys())
        values = list(self.calibration.values())
        keys = np.array([float(i) for i in keys])
        values = np.array([float(i) for i in values])
        coef, offset = np.polyfit(keys, values, 1)
        self.wavelengths = np.zeros(len(self.rawspectrum))
        for i in range(0, len(self.wavelengths)):
            self.wavelengths[i] = coef * i + offset
#            self.wavelengths[i] = i

    def getMergers(self):
        return self.mergers

if __name__ == '__main__':
    spectrum = np.full(20, 10)
    changes = [5, 5, 20, 1]
    changespos = 10
    for i in range(changespos, changespos + len(changes)):
            spectrum[i] = changes[i - changespos]
    color = { '1': '500', '19': '700'}

    s = Spectrum()
    s.setRawSpectrum(spectrum)
    s.setCalibration(color)

    g, l, z = s.getCookedSpectrum()

    print(g)
    print(l)
    print(z)
