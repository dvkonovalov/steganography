import tkinter as tk
from tkinter import filedialog
from tkinter import ttk
import tkinter.messagebox as mb
import main


global path_image, file_path, r_var

def decod_inf():
    flag = main.find_secret(path_image)
    if flag:
        mb.showinfo('Успех', 'Секретная информация успешно декодировна и записана в файл secret.txt')
    else:
        mb.showinfo('Неудача', 'К сожалению произошла ошибка. Попробуйте еще раз')

def insert_inf():
    global r_var, path_image, file_path
    print()
    if r_var.get()==1:
        flag = main.insert_secret(path_image, 'data.txt', True) #стоит костыть
    else:
        mes = pole_secret.get("1.0","end")
        flag = main.insert_secret(path_image, mes)
    if flag:
        mb.showinfo('Успех', 'Секретная информация успешно вставлена в изображение')
    else:
        mb.showinfo('Неудача', 'К сожалению произошла ошибка. Попробуйте еще раз')


def choice_image_decod():
    global path_image
    path_image = filedialog.askopenfilename()
    stroka_image2.config(text='Выбрано изображение - ' + path_image[path_image.rfind('/') + 1:])

def choice_image_insert():
    global path_image
    path_image = filedialog.askopenfilename()
    stroka_image.config(text='Выбрано изображение - ' + path_image[path_image.rfind('/') + 1:])

def choice_file_insert():
    global file_path
    file_path = filedialog.askopenfilename()
    stroka_file.config(text='Выбран файл - ' + file_path[file_path.rfind('/') + 1:])

window = tk.Tk()
width = 960
height = 640
window.title("LSB-Steganography")
window.config(width=width, height=height)
tk.Label(window, text='Вставка секретной информации', font='Times 20').place(x=300, y=10)
bt1 = tk.Button(window, text='выбрать изображение', font='Times 14', command=choice_image_insert, bg = "#90EE90")
bt1.place(x=10, y=50, width=190, height=35)
stroka_image = tk.Label(window, text='Изображение не выбрано', font='Times 14')
stroka_image.place(x=210, y=55)

stroka_secret = tk.Label(window, text='Введите секретный текст:', font='Times 14')
stroka_secret.place(x=10, y=95)
pole_secret = tk.Text(font='Times 14', width = 105, height = 7, wrap = 'word' )
ys = ttk.Scrollbar(orient="vertical", command=pole_secret.yview)
pole_secret["yscrollcommand"] = ys.set
pole_secret.place(x=5, y=120)

r_var = tk.BooleanVar()
r_var.set(0)
tk.Label(text = 'Откуда взять информацию:', font = 'Times 14').place(x = 10, y = 280)
r1 = tk.Radiobutton(text='Информация из текста', variable=r_var, value=0, font = 'Times 14',)
r2 = tk.Radiobutton(text='Информация из файла', font = 'Times 14', variable=r_var, value=1)
r1.place(x=10, y = 305)
r2.place(x=10, y = 330)

bt2 = tk.Button(window, text='выбрать файл', font='Times 14', command=choice_file_insert, bg = "#90EE90")
bt2.place(x=320, y=280, width=190, height=35)
stroka_file = tk.Label(text = 'Файл не выбран', font = 'Times 14')
stroka_file.place(x = 530, y = 285)

bt3 = tk.Button(window, text = 'Вставить', font = 'Times 16', command = insert_inf, bg = "#00a86b")
bt3.place(x = 800, y = 320)

tk.Label(window, text='Декодировать информацию из изображения', font='Times 20').place(x=245, y=385)
stroka_image2 = tk.Label(window, text='Изображение не выбрано', font='Times 14')
stroka_image2.place(x=220, y=442)
bt4 = tk.Button(window, text='выбрать изображение', font='Times 14', command=choice_image_decod, bg = "#90EE90")
bt4.place(x=10, y=440, width=190, height=35)
bt5 = tk.Button(window, text = 'Декодировать', font = 'Times 16', command = decod_inf, bg = '#90EE90')
bt5.place(x=800, y = 460)

canvas1 = tk.Canvas(bg='white', width=width, height=10)
canvas1.place(x=0, y=375)
canvas1.create_line(0, 5, width, 5, activefill="red", fill="black", width=10)


window.mainloop()
