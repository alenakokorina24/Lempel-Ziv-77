import os
from struct import *


def get_max_substr(window, string):
    # string - следующие n символов за окном, среди которых ищем наибольшую подстроку в окне
    # n - длина окна
    for i in reversed(range(len(window))):
        # начинаем сразу со строки наибольшей длины
        substring = string[:i + 1]
        index = window.find(substring)
        if index != -1:
            return index + 1, i + 1
    return 0, 0


def write_to_file(dictionary, path, filename, window):
    with open(path + filename.split(os.path.sep)[-1] + ".lz77", 'wb') as encoded_file:
        encoded_file.write(pack('B', len(window)))
        encoded_file.write(window)
        flatten_dict = [x for t in dictionary for x in t]
        chunks = [flatten_dict[x:x+256] for x in range(0, len(flatten_dict), 256)]
        for chunk in chunks:
            encoded_file.write(pack('B' * len(chunk), *chunk))


def encode(filename, path, window_size):  # path - путь куда сохранить закодированный файл
    input_file = open(filename, "rb")
    file_size = os.path.getsize(filename)
    dictionary = []
    pos = window_size  # первая позиция после окна в кодируемой последовательности
    data = input_file.read(256)
    original_window = data[:window_size]
    window = original_window
    bytes_read = b''
    while True:
        if len(data) - pos <= window_size < file_size - pos:
            bytes_read = input_file.read(256)
            data = data[pos - window_size:len(data)] + bytes_read
            pos = window_size
        offset, length = get_max_substr(window, data[pos:pos + window_size])
        dictionary.append((offset, length, data[pos+length]))
        pos += (length + 1)
        if pos == len(data) and len(bytes_read) == 0:
            break
        window = data[pos - window_size:pos]
    input_file.close()
    write_to_file(dictionary, path, filename, original_window)


def bytes_to_dict(dict_bytes):  # здесь под словарём подразумевается просто список значений без ключей
    dictionary = []
    i = 0
    while i != len(dict_bytes):
        dictionary.append(unpack('BBB', dict_bytes[i:i+3]))
        i += 3
    return dictionary


def decode(filename, path):  # path - путь куда сохранить закодированный файл
    input_file = open(filename, "rb")
    window_size = unpack('B', input_file.read(1))[0]

    data = b''
    while True:
        bytes_read = input_file.read(256)
        if not bytes_read:
            break
        data += bytes_read
    input_file.close()

    window = data[:window_size]
    decoded_data = window
    pos = len(window)  # первая позиция после окна
    dictionary = bytes_to_dict(data[window_size:])

    for value in dictionary:
        offset = value[0]  # начальный индекс подстроки в текущем окне
        length = value[1]
        k = value[2].to_bytes(1, byteorder='little')
        if offset != 0:
            decoded_data += window[offset-1:offset-1 + length]
        decoded_data += k
        pos += (length + 1)
        window = decoded_data[pos - len(window):pos]

    with open(path + filename.split(os.path.sep)[-1] + "_decoded", 'wb') as decoded_file:
        decoded_file.write(decoded_data)


# encode("/home/alena/Desktop/кот.jpg", "/home/alena/Desktop/", 5)
# decode("/home/alena/Desktop/кот.jpg.lz77", "/home/alena/Desktop/")
#
# encode("/home/alena/Desktop/good.txt", "/home/alena/Desktop/", 5)
# decode("/home/alena/Desktop/good.txt.lz77", "/home/alena/Desktop/")
#
# encode("/home/alena/Desktop/a.jpeg", "/home/alena/Desktop/", 32)
# decode("/home/alena/Desktop/a.jpeg.lz77", "/home/alena/Desktop/")
#
# encode("/home/alena/Desktop/ava.jpg", "/home/alena/Desktop/", 32)
# decode("/home/alena/Desktop/ava.jpg.lz77", "/home/alena/Desktop/")
#
# encode("/home/alena/Desktop/q.txt", "/home/alena/Desktop/", 5)
# decode("/home/alena/Desktop/q.txt.lz77", "/home/alena/Desktop/")
#
# encode("/home/alena/Desktop/деревня.txt", "/home/alena/Desktop/", 5)
# decode("/home/alena/Desktop/деревня.txt.lz77", "/home/alena/Desktop/")

encode("/home/alena/Desktop/best.txt", "/home/alena/Desktop/", 5)
decode("/home/alena/Desktop/best.txt.lz77", "/home/alena/Desktop/")