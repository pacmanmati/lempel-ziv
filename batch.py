from bitarray import bitarray
import sys
import math
import time

# encoder functions

# read file to encode and return as a bitarray
def read_file_bytes(name):
    with open(name, 'rb') as f:
        return bytearray(f.read())

# returns a binary tuple:
# d - distance to start of prefix (int),
# l - length to repeat,
# c - character following prefix input.
def tuple(d, l, c):
    ba = bitarray()
    de = (bin(d)[2:]).zfill(D_BITS)
    le = (bin(l)[2:]).zfill(L_BITS)
    ce = (bin(c)[2:]).zfill(8)
    ba += de + le + ce
    return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f):
    encoded = bitarray()
    i = 0
    count = 0
    while i < len(f):
        count += 1
        prefix = f[i:i+1]
        window_index = max(i-W, 0)
        window = f[window_index:i]
        length = 0
        dist = 0
        if prefix is None: # end of file
            break
        rindex = window.rfind(prefix) #+ window_index + 1
        if rindex != -1: # if a match is found in the window
            save = rindex # will contain the last known rindex
            while rindex != -1 and i + length < len(f) - 1: # find the longest match in the window
                save = rindex
                length += 1
                prefix = f[i:i+length+1]
                rindex = window.rfind(prefix)
            else:
                length += 1
            length -= 1
            rindex = save
            rindex += window_index
            while prefix in f[rindex:rindex+length+1] and length < L and i + length < len(f) - 1:
                length += 1
                prefix = f[i:i+length+1]
                dist = i - rindex# - window_index - 1
            else: # ¯\_(ツ)_/¯
                length += 1
            length -= 1
            # we're done
            dist = i - rindex
            encoded += tuple(dist, length, prefix[-1])
            i += length + 1
        else: # a new prefix was found
            encoded += tuple(0,0,prefix[-1])
            i += 1
    return encoded

# decoder functions

def decode(d_bits, l_bits, cutoff, f):
    decoded = bitarray()
    instructions = []
    i = 0
    count = 0
    #print(len(f))
    while i < len(f) - cutoff:
        #print("--------------------")
        #print("{}th iteration below".format(count))
        count += 1
        # get d, l, c from bitarray
        d = int(f[i:i+d_bits].to01(), 2)
        i += d_bits
        l = int(f[i:i+l_bits].to01(), 2)
        i += l_bits
        c = f[i:i+8]
        i += 8
        # write to decoded output
        for j in range(len(decoded)-d*8, len(decoded)-(d*8)+l*8, 1): # go up in 8s
            decoded.append(decoded[j])
        decoded += c # add the ending character
    return decoded

# batch run

#D_BITS = math.floor(math.log(W, 2) + 1)
#L_BITS = math.floor(math.log(L, 2) + 1)
D_BITS = 0
L_BITS = 0

filename = sys.argv[1]
#original_filesize = os.path.getsize("data/original_files/{}".format(filename))

W_DATA = []
L_DATA = []
TIME_DATA_ENCODER = []
TIME_DATA_DECODER = []
RATIO_DATA = []

f = read_file_bytes("data/original_files/{}".format(filename))

for W in range(1000, 2000, 1000):
    D_BITS = math.floor(math.log(W, 2) + 1)
    for L in range(1000, 2000, 1000):
        L_BITS = math.floor(math.log(L, 2) + 1)
        cutoff = 8 - ((D_BITS + L_BITS) % 8)
        
        W_DATA.append(W)
        L_DATA.append(L)
        
        start = time.time()
        #os.system("python lze.py data/original_files/{} /data/encoded_storage/encoded.bin {} {}".format(filename, W, L))
        encoded = encode(W, L, f)
        TIME_DATA_ENCODER.append(time.time() - start)

        start = time.time()
        #os.system("python lzd.py data/encoded_storage/encoded.bin data/decoded_storage/{} {} {}".format(filename, W, L))
        decoded = decode(D_BITS, L_BITS, cutoff, encoded)
        TIME_DATA_DECODER.append(time.time() - start)
        
        RATIO_DATA.append(len(f)/math.ceil(len(encoded)/8))

def list_to_csv(list):
    ret_string = ""
    for value in list:
        ret_string += "{},".format(value)
    ret_string += "\n"
    return ret_string
        
with open("data/output_files/{}".format(filename), "w") as f:
    f.write(list_to_csv(W_DATA))
    f.write(list_to_csv(L_DATA))
    f.write(list_to_csv(TIME_DATA_ENCODER))
    f.write(list_to_csv(TIME_DATA_DECODER))
    f.write(list_to_csv(RATIO_DATA))
