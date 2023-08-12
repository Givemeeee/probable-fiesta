from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import taiwan_city
from tkcalendar import DateEntry  # 引入 DateEntry 元件
import csv
import mysql.connector


selected_city = ""
selected_town = ""
selected_birthday = ""  # 新增選擇的生日變數
member_id_counter = 0 
def City_choice(event):
    global selected_city, selected_town
    selected_city = combobox_city.get()
    towns = taiwan_city.taiwan_counties_towns.get(selected_city, [])
    combobox_town['values'] = towns
    selected_town = combobox_town.get()

def Birthday_choice():
    global selected_birthday
    selected_birthday = cal.get_date()  # 紀錄選擇的生日日期

def clear_form():
    Id_entry.delete(0, END)
    Name_entry.delete(0, END)
    Tel_entry.delete(0, END)
    Stree_entry.delete(0, END)
    Data_var.set(" ")

# def generate_member_id():
#     global member_id_counter
#     generated_id = f"A{member_id_counter:06d}"
#     member_id_counter += 1

#     # 檢查生成的會員編號是否已存在，若存在，則尋找下一個可用的編號
#     while is_member_id_duplicate(generated_id):
#         member_id_counter += 1
#         generated_id = f"A{member_id_counter:06d}"

#     return generated_id

# def is_member_id_duplicate(member_id):
#     # 讀取文件並檢查會員編號是否存在於記錄中
#     path = ""
#     with open(path, "r", encoding="utf-8") as file:
#         for line in file:
#             record = line.strip().split(",")
#             if record[0] == member_id:
#                 return True
    return False
def ask_yes_no():
    #global member_id_counter
    City_choice(None)  # 觸發 City_choice() 函數以獲取正確的城市和城鎮值
    Birthday_choice()

    # 檢查 Id_entry 是否為空值，若是則自動產生會員編號
    # if not Id_entry.get():
    #     generated_id = generate_member_id()
    #     Id_entry.insert(0, generated_id)

    response = messagebox.askyesno("您是否同意新增此資料？")
    if response:
        save_data()
        Data_var.set("會員編號："+Id_entry.get() + "\n"+"會員姓名：" + Name_entry.get() + "\n"+"會員電話：" + Tel_entry.get() + "\n" +"會員地址："+ selected_city 
                     + selected_town + "\n" + Stree_entry.get() + "\n"+"會員性別：" + combobox.get() + "\n" +"會員生日："+ str(selected_birthday))
        Data_show["fg"] = "black"
        Data_show["font"] = ("Microsoft JhengHei", int(16 * scale_factor))
        Data_show["justify"] = "left"
    else:
        clear_form()


def save_data():
    # 在 ask_yes_no 函式中獲取的資料
    name = Name_entry.get()
    tel = Tel_entry.get()
    street = Stree_entry.get()
    gender = combobox.get()
    city = selected_city
    town = selected_town
    birthday = selected_birthday

    # 建立與資料庫的連線
    cnx = mysql.connector.connect(
        host="Your host",
        user="Your root",
        password="Your p",
        database="Your database ",
        auth_plugin="mysql_native_password"
    )
    cursor = cnx.cursor(buffered=True)

    # 插入資料，不需要指定 Member_ID 欄位，會自動遞增
    sql = "INSERT INTO membership_list (M_NAME, M_Phone, M_Adress, M_Gender, M_Birth) VALUES (%s, %s, %s, %s, %s)"
    values = (name, tel, street + city + town, gender, birthday)
    cursor.execute(sql, values)
    cnx.commit()

    cursor.close()
    cnx.close()




# 設定視窗大小
window = Tk()
window_width = 300
window_height = 475
window.geometry(f"{window_width}x{window_height}")
window.title("會員登記系統")

# 計算比例因子
width_scale_factor = window.winfo_width() / window_width
height_scale_factor = window.winfo_height() / window_height
scale_factor = min(width_scale_factor, height_scale_factor)

# 設定風格和比例因子
style = ttk.Style(window)
style.configure("TLabel", font=("Microsoft JhengHei)", int(24 * scale_factor)))
style.configure("TButton", font=("Microsoft JhengHei)", int(24 * scale_factor)))
style.configure("TCombobox", font=("Microsoft JhengHei)", int(24 * scale_factor)))  # 調整下拉選單字體大小
style.configure("TEntry", font=("Microsoft JhengHei)", int(24 * scale_factor)))

# 設定元件佈局
Tittle1 = Label(window, text="會員登記系統", font=("Microsoft JhengHei)", int(36 * scale_factor)))
Tittle1.pack(pady=25, anchor=CENTER)  # 將標題向左靠齊

frame1 = Frame(window)
frame1.pack(anchor=W)  # 向左靠齊

Id1 = Label(frame1, text="會員號碼",width=12)
Id1.pack(side=LEFT, padx=5)
Id_entry = Entry(frame1)
Id_entry.pack(side=LEFT)

frame2 = Frame(window)
frame2.pack(anchor=W)  # 向左靠齊

Name1 = Label(frame2, text="會員姓名",width=12)
Name1.pack(side=LEFT, padx=5)
Name_entry = Entry(frame2)
Name_entry.pack(side=LEFT)

frame3 = Frame(window)
frame3.pack(anchor=W)  # 向左靠齊

Tel1 = Label(frame3, text="會員電話",width=12)
Tel1.pack(side=LEFT, padx=5)
Tel_entry = Entry(frame3)
Tel_entry.pack(side=LEFT)

frame4 = Frame(window)
frame4.pack(anchor=W)  # 向左靠齊

Gender1 = Label(frame4, text="會員性別",width=12)
Gender1.pack(side=LEFT, padx=5)
options = ["男", "女", "不透露"]
combobox = ttk.Combobox(frame4, values=options, width=6)  # 調整下拉選單寬度
combobox.set(options[0])
combobox.pack(side=LEFT)
combobox.bind("<<ComboboxSelected>>", City_choice)

frame5 = Frame(window)
frame5.pack(anchor=W)  # 向左靠齊

Birthday_label = Label(frame5, text="會員生日", width=12)
Birthday_label.pack(side=LEFT, padx=5)

cal = DateEntry(frame5, width=12, background='darkblue', foreground='white', borderwidth=2, date_pattern='y-mm-dd')
cal.pack(side=LEFT)


frame6 = Frame(window)
frame6.pack(anchor=W)  # 向左靠齊

Address_label = Label(frame6, text="會員地址",width=12)
Address_label.pack(side=LEFT, padx=5)
options_city = list(taiwan_city.taiwan_counties_towns.keys())
combobox_city = ttk.Combobox(frame6, values=options_city, width=6)  # 調整下拉選單寬度
combobox_city.set(options_city[0])
combobox_city.pack(side=LEFT)
combobox_city.bind("<<ComboboxSelected>>", City_choice)
selected_county = combobox_city.get()
towns = taiwan_city.taiwan_counties_towns.get(selected_county, [])
combobox_town = ttk.Combobox(frame6, values=towns, width=6)  # 調整下拉選單寬度
combobox_town.set(towns[0] if towns else "")
combobox_town.pack(side=LEFT)

frame7 = Frame(window)
frame7.pack(anchor=W)
Stree_label = Label(frame7, text="",width=12)
Stree_label.pack(side=LEFT, padx=5)
Stree_entry = Entry(frame7)  # 調整Entry寬度
Stree_entry.pack(side=LEFT)


frame8 = Frame(window)
frame8.pack()

Id_button = Button(frame8, text="確認", command=ask_yes_no)
Id_button.pack(side=LEFT, padx=5)
Name_button = Button(frame8, text="清除", command=clear_form)
Name_button.pack(side=LEFT)
Tel_button = Button(frame8, text="離開", command=window.destroy)
Tel_button.pack(side=LEFT)


frame9 = Frame(window)
frame9.pack(anchor=CENTER)

Data_var = StringVar()
Data_show = Label(frame9, textvariable=Data_var, font=("Microsoft JhengHei)", int(20 * scale_factor)), foreground="black")
Data_show.pack()



window.mainloop()

