from bitarray import bitarray
import sys
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

def decode(d_bits, l_bits, f):
    decoded = bitarray()
    instructions = []
    i = 0
    count = 0
    #print(len(f))
    while i < len(f):
        #print("--------------------")
        #print("{}th iteration below".format(count))
        count += 1
        # get d, l, c from bitarray
        d = int(f[i:i+8].to01(), 2)
        i += 8
        l = int(f[i:i+8].to01(), 2)
        i += 8
        c = f[i:i+8]
        i += 8
        # write to decoded output
        if l > 0:
            ref = decoded[-d*8:]
            # print(len(ref)/8)
            #print(ref.tostring())
        for j in range(0, (l)*8, 8): # go up in 8s
            start_index = j % len(ref)
            #print(start_index)
            decoded += ref[start_index:start_index+8]
        print("tuple is ({},{},{})".format(d, l, chr(int(c.to01(), 2))))
        #print(decoded.tostring())
        #print()
        decoded += c # add the ending character
    return decoded

# if missing args
if len(sys.argv) < 5:
    print("usage: python lzd.py [file_to_decode] [write_file] [d_bytes] [l_bytes]")

# 3 128
# D_BITS = (2**int(sys.argv[3])) - 1
# L_BITS = (2**int(sys.argv[4])) - 1
D_BITS = int(sys.argv[3])*8
L_BITS = int(sys.argv[4])*8
    
start = time.time()
filename = sys.argv[1]    
ba = decode(255, 255, read_file(filename))
print("time taken: {}".format(time.time() - start))
    
# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
