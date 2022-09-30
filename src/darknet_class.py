
from ctypes import *
import math
import random
import cv2
import time
import numpy as np
import darknet_library


def sample(probs):
    s = sum(probs)
    probs = [a/s for a in probs]
    r = random.uniform(0, 1)
    for i in range(len(probs)):
        r = r - probs[i]
        if r <= 0:
            return i
    return len(probs)-1

def c_array(ctype, values):
    arr = (ctype*len(values))()
    arr[:] = values
    return arr

class BOX(Structure):
    _fields_ = [("x", c_float),
                ("y", c_float),
                ("w", c_float),
                ("h", c_float)]

class DETECTION(Structure):
    _fields_ = [("bbox", BOX),
                ("classes", c_int),
                ("prob", POINTER(c_float)),
                ("mask", POINTER(c_float)),
                ("objectness", c_float),
                ("sort_class", c_int)]


class IMAGE(Structure):
    _fields_ = [("w", c_int),
                ("h", c_int),
                ("c", c_int),
                ("data", POINTER(c_float))]

class METADATA(Structure):
    _fields_ = [("classes", c_int),
                ("names", POINTER(c_char_p))]




def convertBack(x, y, w, h):
    xmin = int(round(x - (w / 2)))
    xmax = int(round(x + (w / 2)))
    ymin = int(round(y - (h / 2)))
    ymax = int(round(y + (h / 2)))
    return xmin, ymin, xmax, ymax

def array_to_image(arr):
    # need to return old values to avoid python freeing memory
    arr = arr.transpose(2,0,1)
    c, h, w = arr.shape[0:3]
    arr = np.ascontiguousarray(arr.flat, dtype=np.float32) / 255.0
    data = arr.ctypes.data_as(POINTER(c_float))
    im = IMAGE(w,h,c,data)
    return im, arr

def detect(net, meta, image, thresh=.5, hier_thresh=.5, nms=.45):
    im, image = array_to_image(image)
    darknet_library.rgbgr_image(im)
    num = c_int(0)
    pnum = pointer(num)
    darknet_library.predict_image(net, im)
    dets = darknet_library.get_network_boxes(net, im.w, im.h, thresh,
                             hier_thresh, None, 0, pnum)
    num = pnum[0]
    if nms: do_nms_obj(dets, num, meta.classes, nms)

    res = []
    for j in range(num):
        a = dets[j].prob[0:meta.classes]
        if any(a):
            ai = np.array(a).nonzero()[0]
            for i in ai:
                b = dets[j].bbox
                res.append((meta.names[i], dets[j].prob[i],
                           (b.x, b.y, b.w, b.h)))

    res = sorted(res, key=lambda x: -x[1])
    if isinstance(image, bytes): free_image(im)
    free_detections(dets, num)
    return res
