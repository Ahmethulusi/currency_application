import matplotlib.pyplot as plt
import sqlite3

def get_last_login():
    global true_username
    conn =sqlite3.connect("./veritabanları/Users.db")
    cursor=conn.cursor()
    cursor.execute("SELECT true_username FROM last_logins ORDER BY rowid DESC LIMIT 1")
    last_login=cursor.fetchone()
    true_username=last_login[0]
get_last_login()

değişim_tablo_adı =f"{true_username}_değişim_kayıtları"

def değişim_hareketleri_grafik():
    global true_username
    x = []
    y = []
    conn = sqlite3.connect(f"./veritabanları/{true_username}.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM  {0}".format(değişim_tablo_adı))
    rows=cursor.fetchall()
    for row in rows:
        toplam_varlığım=row[4]
        tarih=row[0]
        tarih=tarih[0:10]
        x.append(toplam_varlığım)
        y.append(tarih)
    conn.close()
    plt.plot(x, y)
    plt.title("Toplam Varlık Değişimi")
    plt.xlabel("toplam varlığım (TL)")
    plt.show()





def kur_hareketleri_grafik_USD():
    x = []
    y = []
    conn = sqlite3.connect("./veritabanları/döviz_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KUR_HAREKETLERİ") 
    rows=cursor.fetchall()
    for row in rows:
        usd = row[1]
        tarih=row[0]
        tarih=tarih[0:10]
        x.append(tarih)
        y.append(usd)
    conn.close()
    plt.plot(x, y)
    plt.title("USD")
    plt.xlabel("tarih")
    plt.ylabel("USD(TL)")
    plt.show()


def kur_hareketleri_grafik_EUR():
    x = []
    y = []
    conn = sqlite3.connect("./veritabanları/döviz_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KUR_HAREKETLERİ") 
    rows=cursor.fetchall()
    for row in rows:
        eur = row[2]
        tarih=row[0]
        tarih=tarih[0:10]
        x.append(tarih)
        y.append(eur)
    conn.close()
    plt.plot(x, y)
    plt.title("EUR")
    plt.xlabel("tarih")
    plt.ylabel("EUR(TL)")
    plt.show()



def kur_hareketleri_grafik_GOLD():
    x = []
    y = []
    conn = sqlite3.connect("./veritabanları/döviz_app.db")
    cursor = conn.cursor()
    cursor.execute("SELECT * FROM KUR_HAREKETLERİ") 
    rows=cursor.fetchall()
    for row in rows:
        gold = row[3]
        tarih=row[0]
        tarih=tarih[0:10]
        x.append(tarih)
        y.append(gold)
    conn.close()
    plt.plot(x, y)
    plt.title("GOLD")
    plt.xlabel("tarih")
    plt.ylabel("GOLD(gr (tl) satış fiyatı)")
    plt.show()


