import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime

# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect('pos_hpp_system.db', check_same_thread=False)
c = conn.cursor()

# Membuat tabel-tabel
c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS raw_materials (id INTEGER PRIMARY KEY, name TEXT, unit TEXT, stock REAL, cost_per_unit REAL, image TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, hpp REAL, image TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY, product_id INT, material_id INT, qty REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, date TEXT, total REAL, payment_method TEXT, user TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

# Default admin & settings
c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'Admin')")
c.execute("INSERT OR IGNORE INTO settings VALUES ('receipt_header', 'SELAMAT DATANG DI TOKO KAMI')")
c.execute("INSERT OR IGNORE INTO settings VALUES ('receipt_footer', 'Terima Kasih Atas Kunjungan Anda!')")
conn.commit()

# ---------------------------------------------------------
# AUTHENTICATION
# ---------------------------------------------------------
st.set_page_config(page_title="Sistem POS & HPP Kompleks", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['role'] = ''

def login():
    st.title("🔑 Login Sistem Kasir & Manajemen HPP")
    username = st.text_input("Username")
    password = st.text_input("Password", type="password")
    if st.button("Login"):
        c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
        res = c.fetchone()
        if res:
            st.session_state['logged_in'] = True
            st.session_state['username'] = username
            st.session_state['role'] = res[0]
            st.rerun()
        else:
            st.error("Username atau password salah")

if not st.session_state['logged_in']:
    login()
    st.stop()

# ---------------------------------------------------------
# SIDEBAR NAVIGATION
# ---------------------------------------------------------
st.sidebar.title(f"👤 {st.session_state['username']} ({st.session_state['role']})")
menu = st.sidebar.radio("Navigasi Menu", [
    "🛒 Kasir (POS)",
    "📦 Input & Stok Bahan Baku",
    "🍔 Kelola Produk & Perhitungan HPP",
    "📊 Laporan Transaksi & Analisis",
    "⚙️ Pengaturan Struk & Printer",
    "👥 Kelola User"
])

if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

# ---------------------------------------------------------
# MENU 1: KASIR (POS)
# ---------------------------------------------------------
if menu == "🛒 Kasir (POS)":
    st.header("🛒 Kasir / Point of Sales")
    
    col1, col2 = st.columns([2, 1])
    
    with col1:
        st.subheader("Daftar Produk")
        products = pd.read_sql("SELECT * FROM products", conn)
        
        if 'cart' not in st.session_state:
            st.session_state['cart'] = []

        grid_cols = st.columns(3)
        for idx, row in products.iterrows():
            with grid_cols[idx % 3]:
                st.write(f"**{row['name']}**")
                st.write(f"Rp {row['price']:,}")
                if st.button(f"Tambah", key=f"btn_{row['id']}"):
                    st.session_state['cart'].append({"id": row['id'], "name": row['name'], "price": row['price']})
                    st.success(f"{row['name']} ditambahkan!")

    with col2:
        st.subheader("Keranjang")
        if st.session_state['cart']:
            cart_df = pd.DataFrame(st.session_state['cart'])
            summary = cart_df.groupby(['id', 'name', 'price']).size().reset_index(name='qty')
            summary['subtotal'] = summary['price'] * summary['qty']
            
            st.dataframe(summary[['name', 'qty', 'subtotal']], hide_index=True)
            
            total = summary['subtotal'].sum()
            st.markdown(f"### **Total: Rp {total:,}**")
            
            pay_method = st.selectbox("Metode Pembayaran", ["Cash", "Transfer Bank", "E-Wallet (QRIS)"])
            
            if st.button("🔴 Selesaikan Transaksi"):
                # Simpan Transaksi
                now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                c.execute("INSERT INTO transactions (date, total, payment_method, user) VALUES (?, ?, ?, ?)",
                          (now, total, pay_method, st.session_state['username']))
                
                # Potong Stok Bahan Baku Berdasarkan Resep
                for _, item in summary.iterrows():
                    c.execute("SELECT material_id, qty FROM recipes WHERE product_id=?", (item['id'],))
                    recipes = c.fetchall()
                    for mat_id, req_qty in recipes:
                        total_deduct = req_qty * item['qty']
                        c.execute("UPDATE raw_materials SET stock = stock - ? WHERE id=?", (total_deduct, mat_id))
                
                conn.commit()
                st.session_state['cart'] = []
                st.balloons()
                st.success("Transaksi Berhasil Diproses!")
        else:
            st.info("Keranjang masih kosong.")

# ---------------------------------------------------------
# MENU 2: INPUT & STOK BAHAN BAKU
# ---------------------------------------------------------
elif menu == "📦 Input & Stok Bahan Baku":
    st.header("📦 Manajemen Bahan Baku & Peringatan Stok")
    
    with st.expander("➕ Tambah / Update Bahan Baku"):
        name = st.text_input("Nama Bahan Baku (Misal: Kopi, Gula, Cup)")
        unit = st.selectbox("Satuan", ["Gram", "ML", "Pcs", "Kg", "Liter"])
        stock = st.number_input("Jumlah Stok Ditambahkan", min_value=0.0)
        cost_total = st.number_input("Total Harga Beli (Rp)", min_value=0.0)
        
        if st.button("Simpan Bahan Baku"):
            if stock > 0:
                cost_per_unit = cost_total / stock
                c.execute("INSERT INTO raw_materials (name, unit, stock, cost_per_unit) VALUES (?, ?, ?, ?)",
                          (name, unit, stock, cost_per_unit))
                conn.commit()
                st.success("Bahan baku berhasil disimpan!")

    st.subheader("📋 Daftar Stok Bahan Baku Saat Ini")
    df_mats = pd.read_sql("SELECT * FROM raw_materials", conn)
    st.dataframe(df_mats, use_container_width=True)

    # Deteksi Bahan Menipis
    low_stock = df_mats[df_mats['stock'] < 10] # Threshold contoh: < 10
    if not low_stock.empty:
        st.warning("⚠️ **Peringatan Bahan Baku Menipis:**")
        st.dataframe(low_stock[['name', 'stock', 'unit']])

# ---------------------------------------------------------
# MENU 3: KELOLA PRODUK & PERHITUNGAN HPP
# ---------------------------------------------------------
elif menu == "🍔 Kelola Produk & Perhitungan HPP":
    st.header("🍔 Kelola Produk & Kalkulasi HPP (Bahan + Overhead)")
    
    st.subheader("1. Input Biaya Operasional (Listrik, Air, Gaji, dll)")
    col_a, col_b = st.columns(2)
    with col_a:
        b_listrik = st.number_input("Biaya Listrik & Air / Bulan", value=500000)
        b_tenaga = st.number_input("Biaya Tenaga Kerja / Bulan", value=2000000)
    with col_b:
        b_bensin = st.number_input("Biaya Operasional/Bensin / Bulan", value=300000)
        est_penjualan = st.number_input("Estimasi Total Pcs Terjual / Bulan", value=1000)
    
    overhead_per_pcs = (b_listrik + b_tenaga + b_bensin) / (est_penjualan if est_penjualan > 0 else 1)
    st.info(f"💡 **Beban Biaya Overhead per Satuan Produk:** Rp {overhead_per_pcs:,.2f}")

    st.markdown("---")
    st.subheader("2. Form Produk Baru & Resep Bahan Baku")
    p_name = st.text_input("Nama Produk Jualan")
    p_price = st.number_input("Harga Jual (Rp)", min_value=0.0)
    
    mats_df = pd.read_sql("SELECT id, name, unit, cost_per_unit FROM raw_materials", conn)
    
    selected_recipe = []
    hpp_bahan = 0.0
    
    st.write("**Pilih Resep Bahan Baku:**")
    for idx, row in mats_df.iterrows():
        qty_used = st.number_input(f"Penggunaan {row['name']} ({row['unit']})", min_value=0.0, key=f"mat_{row['id']}")
        if qty_used > 0:
            cost = qty_used * row['cost_per_unit']
            hpp_bahan += cost
            selected_recipe.append((row['id'], qty_used))
            
    total_hpp_satuan = hpp_bahan + overhead_per_pcs
    st.write(f"### **Total HPP Satuan: Rp {total_hpp_satuan:,.2f}** (Bahan: Rp {hpp_bahan:,.2f} + Overhead: Rp {overhead_per_pcs:,.2f})")
    
    if st.button("Simpan Produk Jualan"):
        c.execute("INSERT INTO products (name, price, hpp) VALUES (?, ?, ?)", (p_name, p_price, total_hpp_satuan))
        p_id = c.lastrowid
        for m_id, q in selected_recipe:
            c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_id, m_id, q))
        conn.commit()
        st.success("Produk dan resep berhasil ditambahkan!")

# ---------------------------------------------------------
# MENU 4: LAPORAN & FILTER TRANSAKSI
# ---------------------------------------------------------
elif menu == "📊 Laporan Transaksi & Analisis":
    st.header("📊 Laporan Penjualan & Analisis Produk")
    
    # Filter
    filter_type = st.selectbox("Filter Waktu", ["Semua", "Harian", "Bulanan"])
    df_tx = pd.read_sql("SELECT * FROM transactions", conn)
    
    if not df_tx.empty:
        st.subheader("📈 Ringkasan Penjualan")
        st.dataframe(df_tx, use_container_width=True)
        
        st.metric("Total Omset", f"Rp {df_tx['total'].sum():,}")
        
        # Filter Produk Terlaris
        st.subheader("🔥 Produk Paling Laris")
        # Analisis rasio pembayaran
        st.subheader("💳 Metode Pembayaran")
        st.bar_chart(df_tx['payment_method'].value_counts())
    else:
        st.info("Belum ada data transaksi.")

# ---------------------------------------------------------
# MENU 5: PENGATURAN STRUK & PRINTER
# ---------------------------------------------------------
elif menu == "⚙️ Pengaturan Struk & Printer":
    st.header("⚙️ Custom Struk Penjualan")
    
    c.execute("SELECT value FROM settings WHERE key='receipt_header'")
    header_val = c.fetchone()[0]
    c.execute("SELECT value FROM settings WHERE key='receipt_footer'")
    footer_val = c.fetchone()[0]
    
    new_header = st.text_area("Header Struk (Bagian Atas)", value=header_val)
    new_footer = st.text_area("Footer Struk (Bagian Bawah)", value=footer_val)
    
    if st.button("Simpan Pengaturan Struk"):
        c.execute("UPDATE settings SET value=? WHERE key='receipt_header'", (new_header,))
        c.execute("UPDATE settings SET value=? WHERE key='receipt_footer'", (new_footer,))
        conn.commit()
        st.success("Tampilan struk berhasil diperbarui!")

# ---------------------------------------------------------
# MENU 6: KELOLA USER
# ---------------------------------------------------------
elif menu == "👥 Kelola User":
    if st.session_state['role'] != 'Admin':
        st.error("Akses ditolak. Menu ini hanya untuk Admin.")
    else:
        st.header("👥 Manajemen Pengguna")
        new_user = st.text_input("Username Baru")
        new_pass = st.text_input("Password Baru", type="password")
        new_role = st.selectbox("Role", ["Kasir", "Admin"])
        
        if st.button("Tambah User"):
            c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (new_user, new_pass, new_role))
            conn.commit()
            st.success(f"User {new_user} berhasil ditambahkan!")
        
        st.subheader("Daftar Pengguna")
        users_df = pd.read_sql("SELECT id, username, role FROM users", conn)
        st.dataframe(users_df)
