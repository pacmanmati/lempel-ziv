from bitarray import bitarray
import sys
import time

# store file in a string
def read_file(name):
    e = bitarray()
    with open(name, 'rb') as f:
        e.fromfile(f)
    return e

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

# slower methods

# def tuple_alt_alt(d, l, c):
#     ba = bitarray()
#     de = "{0:b}".format(d).zfill(8)
#     le = "{0:b}".format(l).zfill(8)
#     ce = "{0:b}".format(ord(c)).zfill(8)
#     ba += de + le + ce
#     return ba

# def tuple_alt(d, l, c):
#     ba = bitarray()
#     de = format(d, '08b')
#     le = format(l, '08b')
#     ce = format(ord(c), '08b')
#     ba += de + le + ce
#     return ba

# lz77 encoder on 'f' using a sliding window of length 'W', and a lookahead buffer 'L'
def encode(W, L, f): # one byte per int
    print(f)
    for i in range(len(f)):
        bit = f[i]
        window_index = bit - W if i - W >= 0 else 0
        look_ahead_index = bit + L if i + L <= len(f) else len(f)
        window = f[window_index:i] 
        look_ahead = f[i+1:look_ahead_index+1] # excludes the current bit
        length = 0
        while pattern in window:
            length += 1
        
# missing file name
if len(sys.argv) < 2:
    print("usage: python lze.py [file_to_encode]")

filename = sys.argv[1]
#encode(1, 1, read_file(filename))

# print(tuple(5,5,'a'))
# print(tuple_alt(5,5,'a'))
# print(tuple_alt_alt(5,5,'a'))

# speed test
def speed_test(NUM_ITER):
    start = time.time()
    for i in range(NUM_ITER):
        tuple(i,i,'a')

    t1 = time.time() - start
    start = time.time()
    for i in range(NUM_ITER):
        tuple_alt(i,i,'a')
    t2 = time.time() - start
    start = time.time()
    for i in range(NUM_ITER):
        tuple_alt_alt(i,i,'a')
    t3 = time.time() - start
    print("t1: {}, t2: {}, t3: {}".format(t1,t2,t3))
speed_test(100000)
