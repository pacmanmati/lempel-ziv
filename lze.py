from bitarray import bitarray
import sys
import time

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
    #print("{},{},'{}'".format(d,l,chr(c)))
    # if d > 255 or l > 255:
    #     print("oopsie")
    return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f):
    encoded = bitarray()
    i = 0
    count = 0
    while i < len(f):
        # print("--------------")
        # print("{}th iteration".format(count))
        count += 1
        prefix = f[i:i+1]
        window_index = max(i-W, 0)
        window = f[window_index:i]
        length = 0
        dist = 0
        # print("i {} prefix {}".format(i, prefix))
        if prefix is None: # end of file
            break
        # print("window:",window)
        rindex = window.rfind(prefix) #+ window_index + 1
        if rindex != -1: # if a match is found in the window
            # print("slice is", f[rindex:rindex+length+1])
            # print("prefix", prefix)
            save = rindex # will contain the last known rindex
            while rindex != -1 and i + length < len(f) - 1: # find the longest match in the window
                save = rindex
                length += 1
                prefix = f[i:i+length+1]
                rindex = window.rfind(prefix)
                # print("length:", length)
                # print("prefix is", prefix)
            else:
                length += 1
            length -= 1
            rindex = save
            rindex += window_index
            # print("found rightmost in window")
            # print("slice is",f[rindex:rindex+length+1])
            while prefix in f[rindex:rindex+length+1] and length < L and i + length < len(f) - 1:
                length += 1
                prefix = f[i:i+length+1]
                # print("length:", length)
                # print("slice is",f[rindex:rindex+length+1])
                # print("prefix is", prefix)
                dist = i - rindex# - window_index - 1
            else: # ¯\_(ツ)_/¯
                length += 1
            length -= 1
            # we're done
            dist = i - rindex
            # print("rindex {}".format(rindex))
            encoded += tuple(dist, length, prefix[-1])
            i += length + 1
            #i = min(i + length, len(f))
            #print("i {} len {}".format(i, len(f)))
        else: # a new prefix was found
            encoded += tuple(0,0,prefix[-1])
            i += 1
    return encoded

# if missing args
if len(sys.argv) < 5:
    print("usage: python lze.py [file_to_encode] [write_file] [W] [L]")
    sys.exit()

# W = int(sys.argv[3])
# L = int(sys.argv[4])

start = time.time()
filename = sys.argv[1]
ba = encode(255, 255, read_file(filename))
#print(ba)
print("time taken: {}".format(time.time() - start))

# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
