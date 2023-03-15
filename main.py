import numpy
from PIL import Image

global height, width, passage
passage = 1

def change_value(number, bit, pos):
    """
    Функция для замены бита pos в числе number на значение bit
    :param number: число в котором производится замена
    :param bit: значение замены
    :param pos: позиция замены
    :return: результат замены
    """
    number = bin(number)[2:]
    if pos==1:
        number = number[:-pos] + str(bit)
    elif pos==len(number):
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
    if (x==passage-1 and y == passage):
        passage += 1
    if (x<width-passage and y==passage-1):
        x+=1
    elif (x==width-passage and y<height-passage):
        y += 1
    elif (y==height-passage and x>passage-1):
        x-=1
    else:
        y -= 1
    return x, y




def embedding_information(path, secret):
    global height, width
    img = Image.open(path)
    matrix = img.load()
    (height, width) = img.size
    secret = ''.join(format(ord(x), '08b') for x in secret)
    x = 0
    y = 0
    for symbol in secret:
        pixel = matrix[y, x]
        temp = (pixel[0], change_value(pixel[1], int(symbol), 1), pixel[2])
        matrix[y, x] = temp
        x, y = next_pixel(x, y)
    img.show()


embedding_information('image1.jpg', 'hello')