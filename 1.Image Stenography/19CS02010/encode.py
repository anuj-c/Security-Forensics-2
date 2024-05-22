import cv2
import numpy as np
import random

image = cv2.imread("../Cover_1.png", cv2.IMREAD_UNCHANGED)

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


def getPSNR(original, decoded):
    mse = np.mean((original - decoded) ** 2)
    print("MSE:", mse)
    l_value = 255
    if mse == 0:
        return 100
    psnr = 20 * np.log10((l_value - 1) / np.sqrt(mse))
    return psnr


key = input("Enter the key:")
a = key[: len(key) // 3]
a = int(a) % len(image)
b = key[len(key) // 3 : 2 * len(key) // 3]
b = int(b) % len(image[0])
step = key[2 * len(key) // 3 :]
step = int(step) % 50 + 1
# a = random.randint(0, 127)
# b = random.randint(0, 127)
# step = random.randint(1, 50)
message = input("Enter the message:")
message += "\0"
msgInBinary = "".join(format(ord(i), "08b") for i in message)

strIndex = 0
random.seed(step)
curRandom = random.randint(1, 50)
i = a
j = b
while i < r:
    for k in range(z):
        if strIndex >= len(msgInBinary) or i >= r:
            break
        else:
            if bnw:
                image[i, j] = int(bin(image[i, j])[:-1] + msgInBinary[strIndex], 2)
            else:
                image[i, j, k] = int(
                    bin(image[i, j, k])[:-1] + msgInBinary[strIndex], 2
                )
            strIndex += 1
            j += curRandom
            if j >= c:
                j = j % c
                i += 1
            random.seed(curRandom)
            curRandom = random.randint(1, 50)
    if strIndex >= len(msgInBinary) or i >= r:
        break

if strIndex < len(msgInBinary):
    print("Message too long to hide in image")
else:
    print("Message hidden successfully")
    cv2.imwrite("res.png", image)

image2 = cv2.imread("res.png", cv2.IMREAD_UNCHANGED)
image = cv2.imread("../Cover_1.png", cv2.IMREAD_UNCHANGED)

psnr = getPSNR(image, image2)
print("PSNR:", psnr)
