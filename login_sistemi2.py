from tkinter import *
from tkinter import messagebox
import subprocess
import sqlite3

root =Tk()
root.title("Login")
root.geometry("375x250+500+300")
root.configure(bg="#A9A9A9")
root.resizable(False,False)


def signup():
    root.destroy()
    subprocess.run(["python", "hesap_oluştur2.py"])  # Çalıştırılacak olan Python dosyasını burada belirtin

def homeopen():
    root.destroy()
    subprocess.run(["python", "main.py"])  # Çalıştırılacak olan Python dosyasını burada belirtin


#label = Label(root, text="Diğer Python dosyasını çalıştırmak için tıklayın", fg="blue", cursor="hand2")
#label.pack()

# Tıklama olayını işlemek için bind metodu kullanılır
#label.bind("<Button-1>", lambda e: run_python_file())


def check_in():

        
        username=entry1.get()
        password=entry2.get()
        

        ## VERİTABANI İŞLEMLERİ YAPILACAK BURAYA Users adlı veritabanından girilen kullanıcı adı ve şifre var mı diye kontrol edilir
        conn =sqlite3.connect("./veritabanları/Users.db")
        cursor =conn.cursor()
        query = "SELECT * FROM Users WHERE username =? and password=?"
        cursor.execute(query,(username,password))
        result =cursor.fetchone()
        if result:
            
            cursor.execute("CREATE TABLE IF NOT EXISTS last_logins(true_username TEXT)")
            cursor.execute("INSERT INTO last_logins VALUES(?)",(username,))
            conn.commit()
            conn.close()
          
            messagebox.showinfo("","Giriş Başarılı")            
            homeopen()
           
        else:
            messagebox.showinfo("Hata","Giriş Hatalı,Kullanıcı adı veya şifrenizi tekrar deneyiniz")
   

     
global entry1
global enrty2


def temizle():
    entry1.delete(0,END)
    entry2.delete(0,END)


Label(root,text="Kullanıcı Adı",bg="#A9A9A9").place(x=40,y=20)

Label(root,text="Şifre",bg="#A9A9A9").place(x=40,y=70)

entry1 =Entry(root,bd=5,font="arial 12",bg="pink")
entry1.place(x=130,y=20)

entry2 =Entry(root,bd=5,font="arial 12",show="*",bg="#00CED1")
entry2.place(x=130,y=70)

Button(root,text="Giriş Yap",command=check_in,height=3,width=13,bd=4,activeforeground="red",activebackground="blue").place(x=120,y=120)
Button(root,text="Temizle",command=temizle,height=3,width=10,bd=4).place(x=250,y=120)
l1=Label(root,text="Üye değilseniz yeni hesap açmak için ",height=1,width=42,bd=6,bg="#A9A9A9").place(x=30,y=200)


Button(root,text=" tıklayın",bg="#A9A9A9",command=signup).place(x=290,y=200)


root.mainloop()







