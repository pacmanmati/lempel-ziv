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
    #ce = bin(ord(c))[2:].zfill(8)
    # c is already encoded (slice of the original bitarray)
    ba += de + le
    ba += c
    # debug: print the tuple
    # print(c)
    print(d,l,c.to01())
    return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f):
    #print(f)
    encoded = bitarray()
    for i in range(len(f)):
        substring = f[i:i+1]
        window_index = i - W if i - W >= 0 else 0
        look_ahead_index = i + L if i + L <= len(f) else len(f)
        window = f[window_index:i]
        length = 1
        occurences = window.search(substring) # begins in window
        rightmost_match = -1 #= occurences[-1] # keep track of the rightmost match
        if len(occurences) > 0: # a match was found
            # keep expanding the search to get the longest prefix beginning in the window
            while len(occurences) > 0: # a match remains
                print('expand')
                length += 1
                substring = f[i:i+length] # the substring we're now matching
                rightmost_match = occurences[-1] # keep track of the rightmost match before searching again
                occurences = window.search(substring)
            # longest prefix starting in window was obtained - try extending the match into the lookahead
            print("rmm", rightmost_match)
            while substring in f[rightmost_match:rightmost_match+length+1]: # runs an extra time but idgaf
                length += 1
                if i + length > look_ahead_index:
                    length -= 1 # undo
                    break
                substring = f[i:i+length]
            # we're done
            encoded += tuple(rightmost_match, length, substring[-1])
            i += length
        else: # a new prefix was found
            print('new 1 len prefix')
            encoded += tuple(0,0,substring)
    return encoded
        
# if missing file name
if len(sys.argv) < 2:
    print("usage: python lze.py [file_to_encode] (write_file)")

filename = sys.argv[1]
ba = encode(1, 1, read_file(filename))
print(ba)

# save as specified file or default
if len(sys.argv) > 2:
    write_file(ba, sys.argv[2])
else:
    write_file(ba)
