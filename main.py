# ===== Fungsi Utama =====
import pymysql
from tabulate import tabulate
from datetime import datetime, timedelta

# ===== Koneksi ke Database MySQL dengan PyMySQL =====
db = pymysql.connect(
    host="localhost",
    user="root",
    password="your_password",
    database="perpustakaan",
    cursorclass=pymysql.cursors.DictCursor
)
cursor = db.cursor()

def menu_perpus():
    print("\n=== Selamat Datang di Perpustakaan Kota ===")
    print("1. Tambah Buku Baru")
    print("2. Tampilkan Buku")
    print("3. Pinjam Buku")
    print("4. Pengembalian Buku")
    print("5. Update Data Buku")
    print("6. Hapus Buku")
    print("7. Keluar")

def tambah_buku():
    tampil_daftar_buku()
    print("\n=== Tambah Buku Baru ===")
    id_buku = input("Masukkan ID Buku (contoh B011): ").upper()
    judul = input("Masukkan Judul Buku: ")
    penulis = input("Masukkan Nama Penulis: ")
    kategori = input("Masukkan Kategori Buku: ")
    
    try:
        stok = int(input("Masukkan Stok Buku: "))
    except ValueError:
        print("Stok harus berupa angka!")
        return

    # cek apakah id_buku sudah ada
    cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id_buku,))
    data = cursor.fetchone()
    
    if data:
        print(f"⚠️ Buku dengan ID {id_buku} sudah ada!")
        return
    
    cursor.execute("""
        INSERT INTO buku (id_buku, judul, penulis, kategori, stok)
        VALUES (%s, %s, %s, %s, %s)
    """, (id_buku, judul, penulis, kategori, stok))
    
    db.commit()
    print(f"Buku '{judul}' berhasil ditambahkan.")

def sub_menu_tampil():
    print("\n=== Pilih Menu ===")
    print("1. Tampilkan Daftar Buku")
    print("2. Cari Buku")
    print("3. Menu Utama")

def tampil_daftar_buku():
    cursor.execute("SELECT * FROM buku")
    hasil = cursor.fetchall()
    print(tabulate(hasil, headers="keys", tablefmt="grid"))

def cari_buku():
    keyword = input("Masukkan kata kunci (Judul/Penulis): ").lower()
    sql = "SELECT * FROM buku WHERE LOWER(judul) LIKE %s OR LOWER(penulis) LIKE %s"
    val = (f"%{keyword}%", f"%{keyword}%")
    cursor.execute(sql, val)
    hasil = cursor.fetchall()
    if hasil:
        print(tabulate(hasil, headers="keys", tablefmt="grid"))
    else:
        print("Buku tidak ditemukan!")

def sub_menu_pinjam():
    print("\n=== Pilih Menu ===")
    print("1. Menu Pinjam Buku")
    print("2. Riwayat Peminjaman")
    print("3. Data Peminjam")
    print("4. Menu Utama")

def pinjam_buku():
    nama_peminjam = input("Masukkan nama peminjam: ")
    no_telp = input("Masukkan nomor telepon peminjam: ")

    tampil_daftar_buku()
    judul_buku = input("Masukkan judul buku yang ingin dipinjam: ")
    
    # cari buku
    sql = "SELECT * FROM buku WHERE LOWER(judul) = %s"
    cursor.execute(sql, (judul_buku.lower(),))
    buku = cursor.fetchone()
    
    if not buku:
        print("Buku tidak ditemukan!")
        return
    
    if buku["stok"] <= 0:
        print("Stok Buku Habis!")
        return
    
    try:
        tanggal_pinjam_input = input("Tanggal Pinjam (DD-MM-YYYY): ")
        tanggal_pinjam = datetime.strptime(tanggal_pinjam_input, "%d-%m-%Y")
        tanggal_kembali = tanggal_pinjam + timedelta(days=10)
    except ValueError:
        print("Format tanggal salah!")
        return

    # cek apakah peminjam sudah ada
    cursor.execute("SELECT id_peminjam FROM peminjam WHERE nama_peminjam = %s", (nama_peminjam,))
    result = cursor.fetchone()

    if result:
        id_peminjam = result["id_peminjam"]
    else:
        # Tambah peminjam baru
        cursor.execute("""
            INSERT INTO peminjam (nama_peminjam, no_telp)
            VALUES (%s, %s)
        """, (nama_peminjam, no_telp))
        id_peminjam = cursor.lastrowid

    # Insert ke tabel peminjaman
    cursor.execute("""
        INSERT INTO peminjaman (id_peminjam, id_buku, tanggal_pinjam, tanggal_kembali)
        VALUES (%s, %s, %s, %s)
    """, (
        id_peminjam,
        buku["id_buku"],
        tanggal_pinjam.strftime("%Y-%m-%d"),
        tanggal_kembali.strftime("%Y-%m-%d")
    ))
    
    # Kurangi stok buku
    cursor.execute("UPDATE buku SET stok = stok - 1 WHERE id_buku = %s", (buku["id_buku"],))
    
    db.commit()
    print(f"Buku '{buku['judul']}' berhasil dipinjam oleh {nama_peminjam}.")

def riwayat_peminjaman():
    query = """
            SELECT
                pe.id_peminjaman,
                p.nama_peminjam,
                p.no_telp,
                b.judul,
                pe.tanggal_pinjam,
                pe.tanggal_kembali 
            FROM peminjaman AS pe
            JOIN peminjam AS p ON pe.id_peminjam = p.id_peminjam
            JOIN buku AS b ON pe.id_buku = b.id_buku
            ORDER BY pe.id_peminjaman;
    """
    cursor.execute(query)
    hasil = cursor.fetchall()
    if hasil:
        print(tabulate(hasil, headers="keys", tablefmt="grid"))
    else:
        print("Belum ada riwayat peminjaman.")

def tampil_data_peminjam():
    cursor.execute("SELECT * FROM peminjam")
    hasil = cursor.fetchall()
    if hasil:
        print(tabulate(hasil, headers="keys", tablefmt="grid"))
    else:
        print("Belum ada data peminjam.")

def pengembalian_buku():
    riwayat_peminjaman()  # tampilkan peminjaman, bukan peminjam
    try:
        id_kembali = int(input("Masukkan ID peminjaman: "))
        
        # Ambil data peminjaman
        sql = """
            SELECT peminjaman.*, peminjam.nama_peminjam, buku.judul
            FROM peminjaman
            JOIN peminjam ON peminjaman.id_peminjam = peminjam.id_peminjam
            JOIN buku ON peminjaman.id_buku = buku.id_buku
            WHERE peminjaman.id_peminjaman = %s
        """
        cursor.execute(sql, (id_kembali,))
        data = cursor.fetchone()
        
        if not data:
            print("Data peminjaman tidak ditemukan!")
            return

        tgl_kembali = data["tanggal_kembali"]
        if isinstance(tgl_kembali, datetime):
            tgl_kembali = tgl_kembali.date()
        tgl_pengembalian_input = input("Masukkan tanggal pengembalian (DD-MM-YYYY): ")
        tgl_pengembalian = datetime.strptime(tgl_pengembalian_input, "%d-%m-%Y").date()

        if tgl_pengembalian > tgl_kembali:
            selisih = (tgl_pengembalian - tgl_kembali).days
            print(f"⚠️ Terlambat {selisih} hari!")
        else:
            print("Buku dikembalikan tepat waktu.")

        # Hapus data peminjaman
        cursor.execute("DELETE FROM peminjaman WHERE id_peminjaman = %s", (id_kembali,))
        
        # Kembalikan stok buku
        cursor.execute("UPDATE buku SET stok = stok + 1 WHERE id_buku = %s", (data["id_buku"],))
        
        db.commit()
        print(f"Buku '{data['judul']}' berhasil dikembalikan oleh {data['nama_peminjam']}.")
    
    except ValueError:
        print("ID harus berupa angka!")

def update_buku():
    tampil_daftar_buku()
    id_buku = input("Masukkan ID buku yang ingin diupdate: ").upper()
    cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id_buku,))
    buku = cursor.fetchone()
    if buku:
        judul = input(f"Judul baru ({buku['judul']}): ") or buku["judul"]
        penulis = input(f"Penulis baru ({buku['penulis']}): ") or buku["penulis"]
        kategori = input(f"Kategori baru ({buku['kategori']}): ") or buku["kategori"]
        stok = input(f"Stok baru ({buku['stok']}): ")
        stok = int(stok) if stok else buku["stok"]
        cursor.execute("""
            UPDATE buku SET judul=%s, penulis=%s, kategori=%s, stok=%s WHERE id_buku=%s
        """, (judul, penulis, kategori, stok, id_buku))
        db.commit()
        print("Buku berhasil diupdate!")
    else:
        print("Buku tidak ditemukan!")

def hapus_buku():
    tampil_daftar_buku()
    id_buku = input("Masukkan ID buku yang ingin dihapus: ").upper()
    cursor.execute("SELECT * FROM buku WHERE id_buku = %s", (id_buku,))
    buku = cursor.fetchone()
    if buku:
        konfirmasi = input(f"Yakin ingin menghapus buku '{buku['judul']}'? (y/n): ")
        if konfirmasi.lower() == 'y':
            cursor.execute("DELETE FROM buku WHERE id_buku = %s", (id_buku,))
            db.commit()
            print("Buku berhasil dihapus.")
        else:
            print("Penghapusan dibatalkan.")
    else:
        print("Buku tidak ditemukan!")

# ===== Loop Menu =====
while True:
    menu_perpus()
    pilihan = input("\nPilih Menu: ")
    if pilihan == "1":
        tambah_buku()
    elif pilihan == "2":
        while True:
            sub_menu_tampil()
            pilih = input("Pilih: ")
            if pilih == "1":
                tampil_daftar_buku()
            elif pilih == "2":
                cari_buku()
            elif pilih == "3":
                break
            else:
                print("Pilihan tidak valid!")
    elif pilihan == "3":
        while True:
            sub_menu_pinjam()
            pilih = input("Pilih: ")
            if pilih == "1":
                pinjam_buku()
            elif pilih == "2":
                riwayat_peminjaman()
            elif pilih == "3":
                tampil_data_peminjam()
            elif pilih == "4":
                break
            else:
                print("Pilihan tidak valid!")
    elif pilihan == "4":
        pengembalian_buku()
    elif pilihan == "5":
        update_buku()
    elif pilihan == "6":
        hapus_buku()
    elif pilihan == "7":
        print("Terima kasih telah menggunakan aplikasi!")
        break
    else:
        print("Pilihan tidak valid!")
