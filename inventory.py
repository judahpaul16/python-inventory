from tkinter import *
import tkinter.messagebox as tkMessageBox
import sqlite3
import tkinter.ttk as ttk
import pandas as pd
from datetime import date

root = Tk()
root.title("Python: Inventory System")

width = 840
height = 540
screen_width = root.winfo_screenwidth()
screen_height = root.winfo_screenheight()
x1 = (screen_width/2) - (width/2)
y1 = (screen_height/2) - (height/2)
root.geometry("%dx%d+%d+%d" % (width, height, x1, y1))
root.resizable(0, 0)
root.config(bg="#4287f5")

USERNAME = StringVar()
PASSWORD = StringVar()
PRODUCT_NAME = StringVar()
PRODUCT_PRICE = IntVar()
PRODUCT_ID = StringVar()
PRODUCT_QTY = IntVar()
SEARCH = StringVar()

def main():

    menubar = Menu(root)
    filemenu = Menu(menubar, tearoff=0)
    filemenu.add_command(label="Login", command=ShowLoginForm)
    filemenu.add_command(label="Exit", command=Exit)
    menubar.add_cascade(label="Account", menu=filemenu)
    root.config(menu=menubar)
    root.protocol('WM_DELETE_WINDOW', Exit) # intercept [X] to stop mainloop()

    Title = Frame(root, bd=1, relief=SOLID)
    Title.pack(pady=10)
    Title.place(relx = 0.5, rely = 0.45, anchor = 'center')

    lbl_display = Label(Title, text="Inventory System", font=('arial', 45))
    lbl_display.pack()
    lbl_display2 = Label(Title, text="Please Login to Continue ( Account > Login )", font=('arial', 14), fg='red')
    lbl_display2.pack()

    ShowLoginForm()
    root.lower()
    root.mainloop()

def Database():

    global conn, cursor
    conn = sqlite3.connect("inventory.db")
    cursor = conn.cursor()
    cursor.execute("CREATE TABLE IF NOT EXISTS `admin` (admin_id INTEGER PRIMARY KEY AUTOINCREMENT NOT NULL, username TEXT, password TEXT)")
    cursor.execute("CREATE TABLE IF NOT EXISTS `product` (product_name TEXT, product_qty TEXT, product_price TEXT, product_id TEXT PRIMARY KEY NOT NULL)")
    cursor.execute("SELECT * FROM `admin` WHERE `username` = 'admin' AND `password` = 'admin'")
    if cursor.fetchone() is None:
        cursor.execute("INSERT INTO `admin` (username, password) VALUES('admin', 'admin')")
        conn.commit()

def Exit():

    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to exit?', icon="warning")
    if result == 'yes':
        root.destroy()
        exit()

def ShowLoginForm():

    global loginform
    loginform = Toplevel()
    loginform.title("Inventory System/Account Login")
    width = 300
    height = 185
    screen_width = root.winfo_screenwidth()
    screen_height = root.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    loginform.resizable(0, 0)
    loginform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    LoginForm()
    
def LoginForm():

    global lbl_result
    TopLoginForm = Frame(loginform, width=300, height=30, bd=1, relief=SOLID)
    TopLoginForm.pack(side=TOP)
    lbl_text = Label(TopLoginForm, text="Administrator Login", font=('arial', 12), width=300)
    lbl_text.pack(fill=X)
    MidLoginForm = Frame(loginform, width=300)
    MidLoginForm.pack(side=TOP)
    lbl_username = Label(MidLoginForm, text="Username:", font=('arial', 12), bd=15)
    lbl_username.grid(row=0)
    lbl_password = Label(MidLoginForm, text="Password:", font=('arial', 12), bd=15)
    lbl_password.grid(row=1)
    lbl_result = Label(MidLoginForm, text="", font=('arial', 12))
    lbl_result.grid(row=3, columnspan=2)
    username = Entry(MidLoginForm, textvariable=USERNAME, font=('arial', 12), width=15)
    username.grid(row=0, column=1)
    username.focus_set() # initial focus
    username.bind('<Return>', Login)
    password = Entry(MidLoginForm, textvariable=PASSWORD, font=('arial', 12), width=15, show="*")
    password.grid(row=1, column=1)
    password.bind('<Return>', Login)
    btn_login = Button(MidLoginForm, text="Login", font=('arial', 12), width=15, command=Login)
    btn_login.grid(row=2, columnspan=2)
    btn_login.bind('<Return>', Login)
    
def Login(event=None):

    global admin_id
    Database()

    if USERNAME.get() == "" or PASSWORD.get() == "":
        lbl_result.config(text="Please complete the required fields!", fg="red")
    else:
        cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
        if cursor.fetchone() is not None:
            cursor.execute("SELECT * FROM `admin` WHERE `username` = ? AND `password` = ?", (USERNAME.get(), PASSWORD.get()))
            data = cursor.fetchone()
            admin_id = data[0]
            USERNAME.set("")
            PASSWORD.set("")
            lbl_result.config(text="")
            ShowHome()
        else:
            lbl_result.config(text="Invalid username or password", font="arial, 11", fg="red")
            USERNAME.set("")
            PASSWORD.set("")

    cursor.close()
    conn.close() 

def Logout():

    result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to logout?', icon="warning")

    if result == 'yes': 
        admin_id = ""
        Home.withdraw()
        root.deiconify()

def ShowHome():

    root.withdraw()
    try:
        Home()
    except TypeError:
        Home.deiconify()

    loginform.destroy()

def Home():

    global Home
    Home = Toplevel()
    Home.protocol('WM_DELETE_WINDOW', Exit) # intercept [X] to stop mainloop()
    Home.title("Inventory System/Home")
    bg = "#4287f5"
    width = 840
    height = 540
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    Home.geometry("%dx%d+%d+%d" % (width, height, x, y))
    Home.resizable(0, 0)
    Title = Frame(Home, bd=1, relief=SOLID)
    Title.pack(pady=10)
    Title.place(relx = 0.5, rely = 0.4, anchor = 'center')
    lbl_display = Label(Title, text="Inventory System", font=('arial', 45))
    lbl_display.pack()
    Description = Frame(Home)
    Description.pack(pady=10)
    Description.place(relx = 0.5, rely = 0.55, anchor = 'center')
    lbl_display2 = Label(Description, text="Welcome Back!", font=('arial', 18), bg=bg)
    lbl_display2.pack()
    menubar = Menu(Home)
    filemenu1 = Menu(menubar, tearoff=0)
    filemenu2 = Menu(menubar, tearoff=0)
    filemenu3 = Menu(menubar, tearoff=0)
    filemenu1.add_command(label="Export to CSV", command=Export)
    filemenu1.add_command(label="Add New Item", command=ShowAddNew)
    filemenu2.add_command(label="Logout", command=Logout)
    filemenu2.add_command(label="Exit", command=Exit)
    filemenu3.add_command(label="View Inventory", command=ShowView)
    # filemenu3.add_command(label="View Clients", command=ShowViewClients)
    menubar.add_cascade(label="File", menu=filemenu1)
    menubar.add_cascade(label="Account", menu=filemenu2)
    menubar.add_cascade(label="View", menu=filemenu3)
    Home.config(menu=menubar)
    Home.config(bg=bg)

def ShowAddNew():

    global addnewform
    addnewform = Toplevel()
    addnewform.title("Inventory System/Add New")
    width = 400
    height = 235
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    addnewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    addnewform.resizable(0, 0)
    AddNewForm()

def AddNewForm():

    global lbl_result2
    TopAddNew = Frame(addnewform, width=300, height=50, bd=1, relief=SOLID)
    TopAddNew.pack(side=TOP, pady=5)
    lbl_text = Label(TopAddNew, text="Add New Product", font=('arial', 14), width=300)
    lbl_text.pack(fill=X)
    MidAddNew = Frame(addnewform, width=300)
    MidAddNew.pack(side=TOP, pady=5)
    lbl_productname = Label(MidAddNew, text="Product Name:", font=('arial', 12), bd=5)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidAddNew, text="Product Quantity:", font=('arial', 12), bd=5)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidAddNew, text="Product Price:", font=('arial', 12), bd=5)
    lbl_price.grid(row=2, sticky=W)
    lbl_barcode = Label(MidAddNew, text="ID / Barcode:", font=('arial', 12), bd=5)
    lbl_barcode.grid(row=3, sticky=W)
    lbl_result2 = Label(MidAddNew, text="", font=('arial', 12))
    lbl_result2.grid(row=5, columnspan=2)
    productname = Entry(MidAddNew, textvariable=PRODUCT_NAME, font=('arial', 12), width=20)
    productname.grid(row=0, column=1)
    productqty = Entry(MidAddNew, textvariable=PRODUCT_QTY, font=('arial', 12), width=20)
    productqty.grid(row=1, column=1)
    productprice = Entry(MidAddNew, textvariable=PRODUCT_PRICE, font=('arial', 12), width=20)
    productprice.grid(row=2, column=1)
    productid = Entry(MidAddNew, textvariable=PRODUCT_ID, font=('arial', 12), width=20)
    productid.grid(row=3, column=1)
    productid.bind('<Return>', AddNew)
    btn_add = Button(MidAddNew, text="Save", font=('arial', 11), width=15, bg="#009ACD", command=AddNew)
    btn_add.grid(row=4, columnspan=2, pady=5)
    btn_add.bind('<Return>', AddNew)

def AddNew():

    Database()

    if PRODUCT_NAME.get() == "" or PRODUCT_PRICE.get() == "" or PRODUCT_QTY.get() == "" or PRODUCT_ID.get() == "":
        lbl_result2.config(text="Please complete the required fields!", fg="red")
    else:
        cursor.execute("INSERT INTO `product` (product_name, product_qty, product_price, product_id) VALUES(?, ?, ?, ?)",
            (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get()), str(PRODUCT_ID.get())))
        conn.commit()
        PRODUCT_NAME.set("")
        PRODUCT_PRICE.set("")
        PRODUCT_QTY.set("")
        PRODUCT_ID.set("")
        cursor.close()
        conn.close()
        try:
            Reset()
        except NameError:
            pass


def ShowUpdate():

    if tree.selection():
        global updateform
        updateform = Toplevel()
        updateform.title("Inventory System/Update")
        width = 400
        height = 235
        screen_width = Home.winfo_screenwidth()
        screen_height = Home.winfo_screenheight()
        x = (screen_width/2) - (width/2)
        y = (screen_height/2) - (height/2)
        updateform.geometry("%dx%d+%d+%d" % (width, height, x, y))
        updateform.resizable(0, 0)
        UpdateForm()

def UpdateForm():

    global lbl_result3
    TopUpdate = Frame(updateform, width=300, height=50, bd=1, relief=SOLID)
    TopUpdate.pack(side=TOP, pady=5)
    lbl_text = Label(TopUpdate, text="Update Product", font=('arial', 14), width=300)
    lbl_text.pack(fill=X)
    MidUpdate = Frame(updateform, width=300)
    MidUpdate.pack(side=TOP, pady=5)
    lbl_productname = Label(MidUpdate, text="Product Name:", font=('arial', 12), bd=5)
    lbl_productname.grid(row=0, sticky=W)
    lbl_qty = Label(MidUpdate, text="Product Quantity:", font=('arial', 12), bd=5)
    lbl_qty.grid(row=1, sticky=W)
    lbl_price = Label(MidUpdate, text="Product Price:", font=('arial', 12), bd=5)
    lbl_price.grid(row=2, sticky=W)
    lbl_barcode = Label(MidUpdate, text="ID / Barcode:", font=('arial', 12), bd=5)
    lbl_barcode.grid(row=3, sticky=W)
    lbl_result3 = Label(MidUpdate, text="", font=('arial', 12))
    lbl_result3.grid(row=5, columnspan=2)
    productname = Entry(MidUpdate, textvariable=PRODUCT_NAME, font=('arial', 12), width=20)
    productname.grid(row=0, column=1)
    productqty = Entry(MidUpdate, textvariable=PRODUCT_QTY, font=('arial', 12), width=20)
    productqty.grid(row=1, column=1)
    productprice = Entry(MidUpdate, textvariable=PRODUCT_PRICE, font=('arial', 12), width=20)
    productprice.grid(row=2, column=1)
    productid = Entry(MidUpdate, textvariable=PRODUCT_ID, font=('arial', 12), width=20)
    productid.grid(row=3, column=1)
    productid.bind('<Return>', Update)
    btn_update = Button(MidUpdate, text="Save", font=('arial', 11), width=15, bg="#009ACD", command=Update)
    btn_update.grid(row=4, columnspan=2, pady=5)
    btn_update.bind('<Return>', Update)

def Update():

    if PRODUCT_NAME.get() == "" or (PRODUCT_PRICE.get() == "" or PRODUCT_PRICE.get() == "0") or (PRODUCT_QTY.get() == "" or PRODUCT_QTY.get() == "0") or PRODUCT_ID.get() == "":
        lbl_result3.config(text="Please complete the required fields!", fg="red")
    else:
        curItem = tree.focus()
        contents = (tree.item(curItem))
        selecteditem = contents['values']
        tree.delete(curItem)
        Database()

        cursor.execute("UPDATE `product` SET `product_name` = ?, `product_qty` = ?, `product_price` = ?, `product_id` = ? WHERE `product_id` == ?",
            (str(PRODUCT_NAME.get()), int(PRODUCT_QTY.get()), int(PRODUCT_PRICE.get()), str(PRODUCT_ID.get()), selecteditem[len(selecteditem) - 1]))
        conn.commit()
        PRODUCT_NAME.set("")
        PRODUCT_PRICE.set("")
        PRODUCT_QTY.set("")
        PRODUCT_ID.set("")
        cursor.close()
        conn.close()
        Reset()

def ShowView():

    global viewform
    viewform = Toplevel()
    viewform.title("Inventory System/Explorer")
    width = 700
    height = 450
    screen_width = Home.winfo_screenwidth()
    screen_height = Home.winfo_screenheight()
    x = (screen_width/2) - (width/2)
    y = (screen_height/2) - (height/2)
    viewform.geometry("%dx%d+%d+%d" % (width, height, x, y))
    viewform.resizable(0, 0)
    ViewForm()

def ViewForm():

    global tree
    TopViewForm = Frame(viewform, width=600, bd=1, relief=SOLID)
    TopViewForm.pack(side=TOP, fill=X)
    LeftViewForm = Frame(viewform, width=600)
    LeftViewForm.pack(side=LEFT, fill=Y)
    MidViewForm = Frame(viewform, width=600)
    MidViewForm.pack(side=RIGHT)
    lbl_text = Label(TopViewForm, text="Inventory Explorer", font=('arial', 18), width=600)
    lbl_text.pack(fill=X)
    lbl_txtsearch = Label(LeftViewForm, text="Search", font=('arial', 15))
    lbl_txtsearch.pack(side=TOP, anchor=CENTER)
    search = Entry(LeftViewForm, textvariable=SEARCH, font=('arial', 15), width=10)
    search.pack(side=TOP,  padx=10, fill=X)
    btn_search = Button(LeftViewForm, text="Search", command=Search)
    btn_search.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_reset = Button(LeftViewForm, text="Reset Product View", command=Reset)
    btn_reset.pack(side=BOTTOM, padx=10, pady=10, fill=X)
    btn_add = Button(LeftViewForm, text="Add", command=ShowAddNew)
    btn_add.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_update = Button(LeftViewForm, text="Edit", command=ShowUpdate)
    btn_update.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_delete = Button(LeftViewForm, text="Delete", command=Delete)
    btn_delete.pack(side=TOP, padx=10, pady=10, fill=X)
    btn_export = Button(LeftViewForm, text="Export Data", command=Export)
    btn_export.pack(side=TOP, padx=10, pady=10, fill=X)
    scrollbarx = Scrollbar(MidViewForm, orient=HORIZONTAL)
    scrollbary = Scrollbar(MidViewForm, orient=VERTICAL)
    tree = ttk.Treeview(
        MidViewForm,
        columns=
        (
            "Product Name",
            "Product Qty",
            "Product Price",
            "ID / Barcode"
        ),
        selectmode="extended",
        height=100,
        yscrollcommand=scrollbary.set,
        xscrollcommand=scrollbarx.set
    )
    scrollbary.config(command=tree.yview)
    scrollbary.pack(side=RIGHT, fill=Y)
    scrollbarx.config(command=tree.xview)
    scrollbarx.pack(side=BOTTOM, fill=X)
    tree.heading('Product Name', text="Product Name",anchor=W)
    tree.heading('Product Qty', text="Qty",anchor=W)
    tree.heading('Product Price', text="Price",anchor=W)
    tree.heading('ID / Barcode', text="ID / Barcode",anchor=W)
    tree.column('#0', stretch=YES, minwidth=0, width=0)
    tree.column('#1', stretch=YES, minwidth=0, width=200)
    tree.column('#2', stretch=YES, minwidth=0, width=75)
    tree.column('#3', stretch=YES, minwidth=0, width=75)
    tree.column('#4', stretch=YES, minwidth=0, width=175)
    tree.pack()
    DisplayData()

def DisplayData():

    Database()
    cursor.execute("SELECT * FROM `product`")
    fetch = cursor.fetchall()
    for data in fetch:
        tree.insert('', 'end', values=(data))
    cursor.close()
    conn.close()

def Search():

    if SEARCH.get() != "":
        tree.delete(*tree.get_children())
        Database()
        cursor.execute("SELECT * FROM `product` WHERE `product_name` LIKE ?", ('%'+str(SEARCH.get())+'%',))
        fetch = cursor.fetchall()
        for data in fetch:
            tree.insert('', 'end', values=(data))
        cursor.close()
        conn.close()

def Reset():

    tree.delete(*tree.get_children())
    DisplayData()
    SEARCH.set("")

def Delete():

    if tree.selection():
        result = tkMessageBox.askquestion('Inventory System', 'Are you sure you want to delete this record?', icon="warning")
        if result == 'yes':
            curItem = tree.focus()
            contents = (tree.item(curItem))
            selecteditem = contents['values']
            tree.delete(curItem)
            Database()
            cursor.execute("DELETE FROM `product` WHERE `product_id` = ?", (selecteditem[len(selecteditem) - 1], ))
            conn.commit()
            cursor.close()
            conn.close()

def Export():

        timestamp = date.today().strftime("%m_%d_%Y")

        Database()
        db_df = pd.read_sql_query("SELECT * FROM `product`", conn)
        db_df.to_csv(f'inventory({timestamp}).csv')
        tkMessageBox.showinfo('Successful Export', 'Database Successfully Exported')

if __name__ == '__main__':
    main()