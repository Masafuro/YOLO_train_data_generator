import imgsim
import numpy as np
import cv2

vtr = imgsim.Vectorizer()

img0 = cv2.imread("trimmed/chips/001.png")
img1 = cv2.imread("trimmed/chips/002.png")

vec0 = vtr.vectorize(img0)
vec1 = vtr.vectorize(img1)
vecs = vtr.vectorize(np.array([img0, img1]))

dist = imgsim.distance(vec0, vec1)
print("distance =", dist)

dist = imgsim.distance(vecs[0], vecs[1])
print("distance =", dist)