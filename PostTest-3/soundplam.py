from abc import ABC, abstractmethod

# [ABSTRAKSI] => Abstract Base Class (ABC)
class Produk(ABC):
    nama_toko = "SoundPlam"
    jumlah_produk = 0
    kategori_produk = ["VST Plugin", "Drum Kit", "Preset Pack"]

    def __init__(self, nama, kategori, harga, stok):
        self.nama = nama
        self.__kategori = kategori
        self._harga = harga
        self._stok = stok
        Produk.jumlah_produk += 1

    @property
    def kategori(self):
        return self.__kategori

    @kategori.setter
    def kategori(self, kategori_baru):
        if kategori_baru not in Produk.kategori_produk:
            raise ValueError(f"[!] Error: Kategori tidak valid. Kategori harus salah satu dari {Produk.kategori_produk}")
        self.__kategori = kategori_baru

    @property
    def harga(self):
        return self._harga

    @harga.setter
    def harga(self, harga_baru):
        if not isinstance(harga_baru, (int, float)):
            raise TypeError("[!] Error: Harga harus berupa angka")
        if harga_baru < 0:
            raise ValueError("[!] Error: Harga tidak boleh negatif")
        self._harga = harga_baru

    @property
    def stok(self):
        return self._stok

    @stok.setter
    def stok(self, stok_baru):
        if not isinstance(stok_baru, int):
            raise TypeError("[!] Error: Stok harus berupa angka")
        if stok_baru < 0:
            raise ValueError("[!] Error: Stok tidak boleh negatif")
        self._stok = stok_baru

    @classmethod
    def info_toko(cls):
        print(f"Nama Toko: {cls.nama_toko}")
        print(f"Jumlah Produk: {cls.jumlah_produk}")

    # [Abstrak Method 1] => tiap jenis produk punya aturan diskon sendiri
    @abstractmethod
    def hitung_diskon(self):
        pass

    # [Abstrak Method 2] => tiap jenis produk menampilkan info khususnya
    @abstractmethod
    def info_produk(self):
        pass

    def tambah_stok(self, jumlah):
        if not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("[!] Error: Jumlah stok yang ditambahkan harus lebih dari 0")
        self.stok += jumlah

    def kurangi_stok(self, jumlah):
        if not isinstance(jumlah, int) or jumlah <= 0:
            raise ValueError("[!] Error: Jumlah stok yang dikurangi harus lebih dari 0")
        if jumlah > self._stok:
            raise ValueError("[!] Error: Jumlah stok yang dikurangi melebihi stok yang tersedia")
        self.stok -= jumlah

    def harga_setelah_diskon(self):
        # Alur sama untuk semua produk, tetapi angka diskonnya ditentukan
        # oleh hitung_diskon() milik masing-masing subclass (polimorfisme).
        return self._harga - self.hitung_diskon()

    def tampilkan_penawaran(self):
        # Seperti jalankan() pada materi: method konkret yang hanya
        # memanggil abstract method, tanpa peduli jenis produknya.
        print(f"  {self.nama:<22} Rp{self._harga:>9,.0f} -> Diskon Rp{self.hitung_diskon():>8,.0f} "
        f"-> Rp{self.harga_setelah_diskon():>9,.0f}")


# [INHERITANCE] => Sub class dari Produk
class VST(Produk):
    def __init__(self, nama, harga, stok, format_plugin, jenis_plugin):
        super().__init__(nama, "VST Plugin", harga, stok)
        self.format_plugin = format_plugin   # atribut unik VST
        self.jenis_plugin = jenis_plugin     # atribut unik VST

    # [Implementasi Abstrak Method 2]
    def info_produk(self):
        print(f"  [{self.kategori}] {self.nama}")
        print(f"    Harga    : Rp{self._harga:,.0f}")
        print(f"    Stok     : {self._stok}")
        status = "Habis" if self._stok == 0 else ("Hampir habis" if self._stok <= 5 else "Tersedia")
        print(f"    Format   : {self.format_plugin}")
        print(f"    Jenis    : {self.jenis_plugin}")
        print(f"    Lisensi  : {status}")

    # [Implementasi Abstrak Method 1] => diskon 10%
    def hitung_diskon(self):
        return self._harga * 0.10


class DrumKit(Produk):
    def __init__(self, nama, harga, stok, jumlah_sample, genre):
        super().__init__(nama, "Drum Kit", harga, stok)
        self.jumlah_sample = jumlah_sample   # atribut unik DrumKit
        self.genre = genre                   # atribut unik DrumKit

    # [Implementasi Abstrak Method 2]
    def info_produk(self):
        print(f"  [{self.kategori}] {self.nama}")
        print(f"    Harga    : Rp{self._harga:,.0f}")
        print(f"    Stok     : {self._stok}")
        harga_per_sample = self._harga / self.jumlah_sample
        print(f"    Sample   : {self.jumlah_sample} file")
        print(f"    Genre    : {self.genre}")
        print(f"    Per sample: Rp{harga_per_sample:,.0f}")

    # [Implementasi Abstrak Method 1]
    def hitung_diskon(self):
        return self._harga * 0.6


# [OCP - Open/Closed Principle]
class PresetPack(Produk):
    def __init__(self, nama, harga, stok, jumlah_preset, synth_target):
        super().__init__(nama, "Preset Pack", harga, stok)
        self.jumlah_preset = jumlah_preset
        self.synth_target = synth_target

    def info_produk(self):
        print(f"  [{self.kategori}] {self.nama}")
        print(f"    Harga    : Rp{self._harga:,.0f}")
        print(f"    Stok     : {self._stok}")
        print(f"    Preset   : {self.jumlah_preset} preset")
        print(f"    Untuk    : {self.synth_target}")

    def hitung_diskon(self):
        return self._harga * 0.05


# [DUCK TYPING] => notifikasi
class EmailNotif:
    def __init__(self, alamat):
        self.alamat = alamat

    def kirim(self, pesan):
        print(f"  [EMAIL => {self.alamat}] {pesan}")


class WhatsAppNotif:
    def __init__(self, nomor):
        self.nomor = nomor

    def kirim(self, pesan):
        print(f"  [WA => {self.nomor}] {pesan}")


def beritahu_pembeli(kanal_list, pesan):
    for kanal in kanal_list:
        kanal.kirim(pesan)

class MutasiSaldo:
    def __init__(self, id_mutasi, tipe, nominal, keterangan):
        self.id_mutasi = id_mutasi
        self.tipe = tipe
        self.nominal = nominal
        self.keterangan = keterangan

    # [MAGIC METHOD]
    def __str__(self):
        simbol = "+" if self.tipe == "KREDIT" else "-"
        return f"[{self.id_mutasi}] {self.tipe:<6} {simbol}Rp{self.nominal:,.0f} | Ket: {self.keterangan}"


class Pengguna:
    jumlah_pengguna = 0
    daftar_pengguna = []

    # [DIP - Dependency Inversion Principle]
    def __init__(self, nama, password, saldo, kanal_notif=None):
        self.nama = nama
        self.__password = password
        self.__saldo = saldo
        self.__riwayat_mutasi = []
        self._kanal_notif = kanal_notif if kanal_notif is not None else []
        Pengguna.daftar_pengguna.append(self)
        Pengguna.jumlah_pengguna += 1

        if saldo > 0:
            self._catat_mutasi("KREDIT", saldo, "Saldo awal akun")

    @property
    def saldo(self):
        return self.__saldo

    @saldo.setter
    def saldo(self, saldo_baru):
        if saldo_baru < 0:
            raise ValueError("[!] Error: Saldo tidak boleh negatif")
        self.__saldo = saldo_baru

    @property
    def password(self):
        return self.__password

    @password.setter
    def password(self, password_baru):
        if len(password_baru) < 6:
            raise ValueError("[!] Error: Password harus minimal 6 karakter")
        self.__password = password_baru

    @classmethod
    def login(cls, nama, password):
        for pengguna in cls.daftar_pengguna:
            if pengguna.nama == nama and pengguna.__password == password:
                print(f"[+] Login berhasil. Selamat datang, {nama}!")
                return pengguna
        print("[!] Login gagal. Username atau password salah.")
        return None

    def _catat_mutasi(self, tipe, nominal, keterangan):
        id_baru = f"MUT-{len(self.__riwayat_mutasi) + 1:04d}"
        self.__riwayat_mutasi.append(MutasiSaldo(id_baru, tipe, nominal, keterangan))

    def tambah_saldo(self, jumlah):
        if jumlah <= 0:
            raise ValueError("[!] Error: Jumlah saldo yang ditambahkan harus lebih dari 0")
        self.__saldo += jumlah
        self._catat_mutasi("KREDIT", jumlah, "Top up saldo")

    def beli_produk(self, produk, jumlah):
        if not isinstance(produk, Produk):
            raise ValueError("[!] Error: Produk tidak valid")
        if jumlah <= 0:
            raise ValueError("[!] Error: Jumlah harus lebih dari 0")
        if jumlah > produk.stok:
            raise ValueError(f"[!] Error: Stok tidak cukup (sisa {produk.stok})")

        total = Transaksi.hitung_total_harga(produk.harga, jumlah, Transaksi.pajak)
        if total > self.__saldo:
            raise ValueError("[!] Error: Saldo tidak cukup")

        transaksi = Transaksi(produk, jumlah, self.nama)
        transaksi.proses()
        self.__saldo -= transaksi.total_bayar
        self._catat_mutasi("DEBET", transaksi.total_bayar, f"Beli {produk.nama} ({transaksi.id_transaksi})")

        # [Duck Typing]
        beritahu_pembeli(self._kanal_notif,
        f"Pembelian {produk.nama} ({transaksi.id_transaksi}) berhasil. "
        f"Total Rp{transaksi.total_bayar:,.0f}")
        return transaksi

    def cetak_mutasi(self):
        print(f"\n  Mutasi Saldo: {self.nama}")
        print(f"  Saldo Akhir : Rp{self.__saldo:,.0f}")
        for mutasi in self.__riwayat_mutasi:
            print(f"    {mutasi}")

    def info_pengguna(self):
        print(f"""
    ===== INFO PENGGUNA =====
    Nama    : {self.nama}
    Saldo   : Rp{self.__saldo:,.0f}
        """)


class Toko:
    def __init__(self, nama_toko):
        self.nama_toko = nama_toko
        self._daftar_produk = []

    @property
    def total_produk(self):
        return len(self._daftar_produk)

    def tambah_produk(self, produk):
        if not isinstance(produk, Produk):
            raise ValueError("[!] Error: Produk tidak valid")
        self._daftar_produk.append(produk)
        print(f"  [+] {produk.nama} dijual di {self.nama_toko}")

    def hapus_produk(self, nama):
        awal = len(self._daftar_produk)
        self._daftar_produk = [p for p in self._daftar_produk if p.nama != nama]
        if len(self._daftar_produk) < awal:
            print(f"  [-] {nama} ditarik dari {self.nama_toko}")

    # [POLIMORFISME VIA PEWARISAN]
    def tampilkan_katalog(self):
        print(f"\n  ===== KATALOG {self.nama_toko} ({self.total_produk} produk) =====")
        for produk in self._daftar_produk:
            produk.info_produk()

    def tampilkan_penawaran(self):
        print(f"\n  ===== PENAWARAN DISKON {self.nama_toko} =====")
        for produk in self._daftar_produk:
            produk.tampilkan_penawaran()


class Transaksi:
    pajak = 0.11
    jumlah_transaksi = 0
    total_pendapatan = 0
    riwayat = []

    def __init__(self, produk, jumlah, nama_pembeli="-"):
        if not isinstance(produk, Produk):
            raise ValueError("[!] Error: Produk tidak valid")

        self.produk = produk
        self.nama_pembeli = nama_pembeli
        self.harga_satuan = produk.harga
        self.pajak_transaksi = Transaksi.pajak
        self.__status = "Pending"
        self.jumlah = jumlah
        Transaksi.jumlah_transaksi += 1
        self.id_transaksi = f"SDP-{Transaksi.jumlah_transaksi}"

    @property
    def jumlah(self):
        return self.__jumlah

    @jumlah.setter
    def jumlah(self, jumlah_baru):
        if not isinstance(jumlah_baru, int):
            raise ValueError("[!] Error: Jumlah harus berupa bilangan bulat")
        if jumlah_baru <= 0:
            raise ValueError("[!] Error: Jumlah harus lebih dari 0")
        if self.__status != "Pending":
            raise ValueError("[!] Error: Transaksi sudah diproses, jumlah tidak bisa diubah")
        self.__jumlah = jumlah_baru

    @property
    def status(self):
        return self.__status

    @property
    def total_bayar(self):
        return Transaksi.hitung_total_harga(self.harga_satuan, self.jumlah, self.pajak_transaksi)

    @staticmethod
    def hitung_total_harga(harga_satuan, jumlah, pajak):
        subtotal = harga_satuan * jumlah
        return subtotal + subtotal * pajak

    @classmethod
    def info_transaksi(cls):
        print(f"Transaksi dibuat     : {cls.jumlah_transaksi}")
        print(f"Transaksi berhasil   : {len(cls.riwayat)}")
        print(f"Total pendapatan     : Rp{cls.total_pendapatan:,.0f}")

    def proses(self):
        if self.__status != "Pending":
            raise ValueError(f"[!] Error: Transaksi sudah berstatus {self.__status}")
        if self.jumlah > self.produk.stok:
            self.__status = "Gagal"
            raise ValueError(f"[!] Error: Stok tidak cukup (sisa {self.produk.stok})")
        self.produk.kurangi_stok(self.jumlah)  # [Method Konkret] => dipakai semua subclass Produk
        self.__status = "Berhasil"
        Transaksi.total_pendapatan += self.total_bayar
        Transaksi.riwayat.append(self)

    def cetak_struk(self):
        print(f"""
        ===== STRUK {self.id_transaksi} =====
        Pembeli      : {self.nama_pembeli}
        Produk       : {self.produk.nama}
        Jumlah       : {self.jumlah}
        Harga satuan : Rp{self.harga_satuan:,.0f}
        Pajak        : {self.pajak_transaksi * 100:.0f}%
        Total bayar  : Rp{self.total_bayar:,.0f}
        Status       : {self.status}
        """)