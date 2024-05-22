import cv2
from scipy.fftpack import dct, idct, dctn, idctn
import matplotlib.pyplot as plt
import numpy as np
import random
import math

imageOriginal = cv2.imread('images/cover.png')
image = imageOriginal.copy()
watermark = cv2.imread('images/iitbbs_logo.jpeg')

print("image shape - ", image.shape)
print("watermark shape - ", watermark.shape)

blksz = 8
step = 0

while True:
  step = ((image.shape[0]*image.shape[1]*image.shape[2])//(blksz*blksz))//(watermark.shape[0]*watermark.shape[1]*watermark.shape[2]*8)
  if step == 0:
    blksz -= 1
  else:
    break

print("block size - ", blksz)
print("step - ", step)
if step == 0:
  print("Image too small for watermark")
  exit()

key = str(blksz) + str(random.randint(1000,9999))
print("key - ", key)

curRandom = int(key[1:])
random.seed(curRandom)
curRandom = random.randint(blksz, step*blksz)
print("curRandom - ", curRandom)

watermarkStr = "".join(format(i, '08b') for i in watermark.flatten())
print("watermark length - ",len(watermarkStr))

def putWatermark(tempDct, val):
  if int((tempDct//10)%2) != int(val):
    tempDct += 10
  tempDct = str(tempDct)
  tempDct = tempDct[:tempDct.find(".")-1] + "5" + tempDct[tempDct.find("."):]
  return float(tempDct)

b = 0
z = 0
a = 0
for x in watermarkStr:
  tempDct = dctn(image[b:b+blksz, a:a+blksz, z], norm="ortho")
  tempDct[0,0] = putWatermark(tempDct[0,0], x)
  newBlock = idctn(tempDct, norm="ortho")
  image[b:b+blksz, a:a+blksz, z] = np.round(newBlock)
  a += curRandom
  random.seed(curRandom)
  curRandom = random.randint(blksz, step*blksz)
  if a >= len(image[0]) - blksz:
    a = 0
    b += blksz
    if b >= len(image) - blksz:
      a = 0
      b = 0
      z += 1
      if z >= len(image[0][0]):
        print("Size full")
        break

cv2.imwrite('watermarkedImage.png', image)

plt.subplot(1,2,1)
plt.axis('off')
plt.imshow(cv2.cvtColor(imageOriginal, cv2.COLOR_BGR2RGB))
plt.subplot(1,2,2)
plt.axis('off')
plt.imshow(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
plt.show()
