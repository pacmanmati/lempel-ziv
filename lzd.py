from bitarray import bitarray
import sys
import math
import time

def read_file(name):
    ba = bitarray()
    with open(name, 'rb') as f:
        ba.fromfile(f)
        #print(ba)
    return ba
    
def write_file(ba, name="decoded.txt"):
    with open(name, 'wb') as f:
        ba.tofile(f)

def decode(d_bits, l_bits, cutoff, f):
    decoded = bitarray()
    instructions = []
    i = 0
    count = 0
    #print(len(f))
    while i < len(f) - cutoff:
        #print("--------------------")
        #print("{}th iteration below".format(count))
        #count += 1
        # get d, l, c from bitarray
        
        d = int(f[i:i+d_bits].to01(), 2)
        i += d_bits
        l = int(f[i:i+l_bits].to01(), 2)
        i += l_bits
        c = f[i:i+8]
        i += 8

        # write to decoded output
        # if l > 0:
        #     ref = decoded[-d*8:]
            # print(len(ref)/8)
            #print(ref.tostring())
        for j in range(len(decoded)-d*8, len(decoded)-(d*8)+l*8, 1): # go up in 8s
            decoded.append(decoded[j])
        #print("tuple is ({},{},{})".format(d, l, chr(int(c.to01(), 2))))
        #print(decoded.tostring())
        #print()
        decoded += c # add the ending character
    return decoded

# if missing args
if len(sys.argv) < 5:
    print("usage: python lzd.py [file_to_decode] [write_file] [d_bytes] [l_bytes]")

W = int(sys.argv[3])
L = int(sys.argv[4])

D_BITS = math.floor(math.log(W, 2) + 1)
L_BITS = math.floor(math.log(L, 2) + 1)

cutoff = 8 - ((D_BITS + L_BITS) % 8)
    
start = time.time()
filename = sys.argv[1]    
ba = decode(D_BITS, L_BITS, cutoff, read_file(filename))
print("time taken: {}".format(time.time() - start))
    
# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
