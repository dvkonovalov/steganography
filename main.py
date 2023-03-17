import time

import numpy
from PIL import Image

global height, width, passage
passage = 1


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
    secret += '☼'
    secret = ''.join(format(ord(x), '08b') for x in secret)
    x = 0
    y = 0
    count = 0
    position = 1
    color = 2

    mas = numpy.zeros((h, w), dtype=numpy.int64)
    sch = 0

    print(height, width, len(secret))
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
        mas[y, x] = sch
        sch += 1
        if count == (height * width):
            x = 0
            y = 0
            passage = 1
            color = (color + 1) % 3
            count = 0
            if color == 2:
                position += 1
    img.show()
    img.save('image2.jpg')
    return matrix

def extracting_information(path):
    img = Image.open(path)
    matrix = img.load()
    message = ''
    no_end = True
    while no_end:
        x = 0
        y = 0
        count = 0
        position = 1
        color = 2
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
        print(symbol)
        symbol = chr(int(symbol, 2))
        message += symbol
        print(message)
        time.sleep(1)
        if symbol=='☼':
            break
    return message


embedding_information('image2.jpg', 'Привет'*10000)

# width = 450
# height = 253
#
# mas = numpy.zeros((253, 450), dtype=numpy.int64)
# x = 0
# y = 0
# sch = 0
# for i in range(width*height):
#     if mas[y, x]!=0:
#         print(y, x)
#     mas[y, x] = sch
#     x, y = next_pixel(x, y)
#     sch += 1
# print(sch)

# print(extracting_information('image2.jpg'))
#
# img = Image.open('image1.jpg')
# matrix = img.load()
#
# for i in range(height):
#     for j in range(width):
#         if matrix[i, j][2]!=matrix1[i, j][2]:
#             print(matrix[i, j][2], matrix1[i, j][2], i, j)
#             time.sleep(1)