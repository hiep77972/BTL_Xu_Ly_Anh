#Import cac thu vien càn thiet
from tkinter import *
from tkinter import filedialog
import gtts
from tkinter.ttk import *
from numpy.core.fromnumeric import var
import numpy as np
from tkinter import messagebox
from tkinter.filedialog import askopenfilename
import tkinter
import cv2
import PIL.Image, PIL.ImageTk
import threading
from PIL import ImageFont, ImageDraw, Image
from datetime import date, datetime
import os
import text_detection as detection
import image_processing as processing

#Khai bao font chu dung de render
fontpath = './Font/fontface.ttf'
font = ImageFont.truetype(fontpath, 32)
#Khai bao cac thu muc su dung
save_data_path = './SaveData'
temp_data_path = './TempData'

#Lay kich thuoc camera
video = cv2.VideoCapture(0)
camera_w = int(video.get(cv2.CAP_PROP_FRAME_WIDTH))
camera_h = int(video.get(cv2.CAP_PROP_FRAME_HEIGHT))
dim = (camera_w, camera_h)



window = Tk()
#Khai bao chi tiet ung dung
window.geometry("1600x740")
window.title("Bài tập lớn - Xử lí ảnh - Sinh viên: Lương Văn Đạt - CNT59DH - 77604")
window.config(background = '#6bcbe1')
icon = PhotoImage(file = './Img/Icon/icon_app.png')
################################KHAI BAO CAC HAM XU LI#######################################
#Khai bao ham update du lieu cho 2 khung du lieu
def SaveData(img_inp, img_res, text_res):
    global is_save
    is_save = False
    now = datetime.now()
    dt_string = now.strftime("%d_%m_%Y, %H-%M-%S")
    path = os.path.join('./SaveData', dt_string)
    os.mkdir(path)
    cv2.imwrite(os.path.join(path, 'img_input.png'), img_inp)
    with open(os.path.join(path, 'text_result.txt'), 'w', encoding='utf8') as file:
        file.write(text_res)
    cv2.imwrite(os.path.join(path, 'img_output.png'), img_res)

#Khai bao hàm update canvas input
photo_inp = None
def Update_canvas_inp():
    global canvas_inp, photo_inp, file_name
    if(file_name == None):
        ret, frame = video.read()
        frame = cv2.resize(frame, dim, fx = 1, fy = 1)
        frame = cv2.cvtColor(frame, cv2.COLOR_BGR2RGB)
        photo_inp = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame))
        canvas_inp.create_image(0, 0, image = photo_inp, anchor = tkinter.NW)
        window.after(10, Update_canvas_inp)
    else:
        img = cv2.imread(file_name)
        img = cv2.resize(img, dim, fx = 1, fy = 1)
        img = cv2.cvtColor(img, cv2.COLOR_BGR2RGB)
        photo_inp = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img))
        canvas_inp.create_image(0, 0, image = photo_inp, anchor = tkinter.NW)


#Khai bao hàm update canvas res
photo_res = None
def Update_canvas_res():
    global canvas_res, photo_res, is_video_detection, is_image_detection, is_detection_button_click, is_get_text, is_save, file_name, rdo_choice, cb_alp, cb_num, cb_withtext, text_result
    if(is_video_detection):
        ret, frame = video.read()
        frame_inp = cv2.resize(frame, dim, fx = 1, fy = 1)
        frame_res = cv2.cvtColor(frame_inp, cv2.COLOR_BGR2RGB)
        frame_res = cv2.resize(frame_inp, (1000, 1000), fx = 1, fy = 1)
        frame_res = processing.apply_processing(frame_inp, rdo_choice)
        if(is_get_text):
            is_get_text = False
            DeleteText()
            text_result.insert(INSERT, detection.img_to_text(frame_res))
        frame_res = detection.img_to_box(frame_res, cb_alp.get(), cb_num.get(), cb_withtext.get())
        frame_res = cv2.resize(frame_inp, dim, fx = 1, fy = 1)
        photo_res = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(frame_res))
        canvas_res.create_image(0, 0, image = photo_res, anchor = tkinter.NW)
        if(is_save):
            cv2.imwrite('.//TempData//temp.png',frame_inp)
            file_name = './/TempData/temp.png'
            is_video_detection = False
            is_image_detection = True
            messagebox.showinfo("Thông báo!", "Lưu dữ liệu thành công")
            is_save = False
        window.after(10, Update_canvas_res)
    if(is_image_detection and is_detection_button_click):
        img_inp = cv2.imread(file_name)
        img_inp = cv2.resize(img_inp, dim, fx = 1, fy = 1)
        img_res = cv2.cvtColor(img_inp, cv2.COLOR_BGR2RGB)
        img_res = cv2.resize(img_inp, (1000, 1000), fx = 1, fy = 1)
        img_res = processing.apply_processing(img_res, rdo_choice)
        if(is_get_text):
            is_get_text = False
            DeleteText()
            text_result.insert(INSERT, detection.img_to_text(img_res))
        img_res = detection.img_to_box(img_res, cb_alp.get(), cb_num.get(), cb_withtext.get())
        img_res = cv2.resize(img_res, dim, fx = 1, fy = 1)
        photo_res = PIL.ImageTk.PhotoImage(image = PIL.Image.fromarray(img_res))
        canvas_res.create_image(0, 0, image = photo_res, anchor = tkinter.NW)
        if(is_save):
            SaveData(img_inp, img_res, text_result.get(1.0, END))
            messagebox.showinfo("Thông báo!", "Lưu dữ liệu thành công")
            is_save = False

###################################### KHAI BAO CAC DOI TUONG ##################################################
#Khai bao khung du lieu lam viec
canvas_inp = Canvas(window, width = camera_w, height = camera_h, bg = '#303036')
canvas_inp.place(x = 20, y = 40)
canvas_res = Canvas(window, width = camera_w, height = camera_h, bg = '#303036')
canvas_res.place(x = 700, y = 40)
#Khai bao khung lua chon hien thi
tkinter.Label(window, width = 28, height = 30, fg = '#00FF00',  bd = 10, relief = RAISED).place(x = 1350, y = 50)
#Khai bao khung chua cac button
tkinter.Label(window, width = 90, height = 10, fg = '#00FF00',  bd = 10, relief = RAISED).place(x = 20, y = 550)
#Khai bao cac lable hien thi text
tkinter.Label(window, text = "Đầu vào", fg = 'red', font = ("Arial", 30)).place(x = 20, y = 0)
tkinter.Label(window, text = "Đầu ra", fg = 'red', font = ("Arial", 30)).place(x = 700, y = 0)
tkinter.Label(window, text = "Lựa chọn", fg = 'red', font = ("Arial", 30)).place(x = 1350, y = 0)
tkinter.Label(window, text = "LỰA CHỌN HIỂN THỊ", fg = 'black', font = ("Arial", 10)).place(x = 1400, y = 70)
tkinter.Label(window, text = "ÁP DỤNG XỬ LÍ ẢNH", fg = 'black', font = ("Arial", 10)).place(x = 1400, y = 170)
#Khai bao khung chua tra ve
text_result = tkinter.Text(window, width = 79, height = 10)
text_result.place(x = 700, y = 550)
#Khai bao anh
logo_vmu = PIL.ImageTk.PhotoImage(Image.open(r".//Img//Logo/vmu.png").resize((180, 180), Image.ANTIALIAS))
lable_logo = tkinter.Label(window, width = 200, height = 200, bg = '#6bcbe1', image = logo_vmu)
lable_logo.place(x = 1360, y = 540)
#Khai bao button mo camera
is_video_detection = False
camera_is_open = False
def button_opencamera_click():
    global camera_is_open, is_video_detection, is_image_detection, file_name
    camera_is_open = True
    is_video_detection = True
    is_image_detection = False
    file_name = None
    Update_canvas_inp()
    return
button = Button(window, text = 'Mở camera', command = button_opencamera_click).place(x = 40, y = 580)
#Khai bao buton nhan dang
is_detection_button_click = False
def button_detection_click():
    global camera_is_open, is_detection_button_click
    if(camera_is_open):
        is_detection_button_click = True
        Update_canvas_res()
    else:
        messagebox.showinfo("Cảnh báo!", "Camera chưa được mở")
    return
button = Button(window, text = 'Bắt đầu nhận dạng', command = button_detection_click).place(x = 150, y = 580)
#Khai bao button chon anh
is_image_detection = False
file_name = None
def OpenFile():
    global file_name, is_video_detection, is_image_detection, is_detection_button_click, camera_is_open
    file_name = askopenfilename(initialdir="C:/Users/luong/PycharmProjects/BTL_XLA_UI/Img/Icon/",
                           filetypes =(("All Files","*.*"), ("PNG File", "*.png"), ("JPG File", "*.jpg")),
                           title = "Choose a file."
                           )
    if(file_name != ""):
        camera_is_open = True
        is_detection_button_click = False
        is_video_detection = False
        is_image_detection = True
        Update_canvas_inp()
button_take_photo = Button(window, text = 'Chọn hình ảnh', command = OpenFile).place(x = 40, y = 620)
#Khai bao button GetText
is_get_text = False
def GetText():
    global is_get_text
    is_get_text = True
    Update_canvas_res()
button_get_text = Button(window, text = 'Lấy văn bản', command = GetText).place(x = 40, y = 660) 
#Khai bao button Xoa
def DeleteText():
    global text_result
    text_result.delete(1.0, END)
button_delete_text = Button(window, text = 'Xóa', command = DeleteText).place(x = 150, y = 660)
#Khai bao button Save
is_save = False
def SaveText():
    global is_save
    is_save = True
    Update_canvas_res()
button_save_text = Button(window, text = 'Lưu lại kết quả', command = SaveText).place(x = 150, y = 620)
#Khai bao button mo thu muc
def OpenFolder():
    path = 'C://Users//luong//PycharmProjects//BTL_XLA_UI//SaveData'
    path = os.path.realpath(path)
    os.startfile(path)
    return
button_save_text = Button(window, text = 'Mở thư mục lưu', command = OpenFolder).place(x = 300, y = 620)
#Khai bao checkbox chon lua
cb_alp = IntVar()
cb_num = IntVar()
cb_withtext = IntVar()
def cb_click():
    global is_image_detection
    if(is_image_detection):
        Update_canvas_res()
Checkbutton(window, text = "Only alphabet",variable = cb_alp, command = lambda :cb_click()).place(x = 1365, y = 100)
Checkbutton(window, text = 'Only numeric', variable = cb_num, command = lambda :cb_click()).place(x = 1365, y = 120)
Checkbutton(window, text = 'Hiển thị văn bản', variable = cb_withtext, command = lambda :cb_click()).place(x = 1365, y = 140)
#Khai bao ra radiobutton chon lua
rdo_choice = 0
def rdo_click(value):
    global rdo_choice, is_image_detection
    rdo_choice = value
    if(is_image_detection):
        Update_canvas_res()

rdo = IntVar()
Radiobutton(window, text = "Original", variable = rdo, value = 0, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 200)
Radiobutton(window, text = "Gray Scale", variable = rdo, value = 1, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 220)
Radiobutton(window, text = "Remove Noise", variable = rdo, value = 2, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 240)
Radiobutton(window, text = "Thresholding", variable = rdo, value = 3, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 260)
Radiobutton(window, text = "Dilate", variable = rdo, value = 4, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 280)
Radiobutton(window, text = "Erode", variable = rdo, value = 5, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 300)
Radiobutton(window, text = "Opening", variable = rdo, value = 6, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 320)
Radiobutton(window, text = "Canny", variable = rdo, value = 7, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 340)
Radiobutton(window, text = "Deskew", variable = rdo, value = 8, command = lambda :rdo_click(rdo.get())).place(x = 1365, y = 360)
#Khai bao button save
window.mainloop()