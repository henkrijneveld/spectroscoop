import numpy as np
import cv2


class ColorImg:
    def __init__(self):
        self.spectrum = []
        self.wavelengths = []
        self.normalized = []
        self.color = {}

    def setSpectrum(self, spectrum):
        self.spectrum = spectrum
        self.normalizeIntensity()

    def setColor(self, color):
        self.color = color
        self.makeWavelengths()

    def normalizeIntensity(self):
        m = max(self.spectrum)
        self.normalized = np.array([i / m for i in self.spectrum])

    def makeWavelengths(self):
        if len(self.color) < 2:
            print("Colorarray missing")
            exit(-1)
        keys = list(self.color.keys())
        values = list(self.color.values())
        keys = np.array([float(i) for i in keys])
        values = np.array([float(i) for i in values])
        coef, offset = np.polyfit(keys, values, 1)
        self.wavelengths = np.zeros(len(self.spectrum))
        for i in range(0, len(self.wavelengths)):
            self.wavelengths[i] = coef * i + offset

    def showImg(self):
        img = np.zeros(shape=(200, len(self.spectrum)), dtype=('u1', 3))
        for i in range(0, len(self.spectrum)):
            reductie = self.normalized[i]
            color = self.wav2RGB(self.wavelengths[i], reductie)
            for k in range(0, 200):
                img[k, i] = color
        cv2.imshow("Spectrum", img)
        cv2.waitKey(0)
        cv2.destroyWindow("Spectrum")
        pass

    def wav2RGB(self, wavelength, reduction = 1.0):
        # definitions of intensity (in nm):
        # start at zero, max low, max high, end at zero
        violet = [0, 0, 350, 470] # actually red
        blue = [0, 0, 483, 560]
        green = [420, 497, 608, 710]
        red = [520, 612, 780, 0]

        R = self._getValue(wavelength, violet) + self._getValue(wavelength, red)
        G = self._getValue(wavelength, green)
        B = self._getValue(wavelength, blue)

        # general intensity correction
        # lowintensity -> 1 -> 1 -> lowintensity
        lowintensity = 0.3
        intensity = [350, 420, 680, 780]
        correction = self._getIntensity(wavelength, intensity, lowintensity)

        # color correction for non linerarities
        gamma = 0.8
        R = self._getGammaCorrection(R, correction, gamma)
        G = self._getGammaCorrection(G, correction, gamma)
        B = self._getGammaCorrection(B, correction, gamma)

        # compute reduction to end with 255 max
        reduction = 255. * reduction

        return (int(reduction * B), int(reduction * G), int(reduction * R))

    def _getGammaCorrection(self, color, correction, gamma):
        return (color * pow(color * correction, gamma))

    def _getIntensity(self, wavelength, intensity, low):
        if (wavelength < intensity[0]):
            return 0.
        if (wavelength < intensity[1]):
            return low + (1. - low) * (wavelength - intensity[0]) / (intensity[1] - intensity[0])
        if (wavelength < intensity[2]):
            return 1.
        if (wavelength < intensity[3]):
            return low + (1. - low) * (intensity[3] - wavelength) / (intensity[3] - intensity[2])
        return 0.

    def _getValue(self, wavelength, intensity):
        if (wavelength < intensity[0]):
            return 0.
        if (wavelength < intensity[1]):
            return (wavelength - intensity[0]) / (intensity[1] - intensity[0])
        if (wavelength < intensity[2]):
            return 1.
        if (wavelength < intensity[3]):
            return (intensity[3] - wavelength) / (intensity[3] - intensity[2])
        return 0.

if __name__ == '__main__':
    spectrum = np.full(600, 100)

    changes = [125]
    changespos = 20
    for i in range(changespos, changespos + len(changes)):
       spectrum[i] = changes[i - changespos]
    color = { '200': '490', '320': '580'}

    cimg = ColorImg()
    cimg.setSpectrum(spectrum)
    cimg.setColor(color)
    cimg.showImg()


