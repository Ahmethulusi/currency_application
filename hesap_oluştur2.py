from tkinter import * 
from tkinter import messagebox
import sqlite3
import subprocess

pencere =Tk()
pencere.geometry("375x450+500+300")
pencere.title("Sign Up")
pencere.configure(bg="#A9A9A9")
connection = sqlite3.connect('./veritabanları/Users.db')
cursor = connection.cursor()
cursor.execute('CREATE TABLE IF NOT EXISTS Users (Name text,Surname text,Username text,Password text)')
 

def signin():
    
    pencere.destroy()
    subprocess.run(["python", "login_sistemi2.py"])  # Çalıştırılacak olan Python dosyasını burada belirtin
def SignUp():
        name=namevalues.get()
        surname=surnamevalues.get()
        username=usernamevalues.get()
        password=passwordvalues.get()
        refreshpsword=rfrspassvalues.get()
        conn = sqlite3.connect("./veritabanları/Users.db")
        cursor = conn.cursor()
        if (password==refreshpsword):    
            cursor.execute("INSERT INTO Users (Name,Surname,Username,Password) Values(?,?,?,?)",(name,surname,username,password))
            conn.commit()
            messagebox.showinfo("","Kayıt Başarılı")
            """
            kişiler =[]
            cursor.execute("SELECT * FROM Users")
            rows=cursor.fetchall()
            for row in rows:
                username = row[2]
                kişiler.append(username)            
            for kişi in kişiler:
                username = kişi     
"""
                 
            kullanıcı_db =sqlite3.connect(f"./veritabanları/{username}.db")
               
            varlığım_tablo = f"{username}_varlığım"
            döviz_varlığı_tablosu = f"{username}_döviz_varlığım"

            işlem = kullanıcı_db.cursor()  
            işlem.execute(f"CREATE TABLE IF NOT EXISTS {username}_anlık_kur (ALINAN_TARİH DATE,GÜNCELLENEN_USD REAL,GÜNCELLENEN_EUR REAL,GÜNCELLENEN_GOLD REAL)")          
            işlem.execute(f"CREATE TABLE IF NOT EXISTS {döviz_varlığı_tablosu} (MEVCUT_USD REAL,MEVCUT_EUR REAL,MEVCUT_GOLD REAL,MEVCUT_TOPLAM REAL)")    
            işlem.execute(f""" CREATE TABLE  IF NOT EXISTS {username}_varlığım (MEVCUT_USD_TL REAL,MEVCUT_EUR_TL REAL,MEVCUT_GOLD_TL REAL,MEVCUT_TOPLAM_TL REAL)    """)
            işlem.execute(f"CREATE TABLE IF NOT EXISTS {username}_değişim_kayıtları (ALINAN_TARİH DATE,USD_MİKTAR REAL,EUR_MİKTAR REAL,GOLD_MİKTAR REAL,USD_TL REAL,EUR_TL,GOLD_TL,TOPLAM_KUR_TL REAL)")
            işlem.execute(f"INSERT INTO {varlığım_tablo} VALUES(?,?,?,?)",(0,0,0,0))
            işlem.execute(f"INSERT INTO {döviz_varlığı_tablosu} VALUES(?,?,?,?)",(0,0,0,0))
            kullanıcı_db.commit()
            kullanıcı_db.close()


     

          




global nameent,surnameent,usarnameent,passent,rfrspassentr

namevalues =StringVar()
surnamevalues =StringVar()
usernamevalues =StringVar()
passwordvalues =StringVar()
rfrspassvalues =StringVar()


Namelbl =Label(pencere,text="Name",bg="#A9A9A9")
Namelbl.place(x=30,y=50)

Surnamelbl =Label(pencere,text="Surname",bg="#A9A9A9")
Surnamelbl.place(x=30,y=100)

Usernamelbl =Label(pencere,text="Username",bg="#A9A9A9")
Usernamelbl.place(x=30,y=150)


Passwordlbl =Label(pencere,text="Password",bg="#A9A9A9")
Passwordlbl.place(x=30,y=200)


rfrshPasswordlbl =Label(pencere,text="Refresh Password",bg="#A9A9A9")
rfrshPasswordlbl.place(x=30,y=250)




nameent=Entry(pencere,textvariable=namevalues,bd=2,font="arial 12").place(x=130,y=50)
surnameent=Entry(pencere,textvariable=surnamevalues,bd=2,font="arial 12").place(x=130,y=100)
usarnameent=Entry(pencere,bd=2,textvariable=usernamevalues,font="arial 12").place(x=130,y=150)
passent=Entry(pencere,textvariable=passwordvalues,bd=2,font="arial 12",show="*").place(x=130,y=200)
rfrspassentr=Entry(pencere,textvariable=rfrspassvalues,bd=2,font="arial 12",show="*").place(x=130,y=250)

btn1 =Button(pencere,text="Kaydol",font="calibri 15",command=SignUp).place(x=150,y=300)

btn2 =Button(pencere,text="Geri",font="calibri 15",command=lambda:[signin()]).place(x=150,y=350)


pencere.mainloop()

