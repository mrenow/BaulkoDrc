''' Colour Detection.

Input: n videos, colour centres
Output: Equations of ellipses for selected centres


'''


import cv2 as cv
import numpy as np
import matplotlib.colors
import matplotlib.pyplot as plt
import matplotlib.cm as cmx
from mpl_toolkits.mplot3d import Axes3D
from sklearn.mixture import GaussianMixture

#Small util

# Returns the openCV code if it exists, None if no conversion necessary.
def cvtCode(space1, space2):
    if(space1 == space2):
        return None
    ID = "COLOR_{}2{}".format(space1,space2)
    return getattr(cv,ID)


#incomplete
def getEqs(imgdata, centres:dict):

    colorspace = getColorSpace(imgdata)


# prunes as much floor data as possible
def irrelevantMask(image, thresh = ((0,50,0),(255,255,255))):
    hsv = cv.cvtColor(image,cv.COLOR_BGR2HSV)
    return cv.inRange(hsv, thresh[0], thresh[1])



def getColorSpace(imgdata, bins = (8,8,8), colorin = "BGR", colorout = "BGR"):
    #Colour histogram in rgb space
    histogram:np.ndarray = np.zeros(bins,dtype = np.uint32)


    data:np.ndarray

    # Multiple videos or images
    if (type(imgdata) == list):

        imgdata: list[str]
        for data in imgdata:
            if (data[-4:] is ".avi"):
                capture = cv.VideoCapture(data)
                ret, frame = capture.read()
                while(ret):
                    histogram += toColorHist(frame, irrelevantMask(frame), bins, colorin, colorout)
                    #cv.imshow("a",frame)

                    ret, frame = capture.read()
                capture.release()
            else:
                img = cv.imread(data)
                histogram += toColorHist(img, irrelevantMask(img), bins, colorin, colorout)
    # One video or image
    if (type(imgdata) == str):
        imgdata: str
        if (imgdata[-4:] == ".avi"):
            capture = cv.VideoCapture(imgdata)
            ret, frame = capture.read()
            while (ret):
                histogram += toColorHist(frame, irrelevantMask(frame), bins, colorin, colorout)
                ret, frame = capture.read()
            capture.release()
        else:
            img = cv.imread(imgdata)
            mask = irrelevantMask(img)
            cv.imshow("mask", mask)
            histogram += toColorHist(img, irrelevantMask(img), bins, colorin, colorout)
    return histogram

def toColorHist(image:np.ndarray, mask, bins = (8,8,8), colorin = "BRG", colorout = "BRG"):
    cvt = cvtCode(colorin, colorout)
    if(cvt):
        image = cv.cvtColor(image, cvt)
    return cv.calcHist([image], [0, 1, 2], mask, bins, [0, 256, 0, 256, 0, 256]).astype(np.uint32)

def extract_color_histogram(image, bins=(8, 8, 8)):
    # extract a 3D color histogram from the HSV color space using
    # the supplied number of `bins` per channel
    hist = cv.calcHist([image], [0, 1, 2], None, bins, [0, 256, 0, 256, 0, 256])
    # handle normalizing the histogram if we are using OpenCV 2.4.X
    print(hist.shape)
    # return the flattened histogram as the feature vector
    return hist.flatten()

def plot3DHist(hist, means, depth = (3,3,3), colorout = "BGR", thresh = 1000):

    bins = (2**depth[0], 2**depth[1], 2**depth[2])
    maxsize = (bins[0]*bins[1]*bins[2])
    xs = np.zeros(maxsize)
    ys = np.zeros(maxsize)
    zs = np.zeros(maxsize)
    colors = np.zeros((maxsize,3),dtype= np.float32)
    hist = hist.flatten()

    # Generate points for indices that exceed a particular threshold
    for i in range(maxsize):
        z = i % bins[2]
        y = (i >> depth[2])%bins[1]
        x = (i >> (depth[1]+depth[2])) % bins[0]
        colors[i] = np.array([x*256//bins[0],y*256//bins[1],z*256//bins[2]],dtype = np.uint8)
        zs[i] = z
        ys[i] = y
        xs[i] = x
    filter = hist>thresh
    xs = xs[filter]
    ys = ys[filter]
    zs = zs[filter]
    colors = colors[filter]
    hist = hist[filter]
    if(cvtCode(colorout,"RGB")):
        colors = cv.cvtColor(np.array([colors],dtype = np.uint8),cvtCode(colorout,"RGB"))[0]
        print(colors)
    colors = np.divide(colors,256)
    print(colors)
    ax1 = plotScatter3D(xs, ys, zs, getColorMap(np.log(1+hist)),bins)
    ax2 = plotScatter3D(xs, ys, zs, colors.astype(np.float32),bins)
    ax1.set
    ax1.scatter(means[:, 0], means[:, 1], means[:, 2], "k", marker = "^")
    ax2.scatter(means[:, 0], means[:, 1], means[:, 2], "k", marker = "^")


def getColorMap(cs,colorsMap = 'jet'):
    cm = plt.get_cmap(colorsMap)
    cNorm = matplotlib.colors.Normalize(vmin=min(cs), vmax=max(cs))
    scalarMap = cmx.ScalarMappable(norm=cNorm, cmap=cm)
    scalarMap.set_array(cs)
    return scalarMap.to_rgba(cs)

def plotScatter3D(x,y,z,cmap, scale):

    fig: plt.Figure = plt.figure()
    ax = Axes3D(fig)
    ax.scatter(x, y, z, c=cmap, marker = ".")
    #cant use because scalar map is in the getColorMap context
    #fig.colorbar(scalarMap)

    # Axes and scale
    ax.set_xlim(0,scale[0])
    ax.set_ylim(0,scale[1])
    ax.set_zlim(0,scale[2])
    ax.set_xlabel("Blue")
    ax.set_ylabel("Green")
    ax.set_zlabel("Red")
    return ax

# Scales and rounds values to integer values. maximum value is bins.
def discretize(data, bins):
    maxval = data.max()
    binsize = maxval/bins
    return (data/binsize).astype(np.uint32)

# Create points for each of the indices of an array. Used to convert into a format compatible with the kmeans function
def toPoints(array3D:np.ndarray) -> np.ndarray:
    numpoints = array3D.flatten().sum()
    points = np.ndarray((numpoints, 3))
    index = 0
    for i in range(array3D.shape[0]):
        for j in range(array3D.shape[1]):
            for k in range(array3D.shape[2]):
                for l in range(array3D[i,j,k]):
                    points[index] = np.array([i,j,k])
                    index += 1
    return points



colors = [(255,0,0),(0,255,255),(255,0,0)]
def Kmeans(image:np.ndarray, k, ranges:list = (1,1,1)):
    assert image.shape[-1] == len(ranges)
    # K centroids
    means = np.random.rand(k,3)
    image = cv.cvtColor(image, cv.COLOR_BGR2HSV)
    mask = cv.inRange(image,(0,70,0), (255,255,255))
    image = cv.bitwise_and(image,image,mask = mask)
    normed_img = np.divide(image, np.array(ranges)).reshape((-1,3))
    compactness, labels, centres = cv.kmeans(normed_img.astype(np.float32),k, None, criteria = (cv.TERM_CRITERIA_EPS, 100000, 0.01), attempts=1, flags = cv.KMEANS_PP_CENTERS)
    return (centres, labels)

def EMClustering(colors:np.ndarray, nclusters):
    gmm = GaussianMixture(n_components = nclusters)
    gmm.fit(colors)


    print("means",gmm.means_)
    print('\n')
    print("covar",gmm.covariances_)
    eig = np.linalg.eig(gmm.covariances_)
    print("eig", eig)
    return gmm.means_,eig



    

if __name__ == "__main__":
    name = "../testdata/TrackTest2.avi"
    colorout = "HSV"
    depth = (8,5,5)
    bins = (2**depth[0], 2**depth[1], 2**depth[2])
    hist = getColorSpace(name, bins, "BGR",colorout)
    #points = toPoints(discretize(hist, 100))
    #centres, labels = Kmeans(points, 5)
    #print(labels.shape)
    pts = toPoints((hist//10000).astype(np.uint32))
    print(pts.flatten().sum())
    means, eig = EMClustering(pts, 4)

    plot3DHist(hist, means, depth, colorout)

    plt.show()






    cv.waitKey()