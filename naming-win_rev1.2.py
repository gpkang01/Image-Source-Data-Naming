# Please check line #697

from __future__ import print_function
from tkinter import *
from tkinter import filedialog
import tkinter.ttk as ttk
import os
import tkinter.messagebox as msgbox
from PIL import Image, ImageTk
from PIL.ExifTags import TAGS
import keyboard
from googleapiclient.discovery import build
from httplib2 import Http
from oauth2client import file, client, tools
import shutil
import time
import os.path
from google_auth_oauthlib.flow import InstalledAppFlow
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from datetime import datetime

root = Tk() # root 메인 창
root.title("네이밍 및 구글 드라이브 자동 업로드")
root.geometry('750x522+350+100') 
root.resizable(False, False) 

current_path = os.getcwd()

def add_file():
    global files, order
    order = 0
    files = filedialog.askopenfilenames(title = '이미지 파일을 선택하세요.', \
        filetypes = (('JPG 파일', '*.jpg'), ('모든 파일', '*.*')), \
        initialdir = current_path)

    list_file.delete(0)
    list_file.insert(END, files[0])

    list_file.selection_set(0)
    preview_image(list_file.get(0))

    progress1(0, len(files))
    state = 'Saved : {} / {}'.format(0, len(files))
    prog_rate1.configure(text = state)

    reset()

def reset():
    global direction, occlusion
    direction = 0
    direc_id1.config(bg = 'SystemButtonFace')
    direc_id2.config(bg = 'SystemButtonFace')
    direc_id3.config(bg = 'SystemButtonFace')
    direc_id4.config(bg = 'SystemButtonFace')
    occlusion = 0
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'SystemButtonFace')

def preview_image(path):
    img_width = 400
    img_height = 400

    image = Image.open(path)
    width, height = image.size[0], image.size[1]
    
    if width >= height:
        pre_width, pre_height = img_width, int(height * img_width / width)
    else:
        pre_width, pre_height = int(width * img_height / height), img_height

    resized_img = image.resize((pre_width, pre_height))
   
    photo = ImageTk.PhotoImage(resized_img)
    photo_frame.configure(image = photo)
    photo_frame.image_names = photo

def empty_image():
    photo = PhotoImage()
    photo_frame.configure(image = photo)
    photo_frame.image_names = photo

def next_img():
    global pre_order, change_name
    previous_btn.config(state = 'normal')

    if pre_order < len(pre_img_order) - 1:
        next_sub()
        path1 = pre_img_order[pre_order + 1][0]
        list_file.delete(0)
        list_file.insert(END, path1)
        list_file.selection_set(0)
        preview_image(path1)
        save_name_is.config(state = 'normal')
        save_name_is.delete(0, END)
        save_name_is.insert(0, pre_img_order[pre_order + 1][1])
        save_name_is.config(state = 'disable')
        pre_order += 1
    else:
        if len(pre_img_order) == len(files):
            next_btn.config(state = 'disabled')
        elif len(pre_img_order) < len(files):
            next_sub()
            path2 = files[pre_order + 1]
            list_file.delete(0)
            list_file.insert(END, path2)
            list_file.selection_set(0)
            preview_image(path2)
            save_name_is.config(state = 'normal')
            save_name_is.delete(0, END)
            save_name_is.config(state = 'disable')
            next_btn.config(state = 'disabled')
            pre_order += 1
            change_name = 0

change_name = 0
def pre_img():
    global pre_order, change_name
    next_btn.config(state = 'normal')
    change_name = 1

    if pre_order > 1:
        pre_sub()
        path1 = pre_img_order[pre_order - 1][0]
        list_file.delete(0)
        list_file.insert(END, path1)
        list_file.selection_set(0)
        preview_image(path1)
        save_name_is.config(state = 'normal')
        save_name_is.delete(0, END)
        save_name_is.insert(0, pre_img_order[pre_order - 1][1])
        save_name_is.config(state = 'disable')
        pre_order -= 1
    else:
        pre_sub()
        path1 = pre_img_order[pre_order - 1][0]
        list_file.delete(0)
        list_file.insert(END, path1)
        list_file.selection_set(0)
        preview_image(path1)
        save_name_is.config(state = 'normal')
        save_name_is.delete(0, END)
        save_name_is.insert(0, pre_img_order[pre_order - 1][1])
        save_name_is.config(state = 'disable')
        previous_btn.config(state = 'disabled')
        pre_order -= 1

def pre_sub():
    order_name = pre_img_order[pre_order - 1][1].strip().split('\\')[2]
    order_class = order_name.strip().split('_')[0]
    order_insta = order_name.strip().split('_')[2]
    order_direc = order_name.strip().split('_')[3]
    order_occlu = order_name.strip().split('_')[4]
    class_key_lists = list(class_dict.keys())
    class_value_lists = list(class_dict.values())

    value_index = class_value_lists.index(order_class)
    class_key = class_key_lists[value_index]

    class_combobox.set(class_key)
    ins_combobox.set(order_insta)

    if order_direc == '01':
        direc1()
    elif order_direc =='02':
        direc2()
    elif order_direc == '03':
        direc3()
    elif order_direc == '04':
        direc4()

    if order_occlu == 'None.jpg':
        occ1()
    elif order_occlu =='SemiTransparent.jpg':
        occ2()
    elif order_occlu == 'WireDense.jpg':
        occ3()
    elif order_occlu == 'WireMedium.jpg':
        occ4()
    elif order_occlu == 'WireLoose.jpg':
        occ5()

def next_sub():
    order_name = pre_img_order[pre_order + 1][1].strip().split('\\')[2]
    order_class = order_name.strip().split('_')[0]
    order_insta = order_name.strip().split('_')[2]
    order_direc = order_name.strip().split('_')[3]
    order_occlu = order_name.strip().split('_')[4]
    class_key_lists = list(class_dict.keys())
    class_value_lists = list(class_dict.values())

    value_index = class_value_lists.index(order_class)
    class_key = class_key_lists[value_index]
    class_combobox.set(class_key)
    ins_combobox.set(order_insta)

    if order_direc == '01':
        direc1()
    elif order_direc =='02':
        direc2()
    elif order_direc == '03':
        direc3()
    elif order_direc == '04':
        direc4()

    if order_occlu == 'None.jpg':
        occ1()
    elif order_occlu =='SemiTransparent.jpg':
        occ2()
    elif order_occlu == 'WireDense.jpg':
        occ3()
    elif order_occlu == 'WireMedium.jpg':
        occ4()
    elif order_occlu == 'WireLoose.jpg':
        occ5()

def next_order():
    global files, order, dirction, occlusion
    order += 1
    if order < len(files):
        list_file.delete(0)
        list_file.insert(END, files[order])
        list_file.selection_set(0)
        preview_image(list_file.get(0))
        if occlusion == 1:
            occ2()
        elif occlusion ==2:
            occ3()
        elif occlusion ==3:
            occ4()
        elif occlusion ==4:
            occ5()
        else:
            occ1()
            if direction == 1:
                direc2()
            elif direction == 2:
                direc3()
            elif direction == 3:
                direc4()
            else:
                direc1()
                msgbox.showinfo('알림', 'Class 명이나 객체 ID를 변경했는지 확인하세요.')
    else:
        list_file.delete(0)
        empty_image()
        save_finish_notice()

def progress1(current_qy, total_qy):
    i = (current_qy / total_qy) * 100

    pro_var1.set(i)
    progressbar1.update()

    state = 'Saved : {} / {}'.format(current_qy, total_qy)
    prog_rate1.configure(text = state)

response = ''
def worker_id_ok():
    global response
    if worker_id_right.get() == '':
        msgbox.showinfo('알림', 'Worker ID가 입력되지 않았습니다.')
    else:
        response = msgbox.askokcancel('확인 / 취소', 'Worker ID가 {}입니다. 계속 진행하시겠습니까?\n확인을 누르면 \
Worker ID를 변경할 수 없고 변경을 눌러야 변경 가능합니다.'.format(worker_id_right.get()))
        if response == True:
            with open('create/cur_workerid.txt', 'w') as tmp_file:
                tmp_file.write(worker_id_right.get())
            worker_id_right.config(state = 'disabled')
            worker_id_btn.config(state = 'disabled')
            view_save_name()
        else:
            worker_id_right.delete(0, END)

def worker_id_change():
    worker_id_right.config(state = 'normal')
    worker_id_btn.config(state = 'normal')
    worker_id_right.delete(0, END)

direction = 0
def direc1():
    global direction
    direction = 1
    direc_id1.config(bg = 'yellow')
    direc_id2.config(bg = 'SystemButtonFace')
    direc_id3.config(bg = 'SystemButtonFace')
    direc_id4.config(bg = 'SystemButtonFace')
    view_save_name()

def direc2():
    global direction
    direction = 2
    direc_id1.config(bg = 'SystemButtonFace')
    direc_id2.config(bg = 'yellow')
    direc_id3.config(bg = 'SystemButtonFace')
    direc_id4.config(bg = 'SystemButtonFace')
    view_save_name()

def direc3():
    global direction
    direction = 3
    direc_id1.config(bg = 'SystemButtonFace')
    direc_id2.config(bg = 'SystemButtonFace')
    direc_id3.config(bg = 'yellow')
    direc_id4.config(bg = 'SystemButtonFace')
    view_save_name()

def direc4():
    global direction
    direction = 4
    direc_id1.config(bg = 'SystemButtonFace')
    direc_id2.config(bg = 'SystemButtonFace')
    direc_id3.config(bg = 'SystemButtonFace')
    direc_id4.config(bg = 'yellow')
    view_save_name()

occlusion = 0
def occ1():
    global occlusion
    occlusion = 1
    occ_name1.config(bg = 'yellow')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'SystemButtonFace')
    view_save_name()

def occ2():
    global occlusion
    occlusion = 2
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'yellow')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'SystemButtonFace')
    view_save_name()

def occ3():
    global occlusion
    occlusion = 3
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'yellow')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'SystemButtonFace')
    view_save_name()

def occ4():
    global occlusion
    occlusion = 4
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'yellow')
    occ_name5.config(bg = 'SystemButtonFace')
    view_save_name()

def occ5():
    global occlusion
    occlusion = 5
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'yellow')
    view_save_name()

save_item = {}
save_check = True
def info_check():
    global check_result, order, save_item, save_check
    check_result = ''
    if worker_id_right.get() == '':
        check_result = msgbox.showinfo('알림', 'Worker ID가 입력되지 않았습니다.')
    elif response != True:
        check_result = msgbox.showinfo('알림', 'Worker ID가 Confirm 되지 않았습니다.')
    elif mon_combobox.get() == '':
        check_result = msgbox.showinfo('알림', '촬영일자가 월이 선택되지 않았습니다.')
    elif day_combobox.get() == '':
        check_result = msgbox.showinfo('알림', '촬영일자가 일이 선택되지 않았습니다.')
    elif class_combobox.get() == '':
        check_result = msgbox.showinfo('알림', '클래스명이 선택되지 않았습니다.')
    elif ins_combobox.get() == '':
        check_result = msgbox.showinfo('알림', '객체 ID가 선택되지 않았습니다.')
    elif direction == 0:
        check_result = msgbox.showinfo('알림', '촬영 뷰 방향 ID가 선택되지 않았습니다.')
    elif occlusion == 0:
        check_result = msgbox.showinfo('알림', '가림막명이 선택되지 않았습니다.')
    save_item[order] = [class_dict[class_combobox.get()], ins_combobox.get(), direction, occlusion]
    if order != 0:
        if save_item[order - 1][0] == save_item[order][0] and save_item[order - 1][1] == save_item[order][1] and \
            save_item[order - 1][2] == save_item[order][2] and save_item[order - 1][3] == save_item[order][3] :
            save_check = msgbox.askokcancel('확인 / 취소', '이전 작업과 저장 정보가 같습니다. 계속 진행하시겠습니까?')
        else:
            save_check = True

def view_toggle():
    global direction
    if direction == 0:
        direction = 1
        direc_id1.config(bg = 'yellow')
        direc_id2.config(bg = 'SystemButtonFace')
        direc_id3.config(bg = 'SystemButtonFace')
        direc_id4.config(bg = 'SystemButtonFace')
        view_save_name()
    elif direction == 1:
        direction = 2
        direc_id1.config(bg = 'SystemButtonFace')
        direc_id2.config(bg = 'yellow')
        direc_id3.config(bg = 'SystemButtonFace')
        direc_id4.config(bg = 'SystemButtonFace')
        view_save_name()
    elif direction == 2:
        direction = 3
        direc_id1.config(bg = 'SystemButtonFace')
        direc_id2.config(bg = 'SystemButtonFace')
        direc_id3.config(bg = 'yellow')
        direc_id4.config(bg = 'SystemButtonFace')
        view_save_name()
    elif direction == 3:
        direction = 4
        direc_id1.config(bg = 'SystemButtonFace')
        direc_id2.config(bg = 'SystemButtonFace')
        direc_id3.config(bg = 'SystemButtonFace')
        direc_id4.config(bg = 'yellow')
        view_save_name()
    elif direction == 4:
        direction = 1
        direc_id1.config(bg = 'yellow')
        direc_id2.config(bg = 'SystemButtonFace')
        direc_id3.config(bg = 'SystemButtonFace')
        direc_id4.config(bg = 'SystemButtonFace')
        view_save_name()
    
def occ_toggle():
    global occlusion
    if occlusion == 0:
        occlusion = 1
        occ_name1.config(bg = 'yellow')
        occ_name2.config(bg = 'SystemButtonFace')
        occ_name3.config(bg = 'SystemButtonFace')
        occ_name4.config(bg = 'SystemButtonFace')
        occ_name5.config(bg = 'SystemButtonFace')
        view_save_name()
    elif occlusion == 1:
        occlusion = 2
        occ_name1.config(bg = 'SystemButtonFace')
        occ_name2.config(bg = 'yellow')
        occ_name3.config(bg = 'SystemButtonFace')
        occ_name4.config(bg = 'SystemButtonFace')
        occ_name5.config(bg = 'SystemButtonFace')
        view_save_name()
    elif occlusion == 2:
        occlusion = 3
        occ_name1.config(bg = 'SystemButtonFace')
        occ_name2.config(bg = 'SystemButtonFace')
        occ_name3.config(bg = 'yellow')
        occ_name4.config(bg = 'SystemButtonFace')
        occ_name5.config(bg = 'SystemButtonFace')
        view_save_name()
    elif occlusion == 3:
        occlusion = 4
        occ_name1.config(bg = 'SystemButtonFace')
        occ_name2.config(bg = 'SystemButtonFace')
        occ_name3.config(bg = 'SystemButtonFace')
        occ_name4.config(bg = 'yellow')
        occ_name5.config(bg = 'SystemButtonFace')
        view_save_name()
    elif occlusion == 4:
        occlusion = 5
        occ_name1.config(bg = 'SystemButtonFace')
        occ_name2.config(bg = 'SystemButtonFace')
        occ_name3.config(bg = 'SystemButtonFace')
        occ_name4.config(bg = 'SystemButtonFace')
        occ_name5.config(bg = 'yellow')
        view_save_name()
    elif occlusion == 5:
        occlusion = 1
        occ_name1.config(bg = 'yellow')
        occ_name2.config(bg = 'SystemButtonFace')
        occ_name3.config(bg = 'SystemButtonFace')
        occ_name4.config(bg = 'SystemButtonFace')
        occ_name5.config(bg = 'SystemButtonFace')
        view_save_name()

def view_save_name():
    direction_list = ['', '01', '02', '03', '04' ]
    occlusion_list = ['', 'None', 'SemiTransparent', 'WireDense', 'WireMedium', 'WireLoose']
    save_name = '{}_{}_{}_{}_{}.jpg'.format(class_dict[class_combobox.get()], worker_id_right.get(), ins_combobox.get(), \
                direction_list[direction], occlusion_list[occlusion])
    save_name_is.config(state = 'normal')
    save_name_is.delete(0, END)
    save_name_is.insert(0, save_name)
    save_name_is.config(state = 'readonly')

def save_new():
    global pre_img_order, pre_order, change_name

    if list_file.size() > 0:
        info_check()
        if check_result == '' and save_check == True:
            view_save_name()
            total_qy = len(files)
            current_qy = order + 1
            month = str('{0:02d}'.format(int(mon_combobox.get())))
            day = str('{0:02d}'.format(int(day_combobox.get())))
            w_date = '{}{}'.format(month, day)
            now = datetime.now()
            y_date = '{}{}{}'.format(now.year, month, day)
            w_id = worker_id_right.get()
            if os.path.isdir('tmp'):
                if os.path.isdir('tmp\{}'.format(w_id)):
                    if os.path.isdir('tmp\{}\{}_renamed'.format(w_id, w_date)):
                        if os.path.isfile('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))\
                             and change_name == 0:
                            msgbox.showinfo('알림', '같은 파일명이 존재합니다. 확인해 주세요.')
                        elif os.path.isfile('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))\
                             and change_name == 1:
                            response = msgbox.askokcancel('확인 / 취소', '파일명을 변경합니다. \
계속 진행하시겠습니까?')
                            if response:
                                read_dict_file2('create/temp.log')
                                for i in range(len(read_dict)):
                                    if read_dict[i][0] == list_file.get(0):
                                        change_line = read_dict[i][0]
                                os.remove('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                change_save_log(change_line, '{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                change_temp_log(change_line, '{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                        elif not os.path.isfile('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))\
                             and change_name == 1:
                            response = msgbox.askokcancel('확인 / 취소', '파일명을 변경합니다. \
계속 진행하시겠습니까?')
                            if response:
                                read_dict_file2('create/temp.log')
                                for i in range(len(read_dict)):
                                    if read_dict[i][0] == list_file.get(0):
                                        change_line = read_dict[i][0]
                                os.remove('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                change_save_log(change_line, '{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                                change_temp_log(change_line, '{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                        elif not os.path.isfile('tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))\
                             and change_name == 0:
                            shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                            progress1(current_qy, total_qy)
                            save_log(w_date, y_date)
                            temp_log(w_date)
                            next_order()
                    else:
                        os.mkdir('tmp\{}\{}_renamed'.format(w_id, w_date))
                        shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                        progress1(current_qy, total_qy)
                        save_log(w_date, y_date)
                        temp_log(w_date)
                        next_order()
                else:
                    os.mkdir('tmp\{}'.format(w_id))
                    os.mkdir('tmp\{}\{}_renamed'.format(w_id, w_date))
                    shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                    progress1(current_qy, total_qy)
                    save_log(w_date, y_date)
                    temp_log(w_date)
                    next_order()
            else:
                os.mkdir('tmp')
                os.mkdir('tmp\{}'.format(w_id))
                os.mkdir('tmp\{}\{}_renamed'.format(w_id, w_date))
                shutil.copyfile(list_file.get(0), 'tmp\{}\{}_renamed\{}'.format(w_id, w_date, save_name_is.get()))
                progress1(current_qy, total_qy)
                save_log(w_date, y_date)
                temp_log(w_date)
                next_order()
        
            previous_btn.config(state = 'normal')
            read_dict_file2('create/temp.log')
            pre_img_order = read_dict.copy()
            pre_order = len(pre_img_order)
            change_name = 0
    else:
        msgbox.showinfo('알림', '이미지 파일이 추가되지 않았습니다.')

def dele_new():
    shutil.rmtree('tmp')
    os.remove('create/temp.log')

def upload():
    global total_time
    upload_file()
    dele_new()
    upload_btn.config(state = 'disabled')

    pro_var1.set(0)
    progressbar1.update()
    state = ''
    prog_rate1.configure(text = state)
    prog_rate2.configure(text = state)
    total_time = 0

def write_dict_file1(path, list):
    with open(path, 'w') as tmp_file:
        tmp_file.write(list)

def write_dict_file2(path, list):
    with open(path, 'a') as tmp_file:
        tmp_file.writelines(list)

def read_dict_file(path):
    global read_dict
    read_dict = {}
    with open(path, 'r') as tmp_file:
        while True:
            tmp_line1 = tmp_file.readline().strip()
            if not tmp_line1:
                break
            tmp_line2 = tmp_line1.split('|')
            read_dict[tmp_line2[0]] = tmp_line2[1]

def read_dict_file2(path):
    global read_dict
    read_dict = []
    with open(path, 'r') as tmp_file:
        while True:
            tmp_line1 = tmp_file.readline().strip()
            if not tmp_line1:
                break
            tmp_line2 = tmp_line1.split('|')
            read_dict.append([tmp_line2[2], tmp_line2[3]])

def upload_file():
    start = time.time()
    upload_count = 0

    read_dict_file2('create/temp.log')
    upload_dict = read_dict.copy()

    pro_var1.set(0)
    progressbar1.update()
    state = 'Uploaded : {} / {}'.format(0, len(upload_dict))
    prog_rate1.configure(text = state)

    direction = 0
    direc_id1.config(bg = 'SystemButtonFace')
    direc_id2.config(bg = 'SystemButtonFace')
    direc_id3.config(bg = 'SystemButtonFace')
    direc_id4.config(bg = 'SystemButtonFace')
    occlusion = 0
    occ_name1.config(bg = 'SystemButtonFace')
    occ_name2.config(bg = 'SystemButtonFace')
    occ_name3.config(bg = 'SystemButtonFace')
    occ_name4.config(bg = 'SystemButtonFace')
    occ_name5.config(bg = 'SystemButtonFace')

    try :
        import argparse
        flags = argparse.ArgumentParser(parents=[tools.argparser]).parse_args()
    except ImportError:
        flags = None

    # SCOPES = 'https://www.googleapis.com/auth/drive.file'
    SCOPES = 'https://www.googleapis.com/auth/drive.metadata'
    store = file.Storage('setting/storage.json')
    creds = store.get()

    if not creds or creds.invalid:
        state = "make new storage data file"
        flow = client.flow_from_clientsecrets('setting/client_secret_drive.json', SCOPES)
        creds = tools.run_flow(flow, store, flags) \
                if flags else tools.run_flow(flow, store)

    # DRIVE = build('drive', 'v3', http = creds.authorize(Http()))
    DRIVE = build('drive', 'v3', credentials = creds, static_discovery = False)

    for i in range(len(upload_dict)):
        up_data = upload_dict[i][1]
        up_id = up_data.strip().split('\\')[0]
        up_date = up_data.strip().split('\\')[1]
        up_name = up_data.strip().split('\\')[2]
        
        save_name_is.config(state = 'normal')
        save_name_is.delete(0, END)
        save_name_is.insert(0, up_name)
        save_name_is.config(state = 'readonly')

        read_dict_file('setting/up_d_id.txt')
        shared_drive_id = read_dict.copy()
        if up_id not in shared_drive_id.keys():
            msgbox.showinfo('알림', '존재하지 않는 ID 폴더이므로 새로 추가합니다.')
            # 드라이브 작업자 ID 폴더 생성
            drive_metadata = {
                'name': up_id,
                'mimeType': 'application/vnd.google-apps.folder',
                # Put your google driver folder link key
                'parents': ['Put your google driver folder link key']
            }
            # 폴더 실행문
            res1 = DRIVE.files().create(body = drive_metadata, fields = 'id').execute()
            supportsAllDrives = True
            print ('Folder ID: %s' % res1.get('id'))
            res1_id = res1.get('id')
            worker_id_dict = '{}|{}\n'.format(up_id, res1_id)
            write_dict_file2('setting/up_d_id.txt', worker_id_dict)
            if not res1:
                msgbox.showwarning('경고', '폴더 생성에 실패했습니다.\n다시 시도해 주세요.')
        else:
            # 드라이브 작업자 ID 폴더 생성
            res1_id = shared_drive_id[up_id]

        if not os.path.isfile('create/date_list.txt'):
            # 드라이브 날짜 폴더2 생성
            drive_metadata = {
                'name': up_date,
                'mimeType': 'application/vnd.google-apps.folder',
                'parents':[res1_id]
            }
            # 폴더 실행문
            res2 = DRIVE.files().create(body = drive_metadata, fields = 'id').execute()
            supportsAllDrives = True
            print ('Folder ID: %s' % res2.get('id'))
            res2_id = res2.get('id')
            date_dict = '{}_{}|{}\n'.format(up_id, up_date, res2_id)
            write_dict_file1('create/date_list.txt', date_dict)
            if not res2:
                msgbox.showwarning('경고', '폴더 생성에 실패했습니다.\n다시 시도해 주세요.')
        else:
            # 드라이브 날짜 폴더2 생성
            read_dict_file('create/date_list.txt')
            shared_date_id = read_dict.copy()
            date_id = '{}_{}'.format(up_id, up_date)
            if date_id not in shared_date_id.keys():
                drive_metadata = {
                    'name': up_date,
                    'mimeType': 'application/vnd.google-apps.folder',
                    'parents':[res1_id]
                }
                # 폴더 실행문
                res2 = DRIVE.files().create(body = drive_metadata, fields = 'id').execute()
                supportsAllDrives = True
                print ('Folder ID: %s' % res2.get('id'))
                res2_id = res2.get('id')
                date_dict = '{}_{}|{}\n'.format(up_id, up_date, res2_id)
                write_dict_file2('create/date_list.txt', date_dict)
                if not res2:
                    msgbox.showwarning('경고', '폴더 생성에 실패했습니다.\n다시 시도해 주세요.')
            else:
                res2_id = shared_date_id[date_id]

        #파일 업로드
        from googleapiclient.http import MediaFileUpload
        file_metadata = {'name': up_name, 'parents':[res2_id]}
        file_path = '{}\\tmp\\{}'.format(current_path, up_data)
        media = MediaFileUpload(file_path, resumable = True)

        res3 = DRIVE.files().create(body = file_metadata, media_body = media, fields = 'id').execute()
        supportsAllDrives = True

        if res3:
            upload_count += 1
            end = time.time()
            elapsed_time = end - start
            progress2(upload_count, len(upload_dict), elapsed_time)
    upload_finish_notice(upload_count)

total_time = 0
def progress2(upload_count, total_count, elapsed_time):
    global total_time
    total_time += elapsed_time

    state1 = 'Uploaded : {} / {}'.format(upload_count, total_count,)
    prog_rate1.configure(text = state1)

    state2 = 'Elapsed Time : {:.2f} 초,  Total Time : {:.2f} 초'.format(elapsed_time, total_time)
    prog_rate2.configure(text = state2)

    j = (upload_count / total_count) * 100
    pro_var1.set(j)
    progressbar1.update()

def save_log(w_date, y_date):
    if not os.path.isfile('create/save.log'):
        with open('create/save.log', 'w') as file:
            file.writelines('1|Saved Image|{}|{}\{}_renamed\{}|{}\n'.format(list_file.get(0), worker_id_right.get(), w_date, save_name_is.get(), y_date))
    else:
        with open('create/save.log', 'r') as file:
            file_line = len(file.readlines()) + 1
        with open('create/save.log', 'at') as file:
            file.writelines('{}|Saved Image|{}|{}\{}_renamed\{}|{}\n'.format(file_line, list_file.get(0), worker_id_right.get(), w_date, save_name_is.get(), y_date))

def change_save_log(change_line, save_name):
    read_dict = []
    with open('create/save.log', 'r') as tmp_file:
        while True:
            tmp_line1 = tmp_file.readline().strip()
            if not tmp_line1:
                break
            tmp_line2 = tmp_line1.split('|')
            if tmp_line2[2] != change_line:
                read_dict.append(tmp_line1)
            else:
                read_dict.append('{}|{}|{}|{}|{}'.format(tmp_line2[0], tmp_line2[1], tmp_line2[2], save_name, tmp_line2[4]))
    with open('create/save.log', 'w') as file:
        file.writelines('{}\n'.format(read_dict[0]))
    with open('create/save.log', 'at') as file:
        for i in range(1, len(read_dict)):
            file.writelines('{}\n'.format(read_dict[i]))

def temp_log(w_date):
    if not os.path.isfile('create/temp.log'):
        with open('create/temp.log', 'w') as file:
            file.writelines('1|Saved Image|{}|{}\{}_renamed\{}\n'.format(list_file.get(0), worker_id_right.get(), w_date, save_name_is.get()))
    else:
        with open('create/temp.log', 'r') as file:
            file_line = len(file.readlines()) + 1
        with open('create/temp.log', 'at') as file:
            file.writelines('{}|Saved Image|{}|{}\{}_renamed\{}\n'.format(file_line, list_file.get(0), worker_id_right.get(), w_date, save_name_is.get()))

def change_temp_log(change_line, save_name):
    read_dict = []
    with open('create/temp.log', 'r') as tmp_file:
        while True:
            tmp_line1 = tmp_file.readline().strip()
            if not tmp_line1:
                break
            tmp_line2 = tmp_line1.split('|')
            if tmp_line2[2] != change_line:
                read_dict.append(tmp_line1)
            else:
                read_dict.append('{}|{}|{}|{}'.format(tmp_line2[0], tmp_line2[1], tmp_line2[2], save_name))
    with open('create/temp.log', 'w') as file:
        file.writelines('{}\n'.format(read_dict[0]))
    with open('create/temp.log', 'at') as file:
        for i in range(1, len(read_dict)):
            file.writelines('{}\n'.format(read_dict[i]))

def save_finish_notice():
    with open('create/temp.log', 'r') as file:
        file_cont = file.readlines()
        file_line = len(file_cont)
    msgbox.showinfo('알림', '수고하셨습니다. 총 {}개의 이미지가 네이밍 완료 되었습니다.\n\
업로드 버튼 클릭하면 구글 드라이브로 업로드가 시작됩니다.'.format(file_line))
    upload_btn.config(state = 'normal')

def upload_finish_notice(upload_count):
    msgbox.showinfo('알림', '수고하셨습니다. 총 {}개의 이미지가 업로드 완료 되었습니다.'.format(upload_count))
    upload_btn.config(state = 'normal')

def open_report():
    report = Tk() # report 창
    report.title("작업 집계 리포트")
    report.geometry('710x510+450+150') 
    report.resizable(False, False) 
    
    date_list, worker_list1, class_list1, insta_list1 = [], [], [], []
    worker_list2, class_list2, insta_list2 = [], [], []
    class_list3, insta_list3, insta_list4, image_list = [], [], [], []
    with open('create/save.log', 'r') as tmp_file:
        while True:
            tmp_line1 = tmp_file.readline().strip()
            if not tmp_line1:
                break
            tmp_line2 = tmp_line1.split('|')
            date_list.append(tmp_line2[4])
            cont_name = tmp_line2[3].strip().split('\\')[2]
            worker_list1.append(cont_name.strip().split('_')[1])
            class_list1.append(cont_name.strip().split('_')[0])
            insta_list1.append(cont_name.strip().split('_')[2])

    date_setlist1 = sorted(list(set(date_list)))
    date_setlist = list(reversed(date_setlist1))
    for i in range(len(date_setlist)):
        worker_list2, class_list2, insta_list2 = [], [], []
        for j in range(len(date_list)):
            if date_setlist[i] == date_list[j]:
                worker_list2.append(worker_list1[j])
                class_list2.append(class_list1[j])
                insta_list2.append(insta_list1[j])
        worker_setlist = list(set(worker_list2))
        for k in range(len(worker_setlist)):
            class_list3, insta_list3 = [], []
            for l in range(len(worker_list2)):
                if worker_setlist[k] == worker_list2[l]:
                    class_list3.append(class_list2[l])
                    insta_list3.append(insta_list2[l])
            class_setlist = list(set(class_list3))
            insta_count, image_count = 0, 0
            for m in range(len(class_setlist)):
                insta_list4 = []
                for n in range(len(class_list3)):
                    if class_setlist[m] == class_list3[n]:
                        insta_list4.append(insta_list3[n])
                insta_setlist = list(set(insta_list4))
                insta_count += len(insta_setlist)
                for o in range(len(insta_setlist)):
                    image_list = []
                    for p in range(len(insta_list4)):
                        if insta_setlist[o] == insta_list4[p]:
                            image_list.append(insta_list4[p])
                    image_count += len(image_list)
                with open('setting/report.txt', 'at') as f:
                    f.writelines(('{} : {} 워커님 >> {} 클래스 >> 인스턴스 {}개 >> 이미지 {}개\n')\
                    .format(date_setlist[i], worker_setlist[k], class_setlist[m], len(insta_setlist), len(image_list)))
            with open('setting/report.txt', 'at') as f:
                    f.writelines(('Total : {} {} 워커님은 클래스 총 {}개 >> 인스턴스 총 {}개 >> 이미지 총 {}개 작업\n\n')\
                    .format(date_setlist[i], worker_setlist[k], len(class_setlist), insta_count, image_count))

    with open('setting/report.txt', 'r') as f:
        report_cont = f.read()

    # report frame
    frame_report = Frame(report, relief = 'solid', bd = 1, width = 750)
    frame_report.pack(fill = 'both', expand = True)
    
    scrollbar = Scrollbar(frame_report)
    scrollbar.pack(side = 'right', fill = 'both')

    report_txt = Text(frame_report, width = 97, height = 39, yscrollcommand = scrollbar.set) 
    report_txt.pack(fill = 'both', expand = True)
    report_txt.insert(END, report_cont)

    scrollbar.config(command = report_txt.yview)

    with open('setting/report.txt', 'w') as f:
        f.write('')

keyboard.add_hotkey('z', view_toggle)
keyboard.add_hotkey('x', occ_toggle)

# Report menu
menu = Menu(root)

menu_file = Menu(menu, tearoff = 0)
menu_file.add_command(label = 'Report', command = open_report)
menu_file.add_command(label = 'Exit', command = root.quit)
menu.add_cascade(label = 'File', menu = menu_file)

# top 프레임
frame_top = Frame(root, relief = 'solid', bd = 1, width = 750)
frame_top.pack(side = 'top', fill = 'y', expand = True)

# top_left 이미지 preview 프레임
frame_image = LabelFrame(frame_top, text = 'Image Preview', width = 410)
frame_image.pack(side = 'left', fill = 'both', expand = True)

# top_left add/del 프레임
frame_add_del = Frame(frame_image)
frame_add_del.pack(side = 'top', fill = 'both', expand = True)

btn_add_file = Button(frame_add_del, width = 10, text = 'File Open', command = add_file)
btn_add_file.pack(side = 'right', fill = 'x', padx = 5, pady = 3)

# 선택 이미지 리스트 프레임
list_frame = Frame(frame_image, width = 400)
list_frame.pack(fill = 'both')

list_file = Listbox(list_frame, selectmode = 'single', width = 57, height = 1)
list_file.pack(side = 'left', expand = True, padx = 5, pady = 5)

# 이미지 preview 프레임
photo = PhotoImage()
photo_frame = Label(frame_image, width = 400, height = 400, bg = 'white', image = photo)
photo_frame.pack(expand = 1, anchor = 'center')

# work progressbar 프레임
frame_progress1 = Frame(frame_image)
frame_progress1.pack(fill = 'both', expand = True)

pro_var1 = DoubleVar() # 실수형 자료 입력
progressbar1 = ttk.Progressbar(frame_progress1, maximum =100, length = 250, variable = pro_var1)
progressbar1.pack(side = 'left', padx =5, pady = 5)

prog_rate1 = Label(frame_progress1, text = '')
prog_rate1.pack(side = 'right', padx = 5, pady = 5)

# top_right 이미지 upload 프레임
frame_upload = LabelFrame(frame_top, text = 'Image Upload', width = 340)
frame_upload.pack(side = 'right', fill = 'both', expand = True)

# top_right 이미지 저장정보 프레임
save_info = LabelFrame(frame_upload, text = 'Infomation Setting', width = 330)
save_info.pack(side = 'top', fill = 'x', ipady = 2, expand = True)

# Save Info Left frame
info_left_frame = Frame(save_info, width = 80)
info_left_frame.pack(side = 'left', fill = 'both')

# work_id_left
worker_id_left = Label(info_left_frame, text = 'Worker_ID :')
worker_id_left.pack(anchor = 'e', padx = 5, pady = 5)

# date_left
photo_date_left = Label(info_left_frame, text = '촬영일자 :')
photo_date_left.pack(anchor = 'e', padx = 5, pady = 5)

# class_name_left
class_name_left = Label(info_left_frame, text = 'Class 명 :')
class_name_left.pack(anchor = 'e', padx = 5, pady = 5)

# instance_id_left
ins_list_left = Label(info_left_frame, text = '객체 ID :')
ins_list_left.pack(anchor = 'e', padx = 5, pady = 5)

# view_direction_left
view_dir_left = Label(info_left_frame, text = 'View Direction :\n(toggle : z key)')
view_dir_left.pack(anchor = 'e', padx = 5)

# occlusion_name_left
occ_list_left = Label(info_left_frame, text = 'Occlusion Name :\n(toggle : x key)')
occ_list_left.pack(anchor = 'e', padx = 5, pady = 3)

# Save Info Right frame
info_right_frame = Frame(save_info, width = 250)
info_right_frame.pack(side = 'right', fill = 'both')

# work_id_right
work_id_frame = Frame(info_right_frame)
work_id_frame.pack(anchor = 'w', fill = 'x')

values_workerid = ['{0:03d}'.format(i) for i in range(1, 151)]
worker_id_right = ttk.Combobox(work_id_frame, width = 5, value = values_workerid, state = 'readonly')
worker_id_right.pack(side = 'left', pady = 5)
worker_id_right.set('')

worker_id_btn = Button(work_id_frame, text = '확인', width = 6, state = 'normal', command = worker_id_ok)
worker_id_btn.pack(side = 'left', padx = '10', pady = 3)

worker_id_btn1 = Button(work_id_frame, text = '변경', width = 6, state = 'normal', command = worker_id_change)
worker_id_btn1.pack(side = 'left', pady = 3)

# date_right
date_frame = Frame(info_right_frame)
date_frame.pack(anchor = 'w', fill = 'x')

values_year = [str(i) for i in range(2021, 2023)]
year_combobox = ttk.Combobox(date_frame, width = 4, height = 2, value = values_year, state = 'readonly')
year_combobox.current(0)
year_combobox.pack(side = 'left', pady = 5)

year_label = Label(date_frame, text = '년')
year_label.pack(side = 'left', padx = 1, pady = 5)

values_mon = [str(i) for i in range(1, 13)]
mon_combobox = ttk.Combobox(date_frame, width = 2, height = 5, value = values_mon, state = 'readonly')
mon_combobox.pack(side = 'left', pady = 5)
mon_combobox.set('')

mon_label = Label(date_frame, text = '월')
mon_label.pack(side = 'left', padx = 1, pady = 5)

values_day = [str(i) for i in range(1, 32)]
day_combobox = ttk.Combobox(date_frame, width = 2, height = 5, value = values_day, state = 'readonly')
day_combobox.pack(side = 'left', pady = 5)
day_combobox.set('')

day_label = Label(date_frame, text = '일')
day_label.pack(side = 'left', padx = 1, pady = 5)

# class_list
class_dict = {}
with open('setting/class_list.txt', 'rt', encoding = 'utf-8') as tmp_file:
    while True:
        tmp_line1 = tmp_file.readline().strip()
        if not tmp_line1:
            break
        tmp_line2 = tmp_line1.split('|')
        class_dict[tmp_line2[0]] = tmp_line2[1]
        
class_key_lists = list(sorted(class_dict.keys()))

class_combobox = ttk.Combobox(info_right_frame, width = 23, height = 5, value = class_key_lists, state = 'readonly')
class_combobox.pack(anchor = 'w', pady = 5)

# instance_id
ins_lists = [str('{0:03d}'.format(i)) for i in range(1, 101)]
ins_combobox = ttk.Combobox(info_right_frame, width = 5, height = 5, value = ins_lists, state = 'readonly')
ins_combobox.pack(anchor = 'w', pady = 5)
ins_combobox.set('')

# view_direction_right
view_dir_right_frame = Frame(info_right_frame)
view_dir_right_frame.pack(anchor = 'w', fill = 'x')

direc_id1 = Button(view_dir_right_frame, text = '01', width = 5, command = direc1)
direc_id1.pack(side = 'left', pady = 5)

direc_id2 = Button(view_dir_right_frame, text = '02', width = 5, command = direc2)
direc_id2.pack(side = 'left', padx = 4, pady = 5)

direc_id3 = Button(view_dir_right_frame, text = '03', width = 5, command = direc3)
direc_id3.pack(side = 'left', pady = 5)

direc_id4 = Button(view_dir_right_frame, text = '04', width = 5, command = direc4)
direc_id4.pack(side = 'left', padx = 4, pady = 5)

# occlusion_name_right
occ_list_right_frame = Frame(info_right_frame)
occ_list_right_frame.pack(anchor = 'w', fill = 'x')

occ_name1 = Button(occ_list_right_frame, text = 'None', width = 26, activebackground = 'yellow', state = 'normal', command = occ1)
occ_name1.pack(anchor = 'w', pady = 2)

occ_name2 = Button(occ_list_right_frame, text = 'SemiTransparent', width = 26, activebackground = 'yellow', state = 'normal', command = occ2)
occ_name2.pack(anchor = 'w', pady = 2)

occ_name3 = Button(occ_list_right_frame, text = 'WireDense', width = 26, activebackground = 'yellow', state = 'normal', command = occ3)
occ_name3.pack(anchor = 'w', pady = 2)

occ_name4 = Button(occ_list_right_frame, text = 'WireMedium', width = 26, activebackground = 'yellow', state = 'normal', command = occ4)
occ_name4.pack(anchor = 'w', pady = 2)

occ_name5 = Button(occ_list_right_frame, text = 'WireLoose', width = 26, activebackground = 'yellow', state = 'normal', command = occ5)
occ_name5.pack(anchor = 'w', pady = 2)

# view save name frame
save_name_view = Frame(frame_upload, width = 330)
save_name_view.pack(side = 'top', fill = 'x')

save_name_is = Entry(save_name_view, width = 46, justify = 'center', state = 'normal')
save_name_is.pack(side = 'left', pady = 2)

# top_right move_save frame
rework_upload = LabelFrame(frame_upload, text = '이동 및 네이밍 저장', width = 330)
rework_upload.pack(side = 'top', fill = 'x', ipady = 2, expand = True)

previous_btn = Button(rework_upload, text = 'Previous', width = 10, state = 'disabled', command = pre_img)
previous_btn.pack(side = 'left', padx = 5, pady = 5)

next_btn = Button(rework_upload, text = 'Next', width = 10, state = 'disabled', command = next_img)
next_btn.pack(side = 'left', padx = 5, pady = 5)

save_btn = Button(rework_upload, text = 'Save', width = 15, command = save_new)
save_btn.pack(side = 'right', padx = 5, pady = 5)

# top_right upload frame
google_upload = LabelFrame(frame_upload, text = '네이밍 작업 완료 후 구글 드라이브 업로드', width = 330)
google_upload.pack(side = 'bottom', fill = 'both', ipady = 5, expand = True)

upload_btn = Button(google_upload, text = 'Upload to Google Drive', width = 45, state = 'disabled', command = upload)
upload_btn.pack(anchor = 'w', padx = 5, pady = 5)

# upload progressbar 프레임
frame_progress2 = Frame(google_upload)
frame_progress2.pack(anchor = 'w', fill = 'both', expand = True)

prog_rate2 = Label(frame_progress2, text = '')
prog_rate2.pack(side = 'left', padx = 5, pady = 0)

if os.path.isfile('create/cur_workerid.txt'):
    with open('create/cur_workerid.txt', 'r') as tmp_file:
        worker_id = tmp_file.read()
    worker_id_right.set(worker_id)
    response = True
    worker_id_right.config(state = 'disabled')
    worker_id_btn.config(state = 'disabled')

root.config(menu = menu)
root.mainloop()