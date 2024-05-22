import random
from scipy.io import wavfile

rate, secret_file = wavfile.read("stego_audio.wav")
secret_bytes = secret_file.T
secret_len = len(secret_bytes[0])

key = input("Enter the key: ")
i = int(key[:len(key)//2]) % ( secret_len // 2)
step = int(key[len(key)//2:])

ex_msg = ""
temp_msg = ""
msgLen = ""

# Getting the length of message
while i < secret_len:
  msgLen += str(secret_bytes[0][i] & 1)
  if len(msgLen) == 16:
    break
  i += 1

random.seed(step)
range = secret_len // int(msgLen, 2)
step = random.randint(range//2,range)
i += step
random.seed(step)
step = random.randint(range//2,range)
while i < secret_len:
  temp_msg += str(secret_bytes[0][i] & 1)
  if len(temp_msg) == 8:
    if chr(int(temp_msg, 2)) == "$":
      break
    ex_msg += chr(int(temp_msg, 2))
    temp_msg = ""
  i += step
  random.seed(step)
  step = random.randint(range//2,range)
print("Extracted message len: ", len(ex_msg))
with open("extracted_message.txt", "w") as f:
  f.write(ex_msg)
f.close()
# print("Extracted message: ", ex_msg)