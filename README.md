# 💊 PharmaGest – Pharmacy Management System

Pharmacy Management Desktop Application developed using Python and Tkinter.
This project helps manage pharmacy products, stock, and daily operations through a simple graphical user interface.

> 🚧 **Project status:** under active development.

## ✨ Features

- **Authentication & roles**: secure login (passwords hashed with SHA-256) with two roles:
  - **Admin**: full access, including statistics and user management
  - **User**: access to medicines and sales only
- **Medicine management**: add medicines with dosage, category, stock, expiry date, purchase/sale price and supplier
- **Smart alerts**: expired medicines and low-stock products
- **Sales management**:
  - simple sales and sales on prescription (doctor, prescription number, client)
  - shopping cart with automatic total
  - automatic stock update after each sale
  - sales history
- **Statistics**: monthly revenue, profit and sales summary per medicine
- **User management**: add, edit and delete users

## 🛠️ Tech Stack

- Python 3
- Tkinter (GUI)
- Pillow (images)
- openpyxl (Excel storage, current version)

## 🚀 Getting Started

1. Clone the repository
2. Install the dependencies:
   pip install openpyxl pillow
3. Run the application:
   python main.py

Default account on first launch: `admin` / `admin123` (change it after your first login).

## 🗺️ Roadmap

- [ ] Migrate data storage from Excel files to **SQL Server**
- [ ] Add **search and filters** in the Medicines section (by name, category, expiry date, stock level...)
- [ ] Improve the dashboard with real stock figures
- [ ] Add more tests and error handling

## 📁 Project Structure

├── controleur/   # business logic (login, medicines, sales, statistics)
├── view/         # Tkinter interfaces
└── images/       # application images
