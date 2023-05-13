from Info_Theory.Source_Encoding_v6 import huffman_zip

if __name__ == "__main__":
    file_name = "testfile2"
    n = 32
    zip_name = huffman_zip(file_name, n)
    # unzip_name = huffman_unzip(file_name)
    # cmp_file(file_name, unzip_name)
