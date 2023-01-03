import cv2

img = cv2.imread("noname.png", -1)
imgA = cv2.cvtColor(img, cv2.COLOR_BGR2BGRA)
hsv = cv2.cvtColor(img, cv2.COLOR_BGR2HSV)
mask = cv2.inRange(hsv, (60, 50,50), (86, 255, 255))
ksize=15
mask = cv2.medianBlur(mask,ksize)
img2 = cv2.bitwise_not(imgA, imgA, mask=mask)
cv2.imwrite('overlay.png',img2)
