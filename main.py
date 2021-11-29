import math
import random
import os
import time
import matplotlib.pyplot as plt

from Huffman import HuffmanCoding
from Shannon_Fano import Shannon_fano_structure

class myData:
    def __init__(self,algorithm, complexity, original_size, compressed_size, compression_duration, decompressed_size, decompression_duration, efficiency, performance):
        self.algorithm = algorithm
        self.complexity = complexity
        self.original_size = original_size
        self.compressed_size = compressed_size
        self.compression_duration = compression_duration
        self.decompressed_size = decompressed_size
        self.decompression_duration = decompression_duration
        self.efficiency = efficiency
        self.performance = performance

def getSize(file):
    file_size = os.path.getsize(file)/1000
    return file_size

def executeHuffman(original_file, complexity):
    # HUFFMAN CODE
    # ORIGINAL SIZE, COMPRESSED SIZE, DURATION, COMPLEXITY
    huffman_compressed = complexity + "_huffman_compressed.bin"
    hc = HuffmanCoding(original_file)

    start_compressing =time.time()
    hc.compress()
    print("Huffman compression for",complexity,"successful")
    end_compressing = time.time()
    compressed_size = getSize(huffman_compressed)

    start_decompressing = time.time()
    hc.decompress(huffman_compressed)
    print("Huffman decompression for",complexity,"successful")
    end_decompressing = time.time()


    original_size = getSize(original_file)
    efficiency = ( original_size - compressed_size ) / original_size *100
    decompressed_size = original_size
    algorithm = "Huffman"
    compression_duration = end_compressing-start_compressing
    decompression_duration = end_decompressing-start_decompressing

    if compression_duration != 0:
        angle = math.degrees(math.atan((original_size-compressed_size)/(compression_duration*1000)))
    else:
        angle = 90

    data = myData(algorithm, complexity, original_size, compressed_size, compression_duration, decompressed_size, decompression_duration, efficiency, angle)
    data_arr.append(data)

def executeShannon(original_file, complexity):
    output_file = complexity+"_shannon_compressed.bin"
    with open(original_file, 'r+', encoding="utf-8") as file, open(output_file, "wb") as output:
        text = file.read()
        start_compressing = time.time()

        sf = Shannon_fano_structure()
        sf.compress_(text)
        after_compression = sf.compression(text)
        pad_encoded_text = sf.pad_encoded_text(after_compression)
        b = sf.get_byte_array(pad_encoded_text)
        output.write(bytes(b))
        end_compressing = time.time()
        print("Shannon-Fano compression for",complexity,"successful")

    # DATA TO BE RECORDED
    algorithm = "ShannonFano"
    original_size = getSize(original_file)
    compressed_size = getSize(output_file)
    compression_duration = end_compressing-start_compressing
    decompressed_size = 0
    decompression_duration = 0
    efficiency = ( original_size - compressed_size ) / original_size *100
    if compression_duration != 0:
        angle = math.degrees(math.atan((original_size-compressed_size)/(compression_duration*1000)))
    else:
        angle = 90
    data = myData(algorithm, complexity, original_size, compressed_size, compression_duration, decompressed_size, decompression_duration, efficiency,angle)
    data_arr.append(data)

def printData():
    print("="*200)
    for i in range(len(data_arr)+1):
        if i == 0:
            print('{:<15}|{:<20}|{:<17}|{:<17}|{:<25}|{:<20}|{:<25}|{:<25}|{:<10}'.format("Algorithm","Complexity","Original Size","Compressed Size","Compression Duration",
                                                                 "Decompressed Size", "Decompression Duration","Efficiency","Performance"))

        else:
            print('{:<15}|{:<20}|{:<13}KB  |{:<13}KB  |{:<25}|{:<16}KB  |{:<25}|{:<23} %|{:<10}'.format(data_arr[i-1].algorithm,data_arr[i-1].complexity,data_arr[i-1].original_size,
                                                             data_arr[i-1].compressed_size,data_arr[i-1].compression_duration,data_arr[i-1].decompressed_size,
                                                             data_arr[i-1].decompression_duration,data_arr[i-1].efficiency,data_arr[i-1].performance))
        if i % 6 == 0:
            print("-"*200)

def generate_txt(n_smaller_file):
    binary = "01"
    octal = '01234567'
    character = 'abcdefghijklmnopqrstuvxyzABCDEFGHIJKLMNOPQRSTUVWUXYZ'

    random_bin_str = ''
    random_oct_str = ''
    random_char_str = ''

    # for smaller file
    binarysmaller = "binary" + str(n_smaller_file) +".txt"
    octalsmaller = "octal" + str(n_smaller_file) +".txt"
    charactersmaller = "character" + str(n_smaller_file) +".txt"
    binary100_txt = open(binarysmaller,"w")
    octal100_txt = open(octalsmaller,"w")
    character100_txt = open(charactersmaller,"w")


    for j in range (n_smaller_file):
        # 2 Varies
        random_bin = random.choice(binary)
        random_bin_str += random_bin
        # 8 Varies
        random_oct = random.choice(octal)
        random_oct_str += random_oct

        # 52 Varies
        random_char = random.choice(character)
        random_char_str += random_char


    binary100_txt.write(random_bin_str)
    octal100_txt.write(random_oct_str)
    character100_txt.write(random_char_str)

    binary100_txt.close()
    print(binarysmaller,"Successfuly written into txt file")
    octal100_txt.close()
    print(octalsmaller,"Successfuly written into txt file")
    character100_txt.close()
    print(charactersmaller,"Successfuly written into txt file")


def show_graph():
    fig1 = plt.figure(1)
    ax1 = fig1.add_subplot(131)
    ax2 = fig1.add_subplot(132)
    ax3 = fig1.add_subplot(133)

    for i in range(len(data_arr)//3):
        curr = i
        x = [0,data_arr[curr].compression_duration]
        y = [data_arr[curr].original_size, data_arr[curr].compressed_size]
        ax1.plot(x, y, "o-",markersize = 5,label=data_arr[curr].complexity+data_arr[curr].algorithm)
        ax1.set_xlabel("Time(S)")
        ax1.set_ylabel("Size(KB)")
        ax1.set_title("First Run")
        ax1.legend(loc="upper right")

    for i in range(len(data_arr)//3):
        curr = i+6
        x = [0,data_arr[curr].compression_duration]
        y = [data_arr[curr].original_size, data_arr[curr].compressed_size]
        ax2.plot(x, y, "o-",label=data_arr[curr].complexity+data_arr[curr].algorithm)
        ax2.set_xlabel("Time(S)")
        ax2.set_ylabel("Size(KB)")
        ax2.set_title("Second Run")
        ax2.legend(loc="upper right")

    for i in range(len(data_arr)//3):
        curr = i+12
        x = [0,data_arr[curr].compression_duration]
        y = [data_arr[curr].original_size, data_arr[curr].compressed_size]
        ax3.plot(x, y, "o-",label=data_arr[curr].complexity+data_arr[curr].algorithm)
        ax3.set_xlabel("Time(S)")
        ax3.set_ylabel("Size(KB)")
        ax3.set_title("Third Run")
        ax3.legend(loc="upper right")

    plt.show()

# MAIN PROGRAM GOES HERE
data_arr = []
n_smaller_file = int(input("Input Num of Character(s) :"))
generate_txt(n_smaller_file)
# executes all compressions
original_file_arr = ["binary","octal","character"]
for i in range(9):
    if i < (len(original_file_arr)):
        curr = i
        print("FIRST RUN")
        original_file = original_file_arr[curr] + str(n_smaller_file) +".txt"

    elif 2<i<6 :
        curr = i - 3
        print("SECOND RUN")
        original_file = original_file_arr[curr] + str(n_smaller_file) +".txt"

    else:
        curr = i - 6
        print("THIRD RUN")
        original_file = original_file_arr[curr] + str(n_smaller_file) +".txt"


    complexity = original_file[:-4]
    executeHuffman(original_file, complexity)
    executeShannon(original_file,complexity)
    print()

# prints all data
printData()
show_graph()