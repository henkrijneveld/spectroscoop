import sys
import os
import numpy as np
from _plotter import Plotter
from _spectrum import Spectrum
from _painter import Painter
from _capturer import Capturer
from _collapser import Collapser


def run():
    s = Spectrum("kunstlicht-multicap")

    Capturer(s).capture(5) # multicapture parameter

    Collapser(s).collapse()

    p = Plotter(s)
    p.plotNormal()
    p.savePlot()

    i = Painter(s)
    i.paintNormal()
    i.savePainting()
    i.saveRawInput()



#spectrum = np.full(20, 10)
#changes = [5, 5, 20, 8]
#changespos = 10
#for i in range(changespos, changespos + len(changes)):
#    spectrum[i] = changes[i - changespos]
#color = {'1': '400', '19': '700'}

run()

try:
    pass
  #  run()
except ValueError as err:
    # all my own internale exceptions are ValueError
    print(format(err))

