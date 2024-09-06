from tkinter import *
from PIL import Image, ImageDraw, ImageFont, ImageTk
from pdf2image import convert_from_path
import tkinter.messagebox as mb
import time
import os
import random

		
# Добавление штампа
def add_stamp(png_file, dpi_index):
	global stamp_coord, stamp_prop_n, prop_doc_size
	stamp_prop_f = list(stamp_prop_n)
	stamp_prop_f[0] = int(round(stamp_prop_n[0] * prop_doc_size[0]) * dpi_index)
	stamp_prop_f[1] = int(round(stamp_prop_n[1] * prop_doc_size[1]) * dpi_index)
	stamp_coord_n = list(stamp_coord)
	stamp_coord_n[0] = int(round(stamp_coord[0]) * dpi_index)
	stamp_coord_n[1] = int(round(stamp_coord[1]) * dpi_index)
	doc = Image.open(png_file)
	stamp = Image.open('gen_stamp.png').resize(stamp_prop_f)

	mask_stamp = Image.open('gen_stamp.png').resize(stamp_prop_f)
	i = 0
	while i < 9:
		i += 1
		doc.paste(stamp, stamp_coord_n, mask_stamp)
	doc.save(png_file, subsampling=0, quality=95)
	doc.show()

	doc.close()
	stamp.close()
# Преобразование pdf-файла в картинку
def pdf_to_picture(pdf_file, dpi_index):
	print(pdf_file[7:-4])
	png_output_folder = str('Result/') + str(pdf_file[7:-4])
	os.mkdir(png_output_folder)
	dpi = 200 * dpi_index
	pic_pdf = convert_from_path(pdf_file, dpi=dpi, fmt='png', output_folder=png_output_folder, output_file=pdf_file[7:-4], paths_only=True, thread_count = 4)

def picture_to_pdf(png_file):
	picture = Image.open(png_file)
	picture_i = picture.convert('L')
	result_file = str(png_file[0:-10]) + str('.pdf')
	picture_i.save(result_file)
	picture.close()
# Склейка картинок в пдф
def folder_to_pdf(main_folder):
	images_folder = os.listdir(main_folder)
	print(images_folder)
	for pdf_name in images_folder:
		try:
			pic_img = []
			im = {}
			im_mass = []
			print(pdf_name)
			folder = str(main_folder) + str('/')+ str(pdf_name)
			print('='*10,folder)
			images = os.listdir(folder)
			print(images)
			for x in images:
				pic = str(folder) + str('/') + str(x)
				pic_img.append(pic)
			print(pic_img)
			i = 0
			for x in pic_img:
				im[i] = Image.open(str(x)).convert('RGB')
				# im[i].show()
				i += 1
			for x in im:
				print(im[x])
				if x == 0:
					None
				else:
					im_mass.append(im[x])
			print(im_mass)
			res_pdf_name = str(folder) + str('.pdf')
			im[0].save(res_pdf_name, save_all=True, append_images=im_mass)
		except:
			None
# Конвейер обработки документов
def pdf_conveyor():
	global doc_num, dpi_index
	dpi_index = VScale.get()
	files = os.listdir('Source')
	for x in files:
		pdf_file = str('Source/') + str(x)
		print(pdf_file)
		pdf_to_picture(pdf_file, dpi_index)
	files = os.listdir('Result')
	print(files)
	for x in files:
		output_folder = str('Result/') + str(x)
		png_files = os.listdir(output_folder)
		print(png_files)
		print(doc_num)
		png_file = str(output_folder) + str('/') + str(png_files[doc_num])
		print(png_file)
		add_stamp(png_file, dpi_index)
		folder_to_pdf('Result')
		for x in png_files:
			png_file = str(output_folder) + str('/') + str(x)
			print('='*10, png_file)
			os.remove(png_file)
		os.rmdir(output_folder)
	Lbl['text'] = 'Done!'
	mb.showinfo('Успешно', "Процесс закончен успешно!")
# Генератор штампа
def stamp_generator(otk_date):
	img = Image.new('RGBA', (2000, 600))
	draw = ImageDraw.Draw(img)
	font_text = ImageFont.truetype("Montserrat-Regular.ttf", 250)
	font_date = ImageFont.truetype('Montserrat-Regular.ttf', 75)
	ds_logo = Image.open('Logо.png')
	img.paste(ds_logo)
	draw.text((600, 25), "OTK", font=font_text, fill='black')
	date = str('Дата ') + str(otk_date)
	draw.text((600, 325), date, font=font_date, fill='black')
	draw.text((600, 425), "Действует с 10.01.2024 по 10.01.2025", font=font_date, fill='black')
	img.save('gen_stamp.png',subsampling=0, quality=95)
	img.show()
	img.close()
# Генератор штампа с сегодняшней датой
def stamp_generator_today():
	otk_date = time.strftime('%d.%m.%Y', time.localtime(time.time()))
	stamp_generator(otk_date)
# Генератор штапма с изменённой датой
def stamp_generator_wrong_date():
	otk_date = str(Txt.get())
	stamp_generator(otk_date)
# Перемещение штампа
def move_stamp(event):
	global stamp_coord, msx, msy, rsx, rsy
	msx = round(event.x * prop_x, 0)
	msy = round(event.y * prop_y, 0)
	rsx = round(event.x, 0)
	rsy = round(event.y, 0)
	canvas.coords(testimg, event.x, event.y)
	stamp_coord = (int(msx), int(msy))
	print('Coord: ', stamp_coord)
# Изменение размера штампа
def resize_stamp(event):
	global img, img1, testimg, stamp_prop, stamp_prop_n, rsx, rsy
	if event.num == 4:
		stamp_prop_n[0] = int(round(stamp_prop_n[0] * 1.1))
		stamp_prop_n[1] = int(round(stamp_prop_n[1] * 1.1))
		img = Image.open('gen_stamp.png').resize(stamp_prop_n)
		img.thumbnail((1200,1200))
		img1 = ImageTk.PhotoImage(img)
		testimg = canvas.create_image(rsx, rsy, anchor= NW, image = img1)
		print('Size: ',img.size)
	else:
		stamp_prop_n[0] = int(round(stamp_prop_n[0] * 0.9))
		stamp_prop_n[1] = int(round(stamp_prop_n[1] * 0.9))
		img = Image.open('gen_stamp.png').resize(stamp_prop_n)
		img.thumbnail((1200,1200))
		img1 = ImageTk.PhotoImage(img)
		testimg = canvas.create_image(rsx, rsy, anchor= NW, image = img1)
		print('Size: ',img.size)
# Возврат штампа в нормальное положение
def normal_stamp():
	global stamp_coord, img, img1, testimg, stamp_prop, stamp_prop_n
	img = Image.open('gen_stamp.png').resize((2000, 600))
	img1 = ImageTk.PhotoImage(img)
	testimg = canvas.create_image(x, y, anchor= NW, image = img1)
	stamp_coord = (int(round(50 * prop_x, 0)), int(round(50 * prop_y, 0)))
	canvas.coords(testimg, 50, 50)
	stamp_prop_n = list(stamp_prop)
# Изменение пропорции
def prop_size():
	doc_size = doc.size
	print(doc_size)
	prop_x = doc_size[0] / 768
	prop_y = doc_size[1] / 768
	prop_doc_size = (prop_x, prop_y)
	print(prop_doc_size)
	stamp_prop_x = 2000 // prop_x
	stamp_prop_y = 600 // prop_y 
	stamp_prop = (stamp_prop_x, stamp_prop_y)
	print(stamp_prop)
# Обновление штампа
def refresh_stamp():
	global img, img1, testimg, stamp_prop_n, msx, msy, rsx, rsy
	img = Image.open('gen_stamp.png').resize(stamp_prop_n)
	img1 = ImageTk.PhotoImage(img)
	testimg = canvas.create_image(rsx, rsy, anchor= NW, image = img1)
	# canvas.coords(testimg, 50, 50)
# Следующая страница
def next_doc():
	global pre_images, doc_num, doc, doc1, testdoc
	try:
		doc_num = doc_num + 1
		doc = Image.open(pre_images[doc_num]).resize((768, 768))
		doc1 = ImageTk.PhotoImage(doc)
		testdoc = canvas.create_image(0, 0, anchor = NW, image = doc1)
		num_str = str('Номер страницы: ') + str(doc_num + 1)
		Lbl['text'] = num_str
		print(doc_num)
		refresh_stamp()
	except:
		doc_num = doc_num - 1
		Lbl['text'] = 'Это последняя страница'
# Предыдущая страница
def prev_doc():
	global pre_images, doc_num, doc, doc1, testdoc
	if doc_num > 0:
		try:
			doc_num = doc_num - 1
			doc = Image.open(pre_images[doc_num]).resize((768, 768))
			doc1 = ImageTk.PhotoImage(doc)
			testdoc = canvas.create_image(0, 0, anchor = NW, image = doc1)
			num_str = str('Номер страницы: ') + str(doc_num + 1)
			Lbl['text'] = num_str
			print(doc_num)
			refresh_stamp()
		except:
			doc_num = doc_num + 1
			Lbl['text'] = 'Это первая страница'
	else:
		Lbl['text'] = 'Это первая страница'
# Предпросмотр
def preview():
	pdf_files = os.listdir('Source')
	pdf = str('Source/') + str(pdf_files[0])
	print(pdf)
	png_output_folder = str('Preview')
	pic_pdf = convert_from_path(pdf, fmt='png', output_folder=png_output_folder, output_file=pdf[7:-4], paths_only=True, thread_count = 4)
	pre_images = os.listdir('Preview')
	images = []
	for x in pre_images:
		x = str('Preview/') + str(x)
		images.append(x)
	return(images)

def preview_doc():
	global stamp_coord, stamp_prop_n, prop_doc_size, doc_num
	stamp_prop_f = list(stamp_prop_n)
	stamp_prop_f[0] = int(round(stamp_prop_n[0] * prop_doc_size[0]))
	stamp_prop_f[1] = int(round(stamp_prop_n[1] * prop_doc_size[1]))
	png_files = os.listdir('Preview')
	png_file = str('Preview/') + str(png_files[doc_num])
	doc = Image.open(png_file)
	stamp = Image.open('gen_stamp.png').resize(stamp_prop_f)

	mask_stamp = Image.open('gen_stamp.png').resize(stamp_prop_f)
	i = 0
	while i < 9:
		i += 1
		doc.paste(stamp, stamp_coord, mask_stamp)
	doc.show()
	doc.close()
	stamp.close()


x = 50
y = 50
SignResize = 1
doc_num = 0
msx = 0
msy = 0
rsx = 50
rsy = 50
stamp_coord = (x,y)


pre_images = preview()

window = Tk()
window.title('Same')
window.geometry('1068x768')

canvas = Canvas(window, bg = 'white', height = 768, width = 768)
canvas.pack(side = 'left', fill = BOTH)

MenuFrame = Frame(window, width = 120, bg = 'gray22')
MenuFrame.pack(side = 'right', fill = Y)

# img = PhotoImage(file = 'gen_stamp.png')
prop_doc = Image.open(pre_images[doc_num])

doc_size = prop_doc.size
print(doc_size)
prop_x = doc_size[0] / 768
prop_y = doc_size[1] / 768
prop_doc_size = (prop_x, prop_y)
print(prop_doc_size)
stamp_prop_x = 2000 // prop_x
stamp_prop_y = 600 // prop_y 
stamp_prop = (int(stamp_prop_x), int(stamp_prop_y))
print(stamp_prop)
stamp_prop_n = list(stamp_prop)

doc = Image.open(pre_images[doc_num]).resize((768, 768))
doc1 = ImageTk.PhotoImage(doc)
testdoc = canvas.create_image(0, 0, anchor = NW, image = doc1)

img = Image.open('gen_stamp.png').resize(stamp_prop)
img1 = ImageTk.PhotoImage(img)
testimg = canvas.create_image(x, y, anchor= NW, image = img1)

dpi_index = IntVar(window)
dpi_index.set(1)

canvas.bind("<B1-Motion>", move_stamp)
canvas.bind("<Button-4>", resize_stamp)
canvas.bind("<Button-5>", resize_stamp)
canvas.bind("<MouseWheel>", resize_stamp)



Btn = Button(MenuFrame, text = 'Начальное положение штампа', command = normal_stamp)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Предпросмотр', command = preview_doc)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Обновить штамп', command = refresh_stamp)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Генератор сегодняшнего штампа', command = stamp_generator_today)
Btn.pack(fill = X, padx = 5, pady = 5)
Txt = Entry(MenuFrame)
Txt.pack(fill = X, padx = 5, pady = 5)
Txt.insert(0, "DD.MM.YYYY")
Btn = Button(MenuFrame, text = 'Генератор штампа с изменённой датой', command = stamp_generator_wrong_date)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Следующая страница', command = next_doc)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Предыдущая страница', command = prev_doc)
Btn.pack(fill = X, padx = 5, pady = 5)
Btn = Button(MenuFrame, text = 'Начать проставление печатей', command = pdf_conveyor)
Btn.pack(fill = X, padx = 5, pady = 5)


Lbl = Label(MenuFrame, background = 'gray22', foreground = 'white', text = 'Качество итогового документа')
Lbl.pack(fill = X, padx = 5, pady = 5)
VScale = Scale(MenuFrame, orient = HORIZONTAL, length = 120, from_ = 1, to = 10, variable = dpi_index)
VScale.pack(fill = X, padx = 5, pady = 5)


Lbl = Label(MenuFrame, text = 'Статус')
Lbl.pack(fill = X, padx = 5, pady = 5)

window.mainloop()