import cv2
import numpy as np
import random

image = cv2.imread('res.png', cv2.IMREAD_UNCHANGED)

bnw = False
if len(image.shape) == 2:
  bnw = True
else:
  bnw = False

r = len(image)
c = len(image[0])
z = 1
if not bnw:
  z = len(image[0][0])

key = input("Enter the key:")
a = key[:len(key)//3]
a = int(a) % len(image)
b = key[len(key)//3:2*len(key)//3]
b = int(b) % len(image[0])
step = key[2*len(key)//3:]
step = int(step) % 50 + 1
# a = random.randint(0, 127)
# b = random.randint(0, 127)
# step = random.randint(1, 50)

decodedMsg = ""
random.seed(step)
curRandom = random.randint(1,50)
i = a
j = b
cur = 0
curChar = ""
while i < r:
    for k in range(z):
        if i >= r:
            break
        if bnw:
            curChar += bin(image[i,j])[-1]
        else:
            curChar += bin(image[i,j,k])[-1]
        j += curRandom
        if j >= c:
            j = j % c
            i += 1
        random.seed(curRandom)
        curRandom = random.randint(1,50)
        if len(curChar) == 8:
            if chr(int(curChar, 2)) == '\0':
                break
            else:
                decodedMsg += chr(int(curChar, 2))
                curChar = ""
    if len(curChar) == 8 or i >= r:
        break
print("Decoded message:", decodedMsg)