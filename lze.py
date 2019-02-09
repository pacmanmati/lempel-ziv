from bitarray import bitarray
import sys

# read file to encode and return as a bitarray
def read_file(name):
    ba = bitarray()
    with open(name, 'rb') as f:
        ba.fromfile(f)
    return ba

# write encoded bitarray to file
def write_file(ba, name="encoded.bin"):
    with open(name, 'wb') as f:
        ba.tofile(f)

# returns a binary tuple:
# d - distance to start of prefix (int),
# l - length to repeat,
# c - character following prefix input.
def tuple(d, l, c):
    ba = bitarray()
    de = bin(d)[2:].zfill(8)
    le = bin(l)[2:].zfill(8)
    ce = bin(ord(c))[2:].zfill(8)
    ba += de + le + ce
    return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f): # one byte per int
    print(f)
    encoded = bitarray()
    for i in range(len(f)):
        bit = f[i]
        window_index = bit - W if i - W >= 0 else 0
        look_ahead_index = bit + L if i + L <= len(f) else len(f)
        window = f[window_index:i] 
        look_ahead = f[i+1:look_ahead_index+1] # excludes the current bit
        length = 0
        # while pattern in window:
        #     length += 1
    return encoded
        
# if missing file name
if len(sys.argv) < 2:
    print("usage: python lze.py [file_to_encode] (write_file)")

filename = sys.argv[1]
ba = encode(1, 1, read_file(filename))

# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
