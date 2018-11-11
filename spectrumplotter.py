import sys
import numpy as np
import matplotlib.pyplot as plt


class SpectrumPlotter:
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

    def plot(self, name = "Spectrum", figsize = (10, 8), dpi = 80):
        fig, ax_lst = plt.subplots(1, 1, figsize=figsize, dpi=dpi) # ax_lst will be array when more then one subplot
        ax_lst.set_xlabel("Wavelength (nm)")
        ax_lst.set_ylabel("Intensity")
        ax_lst.set_title(name)
        ax_lst.plot(self.wavelengths, self.normalized, color='black', linewidth=2)
        pass

    def showPlot(self, name = "Spectrum"):
        self.plot(name)
        plt.show()

    def savePlot(self, name = "Spectrum", fname = "spectrum"):
        self.plot(name, figsize = (6, 4.25), dpi = 300)
        plt.savefig(fname+".png", format="png")

if __name__ == '__main__':
    spectrum = np.full(600, 100)

    changes = [100, 101, 110, 50, 90, 110, 115, 180, 245, 110]
    changespos = 100
    for i in range(changespos, changespos + len(changes)):
            spectrum[i] = changes[i - changespos]

    color = { '195': '490', '350': '580'}

    splot = SpectrumPlotter()
    splot.setSpectrum(spectrum)
    splot.setColor(color)
    splot.showPlot()
#    splot.savePlot()


