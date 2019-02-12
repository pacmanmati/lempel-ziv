from bitarray import bitarray
import sys

# read file to encode and return as a bitarray
def read_file(name):
    with open(name, 'rb') as f:
        return bytearray(f.read())

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
    de = (bin(d)[2:]).zfill(8)
    le = (bin(l)[2:]).zfill(8)
    ce = (bin(c)[2:]).zfill(8)
    ba += de + le + ce
    print("{},{},'{}'".format(d,l,chr(c)))
    if d > 255 or l > 255:
        print("oopsie")
    return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f):
    encoded = bitarray()
    i = 0
    count = 0
    while i < len(f):
        print("{}th iteration".format(count))
        count += 1
        prefix = f[i:i+1]
        window_index = max(i-W, 0)
        window = f[window_index:i]
        length = 1
        dist = 0
        print("i {} prefix {}".format(i, prefix))
        if prefix is None: # end of file
            break
        rindex = window.rfind(prefix) #+ window_index + 1
        if rindex != -1: # if a match is found in the window
            rindex += window_index
            while prefix in f[rindex:rindex+length] and length < L and i + length < len(f):
                length += 1
                prefix = f[i:i+length]
                dist = i - rindex# - window_index - 1
            else: # ¯\_(ツ)_/¯
                length += 1
            length -= 1
            # we're done
            dist = i - rindex
            print("rindex {}".format(rindex))
            encoded += tuple(dist, length, prefix[-1])
            i += length
            #i = min(i + length, len(f))
            #print("i {} len {}".format(i, len(f)))
        else: # a new prefix was found
            encoded += tuple(0,0,prefix[-1])
            i += 1
    return encoded

# if missing file name
if len(sys.argv) < 2:
    print("usage: python lze.py [file_to_encode] (write_file)")

filename = sys.argv[1]
ba = encode(255, 255, read_file(filename))
#print(ba)

# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
