# Library Management System - MySQL & Python (Terminal CRUD)

A simple **Python** and **MySQL** library management system.  
Runs in the terminal for managing books and lending transactions.

## 🚀 Features

✅ Add new books  
✅ View book list  
✅ Search books  
✅ Update book data  
✅ Delete books  
✅ Borrow books  
✅ Return books  
✅ View lending history  
✅ View borrower data
---
## 💾 Database Structure (MySQL)

### Table Structures

#### 1. Table `buku`

| Column     | Data Type     | Description         |
|------------|---------------|---------------------|
| id_buku    | VARCHAR(10)   | Primary Key         |
| judul      | VARCHAR(100)  | Book title          |
| penulis    | VARCHAR(100)  | Author name         |
| kategori   | VARCHAR(50)   | Book category       |
| stok       | INT           | Stock quantity      |

#### 2. Table `peminjam`

| Column          | Data Type     | Description               |
|-----------------|---------------|---------------------------|
| id_peminjam     | INT           | Primary Key, Auto Increment |
| nama_peminjam   | VARCHAR(100)  | Borrower's name           |
| no_telp         | VARCHAR(20)   | Borrower's phone number   |

#### 3. Table `peminjaman`

| Column             | Data Type     | Description                      |
|--------------------|---------------|----------------------------------|
| id_peminjaman      | INT           | Primary Key, Auto Increment      |
| id_peminjam        | INT           | Foreign Key → peminjam.id_peminjam |
| id_buku            | VARCHAR(10)   | Foreign Key → buku.id_buku       |
| tanggal_pinjam     | DATE          | Borrowing date                   |
| tanggal_kembali    | DATE          | Return due date                  |


## 📥 Installation
### 1. Import the Database
Run the SQL file:
```bash
mysql -u root -p perpustakaan < perpustakaan_data.sql

### 2. Install Python libraries:
pip install pymysql tabulate

## 📝 Files Included
perpustakaan.sql → SQL script for database schema and dummy data
main.py → Python script for terminal CRUD operations

## 📃 License
This project is created for learning purposes and is free to use and modify.
