from PIL import Image

import cv2
import numpy as np

def compare_images(img1, img2):

    # Don't compare if images are of different modes or different sizes.
    if (img1.mode != img2.mode) \
            or (img1.size != img2.size) \
            or (img1.getbands() != img2.getbands()):
        return None

    pairs = zip(img1.getdata(), img2.getdata())
    if len(img1.getbands()) == 1:
        # for gray-scale jpegs
        dif = sum(abs(p1 - p2) for p1, p2 in pairs)
    else:
        dif = sum(abs(c1 - c2) for p1, p2 in pairs for c1, c2 in zip(p1, p2))

    ncomponents = img1.size[0] * img1.size[1] * 3
    return (dif / 255.0 * 100) / ncomponents  # Difference (percentage)


img1 = Image.open("img1.jpg")
img2 = Image.open("img2.jpg")
print(compare_images(img1, img2))