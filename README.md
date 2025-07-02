# Library Management System - MySQL & Python (Terminal CRUD)

A simple **Python** and **MySQL** library management system.  
Runs in the terminal for managing books and lending transactions.

## 🚀 Features
This application implements full CRUD operations for library management:
---
### ✅ Create
- **Add New Book**  
  Add new books into the library’s database, including book ID, title, author, category, and stock quantity.
- **Borrow Book**  
  Record a new borrowing transaction, linking a borrower with the book they borrow, along with borrowing and return dates. If the borrower does not exist, the app will create their record automatically.
---
### ✅ Read
- **View Book List**  
  Display all books in the database, including ID, title, author, category, and stock.
- **Search Books**  
  Search for books by title or author keyword.
- **View Borrowing History**  
  Display all borrowing transactions, showing who borrowed which books and the return dates.
- **View Borrower Data**  
  Display a list of all borrowers with their names and phone numbers.
---
### ✅ Update
- **Update Book Data**  
  Modify the details of an existing book, such as title, author, category, or stock.
---
### ✅ Delete
- **Delete Book**  
  Remove a book from the library database.
- **Return Book**  
  Process a book’s return, deleting the lending record and updating the book’s stock accordingly.
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
```
### 2. Install Python libraries:
pip install pymysql tabulate

### 3. Clone The Repository
git clone https://github.com/devitrisnaw/CRUD-Library-Management-System-with-MySQL.git

cd library-mysql-python

## 📝 Files Included
perpustakaan.sql → SQL script for database schema and dummy data

main.py → Python script for terminal CRUD operations

## 📃 License
This project is created for learning purposes and is free to use and modify.
