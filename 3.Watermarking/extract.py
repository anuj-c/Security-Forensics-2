import cv2
from scipy.fftpack import dct, idct, dctn, idctn
import matplotlib.pyplot as plt
import numpy as np
import random
import math

imageOriginal = cv2.imread('watermarkedImage.png', cv2.IMREAD_UNCHANGED)
image2 = imageOriginal.copy()
watermark = cv2.imread('images/iitbbs_logo.jpeg')

watermarkStr = "".join(format(i, '08b') for i in watermark.flatten())

key = input("Enter key: ")
curRandom = int(key[1:])
random.seed(curRandom)
blksz = int(key[0])

step = ((image2.shape[0]*image2.shape[1]*image2.shape[2])//(blksz*blksz))//(watermark.shape[0]*watermark.shape[1]*watermark.shape[2]*8)

print("curRandom - ", curRandom)

def getWatermark(tempDct):
  return int(tempDct//10)%2

def getwatermark2d(watermarkStr):
  i=0
  watermarkStr2 = "".join('1' if i=='1' else '0' for i in watermarkStr)
  watermark2d = []
  while i<len(watermarkStr2):
    watermark2d.append([int(watermarkStr2[i:i+8], 2)])
    i+=8
  watermark2d = np.array(watermark2d).reshape(watermark.shape)
  return watermark2d

def psnr(image1, image2):
  mse = np.mean((image1 - image2) ** 2)
  if mse == 0:
    return 100
  PIXEL_MAX = 255.0
  return 20 * math.log10(PIXEL_MAX / math.sqrt(mse))

def nccValue(image1, image2):
  image1 = image1/np.linalg.norm(image1)
  image2 = image2/np.linalg.norm(image2)

  return np.sum(image1*image2)

def croppingAttack(image2):
  x = int(0.05*image2.shape[0])
  y = int(0.05*image2.shape[1])
  image3 = image2.copy()
  image3[:x, :, :] = 0
  image3[:, :y, :] = 0
  image3[-x:, :, :] = 0
  image3[:, -y:, :] = 0
  return image3

def saltAndPepperAttack(image2):
  import time
  random.seed(time.time())
  image3 = image2.copy()
  i = random.randint(0, image2.shape[0])
  j = random.randint(0, image2.shape[1])

  cnt = int(0.002*(image2.shape[0])*(image2.shape[1]))
  while cnt > 0:
    image3[i:i+4, j:j+4, :] = 0 if random.randint(0, 1) else 255
    i = random.randint(0, image2.shape[0])
    j = random.randint(0, image2.shape[1])
    cnt -= 1
  return image3

def medianFiltering(image2, ksize):
  image3 = cv2.medianBlur(image2, ksize).copy()
  return image3

def scalingAttack(image2):
  image3 = image2.copy()
  image3 = cv2.resize(image3, (int(image3.shape[1]*0.85), int(image3.shape[0]*0.85)))
  image3 = cv2.resize(image3, (image2.shape[1], image2.shape[0]))
  return image3

def decodeWatermark(image3):
  b = 0
  z = 0
  a = 0
  cnt=0
  watermark2 = ""
  for i in range(len(watermarkStr)):
    cnt += 1
    tempDct = dctn(image3[b:b+blksz, a:a+blksz, z], norm="ortho")
    watermark2 += str(getWatermark(tempDct[0,0]))
    curRandom = random.randint(blksz, step*blksz)
    random.seed(curRandom)
    a += curRandom
    if a >= len(image3[0]) - blksz:
      a = 0
      b += blksz
      if b >= len(image3) - blksz:
        a = 0
        b = 0
        z += 1
        if z >= len(image3[0][0]):
          print("Size full")
          break
  watermark2 = getwatermark2d(watermark2)
  return watermark2

def PlotTwoImages(image2, image3, watermark, watermark2):
  plt.figure(figsize=(5,5))
  plt.subplot(2, 2, 1)
  plt.axis("off")
  plt.title("Original Image")
  plt.imshow(cv2.cvtColor(image2, cv2.COLOR_BGR2RGB))
  plt.subplot(2, 2, 2)
  plt.axis("off")
  plt.title("Attacked Image")
  plt.imshow(cv2.cvtColor(image3.astype(np.uint8), cv2.COLOR_BGR2RGB))
  plt.subplot(2, 2, 3)
  plt.axis("off")
  plt.title("Original Watermark")
  plt.imshow(cv2.cvtColor(watermark.astype(np.uint8), cv2.COLOR_BGR2RGB))
  plt.subplot(2, 2, 4)
  plt.axis("off")
  plt.title("Extracted Watermark")
  plt.imshow(cv2.cvtColor(watermark2.astype(np.uint8), cv2.COLOR_BGR2RGB))
  plt.show()

print("PSNR",psnr(imageOriginal, image2))
watermark2 = decodeWatermark(image2)
print("Without Attack")
print("NCC",nccValue(watermark, watermark2))
PlotTwoImages(image2, image2, watermark, watermark2)
cv2.imwrite("extractedWatermark.png", watermark2)

image3 = croppingAttack(image2)
watermark2 = decodeWatermark(image3)
print("Cropping Attack")
print("NCC",nccValue(watermark, watermark2))
PlotTwoImages(image2, image3, watermark, watermark2)
cv2.imwrite("cropped.png", watermark2)

image3 = saltAndPepperAttack(image2)
watermark2 = decodeWatermark(image3)
print("Salt and Pepper Attack")
print("NCC",nccValue(watermark, watermark2))
PlotTwoImages(image2, image3, watermark, watermark2)
cv2.imwrite("salt_pepper.png", watermark2)

image3 = scalingAttack(image2)
watermark2 = decodeWatermark(image3)
print("Scaling Attack")
print("NCC",nccValue(watermark, watermark2))
PlotTwoImages(image2, image3, watermark, watermark2)
cv2.imwrite("scaling.png", watermark2)

image3 = medianFiltering(image2, 3)
watermark2 = decodeWatermark(image3)
print("Median Filtering noise Attack")
print("NCC",nccValue(watermark, watermark2))
PlotTwoImages(image2, image3, watermark, watermark2)
cv2.imwrite("median_filtering.png", watermark2)