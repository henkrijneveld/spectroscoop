import numpy as np
from matplotlib import pyplot as plt
from _spectrum import Spectrum

class Collapser:
    def __init__(self, spectrum):
        self.spectrum = spectrum # type: Spectrum

    def collapse(self):
        img = self.spectrum.getSpectrumimg()
        intensity = img[:,:,0] # only works in gray scale !!

        # find the lines that are completely filled
        intensity = self._cropToEffectiveHeight(intensity)

        # find the tilt
        stepsize = self._deltaStep(intensity[0], intensity[-1])
        print("Stepsize: " + str(stepsize))

        # collapse the lines
        collapsed = self._collapseSpectrum(intensity, stepsize)
        self.spectrum.setRawSpectrum(collapsed)


    def _collapseSpectrum(self, spectrum, step):
        height, width = spectrum.shape[:2]

        intensity = np.zeros(width, 'u4')

        for i in range(0, height):
            shift = 0
            if (step != 0):
                delta = height / step
                shift = int(i / delta + 0.5)
            for j in range(abs(step), width - abs(step)):
                intensity[j] += spectrum[i, j + shift]
        return intensity

    #
    # determine which step size to map two rows
    #
    def _deltaStep(self, firstrow, lastrow):
        maxstep = 20  # maximum allowable step size
        delta = np.zeros(2 * maxstep + 1, dtype=np.int32)
        minx = maxstep
        maxx = firstrow.size - maxstep

        # due to the threshold we eliminate noise
        signalmin = min(firstrow)
        signalmax = max(firstrow)
        signalThreshold = signalmin + (signalmax - signalmin) * 0.75

        dmin = 100000000000
        dminpos = -1
        for step in range(-maxstep, maxstep):
            d = 0
            for i in range(minx, maxx):
                if (firstrow[i] > signalThreshold):
                    nf = int(firstrow[i])
                    nl = int(lastrow[i + step])
                    erbij = (nf - nl) * (nf - nl)
                    d += erbij
            delta[step + maxstep] = d # for debugging
            if (d < dmin):
                dmin = d
                dminpos = step
        return dminpos

    #
    # remove top and bottom side with black bands
    #
    def _cropToEffectiveHeight(self, img):
        height, width = img.shape[:2]
        minheight = 0
        maxheight = 0
        totals = np.zeros(height, dtype=np.int32)
        for i in range(0, height):
            totals[i] = np.sum(img[i, :])
        maxtotal = max(totals)
        mintotal = min(totals)
        threshold = mintotal + ((maxtotal - mintotal) * 0.90)
        for i in range(0, height):
            if (totals[i] >= threshold):
                minheight = i
                break
        for i in range(height - 1, 0, -1):
            if (totals[i] >= threshold):
                maxheight = i
                break
        return img[minheight:maxheight,:]
