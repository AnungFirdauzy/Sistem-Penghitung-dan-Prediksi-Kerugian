import sqlite3
from getpass import getpass

connection = sqlite3.connect("C:/sqlite/TestKasir.db")


class Login:
    def __init__(self, raw_username, raw_password):
        self.raw_username = raw_username
        self.raw_password = raw_password
        self.akses = 0

    def cekAkun(self):
        for akun in connection.execute("select * from akun"):
            if akun[0] == self.raw_username:
                if akun[1] == self.raw_password:
                    self.akses = 1
                    break
                else:
                    print("password salah")

        if self.akses == 0:
            print("Akun tidak dikenal")

    def getAkses(self):
        return self.akses


while True:
    print("""

    _____ Login _____
    
    """)
    raw_username = str(input(" Username : "))
    raw_password = getpass("Password : (Disembunyikan) ")
    user = Login(raw_username, raw_password)
    user.cekAkun()
    while True:
        if user.getAkses() == 1:
            for akun in connection.execute("select nama from akun where username = '{}'".format(raw_username)):
                nama = akun[0]
            print("""

            ----- Selamat Datang {} -----

            1. Input Transaksi
            2. Lihat Data Barang
            3. Lihat Riwayat Transaksi
            4. Logout

            """.format(nama))
            pilihan = input("Input Pilihan : ")
            if pilihan == "1":
                print("input transaksi")
            elif pilihan == "2":
                print("lihat data barang")
            elif pilihan == "3":
                print("lihat riwayat transaksi")
            elif pilihan == "4":
                break
