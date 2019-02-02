from bitarray import bitarray
import sys

# store file in a string
def read_file(name):
    s = open(name).read()
    return s

# missing file name
if len(sys.argv) < 2:
    print("usage: python lze.py [file_to_encode]")

print(read_file(sys.argv[1]))
