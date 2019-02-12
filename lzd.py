from bitarray import bitarray
import sys

def read_file(name):
    ba = bitarray()
    with open(name, 'rb') as f:
        ba.fromfile(f)
        print(ba)
    return ba
    
def write_file(ba, name="decoded.txt"):
    with open(name, 'wb') as f:
        ba.tofile(f)

def decode(d_bits, l_bits, f):
    decoded = bitarray()
    instructions = []
    i = 0
    count = 0
    print(len(f))
    while i < len(f):
        print("{}th iteration below".format(count))
        count += 1
        # get d, l, c from bitarray
        d = int(f[i:i+d_bits].to01(), 2)
        i += d_bits
        l = int(f[i:i+l_bits].to01(), 2)
        i += l_bits
        c = f[i:i+8]
        i += 8
        # write to decoded output
        if l > 0:
            ref = decoded[-d*8:]
            # print(len(ref)/8)
            # print(ref.tostring())
        for j in range(0, (l-1)*8, 8): # go up in 8s
            start_index = j % len(ref)
            # print(start_index)
            decoded += ref[start_index:start_index+8]
        print("tuple is ({},{},{})".format(d, l, c))
        print(decoded.tostring())
        print()
        decoded += c # add the ending character
    return decoded

# if missing file name
if len(sys.argv) < 2:
    print("usage: python lzd.py [file_to_decode] (write_file)")

filename = sys.argv[1]    
ba = decode(8, 8, read_file(filename))
    
# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
