import sqlite3
from getpass import getpass

connection = sqlite3.connect("C:/sqlite/kasir_edit.db")


class Login:
    def __init__(self, raw_username, raw_password):
        self._raw_username = raw_username
        self._raw_password = raw_password
        self.akses = 0
        self.role = None

    def cekAkun(self):
        for akun in connection.execute("select * from akun"):
            if akun[0] == self._raw_username:
                if akun[1] == self._raw_password:
                    self.akses = 1
                    self.role = akun[3]
                    break
                else:
                    print("password salah")

        if self.akses == 0:
            print("Akun tidak dikenal")

    def getAkses(self):
        return self.akses

    def getRole(self):
        return self.role

    def getUsername(self):
        return self._raw_username


class kelolaAkun(Login):
    def __init__(self, raw_username, raw_password, nama, role):
        super().__init__(raw_username, raw_password)
        self.nama = nama
        self.role = role

    def TambahAkun(self):
        connection.execute(
            f'insert into akun(username,password,nama,role,tgl_pembuatan)  values ("{self._raw_username}","{self._raw_username}","{self.nama}",{self.role},datetime("now"))')
        kelolaAkun.ListAkun()
        connection.commit()

    @staticmethod
    def GantiPassword(raw_username, raw_password):
        connection.execute(
            f'update akun set password = "{raw_username}" where username = "{raw_username}"')
        print("___ selesai ___ ")
        connection.commit()

    @staticmethod
    def GantiRole(raw_username, new_role):
        connection.execute(
            f"update akun set role = {new_role} where username ='{raw_username}'")
        print("___ Selesai ___")
        connection.commit()

    @staticmethod
    def ListAkun():
        print("""Username   |   Nama   |   role   |   tgl_pembuatan  |""")
        for akun in connection.execute("select akun.username, akun.nama, role_table.role_name as Role,akun.tgl_pembuatan  from akun inner join role_table on role_table.role_id = akun.role order by tgl_pembuatan desc"):
            print(
                f"""{akun[0]}   |   {akun[1]}   |   {akun[2]}   |   {akun[3]}   |""")


class Barang:
    def __init__(self, barcode, nama_barang, stok, harga_jual, harga_beli, tanggal_pembayaran, tanggal_kadaluarsa):
        self.barcode = barcode
        self.nama_barang = nama_barang
        self.stok = stok
        self.harga_jual = harga_jual
        self.harga_beli = harga_beli
        self.tanggal_pembayaran = tanggal_pembayaran
        self.tanggal_kadaluarsa = tanggal_kadaluarsa

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
    def __init__(self, barcode, nama_barang, stok, harga_jual, harga_beli, tanggal_pembayaran, tanggal_kadaluarsa):
        super().__init__(barcode, nama_barang, stok,
                         harga_jual, harga_beli, tanggal_pembayaran, tanggal_kadaluarsa)

    def tambahdata(self):
        connection.execute(
            f"insert into barang (barcode,nama_barang,stok,harga_jual,harga_beli,tanggal_pembayaran,tanggal_kadaluarsa) values('{self.barcode}','{self.nama_barang}','{self.stok}','{self.harga_jual}','{self.harga_beli}','{self.tanggal_pembayaran}','{self.tanggal_kadaluarsa}')")
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


class Transaksi:

    @staticmethod
    def lihattransaksi(id_pesanan):
        print("""
            BARCODE  |  NAMA BARANG  |  QTY  |  SUBTOTAL""")
        for data in connection.execute(f"select detail_pesanan.barcode, barang.nama_barang, detail_pesanan.qty, detail_pesanan.sub_total  from detail_pesanan inner join barang on barang.barcode=detail_pesanan.barcode where id_pesanan = '{id_pesanan}'"):
            barcode = data[0]
            nama = data[1]
            qty = data[2]
            subttl = data[3]
            print(f"""
            {barcode}  |  {nama}  |  {qty}  |  {subttl}
            """)

    @staticmethod
    def lihatsemuatransaksi():
        for data in connection.execute(f"select detail_pesanan.id_pesanan,pesanan.tanggal,akun.nama as kasir,detail_pesanan.barcode,barang.nama_barang,detail_pesanan.qty,detail_pesanan.sub_total from detail_pesanan inner join pesanan on pesanan.id_pesanan=detail_pesanan.id_pesanan inner join barang on detaiL_pesanan.barcode = barang.barcode inner join akun on akun.username=pesanan.username order by tanggal desc"):
            print(data)

    @staticmethod
    def TampilkanRiwayatTransaksi(id_pesanan):
        print("""
        BARCODE | NAMA BARANG | JUMLAH | SUBTOTAL""")
        for data in connection.execute(f"select detail_pesanan.id_pesanan,pesanan.tanggal,akun.nama as kasir,detail_pesanan.barcode,barang.nama_barang,detail_pesanan.qty,detail_pesanan.sub_total from detail_pesanan inner join pesanan on pesanan.id_pesanan=detail_pesanan.id_pesanan inner join barang on detaiL_pesanan.barcode = barang.barcode inner join akun on akun.username=pesanan.username where detail_pesanan.id_pesanan = {id_pesanan}"):
            idPesanan = data[0]
            tgl = data[1]
            kasir = data[2]
            barcode = data[3]
            barang = data[4]
            jml = data[5]
            sbttl = data[6]
            print(f"""
        {barcode} | {barang} | {jml} | {sbttl}""")
        for data in connection.execute(f"select sum(sub_total) from detail_pesanan where id_pesanan={id_pesanan}"):
            total = data[0]
        for data in connection.execute(f"select pembayaran,kembalian from pesanan where id_pesanan ={id_pesanan}"):
            pembayaran = data[0]
            kembalian = data[1]
        print(f"""
        Id Pesanan          : {idPesanan}
        Tanggal Transaksi   : {tgl}
        Kasir               : {kasir}
        Total               : {total}
        Pembayaran          : {pembayaran}
        Kembalian           " {kembalian}
        """)
        # print("Tanggal Transaksi : ", tgl)
        # print("Kasir : ", kasir)
        # print("Total : ", total)
        # print("Pembayaran : ", pembayaran)
        # print("Kembalian : ", kembalian)

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
            if int(qty) > stokSementara:
                qty = stokSementara
            stokBaru = stokSementara-qty
            connection.execute(
                f"update barang set stok={stokBaru} where barcode='{barcode}'")
            connection.execute(
                f"insert into detail_pesanan (id_pesanan,barcode,qty,sub_total) values ('{id_pesanan}', '{barcode}','{qty}','{subtotal}')")
            connection.commit()
            Transaksi.lihattransaksi(id_pesanan)

    @staticmethod
    def buatTransaksi(username):
        connection.execute(
            f"insert into pesanan(username,tanggal,pembayaran,kembalian) values ('{username}',datetime('now'),0,0)")
        connection.commit()

    @staticmethod
    def getrugi(tgl_input):
        for data in connection.execute(f"select * from barang where tanggal_pembayaran between  date('now') and '{tgl_input}'"):
            kerugian = data[2]*data[4]
            print(f"""
            Barcode : {data[0]} | Produk : {data[1]} | Stok : {data[2]} | Harga Jual : {data[3]} | Harga Beli : {data[4]} | Tanggal Pembayaran : {data[5]} | Perkiraan Kerugian : {kerugian}""")

    @staticmethod
    def getMean(barcode):
        qty = 0
        Banyak_Transaksi = 0
        for data in connection.execute(f"select detail_pesanan.barcode, detail_pesanan.qty, pesanan.tanggal from detail_pesanan inner join pesanan on pesanan.id_pesanan = detail_pesanan.id_pesanan where barcode = '{barcode}' and tanggal >= date('now') "):
            qty = qty + data[1]
            Banyak_Transaksi += 1
        print(f"""
        Total Terjual {qty} 
        Rata- Rata Pejualan {qty/Banyak_Transaksi} dari {Banyak_Transaksi} Transaksi
        """)

    @staticmethod
    def getBarangTerjual():
        for data in connection.execute("select detail_pesanan.barcode, count(barcode) as jumlah, pesanan.tanggal from detail_pesanan inner join pesanan on pesanan.id_pesanan=detail_pesanan.id_pesanan where pesanan.tanggal >= date('now') group by barcode order by jumlah asc;"):
            print(f"""
            Barcode : {data[0]}  |  Jumlah : {data[1]} | 
            """)
        for data in connection.execute("select detail_pesanan.barcode, count(barcode) as jumlah, pesanan.tanggal from detail_pesanan inner join pesanan on pesanan.id_pesanan=detail_pesanan.id_pesanan where pesanan.tanggal >= date('now') group by barcode order by jumlah desc;"):
            barcode_max = data[0]
            jumlah_max = data[1]
            break
        for data in connection.execute(f"select nama_barang from barang where barcode = '{barcode_max}'"):
            nama_barang = data[0]
        print(f"""
            Barang Paling Laku : {nama_barang}
            Barcode : {barcode_max}
            dengan Jumlah terjual : {jumlah_max}""")


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
            if user.getRole() == 1:
                print("""

                ___ Admin Mode ___

                1. Tambah Akun
                2. Ganti Password
                3. Ganti Role
                4. List Akun
                5. Logout

                """)
                pilihan = input("Input Pilihan : ")
                if pilihan == "5":
                    break
                elif pilihan == "1":
                    nama = input("Nama Pengguna : ")
                    raw_username = input("Username : ")
                    raw_password = input("Password : ")
                    confirm_pass = input("Konfirmasi Password : ")
                    print("""
                    ___ List Role : ___

                    1. Admin
                    2. Kasir
                    3. Supervisor

                    """)
                    role = int(input("Nomor Role : "))
                    if confirm_pass == raw_password:
                        new_akun = kelolaAkun(
                            raw_username, raw_password, nama, role)
                        new_akun.TambahAkun()
                    else:
                        print("Konfirmasi Password dan Password Harus Sama !!!")
                elif pilihan == "2":
                    raw_username = input("Cari Username : ")
                    raw_password = input("Password Baru :")
                    confirm_pass = input("Konfirmasi Password Baru : ")
                    if confirm_pass == raw_password:
                        kelolaAkun.GantiPassword(raw_username, raw_password)
                    else:
                        print("Konfirmasi Password dan Password Harus Sama !!!")

                elif pilihan == "3":
                    raw_username = input("Cari Username : ")
                    print("""
                    ___ List Role : ___

                    1. Admin
                    2. Kasir
                    3. Supervisor

                    """)
                    new_role = int(input(" Masukkan Role Baru :"))
                    kelolaAkun.GantiRole(raw_username, new_role)

                elif pilihan == "4":
                    kelolaAkun.ListAkun()

            if user.getRole() == 2:
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
                            if BarcodeBarang == "submit":
                                break
                            else:
                                qty = int(input("Jumlah :"))
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
                            print("""
                            Tipe :
                            1. Makanan
                            2. Barang
                            """)
                            tipe = input("Input tipe :")
                            if tipe == "1":
                                tgl_exp = input("Tanggal Kadluarsa : ")
                            elif tipe == "2":
                                tgl_exp = None
                            Tambah = kelolaBarang(
                                in_barcode, in_nama_barang, in_stok, in_HgJual, in_HgBeli, in_TglBayar, tgl_exp)
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

            if user.getRole() == 3:
                for akun in connection.execute("select nama from akun where username = '{}'".format(raw_username)):
                    nama = akun[0]
                print("""
                ----- Selamat Datang {} -----
                1. Lihat Transaksi
                2. Lihat Barang
                3. Rata-Rata Penjualan Barang Hari ini
                4. Barang Paling Laku Hari ini
                5. Cek Kerugian
                6. Logout
                """.format(nama))
                pilihan = input("Input Pilihan : ")
                if pilihan == "6":
                    break

                elif pilihan == "1":
                    print("""
                    _____ Isi "*" apabila ingin menampilkan semua _____
                    """)
                    id_pesanan = input("input ID Pesanan : ")
                    if id_pesanan == "*":
                        Transaksi.lihatsemuatransaksi()
                    else:
                        Transaksi.TampilkanRiwayatTransaksi(id_pesanan)

                elif pilihan == "2":
                    kelolaBarang.LihatSemuaBarang()

                elif pilihan == "3":
                    barcode = input("Barcode : ")
                    Transaksi.getMean(barcode)

                elif pilihan == "5":
                    print("___ Prediksi Kerugian Yang Akan Datang ___")
                    tgl_input = input('Tanggal (YYYY-MM-DD) : ')
                    Transaksi.getrugi(tgl_input)

                elif pilihan == "4":
                    Transaksi.getBarangTerjual()
