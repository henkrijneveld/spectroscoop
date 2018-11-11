import numpy as np
import cv2
from configfile import ConfigData
from matplotlib import pyplot as plt
import time

output = "test2" # dont add the png extension

c = ConfigData()
if (not c.read()):
    print("Init file incorrect")
    exit(-1)

def readColorFrame(c):
    cap = cv2.VideoCapture(2)
    cap.set(cv2.CAP_PROP_FRAME_WIDTH, 2592)
    cap.set(cv2.CAP_PROP_FRAME_HEIGHT, 1944)

    print("1: Raw resolution:")
    print(cap.get(cv2.CAP_PROP_FRAME_WIDTH))
    print(cap.get(cv2.CAP_PROP_FRAME_HEIGHT))

    while(True):
        # Capture frame-by-frame
        ret, frame = cap.read()
        img = frame[c.bottomh:c.toph, c.bottomw:c.topw]
        cv2.imshow('1: cropped frame [push 1 to accept]', img)
        if cv2.waitKey(1) & 0xFF == ord('1'):
            break

    cap.release()
    return img


# img = cv2.imread(bron, cv2.IMREAD_GRAYSCALE)

# cv2.imshow('image', img)
# cv2.waitKey(0)
#cv2.destroyAllWindows()

# cv2.imwrite('messigray.png',img)


# plt.imshow(img, cmap = 'gray', interpolation = 'bicubic')
# plt.xticks([]), plt.yticks([])  # to hide tick values on X and Y axis
# plt.show()

def effectiveHeight(img):
    height, width = img.shape[:2]
    minheight = 0
    maxheight = 0
    totals = np.zeros(height, dtype=np.int32)
    for i in range(0, height):
        totals[i] = np.sum(img[i, :])
    maxtotal = max(totals)
    mintotal = min(totals)
    threshold = mintotal + ((maxtotal - mintotal) * 0.80)
    for i in range(0, height):
        if (totals[i] >= threshold):
            minheight = i
            break
    for i in range(height - 1, 0, -1):
        if (totals[i] >= threshold):
            maxheight = i
            break
    return (minheight, maxheight)

# step for heigher number
def deltaStep(firstrow, lastrow):
    maxstep = 20 # maximum allowable step size
    delta = np.zeros(2 * maxstep + 1, dtype=np.int32)
    minx = maxstep
    maxx = firstrow.size - maxstep
    signalmin = min(firstrow)
    signalmax = max(firstrow)
    signalThreshold = signalmin + (signalmax - signalmin) / 2

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
        delta[step+maxstep] = d
        if (d < dmin):
            dmin = d
            dminpos = step
    return dminpos


def collapseSpectrum(spectrum, step):
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

def normalizeIntensity(collapse):
    intensity = np.zeros(width, 'u1')

    maxintensity = max(collapse[10:-10])
    noise = min(collapse[10:-10])

    # normalise to 255 max
    for k in range(10, collapse.size - 10):
        intensity[k] = min((255 * (collapse[k] - noise) / (maxintensity - noise)), 255)

    return intensity

def createSpectrum(intensity, height, factor = 1):
    spectrum = np.zeros(shape=(height, intensity.size * factor), dtype=np.uint8)
    for j in range(0, (intensity.size - 1) * factor):
        for i in range(0, height):
            if (factor == 1):
                spectrum[i, j] = intensity[j]
            else:
                base = int(j // factor)
                for k in range(0, factor):
                    intens = int(intensity[base]) + (int(intensity[base + 1]) - int(intensity[base])) * k / factor
                    spectrum[i, base * factor + k] = intens
    return spectrum

def wav2RGB(wavelength, reductie = 1.0):
    w = int(wavelength)

    # colour
    if w >= 350 and w < 440:
        R = -(w - 440.) / (440. - 350.)
        G = 0.0
        B = 1.0
    elif w >= 440 and w < 490:
        R = 0.0
        G = (w - 440.) / (490. - 440.)
        B = 1.0
    elif w >= 490 and w < 510:
        R = 0.0
        G = 1.0
        B = -(w - 510.) / (510. - 490.)
    elif w >= 510 and w < 580:
        R = (w - 510.) / (580. - 510.)
        G = 1.0
        B = 0.0
    elif w >= 580 and w < 645:
        R = 1.0
        G = -(w - 645.) / (645. - 580.)
        B = 0.0
    elif w >= 645 and w <= 780:
        R = 1.0
        G = 0.0
        B = 0.0
    else:
        R = 0.0
        G = 0.0
        B = 0.0

    # intensity correction
    if w >= 350 and w < 420:
        SSS = 0.3 + 0.7 * (w - 350) / (420 - 350)
        SSS = 1.0
    elif w >= 420 and w <= 700:
        SSS = 1.0
    elif w > 700 and w <= 780:
        SSS = 0.3 + 0.7 * (780 - w) / (780 - 700)
        SSS = 1.0
    else:
        SSS = 0.0

#    return (int(255 * ((SSS * B) ** 0.7)), int(255 * ((SSS * G) ** 0.6)), int(255 * ((SSS * R) ** 0.7)))

    SSS *= 255 * reductie
    return (int(SSS * B), int(SSS * G), int(SSS * R))


def toGray(img):
    grayimg = cv2.cvtColor(img, cv2.COLOR_BGR2GRAY)

#    height, width = img.shape[:2]
#    grayimg = np.zeros(shape=(height, width), dtype=np.uint8)
#    for y in range(0, height):
#        for x in range(0, width):
#            i, j, k = img[y, x]
#            mx = max(i, j, k)
#            mn = min(i, j, k)
#            total = mx + mn
#            total = (int(i) + int(j) + int(k)) / 3
#            grayimg[y, x] = total

#    for i in range(0, width):
#       print(str([img[40, i][0]]) + ", " + str([img[40, i][1]]) + ", " + str([img[40, i][2]]) + " -> " + str(
#            grey_img[40, i]))

    return grayimg

def plotOneDimArray(arr, c):
    plt.figure(figsize=(10, 3))
    plt.plot(arr)
    plt.show()


img = readColorFrame(c)
height, width = img.shape[:2]

grey_img = toGray(img)

cv2.imshow('2: Converted to grey [push 1 to accept]', grey_img)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break

minheight, maxheight = effectiveHeight(grey_img)

print ("Dimensions from config:")
print (width)
print (height)

print ("Usable height area:")
print (minheight)
print (maxheight)

spectrum = np.array(grey_img[minheight:maxheight,:], 'u4')
height = spectrum[:,1].size

print ("new dimensions (height, width)")
print(height)
print(width)

step = deltaStep(spectrum[0, :], spectrum[height - 1, :])
print ("stepsizefor height")
print(step)

collapse = collapseSpectrum(spectrum, step)
normalized = normalizeIntensity(collapse)
factor = 1 # enlargement output1
spectrumimg = createSpectrum(normalized, 300, factor)

plotOneDimArray(spectrumimg[100,:], c)

cv2.imshow("3: Enhanced grey image [push 1 to accept] " + output, spectrumimg)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break
cv2.imwrite(output + "-grey.png", spectrumimg)

height, width = spectrumimg.shape[:2]

colorimg = np.zeros(shape=(height, width), dtype=('u1', 3))

for i in range(0, width):
    wavelength = c.getWavelength(i / factor)
    print(str(i)+"px -> "+str(wavelength)+" -> "+ str(spectrumimg[0, i]))
    reductie = spectrumimg[0, i] / 256
    color = wav2RGB(wavelength, reductie)
    for k in range(0, height):
        colorimg[k, i] = color

cv2.imshow("4: Enhanced color image [push 1 to accept] " + output, colorimg)
while (True):
    if cv2.waitKey(1) & 0xFF == ord('1'):
        break

cv2.imwrite(output + "-color.png", colorimg)

cv2.destroyAllWindows()

