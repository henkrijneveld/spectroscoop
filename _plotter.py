import sys
import numpy as np
import matplotlib.pyplot as plt
import _spectrum

class Plotter:
    def __init__(self, s):
        self.spectrum = s
        if s.getRawSpectrum() is None:
            raise ValueError("Raw spectrum not initialized for spectrum")
        self.name = s.getName()
        self.figsizescrn = (10, 8)     # format on screen
        self.dpiscrn = 80              # dpi on screen
        self.figsizepng = (6, 4.25)     # format when saved as png
        self.dpipng = 300               # dpi when saved as png

    def plotNormal(self):
        w, c, z = self.spectrum.getCookedSpectrum()
        self._plot(self.figsizescrn, self.dpiscrn, w, c)
        plt.show()

    def plotZoomed(self):
        w, c, z = self.spectrum.getCookedSpectrum()
        self._plot(self.figsizescrn, self.dpiscrn, w, z, " - zoomed")
        plt.show()

    def _plot(self, figsize, dpi, wave, intensity, nameext = ""):
        fig, ax_lst = plt.subplots(1, 1, figsize=self.figsizepng, dpi=self.dpipng) # ax_lst will be array when more then one subplot
        ax_lst.set_xlabel("Wavelength (nm)")
        ax_lst.set_ylabel("Intensity")
        ax_lst.set_title(self.name + nameext)
        ax_lst.plot(wave, intensity, color='black', linewidth=2)

    def savePlot(self, fname = None, zoomed = False):
        if not fname:
            fname = "spectra/"+self.name
        w, c, z = self.spectrum.getCookedSpectrum()

        if not zoomed:
            self._plot(self.figsizepng, self.dpipng, w, c)
            plt.savefig(fname+"-diagram.png", format="png")

        if zoomed:
            self._plot(self.figsizepng, self.dpipng, w, z, " - zoomed")
            plt.savefig(fname+"-diagram-zoomed.png", format="png")

