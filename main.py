from tkinter import *
from tkinter import messagebox
from tkinter import ttk
import sqlite3
from datetime import datetime
from time import *
import http.client
import json
from tkcalendar import *
from grafik import *

def get_last_login():
    global true_username
    conn =sqlite3.connect("./veritabanları/Users.db")
    cursor=conn.cursor()
    cursor.execute("SELECT true_username FROM last_logins ORDER BY rowid DESC LIMIT 1")
    last_login=cursor.fetchone()
    true_username=last_login[0]
get_last_login()    
varlığım_tablo_adı =f"{true_username}_varlığım"
değişim_tablo_adı =f"{true_username}_değişim_kayıtları"
döviz_varlığı_tablosu =f"{true_username}_döviz_varlığım"
anlık_kur_tablosu =f"{true_username}_anlık_kur"

window = Tk()
window.title("Döviz App")
window.geometry("700x500+400+200")  
window.configure(bg="#99CC99")
window.resizable(0, 0)




def dolar_kur_çekme():
    
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5tGY68otSZmvi9q4BAEoVs:6L3RFPW86TwyAyl0U9BYcn"
        }

    conn.request("GET", "/economy/currencyToAll?int=10&base=USD", headers=headers)
    res = conn.getresponse()
    dolar_data = res.read().decode("utf-8")
    
    parsed_data=json.loads(dolar_data)
    try_index = None
    for index, currency in enumerate(parsed_data["result"]["data"]):
        if currency["code"] == "TRY":
            try_index = index
            break
    
    global dolar_tl_karşılığı,alınma_tarih_dolar
    dolar_tl_karşılığı = parsed_data["result"]["data"][try_index]["rate"]
    alınma_tarih_dolar = parsed_data["result"]["lastupdate"]
  #  print(" 1 dolar = {0} TL".format(int(dolar_tl_karşılığı)))

def euro_kur_çekme():

    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5tGY68otSZmvi9q4BAEoVs:6L3RFPW86TwyAyl0U9BYcn"
        }

    
    conn.request("GET", "/economy/currencyToAll?int=10&base=EUR", headers=headers)
    res = conn.getresponse()
    euro_data = res.read().decode("utf-8")
    
    parsed_data=json.loads(euro_data)
    
    try_index = None
    for index, currency in enumerate(parsed_data["result"]["data"]):
        if currency["code"] == "TRY":
            try_index = index
            break
    global euro_tl_karşılığı,alınma_tarih_euro
    euro_tl_karşılığı = parsed_data["result"]["data"][try_index]["rate"]
    alınma_tarih_euro = parsed_data["result"]["lastupdate"]
   # print(" 1 euro = {0} TL".format(int(euro_tl_karşılığı)))
def altın_kur_çekme():
    conn = http.client.HTTPSConnection("api.collectapi.com")

    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5tGY68otSZmvi9q4BAEoVs:6L3RFPW86TwyAyl0U9BYcn"
        }

    global gr_satış_fiyatı
    #altın_türü = input("hangi altın bozdurmak istiyorsunuz ?").title()

    conn.request("GET", "/economy/goldPrice", headers=headers)
    res = conn.getresponse()
    altın_data = res.read().decode("utf-8")
    
    parsed_data=json.loads(altın_data)
    
    try_index = None
    for index, currency in enumerate(parsed_data["result"]):
        if currency["name"] == "Gram Altın":
            try_index = index
            break
    gr_satış_fiyatı = parsed_data["result"][try_index]["selling"]
    
    #print(" 1 {0} = {1} TL".format("Gram Altın",float(gr_satış_fiyatı)))
    

def altın_kur_bozdurma():
    global satış_fiyatı,alınma_tarih_altın,alış_fiyatı,altın_türü_entry,altın_türü
    altın_türü= altın_türü_entry.get()
  
    conn = http.client.HTTPSConnection("api.collectapi.com")
    headers = {
        'content-type': "application/json",
        'authorization': "apikey 5tGY68otSZmvi9q4BAEoVs:6L3RFPW86TwyAyl0U9BYcn"
        }

    

    conn.request("GET", "/economy/goldPrice", headers=headers)
    res = conn.getresponse()
    altın_data = res.read().decode("utf-8")
    
    parsed_data=json.loads(altın_data)
    try_index = None
    for index, currency in enumerate(parsed_data["result"]):
        if currency["name"] == altın_türü.title() +" Altın":
            try_index = index
            break
    satış_fiyatı = parsed_data["result"][try_index]["selling"]
    alış_fiyatı = parsed_data["result"][try_index]["buying"]
    alınma_tarih_altın = parsed_data["result"][try_index]["datetime"]




def mvct_dvz_varlık_güncelle():
    global varlığım_tablo_adı
    conn = sqlite3.connect(f"./veritabanları/{true_username}.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {döviz_varlığı_tablosu}")
    rows = cursor.fetchall()
    for row in rows:
        usd_new=row[0]
        eur_new=row[1]
        gold_new=row[2]
    
    veri_usd_lbl1.destroy()
    veri_eur_lbl1.destroy()
    veri_gold_lbl1.destroy()
        
    
    veri_usd_lbl2 = Label(window, text=f"{usd_new} ",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_usd_lbl2.place(x=160,y=250)


    veri_eur_lbl2 = Label(window, text=f"{eur_new}",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_eur_lbl2.place(x=300,y=250)

    
    veri_gold_lbl2 = Label(window, text=f"{gold_new} ",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_gold_lbl2.place(x=450,y=250)

def mvct_tl_vrlk_güncelle():

    conn = sqlite3.connect(f"./veritabanları/{true_username}.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {varlığım_tablo_adı}")
    rows = cursor.fetchall()
    for row in rows:
        usd_new=row[0]
        eur_new=row[1]
        gold_new=row[2]
        toplam_new=row[3]
    
    veri_usd_lbl.destroy()
    veri_eur_lbl.destroy()
    veri_gold_lbl.destroy()
    veri_toplam_lbl.destroy()

    veri_usd_lbl_new = Label(window, text=f"{usd_new} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_usd_lbl_new.place(x=100,y=140)

        
    veri_eur_lbl_new = Label(window, text=f"{eur_new} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_eur_lbl_new.place(x=250,y=140)

        
    veri_gold_lbl_new = Label(window, text=f"{gold_new} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_gold_lbl_new.place(x=400,y=140)

    
    veri_toplam_lbl_new = Label(window, text=f"{toplam_new} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
    veri_toplam_lbl_new.place(x=550,y=140)


kullanıcı_db = sqlite3.connect(f"./veritabanları/{true_username}.db")
işlem = kullanıcı_db.cursor()
işlem.execute(f"SELECT * FROM {varlığım_tablo_adı}")
rows = işlem.fetchall()
for row in rows:
    usd_tl=row[0]
    eur_tl=row[1]
    gold_tl=row[2]
    toplam_tl=row[3]
    
mevcut_kullanıcı_lbl = Label(window, text=f"{true_username}",font="Arial 14 bold", anchor="center",bg="#99CC99",fg="#000080").place(x=560,y=10)
mevcut_varlığım_lbl = Label(window, text="Mevcut TL Varlığım",font="Arial 14 bold", anchor="center",bg="#99CC99")
mevcut_varlığım_lbl.place(x=280,y=50)

mevcut_usd_lbl = Label(window, text="USD",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_usd_lbl.place(x=100,y=100)

veri_usd_lbl = Label(window, text=f"{usd_tl} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_usd_lbl.place(x=100,y=140)

mevcut_eur_lbl = Label(window, text="EUR",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_eur_lbl.place(x=250,y=100)

veri_eur_lbl = Label(window, text=f"{eur_tl} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_eur_lbl.place(x=250,y=140)

mevcut_gold_lbl = Label(window, text="GOLD",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_gold_lbl.place(x=400,y=100)

veri_gold_lbl = Label(window, text=f"{gold_tl} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_gold_lbl.place(x=400,y=140)

mevcut_toplam_lbl = Label(window, text="TOPLAM",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_toplam_lbl.place(x=550,y=100)

veri_toplam_lbl = Label(window, text=f"{toplam_tl} TL",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_toplam_lbl.place(x=550,y=140)


# döviz varlığım
işlem.execute(f"SELECT * FROM {döviz_varlığı_tablosu}")
datas = işlem.fetchall()
for data in datas:
    usd=data[0]
    eur=data[1]
    gold=data[2]
mvct_dvz_varlığım_lbl = Label(window, text="Mevcut Döviz Varlığım",font="Arial 14 bold", anchor="center",bg="#99CC99")
mvct_dvz_varlığım_lbl.place(x=280,y=180)

mevcut_usd_lbl1 = Label(window, text="USD",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_usd_lbl1.place(x=160,y=220)

veri_usd_lbl1 = Label(window, text=f"{usd} ",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_usd_lbl1.place(x=160,y=250)

mevcut_eur_lbl1 = Label(window, text="EUR",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_eur_lbl1.place(x=300,y=220)

veri_eur_lbl1 = Label(window, text=f"{eur}",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_eur_lbl1.place(x=300,y=250)

mevcut_gold_lbl1 = Label(window, text="GOLD(karışık)",font="Arial 11 bold", anchor="center",bg="#99CC99")
mevcut_gold_lbl1.place(x=450,y=220)

veri_gold_lbl1 = Label(window, text=f"{gold} ",font="Arial 11 bold", anchor="center",fg="#3300FF",bg="#99CC99")
veri_gold_lbl1.place(x=450,y=250)




def bozdur():
        
        kullanıcı_db =sqlite3.connect(f"./veritabanları/{true_username}.db")
        imleç =kullanıcı_db.cursor()
        birim = birim_entry.get()
        miktar_deg = int(miktar_entry.get())
        if birim.upper() =="USD":
            dolar_kur_çekme()
            
            #print(" {0} dolar = {1} TL".format(miktar,miktar*int(dolar_tl_karşılığı)))
            # Önceki toplamı alın
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(dolar_tl_karşılığı) # Örnek olarak yeni değeri 100 olarak varsayalım
           # new_value2= "{:.3f}".format(new_value)
            new_total = float(previous_total) + new_value
            onay = messagebox.askquestion("Dikkat", " {} dolar {} TL, bozdurmak istediğinize emin misiniz ?".format(miktar_deg,new_value))
            if onay == "yes":
                imleç.execute(f"INSERT INTO {değişim_tablo_adı} (ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),miktar_deg,0,0,miktar_deg*int(dolar_tl_karşılığı),0,0,new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET    MEVCUT_USD_TL=MEVCUT_USD_TL+? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL+?", (miktar_deg*int(dolar_tl_karşılığı),miktar_deg*int(dolar_tl_karşılığı),))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?)",(datetime.now(),dolar_tl_karşılığı,0,0))
                #cursor.execute("INSERT INTO DEĞİŞİM_KAYITLARI (ALINAN_TARİH,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES (?, ?, ?, ?, ?) ",(datetime.now(),miktar_deg*int(dolar_tl_karşılığı),0,0,new_total))
                #cursor.execute("UPDATE paralarım SET    MEVCUT_USD_TL=MEVCUT_USD_TL+? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL+?", (miktar_deg*int(dolar_tl_karşılığı),miktar_deg*int(dolar_tl_karşılığı),))
                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
            
        if birim.upper() =="EUR":
            euro_kur_çekme()
            #print(" {0} euro = {1} TL".format(miktar,miktar*int(euro_tl_karşılığı)))
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")            # Önceki toplamı alın
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(euro_tl_karşılığı) # Örnek olarak yeni değeri 100 olarak varsayalım
            new_total = previous_total + new_value
            onay = messagebox.askquestion("Dikkat", " {} euro {} TL ,bozdurmak istediğinize emin misiniz ?".format(miktar_deg,new_value))
            if onay == "yes":
                imleç.execute(f"INSERT INTO {değişim_tablo_adı}  (ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),0,miktar_deg,0,0,miktar_deg*int(euro_tl_karşılığı),0,new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET MEVCUT_EUR_TL=MEVCUT_EUR_TL+? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL+?", (miktar_deg*int(euro_tl_karşılığı),miktar_deg*int(euro_tl_karşılığı),))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?) ",(datetime.now(),0,euro_tl_karşılığı,0))

                #cursor.execute("INSERT INTO DEĞİŞİM_KAYITLARI (ALINAN_TARİH,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES (?, ?, ?, ?, ?) ",(datetime.now(),0,miktar_deg*int(euro_tl_karşılığı),0,new_total))
                #cursor.execute("UPDATE paralarım SET MEVCUT_EUR_TL=MEVCUT_EUR_TL+? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL+?", (miktar_deg*int(euro_tl_karşılığı),miktar_deg*int(euro_tl_karşılığı),))
                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
        if birim.upper() =="GOLD":
            altın_kur_bozdurma()
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")
            # Önceki toplamı alın
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(satış_fiyatı) # Örnek olarak yeni değeri 100 olarak varsayalım
            new_total = previous_total + new_value
            onay = messagebox.askquestion("Dikkat", " {} {} Altın {} TL ,bozdurmak istediğinize emin misiniz ?".format(miktar_deg,altın_türü,new_value))
            #print(" {0} {2}  = {1} TL".format(miktar,miktar*int(satış_fiyatı),altın_türü))
            if onay == "yes":
                imleç.execute(f"INSERT INTO  {değişim_tablo_adı}  (ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),0,0,miktar_deg,0,0,miktar_deg*int(satış_fiyatı),new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET MEVCUT_GOLD_TL=MEVCUT_GOLD_TL+? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL+?", (miktar_deg*int(satış_fiyatı),miktar_deg*int(satış_fiyatı),))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?)",(datetime.now(),0,0,satış_fiyatı))

                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
            
        kullanıcı_db.close()
def döviz_al():
      
        kullanıcı_db =sqlite3.connect(f"./veritabanları/{true_username}.db")
        imleç =kullanıcı_db.cursor()
        birim = birim_entry.get()
        miktar_deg = int(miktar_entry.get())
        if birim.upper() =="USD":
            dolar_kur_çekme()
            
            #print(" {0} dolar = {1} TL".format(miktar,miktar*int(dolar_tl_karşılığı)))
            # Önceki toplamı alın
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(dolar_tl_karşılığı) # Örnek olarak yeni değeri 100 olarak varsayalım
           # new_value2= "{:.3f}".format(new_value)
            new_total = float(previous_total) - new_value
            onay = messagebox.askquestion("Dikkat", " {} dolar {} TL, almak istediğinize emin misiniz ?".format(miktar_deg,new_value))
            if onay == "yes":
                imleç.execute(f"INSERT INTO {değişim_tablo_adı} (ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),miktar_deg,0,0,miktar_deg*int(dolar_tl_karşılığı),0,0,new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET    MEVCUT_USD_TL=MEVCUT_USD_TL-? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL-?", (miktar_deg*int(dolar_tl_karşılığı),miktar_deg*int(dolar_tl_karşılığı),))
                imleç.execute(f"UPDATE {döviz_varlığı_tablosu} SET MEVCUT_USD=MEVCUT_USD+? ", (miktar_deg,))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?)",(datetime.now(),dolar_tl_karşılığı,0,0))
                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_dvz_varlık_güncelle()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
            
        if birim.upper() =="EUR":
            euro_kur_çekme()
            #print(" {0} euro = {1} TL".format(miktar,miktar*int(euro_tl_karşılığı)))
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")            # Önceki toplamı alın
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(euro_tl_karşılığı) # Örnek olarak yeni değeri 100 olarak varsayalım
            new_total = previous_total - new_value
            onay = messagebox.askquestion("Dikkat", " {} euro {} TL ,almak istediğinize emin misiniz ?".format(miktar_deg,new_value))
            if onay == "yes":
                imleç.execute(f"INSERT INTO {değişim_tablo_adı}  ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),0,miktar_deg,0,0,miktar_deg*int(euro_tl_karşılığı),0,new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET MEVCUT_EUR_TL=MEVCUT_EUR_TL-? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL-?", (miktar_deg*int(euro_tl_karşılığı),miktar_deg*int(euro_tl_karşılığı),))
                imleç.execute(f"UPDATE {döviz_varlığı_tablosu} SET MEVCUT_EUR=MEVCUT_EUR+? ", (miktar_deg,))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?)",(datetime.now(),0,euro_tl_karşılığı,0))
                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_dvz_varlık_güncelle()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
        if birim.upper() =="GOLD":
            altın_kur_bozdurma()
            imleç.execute(f"SELECT TOPLAM_KUR_TL FROM {değişim_tablo_adı} ORDER BY rowid DESC LIMIT 1")
            # Önceki toplamı alın
            previous_total_row = imleç.fetchone()
            if previous_total_row is not None:
                previous_total = previous_total_row[0]
            else:
                previous_total = 0.0

            # Yeni değeri hesaplayın ve toplamı güncelleyin
            new_value = miktar_deg*int(satış_fiyatı) # Örnek olarak yeni değeri 100 olarak varsayalım
            new_total = previous_total - new_value
            onay = messagebox.askquestion("Dikkat", " {} {} Altın {} TL ,almak istediğinize emin misiniz ?".format(miktar_deg,altın_türü,new_value))
            #print(" {0} {2}  = {1} TL".format(miktar,miktar*int(satış_fiyatı),altın_türü))
            if onay == "yes":
                imleç.execute(f"INSERT INTO  {değişim_tablo_adı}  ALINAN_TARİH,USD_MİKTAR,EUR_MİKTAR,GOLD_MİKTAR,USD_TL,EUR_TL ,GOLD_TL , TOPLAM_KUR_TL ) VALUES ( ?, ?, ?, ?, ?, ?, ?, ?) ",(datetime.now(),0,0,miktar_deg,0,0,miktar_deg*int(satış_fiyatı),new_total))
                imleç.execute(f"UPDATE {varlığım_tablo_adı} SET MEVCUT_GOLD_TL=MEVCUT_GOLD_TL-? , MEVCUT_TOPLAM_TL=MEVCUT_TOPLAM_TL-?", (miktar_deg*int(alış_fiyatı),miktar_deg*int(alış_fiyatı),))
                imleç.execute(f"UPDATE {döviz_varlığı_tablosu} SET MEVCUT_GOLD=MEVCUT_GOLD+? ", (miktar_deg,))
                imleç.execute(f"INSERT INTO {anlık_kur_tablosu} (ALINAN_TARİH ,GÜNCELLENEN_USD ,GÜNCELLENEN_EUR ,GÜNCELLENEN_GOLD) VALUES (?,?,?,?)",(datetime.now(),0,0,alış_fiyatı))
                kullanıcı_db.commit()
                dvz_bzd_window.destroy()
                mvct_dvz_varlık_güncelle()
                mvct_tl_vrlk_güncelle()
                messagebox.showinfo("işlem", "İşlem başarılı")
            
        kullanıcı_db.close()

def döviz_bozdurma():
    global  dvz_bzd_window,altın_türü_entry,birim_entry,miktar_entry
    
    dvz_bzd_window =Toplevel(window)
    dvz_bzd_window.title("Döviz Bozdurma")
    dvz_bzd_window.configure(bg="lightgray")
    dvz_bzd_window.geometry("450x300+500+350")

    birim_lbl = Label(dvz_bzd_window,text="Birim",font="Arial 11 bold",anchor="center",bg="lightgray")
    birim_lbl.place(x=100,y=50)

    birim_entry = Entry(dvz_bzd_window,width=40,relief="groove")
    birim_entry.place(x=150,y=50)


    miktar_lbl = Label(dvz_bzd_window,text="Miktar",font="Arial 11 bold",anchor="center",bg="lightgray")
    miktar_lbl.place(x=100,y=100)

    miktar_entry = Entry(dvz_bzd_window,width=40,relief="groove")
    miktar_entry.place(x=150,y=100)
    
    altın_türü_lbl = Label(dvz_bzd_window, text="Altınsa eğer hangi altın\n(tek kelime yeterli)?,",font="Arial 11 bold",anchor="center",bg="lightgray")
    altın_türü_lbl.place(x=180,y=130)
    altın_türü_entry=Entry(dvz_bzd_window,width=40,relief="groove")
    altın_türü_entry.place(x=150,y=180)



    bzdr_btn = Button(dvz_bzd_window,text="Bozdur",bg="#99CC99",font="Arial 11 bold",command=bozdur)
    al_btn = Button(dvz_bzd_window,text="Al",bg="#99CC99",font="Arial 11 bold",command=döviz_al)
    bzdr_btn.place(x=200,y=230)
    al_btn.place(x=300,y=230)
    dvz_bzd_window.mainloop()



def satır_sec_işlem(event):
    global table2,selected_row
    selected_row = table2.focus()
    print(selected_row)
def satır_sec_kur(event):
    global table3,selected_row
    selected_row = table3.focus()
    print(selected_row)

def satır_sil_işlem_kayıt():
    global table2
    selected_row = table2.focus()
    if selected_row:
        #seçili satırın kimlik değerini al
        tarih = table2.set(selected_row, "#1")
        # veritabanından silme işlemi
        bağlantı = sqlite3.connect(f"./veritabanları/{true_username}.db")
        cursor = bağlantı.cursor()
        cursor.execute(f"DELETE FROM {değişim_tablo_adı} WHERE ALINAN_TARİH=? """, (tarih,))
        bağlantı.commit()
        # seçili satırı silme işlemi
        table2.delete(selected_row)
        bağlantı.close()
    # tabloya tıklama olayını bağlama

def satır_sil_işlem_kur():
    conn=sqlite3.connect("./veritabanları/döviz_app.db")
    cursor =conn.cursor()
    selected_row = table3.focus()
    if selected_row:
        #seçili satırın kimlik değerini al
        tarih = table3.set(selected_row, "#1")
        # veritabanından silme işlemi
        cursor.execute("DELETE FROM KUR_HAREKETLERİ WHERE ALINAN_TARİH=? """, (tarih,))
        conn.commit()
        table3.delete(selected_row)
        conn.close()
        # seçili satırı silme işlemi
    # tabloya tıklama olayını bağlama
def update_tablo():
        kullanıcı_db = sqlite3.connect(f"./veritabanları/{true_username}.db")
        imleç = kullanıcı_db.cursor()
        table2.delete(*table2.get_children())
        imleç.execute(f"SELECT * FROM {değişim_tablo_adı}")
        rows = imleç.fetchall()
        for row in rows:
            table2.insert("", "end", values=row)
        kullanıcı_db.close()


def update_tablo2():
        
        conn = sqlite3.connect("./veritabanları/döviz_app.db")
        cursor = conn.cursor()
        table3.delete(*table3.get_children())
        cursor.execute("SELECT * FROM KUR_HAREKETLERİ")
        rows = cursor.fetchall()
        for row in rows:
            table3.insert("", "end", values=row)
        conn.close()

def kapat():
    new_table_frame.destroy()
    tabloyu_kapat.destroy()
    geri = Button(işlem_geçmiş_window, text="GERİ",font="Arial 11 bold",command=update_tablo)
    geri.place(x=800,y=300)

    kurları_göster = Button(işlem_geçmiş_window, text="BU TARİHLERDEKİ \n KURLAR",font="Arial 11 bold",command=bu_tarihlerdeki_kurlar)
    kurları_göster.place(x=800,y=400)
    
    toplam_varlık_grafiği =Button(işlem_geçmiş_window, text="Grafikte Göster",font="Arial 11 bold",command=değişim_hareketleri_grafik)
    toplam_varlık_grafiği.place(x=800,y=250)
def bu_tarihlerdeki_kurlar():
    global new_table_frame,tabloyu_kapat
    kullanıcı_db = sqlite3.connect(f"./veritabanları/{true_username}.db")
    imleç = kullanıcı_db.cursor()
    imleç.execute(f"SELECT * FROM {anlık_kur_tablosu}")
    new_table_frame = Frame(işlem_geçmiş_window)
    new_table_frame.pack(expand=True, fill="both")
    table4 = ttk.Treeview(new_table_frame, columns=("Tarih", "USD", "EUR", "GOLD"))
    table4.heading("Tarih", text="Tarih",anchor=CENTER)
    table4.heading("USD", text="USD",anchor=CENTER)
    table4.heading("EUR", text="EUR",anchor=CENTER)
    table4.heading("GOLD", text="GOLD",anchor=CENTER)
    table4.pack(expand=True, fill="both")
    table4.column("#0", width=0, stretch=False) 
    rows = imleç.fetchall()
    for row in rows:
        table4.insert("", "end", values=row)
    kullanıcı_db.close()     
    tabloyu_kapat =Button(işlem_geçmiş_window,text="Kapat",bg="white",font="Arial 11 bold",command=kapat) 
    tabloyu_kapat.place(x=600,y=300)
    geri.destroy()
    toplam_varlık_grafiği.destroy()
def geçmişi_görüntüle():
    global table2,cal_start,cal_end,table_frame,geri,toplam_varlık_grafiği,işlem_geçmiş_window
   
    
    
    işlem_geçmiş_window = Toplevel(window)
    işlem_geçmiş_window.title("İşlem Geçmişim")
    işlem_geçmiş_window.geometry("1000x550+500+150")
    işlem_geçmiş_window.configure(bg="lightgray")
   # işlem_geçmiş_window.resizable(False,False)
    table_frame = Frame(işlem_geçmiş_window)
    table_frame.pack(expand=False, fill="both")
    
    table2 = ttk.Treeview(table_frame, columns=("Tarih", "USD","EUR","GOLD","USD", "EUR", "GOLD", "TOPLAM"))
    table2.heading("Tarih", text="Tarih",anchor=CENTER)
    table2.heading("USD", text="USD_Miktar",anchor=CENTER)
    table2.heading("EUR", text="EUR_Miktar",anchor=CENTER)
    table2.heading("GOLD", text="GOLD_Miktar",anchor=CENTER)
    table2.heading("USD", text="USD",anchor=CENTER)
    table2.heading("EUR", text="EUR",anchor=CENTER)
    table2.heading("GOLD", text="GOLD",anchor=CENTER)
    table2.heading("TOPLAM", text="TOPLAM",anchor=CENTER)
    table2.pack(expand=True, fill="both")
    table2.column("#0", width=0, stretch=False)    # İlk sütun genişliği 0, esneklik kapalı
 
    conn = sqlite3.connect(f"./veritabanları/{true_username}.db")
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {değişim_tablo_adı}")
    veriler = cursor.fetchall()
    for veri in veriler:
        table2.insert("", "end", values=veri)
    conn.close() 
    # Takvim widget'ları
    cal_start = DateEntry(işlem_geçmiş_window, width=20, background='darkblue',
                        foreground='white', date_pattern='yyyy-mm-dd')
    cal_start.pack(pady=10)

    cal_end = DateEntry(işlem_geçmiş_window, width=20, background='darkblue',
                        foreground='white', date_pattern='yyyy-mm-dd')
    cal_end.pack(pady=10)

    # Kayıt arama düğmesi
    btn_search = Button(işlem_geçmiş_window, text="Ara",command=search_records1)
    btn_search.pack(pady=10)
    
    geri = Button(işlem_geçmiş_window, text="GERİ",font="Arial 11 bold",command=update_tablo)
    geri.place(x=800,y=300)

    kurları_göster = Button(işlem_geçmiş_window, text="BU TARİHLERDEKİ \n KURLAR",font="Arial 11 bold",command=bu_tarihlerdeki_kurlar)
    kurları_göster.place(x=800,y=400)
    
    toplam_varlık_grafiği =Button(işlem_geçmiş_window, text="Grafikte Göster",font="Arial 11 bold",command=değişim_hareketleri_grafik)
    toplam_varlık_grafiği.place(x=800,y=250)

    kapat_btn = Button(işlem_geçmiş_window, text="Kapat",bg="white",font="Arial 11 bold",command=lambda:[ işlem_geçmiş_window.destroy()]).place(x=800,y=350)
    table2.bind("<ButtonRelease-1>", satır_sec_işlem)

    
    def show_stık_menu(event):
        stıkMenu.post(event.x_root,event.y_root)

    stıkMenu =Menu(işlem_geçmiş_window,tearoff=0)
    stıkMenu.add_command(label="Sil",command=satır_sil_işlem_kayıt)
    #stıkMenu.add_command(label="Güncelle",command=update_tablo)


    # Sağ tıklama olayını bağlama
    table2.bind("<Button-3>", show_stık_menu)
    table2.bind("<Button-4>", show_stık_menu)
    table2.bind("<Button-5>", show_stık_menu)



def search_records1():
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()
    
    # Veritabanı bağlantısı
    conn = sqlite3.connect(f"./veritabanları/{true_username}.db")
    cursor = conn.cursor()
    
    # Tarih aralığına göre verileri getiren SQL sorgusu
    sorgu = f"SELECT * FROM {değişim_tablo_adı} WHERE ALINAN_TARİH BETWEEN ? AND ?"
    cursor.execute(sorgu, (start_date, end_date))
    rows = cursor.fetchall()
    table2.delete(*table2.get_children())
    for row in rows:
        table2.insert("", "end", values=row)
    # Tabloyu güncelle
    conn.close()
    
    # Bağlantının kapatılması

def search_records2():
    start_date = cal_start.get_date()
    end_date = cal_end.get_date()
    
    # Veritabanı bağlantısı
    conn = sqlite3.connect("./veritabanları/döviz_app.db")
    cursor = conn.cursor()
    
    # Tarih aralığına göre verileri getiren SQL sorgusu
    sorgu = f"SELECT * FROM KUR_HAREKETLERİ WHERE ALINAN_TARİH BETWEEN  ? AND ?"
    cursor.execute(sorgu, (start_date, end_date))
    rows = cursor.fetchall()
    table3.delete(*table3.get_children())
    for row in rows:
        table3.insert("", "end", values=row)
    # Tabloyu güncelle
    conn.close()

def geçmiş_kur_hareketleri():

 
    global table3, cal_start, cal_end,stıkMenu
    kur_geçmiş_window = Toplevel(window)
    kur_geçmiş_window.title("Kur Geçmişi")
    kur_geçmiş_window.geometry("1000x400+500+350")
    kur_geçmiş_window.configure(bg="lightgray")
    kur_geçmiş_window.resizable(False, False)
    table_frame = Frame(kur_geçmiş_window)
    table_frame.pack(expand=False, fill="both")
    
    table3 = ttk.Treeview(table_frame, columns=("Tarih", "USD", "EUR", "GOLD"))
    table3.heading("Tarih", text="Tarih",anchor=CENTER)
    table3.heading("USD", text="USD",anchor=CENTER)
    table3.heading("EUR", text="EUR",anchor=CENTER)
    table3.heading("GOLD", text="GOLD",anchor=CENTER)
    table3.pack(expand=True, fill="both")
    table3.column("#0", width=0, stretch=False)    # İlk sütun genişliği 0, esneklik kapalı
    
    conn = sqlite3.connect("./veritabanları/döviz_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KUR_HAREKETLERİ")
    veriler = cursor.fetchall()
    for veri in veriler:
        table3.insert("", "end", values=veri)
        
    # Takvim widget'ları
    cal_start = DateEntry(kur_geçmiş_window, width=12, background='darkblue',
                        foreground='white', date_pattern='yyyy-mm-dd')
    cal_start.pack(pady=10)

    cal_end = DateEntry(kur_geçmiş_window, width=12, background='darkblue',
                        foreground='white', date_pattern='yyyy-mm-dd')
    cal_end.pack(pady=10)

    # Kayıt arama düğmesi
    btn_search = Button(kur_geçmiş_window, text="Ara",command=search_records2)
    btn_search.pack(pady=10)
    geri = Button(kur_geçmiş_window, text="GERİ",font="Arial 11 bold",command=update_tablo2)
    geri.place(x=800,y=350)
    grafikler = Button(kur_geçmiş_window, text="GRAFİK",font="Arial 11 bold",command=kur_soru_sor)
    grafikler.place(x=800,y=300)

    table3.bind("<ButtonRelease-1>", satır_sec_kur)
    stıkMenu =Menu(kur_geçmiş_window,tearoff=0)
    stıkMenu.add_command(label="Sil",command=satır_sil_işlem_kur)
    stıkMenu.add_command(label="Güncelle",command=update_tablo2)

    
    def show_stık_menu(event):
        
        stıkMenu.post(event.x_root,event.y_root)


    # Sağ tıklama olayını bağlama
    table3.bind("<Button-3>", show_stık_menu)
    table3.bind("<Button-4>", show_stık_menu)
    table3.bind("<Button-5>", show_stık_menu)




def mevcut_döviz_kurları():

    conn=sqlite3.connect("./veritabanları/döviz_app.db")
    cursor =conn.cursor()
    geri = Button(window, text="GERİ",font="Arial 11 bold",command=lambda: [geri.destroy(),table_frame1.destroy()])
    geri.place(x=600,y=260)
    table_frame1 = Frame(window)
    table_frame1.pack(expand=False, fill="both")
    table1 = ttk.Treeview(table_frame1, columns=("Usd", "Eur","Gold"), show="headings")
    table1.heading("Usd", text="USD",anchor="center")
    table1.heading("Eur", text="EUR",anchor="center")
    table1.heading("Gold", text="GOLD",anchor="center")
    dolar_kur_çekme()
    euro_kur_çekme()
    altın_kur_çekme()
    cursor.execute("INSERT INTO KUR_HAREKETLERİ VALUES(?,?, ?, ?)", (datetime.now(),dolar_tl_karşılığı, euro_tl_karşılığı, gr_satış_fiyatı))
    conn.commit()
    conn.close()
    table1.insert("", "end", values=(dolar_tl_karşılığı, euro_tl_karşılığı, gr_satış_fiyatı))
    table1.pack(expand=True, fill="both")
  

def kur_soru_sor():
    soru_pencere = Tk()
    soru_pencere.title("Soru")
    soru_pencere.geometry("450x300+500+350")
    soru_pencere.configure(bg="black")
    label = Label(soru_pencere,font="Arial 11 bold",fg="white",bg="black",text="hangi dövizin geçmiş hareketlerini görmek istiyorsunuz?")
    label.pack()
    def soru_sor():
            soru_pencere.destroy()

    usd_button = Button(soru_pencere,width=30 ,text="USD",command=lambda:[soru_sor(),kur_hareketleri_grafik_USD()])
    usd_button.pack(pady=10)
    eur_button = Button(soru_pencere, width=30,text="EUR",command=lambda:[soru_sor(),kur_hareketleri_grafik_EUR()])
    eur_button.pack(pady=10)
    gr_button = Button(soru_pencere,width=30 ,text="GOLD(gr satış)",command=lambda:[soru_sor(),kur_hareketleri_grafik_GOLD()])
    gr_button.pack(pady=10)
    soru_pencere.mainloop()

  
döviz_bozdurma_btn =Button(window, text="Döviz Bozdurma & Alma",font="Arial 11 bold",command=döviz_bozdurma)
döviz_bozdurma_btn.place(x=270,y=360)
"""
geçmişi_görüntüle_btn =Button(window, text="Geçmiş",font="Arial 11 bold",command=geçmişi_görüntüle)
geçmişi_görüntüle_btn.place(x=450,y=400)
"""
mevcut_döviz_kurları_btn =Button(window, text="Mevcut Döviz Kurları",font="Arial 11 bold",command=mevcut_döviz_kurları)
mevcut_döviz_kurları_btn.place(x=250,y=400)

çıkış_btn =Button(window, text="Çıkış",font="Arial 11 bold",command=window.destroy)
çıkış_btn.place(x=300,y=440)

# geçmiş menüsü oluştur
menubar = Menu(window)
window.config(menu=menubar)
menubar.configure(background="lightgray")
geçmiş_menu = Menu(menubar, tearoff=0)
menubar.add_cascade(label="Geçmiş", menu=geçmiş_menu)
geçmiş_menu.add_command(label="İşlem Geçmişim",command=geçmişi_görüntüle)
geçmiş_menu.add_command(label="Kur  Geçmişi",command=geçmiş_kur_hareketleri)
geçmiş_menu.add_separator()

## kar-zarar hesaplama ksımı

def kar_zarar_hesaplama1():
    seçilen_tarih = start_date
    kullanıcı_db = f"./veritabanları/{true_username}.db"
    conn = sqlite3.connect(kullanıcı_db)
    cursor = conn.cursor()
    cursor.execute(f"SELECT * FROM {anlık_kur_tablosu} WHERE ALINAN_TARİH < '{seçilen_tarih}'ORDER BY ALINAN_TARİH DESC LIMIT 1")
    son_satır1 = cursor.fetchone() 
    if son_satır1 is not None:
        usd_tl_karşılığı = son_satır1[1]

    elif  son_satır1 is not None:
        eur_tl_karşılığı = son_satır1[2]
    elif  son_satır1 is not None:    
        gr_tl_karşılığı = son_satır1[3]
    else:messagebox.showerror("Error", "Bir Sorun Çıktı")
    # sql_tl = f"SELECT * FROM {değişim_tablo_adı} WHERE ALINAN_TARİH < '{seçilen_tarih}'ORDER BY ALINAN_TARİH DESC LIMIT 1"
    sql_tl = f"SELECT * FROM {değişim_tablo_adı} WHERE ALINAN_TARİH ={seçilen_tarih} "
    cursor.execute(sql_tl)
    
    # Güncel TL varlıklarını hesaplamak için değişkenleri başlatın
    toplam_tl = 0
    son_satır2 = cursor.fetchone()
    # Filtrelenen güncellemeleri döngüyle gezin ve TL varlıklarını toplayın
    if son_satır2 is not None:

        toplam_tl = son_satır2[7]  # MEVCUT_TOPLAM_TL sütunu
    else:messagebox.showerror("Error", "Bir Sorun Çıktı")
    sql_miktar =f"SELECT * FROM {değişim_tablo_adı} WHERE ALINAN_TARİH < '{seçilen_tarih} ' ORDER BY ALINAN_TARİH DESC LIMIT 1"
    cursor.execute(sql_miktar)
    data_miktar = cursor.fetchone()
    usd_miktarı = data_miktar[1]
    eur_miktarı = data_miktar[2]
    gold_miktarı = data_miktar[3]

    
    # Önceki tarihe kadar olan güncellemeleri filtrelemek için SQL sorgusu oluşturun
    sql_döviz =f"SELECT * FROM {döviz_varlığı_tablosu} WHERE ALINAN_TARİH < '{seçilen_tarih}'"
    cursor.execute(sql_döviz)
    usd_dvz =0
    eur_dvz =0
    gold_dvz =0
    rows=cursor.fetchall()
    for row in rows:
        usd_dvz += row[1]
        eur_dvz += row[2]
        gold_dvz += row[3]

    usd_kar = (usd_miktarı*usd_tl_karşılığı)-toplam_tl
    usd_zarar = (toplam_tl)-(usd_miktarı*usd_tl_karşılığı)

    eur_kar = (eur_miktarı*eur_tl_karşılığı)-toplam_tl
    eur_zarar = (toplam_tl)-(eur_miktarı*eur_tl_karşılığı)

    gold_kar = (gold_miktarı*gr_tl_karşılığı)-toplam_tl
    gold_zarar = (toplam_tl)-(gold_miktarı*gr_tl_karşılığı)


    if usd_miktarı>=0:
        messagebox.showinfo("Kar", "Dolar Karı: "+str(usd_kar))
    else:messagebox.showinfo("Zarar", "Dolar Zararı: "+str(usd_zarar))

    if eur_miktarı>=0:
        messagebox.showinfo("Kar", "Euro Karı: "+str(eur_kar))
    else:messagebox.showinfo("Zarar", "Euro Zararı: "+str(eur_zarar))

    if gold_miktarı>=0:
        messagebox.showinfo("Kar", "Gold Karı: "+str(gold_kar))
    else:messagebox.showinfo("Zarar", "Gold Zararı: "+str(gold_zarar))

# Veritabanı bağlantısını kapatın
    conn.close()




def kar_zarar_screen():
    global start_date,end_date
    


    kar_zarar_window = Toplevel(window)
    kar_zarar_window.title("Kar-Zarar Hesaplama")
    kar_zarar_window.geometry("450x300+500+350")
    kar_zarar_window.configure(bg="darkblue")
    # Takvim widget'ları
    cal_start = DateEntry(kar_zarar_window, width=12, background='black',
                        foreground='white', date_pattern='yyyy-mm-dd')

    #cal_end = DateEntry(kar_zarar_window, width=12, background='black',
    #                    foreground='white', date_pattern='yyyy-mm-dd')
    start_date = cal_start.get()
    #end_date = cal_end.get()
    Label(kar_zarar_window, text="Kar-Zarar hesabı yapmak istediğiniz tarihi seçin",font="Arial 13 bold", bg="darkblue", fg="white").pack(pady=10)
    cal_start.pack(pady=10)
    #Label(kar_zarar_window, text="Bitiş Tarih", bg="darkblue", fg="white").pack(pady=10)
    #cal_end.pack(pady=10)

    btn_hesapla = Button(kar_zarar_window, text="Hesapla",command=kar_zarar_hesaplama1)
    btn_hesapla.pack(pady=10)

    



btn_kar_zarar = Button(window, text="Kar-Zarar Hesaplama",font="Arial 11 bold",command=kar_zarar_screen).place(x=250,y=320)






window.mainloop()