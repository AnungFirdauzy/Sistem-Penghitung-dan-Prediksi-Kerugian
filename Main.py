import sqlite3
from getpass import getpass

connection = sqlite3.connect("C:/sqlite/testPegawai.db")


class Login:
    def __init__(self, raw_username, raw_password):
        self.raw_username = raw_username
        self.raw_password = raw_password
        self.userID = None
        self.role = None

    def cekAkun(self):
        for akun in connection.execute("select * from akun"):
            if akun[0] == self.raw_username:
                if akun[1] == self.raw_password:
                    self.userID = akun[2]
                    self.role = akun[3]
                    break
                else:
                    print("password salah")

        if self.userID == None:
            print("Akun tidak dikenal")

    def getUserID(self):
        return self.userID

    def getRole(self):
        return self.role


while True:
    print("___ Login ___")
    raw_username = str(input(" Username : "))
    raw_password = getpass("Password : (Disembunyikan) ")
    user = Login(raw_username, raw_password)
    user.cekAkun()
    if user.getRole() == 1:
        print("kasir")
    elif user.getRole() == 2:
        print("supervisor")
    elif user.getRole() == 3:
        print("pergudangan")
