from soundplam import (
    Produk, VST, DrumKit, PresetPack,
    EmailNotif, WhatsAppNotif, beritahu_pembeli,
    Toko, Pengguna, Transaksi,
)

def garis(judul):
    print(f"\n{'=' * 60}\n{judul}\n{'=' * 60}")


# [BUKTI ABSTRAKSI] => Ntar langsung TypeError Tu

garis("1. BUKTI ABSTRAKSI: Produk tidak bisa diinstansiasi")
try:
    produk_langsung = Produk("Coba", "VST Plugin", 1000, 1)
except TypeError as e:
    print(f"TypeError: {e}")


# [INHERITANCE] => Membuat objek dari 3 subclass Produk

garis("2. MEMBUAT PRODUK DAN MENAMBAHKAN KE TOKO")
serum = VST("Serum Wavetable", 2_500_000, 10, "VST3/AU", "Synthesizer")
trap_kit = DrumKit("Trap Essentials", 350_000, 3, 120, "Trap")
lofi = PresetPack("Lo-Fi Presets Vol.1", 200_000, 8, 64, "Serum")

toko = Toko("SoundPlam")
for produk in (serum, trap_kit, lofi):
    toko.tambah_produk(produk)


# [POLIMORFISME VIA PEWARISAN] => Menjalankan method info_produk() dan hitung_diskon() versi class itu sendiri

garis("3. POLIMORFISME: info_produk() dan hitung_diskon() berbeda tiap subclass")
toko.tampilkan_katalog()
toko.tampilkan_penawaran()


# [DUCK TYPING] => EmailNotif dan WhatsAppNotif tidak berhubungan lewat pewarisan

garis("4. DUCK TYPING: Email dan WhatsApp lewat satu fungsi")
kanal_budi = [EmailNotif("budi@mail.com"), WhatsAppNotif("0812-1234-5678")]
beritahu_pembeli(kanal_budi, "Selamat datang di SoundPlam!")


# [DIP (SOLID)] => kanal notifikasi disuntikkan ke Pengguna dari luar
# [Method Konkret] => kurangi_stok() dipakai oleh semua subclass Produk

garis("5. PEMBELIAN: dependency injection + method konkret")
budi = Pengguna("budi", "rahasia123", 5_000_000, kanal_notif=kanal_budi)

print(f"Stok {trap_kit.nama} sebelum beli: {trap_kit.stok}")
transaksi = budi.beli_produk(trap_kit, 2)
print(f"Stok {trap_kit.nama} sesudah beli: {trap_kit.stok}")

transaksi.cetak_struk()
budi.cetak_mutasi()

print()
Transaksi.info_transaksi()