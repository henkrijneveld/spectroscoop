from configparser import ConfigParser

class Config:
    height = 0
    width = 0
    toph = 0
    topw = 0
    bottomh = 0
    bottomw = 0
    calibration = {}

    def __init__(self, read = True):
        if read:
            if (not self.read()):
                raise ValueError("Problem reading configfile")

    def write(self):
        config = ConfigParser()
        config['img'] = { 'height' : self.height,
                          'width' : self.width,
                          'toph' : self.toph,
                          'topw' : self.topw,
                          'bottomh' : self.bottomh,
                          'bottomw' : self.bottomw}
        config['calibration'] = {}
        for pixel, wavelength in self.calibration.items():
            config['calibration'][pixel] = wavelength
        with open('_config.ini', 'w') as configfile:
            config.write(configfile)

    def read(self):
        config = ConfigParser()

        try:
            config.read('_config.ini')
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
                self.calibration[pixel] = wavelength
            if len(self.calibration) < 2:
                return False
        else:
            return False

        return True
