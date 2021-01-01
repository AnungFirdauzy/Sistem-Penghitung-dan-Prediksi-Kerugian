import sqlite3
from getpass import getpass

connection = sqlite3.connect("C:/sqlite/cashier.db")


class Login:
    def __init__(self, raw_username, raw_password):
        self._raw_username = raw_username
        self.__raw_password = raw_password
        self.akses = 0

    def cekAkun(self):
        for akun in connection.execute("select * from akun"):
            if akun[0] == self._raw_username:
                if akun[1] == self.__raw_password:
                    self.akses = 1
                    break
                else:
                    print("password salah")

        if self.akses == 0:
            print("Akun tidak dikenal")

    def getAkses(self):
        return self.akses


class Barang:
    def __init__(self, barcode, nama_barang, stok, harga_jual, harga_beli, tanggal_pembayaran):
        self.barcode = barcode
        self.nama_barang = nama_barang
        self.stok = stok
        self.harga_jual = harga_jual
        self.harga_beli = harga_beli
        self.tanggal_pembayaran = tanggal_pembayaran

    def getNama(self):
        return self.nama_barang

    def getBarcode(self):
        return self.barcode

    def getStok(self):
        return self.stok

    def getHargaBeli(self):
        return self.harga_beli

    def getHargaJual(self):
        return self.harga_jual

    def getTanggal(self):
        return self.tanggal_pembayaran


class kelolaBarang(Barang):
    def __init__(self, barcode, nama_barang, stok, harga_jual, harga_beli, tanggal_pembayaran):
        super().__init__(barcode, nama_barang, stok,
                         harga_jual, harga_beli, tanggal_pembayaran)

    def tambahdata(self):
        connection.execute(
            f"insert into barang (barcode,nama_barang,stok,harga_jual,harga_beli,tanggal_pembayaran) values('{self.barcode}','{self.nama_barang}','{self.stok}','{self.harga_jual}','{self.harga_beli}','{self.tanggal_pembayaran}')")
        connection.commit()

    @staticmethod
    def LihatDataByBarcode(Barcode):
        for data in connection.execute(f"select * from barang where barcode='{Barcode}'"):
            data_barcode = data[0]
            data_nama = data[1]
            data_stok = data[2]
            data_HgJual = data[3]
            data_HgBeli = data[4]
            data_TglPembayaran = data[5]

        print(f"""
        
        code Barcode = {data_barcode}
        Nama Barang = {data_nama}
        Banyak Stok = {data_stok}
        Harga Jual = {data_HgJual}
        Harga Beli = {data_HgBeli}
        Tanggal Pembayaran = {data_TglPembayaran}

        """)

    @staticmethod
    def LihatSemuaBarang():
        print("Format : Barcode, Nama, stok, Harga jual, Harga Beli, Taggal Pembayaran")
        for data in connection.execute(f"select * from barang"):
            print(data)

    @staticmethod
    def updateStok(Barcode, stok_baru):
        for data in connection.execute(f"select stok from barang where barcode = '{Barcode}'"):
            in_stok = data[0]

        total_stok = in_stok + int(stok_baru)
        connection.execute(
            f"UPDATE BARANG SET stok={total_stok} where barcode = '{Barcode}'")
        connection.commit()
        for data in connection.execute(f"select stok from barang where barcode = '{Barcode}'"):
            print(data)


class Transaksi:

    @staticmethod
    def lihattransaksi(id_pesanan):
        for data in connection.execute(f"select * from detail_pesanan where id_pesanan = '{id_pesanan}'"):
            print(data)

    @staticmethod
    def TampilkanRiwayatTransaksi(id_pesanan):
        print("id_pesanan | tanggal | kasir | Barcode | Nama Barang | Jumlah | Subtotal")
        for data in connection.execute(f"select detail_pesanan.id_pesanan,pesanan.tanggal,akun.nama as kasir,detail_pesanan.barcode,barang.nama_barang,detail_pesanan.qty,detail_pesanan.sub_total from detail_pesanan inner join pesanan on pesanan.id_pesanan=detail_pesanan.id_pesanan inner join barang on detaiL_pesanan.barcode = barang.barcode inner join akun on akun.username=pesanan.username where detail_pesanan.id_pesanan = {id_pesanan}"):
            print(data)
        for data in connection.execute(f"select sum(sub_total) from detail_pesanan where id_pesanan={id_pesanan}"):
            total = data[0]
        for data in connection.execute(f"select pembayaran,kembalian from pesanan where id_pesanan ={id_pesanan}"):
            pembayaran = data[0]
            kembalian = data[1]
        print("Total : ", total)
        print("Pembayaran : ", pembayaran)
        print("Kembalian : ", kembalian)

    @staticmethod
    def submittransaksi(id_pesanan):
        for data in connection.execute(f"select max(id_pesanan) from pesanan"):
            id_pesanan = data[0]
        for data in connection.execute(f"select sum(sub_total) as total from detail_pesanan where id_pesanan = {id_pesanan}"):
            total = data[0]
        print(f"Total Biaya = {total}")
        pembayaran = int(input("uang tunai : "))
        kembalian = pembayaran - total
        print("kembalian = {}".format(kembalian))
        connection.execute(
            f"UPDATE pesanan set pembayaran = {pembayaran}, kembalian={kembalian} where id_pesanan={id_pesanan}")
        connection.commit()

    @staticmethod
    def tambahTransksi(barcode, qty):
        for data in connection.execute(f"select max(id_pesanan) from pesanan"):
            id_pesanan = data[0]
        for data in connection.execute(f"select harga_jual from barang where barcode='{barcode}'"):
            harga = data[0]
            print("harga ", harga)
        for data in connection.execute(f"select harga_jual * {qty} as subtotal from barang where barcode ='{barcode}'"):
            subtotal = data[0]
        for data in connection.execute(f"select stok from barang where barcode='{barcode}'"):
            stokSementara = data[0]
        if stokSementara <= 0:
            print("stok Habis")
        else:
            connection.execute(
                f"insert into detail_pesanan (id_pesanan,barcode,qty,sub_total) values ('{id_pesanan}', '{barcode}','{qty}','{subtotal}')")
            connection.commit()
            Transaksi.lihattransaksi(id_pesanan)

    @staticmethod
    def buatTransaksi(username):
        connection.execute(
            f"insert into pesanan(username,tanggal,pembayaran,kembalian) values ('{username}',datetime('now'),0,0)")
        connection.commit()


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
            2. Kelola Data Barang
            3. Lihat Riwayat Transaksi
            4. Logout

            """.format(nama))
            pilihan = input("Input Pilihan : ")

            if pilihan == "1":
                while True:
                    Transaksi.buatTransaksi(raw_username)
                    while True:
                        print("___ ketik 'submit' untuk meyimpan ___")
                        BarcodeBarang = input("Input Barcode Barang : ")
                        qty = input("Jumlah : ")
                        if BarcodeBarang == "submit":
                            break
                        else:
                            Transaksi.tambahTransksi(BarcodeBarang, qty)
                    for data in connection.execute("select max(id_pesanan) as id_pesanan from detail_pesanan"):
                        id_pesanan = data[0]
                    Transaksi.submittransaksi(id_pesanan)
                    Transaksi.TampilkanRiwayatTransaksi(id_pesanan)
                    pilihan2 = input("Tambah Transaksi (y/n) ? ")
                    if pilihan2 == "n":
                        break

            elif pilihan == "2":
                while True:
                    print("""

                    ___ Kelola Data Barang ___

                    1. Lihat data Barang
                    2. Tambah data Barang
                    3. Tambah stok barang
                    4. Kembali
                    
                    """)
                    pilihan = input("masukkan Pilihan : ")
                    if pilihan == "1":
                        print("""
                        
                        Untuk Menampilkan semua data inputkan '1'
                        
                        """)
                        barcode = input("barcode : ")
                        if barcode == "1":
                            kelolaBarang.LihatSemuaBarang()
                        else:
                            kelolaBarang.LihatDataByBarcode(barcode)

                    elif pilihan == "2":
                        in_barcode = input(" Barcode : ")
                        in_nama_barang = input("Nama Barang : ")
                        in_stok = input("Banyak Stok : ")
                        in_HgJual = input("Harga Jual : ")
                        in_HgBeli = input("Harga Beli : ")
                        in_TglBayar = input("Tanggal Pembayaran : ")
                        Tambah = kelolaBarang(
                            in_barcode, in_nama_barang, in_stok, in_HgJual, in_HgBeli, in_TglBayar)
                        Tambah.tambahdata()
                        kelolaBarang.LihatSemuaBarang()

                    elif pilihan == "3":
                        Barcode = input("Barcode : ")
                        kelolaBarang.LihatDataByBarcode(Barcode)
                        stok = input("Stok : ")
                        kelolaBarang.updateStok(Barcode, stok)
                        kelolaBarang.LihatDataByBarcode(Barcode)

                    elif pilihan == "4":
                        break

            elif pilihan == "3":
                id_pesanan = int(input("Id Pesanan : "))
                Transaksi.TampilkanRiwayatTransaksi(id_pesanan)
            elif pilihan == "4":
                break
