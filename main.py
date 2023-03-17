import time

import numpy
from PIL import Image

global height, width, passage
passage = 1


def save_image(matrix, path):
    img = Image.new('RGB', (height, width), 'white')
    matrix_new = img.load()
    for i in range(height):
        for j in range(width):
            matrix_new[i, j] = matrix[i, j]
    img.save(path, 'JPEG')

def get_bit(number, position):
    """
    Функция получения бита
    :param number: число
    :param position: позиция бита
    :return: бит
    """
    number = bin(number)[2:]
    if (len(number)<8):
        number = '0'*(8-len(number)) + number
    return number[-position]


def change_value(number, bit, pos):
    """
    Функция для замены бита pos в числе number на значение bit
    :param number: число в котором производится замена
    :param bit: значение замены
    :param pos: позиция замены
    :return: результат замены
    """
    number = bin(number)[2:]
    if pos == 1:
        number = number[:-pos] + str(bit)
    elif pos == len(number):
        number = str(bit) + number[-pos + 1:]
    else:
        number = number[:-pos] + str(bit) + number[-pos + 1:]
    number = int(number, 2)
    return number


def next_pixel(x, y):
    """
    Перейти спирально к следующему пикселю в матрице
    :param x: координата x
    :param y: координата y
    :return: x, y
    """
    global width, height, passage
    if (x == passage - 1 and y == passage):
        passage += 1
    if (x==width//2 and passage==width//2):
        y-1
    elif (x < width - passage and y == passage - 1):
        x += 1
    elif (x == width - passage and y < height - passage):
        y += 1
    elif (y == height - passage and x > passage - 1):
        x -= 1
    else:
        y -= 1
    return x, y


def embedding_information(path, secret):
    global height, width, passage
    img = Image.open(path)
    matrix = img.load()
    (h, w) = img.size
    height = h
    width = w
    secret = ''.join(format(ord(x), '08b') for x in secret)
    secret += '0'*8
    x = 0
    y = 0
    count = 0
    position = 1
    color = 2
    for symbol in secret:
        if color == 2:
            pixel = matrix[y, x]
            temp = (pixel[0], pixel[1], change_value(pixel[2], int(symbol), position))
            matrix[y, x] = temp
            x, y = next_pixel(x, y)
            count += 1
        elif color == 0:
            pixel = matrix[y, x]
            temp = (change_value(pixel[0], int(symbol), position), pixel[1], pixel[2])
            matrix[y, x] = temp
            x, y = next_pixel(x, y)
            count += 1
        else:
            pixel = matrix[y, x]
            temp = (pixel[0], pixel[1], change_value(pixel[2], int(symbol), position))
            matrix[y, x] = temp
            x, y = next_pixel(x, y)
            count += 1
        if count == (height * width):
            x = 0
            y = 0
            passage = 1
            color = (color + 1) % 3
            count = 0
            if color == 2:
                position += 1
    return matrix

def extracting_information(matrix):
    message = ''
    no_end = True
    x = 0
    y = 0
    count = 0
    position = 1
    color = 2
    while no_end:
        symbol = ''
        for _ in range(8):
            if color == 2:
                number = matrix[y, x][2]
                symbol += get_bit(number, position)
                x, y = next_pixel(x, y)
                count += 1
            elif color == 0:
                number = matrix[y, x][0]
                symbol += get_bit(number, position)
                x, y = next_pixel(x, y)
                count += 1
            else:
                number = matrix[y, x][1]
                symbol += get_bit(number, position)
                x, y = next_pixel(x, y)
                count += 1
            if count == (height * width):
                x = 0
                y = 0
                passage = 1
                color = (color + 1) % 3
                if color == 2:
                    position += 1
        symbol = int(symbol, 2)
        if symbol==0:
            break
        symbol = chr(symbol)
        message += symbol
    return message


matrix = embedding_information('image2.jpg', 'PYTHON'*1)
print(extracting_information(matrix))
# save_image(matrix, 'image3.jpg')
#
# img = Image.open('image3.jpg')
# matrix1 = img.load()

# for i in range(height):
#     for j in range(width):
#         print(matrix1[i, j][2]%2)
#         time.sleep(1)