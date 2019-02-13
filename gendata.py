import os
import time
import sys

filename = sys.argv[1]
original_filesize = os.path.getsize("data/original_files/{}".format(filename))

W_DATA = []
L_DATA = []
TIME_DATA_ENCODER = []
TIME_DATA_DECODER = []
RATIO_DATA = []

for W in range(1000, 2000, 1000):
    for L in range(1000, 2000, 1000):
        
        W_DATA.append(W)
        L_DATA.append(L)
        
        start = time.time()
        os.system("python lze.py data/original_files/{} /data/encoded_storage/encoded.bin {} {}".format(filename, W, L))
        TIME_DATA_ENCODER.append(time.time() - start)
        time.sleep(5)
        start = time.time()
        os.system("python lzd.py data/encoded_storage/encoded.bin data/decoded_storage/{} {} {}".format(filename, W, L))
        TIME_DATA_DECODER.append(time.time() - start)
        
        RATIO_DATA.append(original_filesize/os.path.getsize("data/encoded_storage/encoded.bin"))

def list_to_csv(list):
    ret_string = ""
    for value in list:
        ret_string += value + ","
    return ret_string
        
with open("data/output_files/{}".format(filename), "w") as f:
    f.write(list_to_csv(W_DATA))
    f.write(list_to_csv(L_DATA))
    f.write(list_to_csv(TIME_DATA_ENCODER))
    f.write(list_to_csv(TIME_DATA_DECODER))
    f.write(list_to_csv(RATIO_DATA))
