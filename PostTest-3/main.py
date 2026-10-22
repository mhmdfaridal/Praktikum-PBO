from soundplam import Transaksi, Produk, Pengguna, VST, DrumKit, Toko

def main():
    print("=== AGREGASI: produk dibuat di luar, lalu didaftarkan ke Toko ===")
    serum = VST("Wavetable Synth X", 1500000, 10, "VST3", "Synthesizer")
    reverb = VST("Hall Reverb Pro", 800000, 3, "VST3", "Effect")
    trap = DrumKit("Trap Essentials", 250000, 20, 120, "Trap")

    toko = Toko("SoundPlam")
    toko.tambah_produk(serum)
    toko.tambah_produk(reverb)
    toko.tambah_produk(trap)
    toko.tampilkan_katalog()

    print("\n=== ASOSIASI: Pengguna memakai Produk lewat parameter ===")
    budi = Pengguna("Budi", "rahasia123", 5000000)
    transaksi1 = budi.beli_produk(serum, 1)
    transaksi1.cetak_struk()
    transaksi2 = budi.beli_produk(trap, 2)
    transaksi2.cetak_struk()

    print("=== KOMPOSISI: Pengguna menyimpan MutasiSaldo miliknya sendiri ===")
    budi.tambah_saldo(1000000)
    budi.cetak_mutasi()

    print("\n=== POLIMORFISME & OVERRIDING: info_produk() beda tiap subclass ===")
    for produk in (serum, trap):
        produk.info_produk()

    print("\n=== CEK PEWARISAN ===")
    print("isinstance(serum, Produk)  :", isinstance(serum, Produk))
    print("isinstance(serum, DrumKit) :", isinstance(serum, DrumKit))
    print("issubclass(DrumKit, Produk):", issubclass(DrumKit, Produk))

    print("\n=== BUKTI AGREGASI: toko dihapus, produk tetap ada ===")
    del toko
    print(f"  Produk masih ada: {serum.nama}, {reverb.nama}, {trap.nama}")

    print("\n=== VALIDASI ERROR ===")
    try:
        budi.beli_produk(reverb, 99)
    except ValueError as e:
        print(" ", e)

    print()
    Produk.info_toko()
Transaksi.info_transaksi()

if __name__ == "__main__":
    main()