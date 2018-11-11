import numpy as np
import cv2
from configparser import ConfigParser

class ConfigData:
    height = 0
    width = 0
    toph = 0
    topw = 0
    bottomh = 0
    bottomw = 0
    calib = {}
    coef = 0
    offset = 0
    pc = -1 # pixelfunction coefficient
    pa = 0 # adjustment of pixelfunction

    def analyze(self, img):
        self.height, self.width = img.shape[:2]

        # get active height range
        gray_img = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

        minheight = 0
        maxheight = 0
        totals = np.zeros(self.height, dtype=np.int32)
        for i in range(0, self.height):
            totals[i] = np.sum(gray_img[i, :])
        maxtotal = max(totals)
        mintotal = min(totals)
        threshold = mintotal + ((maxtotal - mintotal) * 0.80)
        for i in range(0, self.height):
            if (totals[i] >= threshold):
                minheight = i
                break
        for i in range(self.height - 1, 0, -1):
            if (totals[i] >= threshold):
                maxheight = i
                break
        self.toph = min(maxheight + 30, self.height)
        self.bottomh = max(minheight - 30, 0)

        # get active width range
        minwidth = 0
        maxwidth = 0
        totals = np.zeros(self.width, dtype=np.int32)
        for i in range(0, self.width):
            totals[i] = np.sum(gray_img[:, i])
        maxtotal = max(totals)
        mintotal = min(totals)
        threshold = mintotal + ((maxtotal - mintotal) * 0.3)
        for i in range(0, self.width):
            if (totals[i] >= threshold):
                minwidth = i
                break
        for i in range(self.width - 1, 0, -1):
            if (totals[i] >= threshold):
                maxwidth = i
                break
        self.topw = min(maxwidth + 50, self.width)
        self.bottomw = max(minwidth - 50, 0)

        # first step, just get change between the colors
        self.calib = {}
        h = int((self.toph + self.bottomh) / 2)
        i = self.bottomw + 100
        b, g, r = img[h, i]
        while (b > g / 2 and i < self.topw):
            i += 1
            b, g, r = img[h, i]

        self.calib[str(i - self.bottomw)]  = "490"
        i += 1
        b, g, r = img[h, i]
        while (g > r / 2 and i < self.topw):
            i += 1
            b, g, r = img[h, i]

        self.calib[str(i - self.bottomw)]  = "580"

    def write(self):
        config = ConfigParser()
        config['img'] = { 'height' : self.height,
                          'width' : self.width,
                          'toph' : self.toph,
                          'topw' : self.topw,
                          'bottomh' : self.bottomh,
                          'bottomw' : self.bottomw}
        config['calibration'] = {}
        for pixel, wavelength in self.calib.items():
            config['calibration'][pixel] = wavelength
        with open('imgconfig.ini', 'w') as configfile:
            config.write(configfile)

    def read(self):
        config = ConfigParser()

        try:
            config.read('imgconfig.ini')
        except:
            print("Error reading ini file")
            return False

        if not config.sections():
            return False

        if config.has_section('img'):
            img = config['img']
            self.height = img.getint('height', 0)
            self.width = img.getint('width', 0)
            self.toph = img.getint('toph', 0)
            self.topw = img.getint('topw', 0)
            self.bottomh = img.getint('bottomh', 0)
            self.bottomw = img.getint('bottomw', 0)
        else:
            return False

        if config.has_section('calibration'):
            calibration = config['calibration']
            for (pixel, wavelength) in calibration.items():
                self.calib[pixel] = wavelength
            if len(self.calib) < 2:
                return False
        else:
            return False

        keys = list(self.calib.keys())
        values = list(self.calib.values())
        keys = np.array([float(i) for i in keys])
        values = np.array([float(i) for i in values])
        self.coef, self.offset = np.polyfit(keys, values, 1)

        return True

    def getWavelength(self, getpixel):
        return float(getpixel) * self.coef + self.offset


if __name__ == '__main__':
    c = ConfigData()
    if c.read():
        print("height: " + str(c.height))
    else:
        print ("Error in inifile")

    img = cv2.imread("test.png", cv2.IMREAD_COLOR)
#    c.analyze(img)
#    c.write()
    print("195 -> " + str(c.getWavelength(195)))
    print("350 -> " + str(c.getWavelength(350)))
