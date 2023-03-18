import os

import numpy
import skimage
from PIL import Image

global height, width, passage


def save_image(matrix, path):
    """
    Функция для сохранения изображения после встраивания информации
    :param matrix: матрица пикселей
    :param path: путь для сохранения
    :return:
    """
    im = Image.new('RGB', (height, width), 'white')
    matrix_new = im.load()
    for i in range(height):
        for j in range(width):
            pixel = matrix[i, j]
            matrix_new[i, j] = (pixel[0], pixel[1], pixel[2])
    im.save(path)


def get_bit(number, position):
    """
    Функция получения бита
    :param number: число
    :param position: позиция бита
    :return: бит
    """
    number = bin(number)[2:]
    if len(number) < 8:
        number = '0' * (8 - len(number)) + number
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
    if x == passage - 1 and y == passage:
        passage += 1
    if x == width // 2 and passage == width // 2:
        y - 1
    elif x < width - passage and y == passage - 1:
        x += 1
    elif x == width - passage and y < height - passage:
        y += 1
    elif y == height - passage and x > passage - 1:
        x -= 1
    else:
        y -= 1
    return x, y


def embedding_information(matrix, secret):
    """
    Функция для встраивания секретной информации в изображение
    :param matrix: матрица начального изображения
    :param secret: секретная информация в виде строки
    :return:матрица пикселей с встроенной секретной информацией
    """
    global passage
    passage = 1
    secret = ''.join(format(ord(x), '08b') for x in secret)
    secret += '0' * 8
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
            if position == 9:
                break
    return matrix


def extracting_information(matrix):
    """
    Декодирование секретной информации из изображения
    :param matrix: матрица пикселей изображения
    :return: секретное сообщение
    """
    global passage
    passage = 1
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
        if symbol == 0:
            break
        symbol = chr(symbol)
        message += symbol
    return message



def find_secret(path):
    """
    Функция для обрадотки декдирования секретной информации из изображения и запись ее в файл secret.txt
    :param path: Путь к изображению
    :return:
    """
    global height, width
    img = Image.open(path)
    matrix = img.load()
    (height, width) = img.size
    message = extracting_information(matrix)
    with open('secret.txt', 'w') as f:
        f.write(message)
    return True



def insert_secret(path_image, message, file=False):
    """
    Функция обработки изображения и взодных данных
    :param path_image: путь до изображения
    :param message: сообщение или путь до файла
    :param file: True если используется файл передачи секретных данных
    :return: True - успех, False - произошла ошибка
    """
    global height, width
    img = Image.open(path_image)
    matrix = img.load()
    (height, width) = img.size
    if file:
        mes = message
        message = ''
        with open(mes, 'r') as f:
            for i in f:
                message += i
    # Скопируем матрицу в массив для подсчета метрик
    main_mas = []
    for i in range(height):
        mas = []
        for j in range(width):
            mas.append(list(matrix[i, j]))
        main_mas.append(mas)
    matrix_orig = numpy.array(main_mas)

    matrix = embedding_information(matrix, message)
    path_image_old = path_image
    if path_image[path_image.rfind('.'):] != 'png':
        path_image = path_image[:path_image.rfind('.') + 1] + 'png'
    save_image(matrix, path_image)
    if path_image_old[-3:] != 'png':
        os.remove(path_image_old)





    # #Расчет метрик PSNR and SSIM
    print('Емкость встраивания - ', round(len(message)*8/(height*width*3*8), 8)*100, '%')
    main_mas = []
    for i in range(height):
        mas = []
        for j in range(width):
            mas.append(list(matrix[i, j]))
        main_mas.append(mas)
    matrix_copy = numpy.array(main_mas)
    print('Метрика PSNR = ', round(skimage.metrics.peak_signal_noise_ratio(matrix_orig, matrix_copy), 2))
    print('Метрика SSIM = ', skimage.metrics.structural_similarity(matrix_orig, matrix_copy, channel_axis = 2))

    img = Image.open(path_image)
    matrix = img.load()
    message_decode = extracting_information(matrix)
    summa = 0
    for i in range(len(message_decode)):
        if (message_decode[i]!=message[i]):
            do = bin(ord(message[i]))[2:]
            posle = bin(ord(message_decode[i]))[2:]
            do = '0'*(8-len(do))+do
            posle = '0'*(8-len(posle)) + posle
            for j in range(8):
                if do[j]!=posle[j]:
                    summa += 1
    print('Метрика BER = ', round(summa/height/width/3*100, 5), '%')
    return True
