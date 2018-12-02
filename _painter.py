import numpy as np
import cv2
import _spectrum

class Painter:
    def __init__(self, spectrum, pixelheight = 200):
        self.spectrum = spectrum
        self.height = pixelheight # height of image in pixels

    def paintNormal(self):
        w, c, z = self.spectrum.getCookedSpectrum()
        self._paint(w, c)

    def paintZoomed(self):
        w, c, z = self.spectrum.getCookedSpectrum()
        self._paint(w, z)

    def savePainting(self, zoomed = False):
        w, c, z = self.spectrum.getCookedSpectrum()

        fname = "spectra/" + self.spectrum.getName() + "-color"
        if zoomed:
            img = self._makepaint(w, z)
            fname = fname + "-zoomed"
        else:
            img = self._makepaint(w, c)
        fname = fname + ".png"
        cv2.imwrite(fname, img)

    def _paint(self, wave, intensity):
        img = self._makepaint(wave, intensity)
        cv2.imshow(self.spectrum.getName(), img)
        cv2.waitKey(0)
        cv2.destroyWindow(self.spectrum.getName())

    def _makepaint(self, wave, intensity):
        img = np.zeros(shape=(self.height, len(wave)), dtype=('u1', 3))
        for i in range(0, len(wave)):
            reductie = intensity[i]
            color = self.wav2RGB(wave[i], reductie)
            for k in range(0, self.height):
                img[k, i] = color
        return img

    def wav2RGB(self, wavelength, reduction = 1.0):
        # definitions of intensity (in nm):
        # start at zero, max low, max high, end at zero
        violet = [0, 0, 350, 470] # actually red
        blue = [0, 0, 483, 590]
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
        gamma = 0.6
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


