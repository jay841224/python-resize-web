import cv2
import numpy as np

def resizeImg(rootimg, width, height):
    img = cv2.resize(rootimg, (width, height), cv2.INTER_CUBIC)
    return img


def html_img_size(rootsize, width):
    #rootsize [width, height]
    rootwidth = rootsize[0]
    outputWidth = (width / rootwidth) * 50
    return outputWidth