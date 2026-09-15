import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os
from PIL import Image

# ---------------------------------------------------------
# SETUP DIRECTORY UNTUK GAMBAR
# ---------------------------------------------------------
UPLOAD_DIR = "uploaded_images"
if not os.path.exists(UPLOAD_DIR):
    os.makedirs(UPLOAD_DIR)

# ---------------------------------------------------------
# DATABASE INITIALIZATION
# ---------------------------------------------------------
conn = sqlite3.connect('pos_hpp_system.db', check_same_thread=False)
c = conn.cursor()

# Membuat tabel-tabel jika belum ada
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
    col1, col2 = st.columns([1, 1])
    with col1:
        username = st.text_input("Username")
        password = st.text_input("Password", type="password")
        if st.button("Login", type="primary"):
            c.execute("SELECT role FROM users WHERE username=? AND password=?", (username, password))
            res = c.fetchone()
            if res:
                st.session_state['logged_in'] = True
                st.session_state['username'] = username
                st.session_state['role'] = res[0]
                st.rerun()
            else:
                st.error("Username atau password salah!")

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

# Helper fungsi simpan gambar
def save_uploaded_file(uploaded_file):
    if uploaded_file is not None:
        file_path = os.path.join(UPLOAD_DIR, uploaded_file.name)
        with open(file_path, "wb") as f:
            f.write(uploaded_file.getbuffer())
        return file_path
    return None

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

        if products.empty:
            st.info("Belum ada produk jualan. Tambahkan produk di menu Kelola Produk.")
        else:
            grid_cols = st.columns(3)
            for idx, row in products.iterrows():
                with grid_cols[idx % 3]:
                    if row['image'] and os.path.exists(row['image']):
                        st.image(row['image'], use_column_width=True)
                    else:
                        st.write("🖼️ *Tanpa Gambar*")
                    st.write(f"**{row['name']}**")
                    st.write(f"Rp {row['price']:,.0f}")
                    if st.button(f"➕ Tambah", key=f"btn_{row['id']}"):
                        st.session_state['cart'].append({"id": row['id'], "name": row['name'], "price": row['price']})
                        st.success(f"{row['name']} masuk keranjang!")

    with col2:
        st.subheader("🛒 Keranjang Belanja")
        if st.session_state['cart']:
            cart_df = pd.DataFrame(st.session_state['cart'])
            summary = cart_df.groupby(['id', 'name', 'price']).size().reset_index(name='qty')
            summary['subtotal'] = summary['price'] * summary['qty']
            
            st.dataframe(summary[['name', 'qty', 'subtotal']], hide_index=True, use_container_width=True)
            
            total = summary['subtotal'].sum()
            st.markdown(f"### **Total: Rp {total:,.0f}**")
            
            pay_method = st.selectbox("Metode Pembayaran", ["Cash", "Transfer Bank", "E-Wallet (QRIS)"])
            
            col_b1, col_b2 = st.columns(2)
            with col_b1:
                if st.button("🔴 Selesaikan Transaksi", type="primary"):
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
                    st.success("Transaksi Berhasil!")
                    st.rerun()
            with col_b2:
                if st.button("🗑️ Kosongkan"):
                    st.session_state['cart'] = []
                    st.rerun()
        else:
            st.info("Keranjang masih kosong.")

# ---------------------------------------------------------
# MENU 2: INPUT & STOK BAHAN BAKU
# ---------------------------------------------------------
elif menu == "📦 Input & Stok Bahan Baku":
    st.header("📦 Manajemen Bahan Baku & Peringatan Stok")
    
    with st.expander("➕ Tambah Bahan Baku Baru"):
        col1, col2 = st.columns(2)
        with col1:
            name = st.text_input("Nama Bahan Baku (Contoh: Whipcream, Cocoa Powder)")
            unit = st.selectbox("Satuan", ["Gram", "ML", "Pcs", "Kg", "Liter"])
            img_file = st.file_uploader("Upload Gambar Bahan Baku (Opsional)", type=["jpg", "png", "jpeg"])
        with col2:
            stock = st.number_input("Jumlah Stok Beli", min_value=0.0, step=1.0)
            cost_total = st.number_input("Total Harga Beli Seluruh Stok (Rp)", min_value=0.0, step=1000.0)
        
        if st.button("Simpan Bahan Baku"):
            if stock > 0 and name:
                cost_per_unit = cost_total / stock
                img_path = save_uploaded_file(img_file)
                c.execute("INSERT INTO raw_materials (name, unit, stock, cost_per_unit, image) VALUES (?, ?, ?, ?, ?)",
                          (name, unit, stock, cost_per_unit, img_path))
                conn.commit()
                st.success(f"Bahan baku '{name}' berhasil disimpan!")
                st.rerun()
            else:
                st.error("Nama dan stok harus diisi!")

    st.subheader("📋 Daftar Stok Bahan Baku Saat Ini")
    df_mats = pd.read_sql("SELECT * FROM raw_materials", conn)
    
    if not df_mats.empty:
        # Format Tampilan Harga Lebih Rapi
        df_display = df_mats.copy()
        df_display['cost_per_unit_formatted'] = df_display['cost_per_unit'].apply(lambda x: f"Rp {x:,.2f}" if pd.notnull(x) else "Rp 0")
        
        st.dataframe(
            df_display[['id', 'name', 'unit', 'stock', 'cost_per_unit_formatted', 'image']],
            column_config={
                "cost_per_unit_formatted": "Harga Satuan (Cost/Unit)",
                "stock": "Sisa Stok",
                "unit": "Satuan",
                "name": "Nama Bahan Baku",
                "image": "Path Gambar"
            },
            use_container_width=True,
            hide_index=True
        )

        st.markdown("---")
        st.subheader("⚙️ Edit / Hapus Bahan Baku")
        selected_id = st.selectbox("Pilih Bahan Baku yang Akan Diubah/Dihapus", df_mats['id'].tolist(), format_func=lambda x: df_mats[df_mats['id']==x]['name'].values[0])
        
        item_data = df_mats[df_mats['id'] == selected_id].iloc[0]
        col_e1, col_e2, col_e3 = st.columns(3)
        
        with col_e1:
            new_stock = st.number_input("Update Stok", value=float(item_data['stock']))
        with col_e2:
            new_cost_unit = st.number_input("Update Harga Satuan (Rp)", value=float(item_data['cost_per_unit']))
        with col_e3:
            st.write("Aksi:")
            if st.button("💾 Update Data"):
                c.execute("UPDATE raw_materials SET stock=?, cost_per_unit=? WHERE id=?", (new_stock, new_cost_unit, selected_id))
                conn.commit()
                st.success("Data berhasil diupdate!")
                st.rerun()
            if st.button("🗑️ Hapus Bahan"):
                c.execute("DELETE FROM raw_materials WHERE id=?", (selected_id,))
                conn.commit()
                st.warning("Bahan baku berhasil dihapus!")
                st.rerun()

        # Deteksi Bahan Menipis
        low_stock = df_mats[df_mats['stock'] < 10]
        if not low_stock.empty:
            st.warning("⚠️ **Peringatan Bahan Baku Menipis (< 10 unit):**")
            st.dataframe(low_stock[['name', 'stock', 'unit']], hide_index=True)
    else:
        st.info("Belum ada data bahan baku.")

# ---------------------------------------------------------
# MENU 3: KELOLA PRODUK & PERHITUNGAN HPP
# ---------------------------------------------------------
elif menu == "🍔 Kelola Produk & Perhitungan HPP":
    st.header("🍔 Kelola Produk & Kalkulasi HPP (Bahan + Overhead)")
    
    st.subheader("1. Input Biaya Operasional (Listrik, Air, Gaji, dll)")
    col_a, col_b = st.columns(2)
    with col_a:
        b_listrik = st.number_input("Biaya Listrik & Air / Bulan (Rp)", value=500000)
        b_tenaga = st.number_input("Biaya Tenaga Kerja / Bulan (Rp)", value=2000000)
    with col_b:
        b_bensin = st.number_input("Biaya Operasional / Bensin / Bulan (Rp)", value=300000)
        est_penjualan = st.number_input("Estimasi Total Produk Terjual / Bulan (Pcs)", value=1000)
    
    overhead_per_pcs = (b_listrik + b_tenaga + b_bensin) / (est_penjualan if est_penjualan > 0 else 1)
    st.info(f"💡 **Beban Biaya Overhead per Satuan Produk:** Rp {overhead_per_pcs:,.2f}")

    st.markdown("---")
    st.subheader("2. Tambah Produk Jualan & Resep Bahan Baku")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_name = st.text_input("Nama Produk Jualan")
        p_price = st.number_input("Harga Jual Produk (Rp)", min_value=0.0)
    with col_p2:
        p_img = st.file_uploader("Upload Foto Produk (Opsional)", type=["jpg", "png", "jpeg"])

    mats_df = pd.read_sql("SELECT id, name, unit, cost_per_unit FROM raw_materials", conn)
    
    selected_recipe = []
    hpp_bahan = 0.0
    
    st.write("**Resep Bahan Baku yang Digunakan:**")
    if not mats_df.empty:
        for idx, row in mats_df.iterrows():
            qty_used = st.number_input(f"Penggunaan {row['name']} ({row['unit']}) per Porsi", min_value=0.0, key=f"mat_{row['id']}")
            if qty_used > 0:
                cost = qty_used * row['cost_per_unit']
                hpp_bahan += cost
                selected_recipe.append((row['id'], qty_used))
                
        total_hpp_satuan = hpp_bahan + overhead_per_pcs
        
        st.markdown(f"""
        ### 📊 Ringkasan HPP Produk:
        * **HPP Bahan Baku:** Rp {hpp_bahan:,.2f}
        * **Biaya Overhead:** Rp {overhead_per_pcs:,.2f}
        * **TOTAL HPP SATUAN:** **Rp {total_hpp_satuan:,.2f}**
        * **Estimasi Margin Keuntungan:** Rp {p_price - total_hpp_satuan:,.2f}
        """)
        
        if st.button("💾 Simpan Produk Jualan", type="primary"):
            if p_name and p_price > 0:
                img_path = save_uploaded_file(p_img)
                c.execute("INSERT INTO products (name, price, hpp, image) VALUES (?, ?, ?, ?)", (p_name, p_price, total_hpp_satuan, img_path))
                p_id = c.lastrowid
                for m_id, q in selected_recipe:
                    c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_id, m_id, q))
                conn.commit()
                st.success(f"Produk '{p_name}' berhasil disimpan!")
                st.rerun()
            else:
                st.error("Isi nama produk dan harga jual terlebih dahulu!")
    else:
        st.warning("Tambahkan bahan baku terlebih dahulu di menu Bahan Baku!")

# ---------------------------------------------------------
# MENU 4: LAPORAN & FILTER TRANSAKSI
# ---------------------------------------------------------
elif menu == "📊 Laporan Transaksi & Analisis":
    st.header("📊 Laporan Penjualan & Analisis Produk")
    
    df_tx = pd.read_sql("SELECT * FROM transactions", conn)
    
    if not df_tx.empty:
        col_l1, col_l2 = st.columns(2)
        with col_l1:
            st.metric("Total Omset Penjualan", f"Rp {df_tx['total'].sum():,.0f}")
        with col_l2:
            st.metric("Total Transaksi", f"{len(df_tx)} Transaksi")
            
        st.subheader("📈 Daftar Riwayat Transaksi")
        st.dataframe(df_tx, use_container_width=True, hide_index=True)
        
        st.subheader("💳 Metode Pembayaran Digunakan")
        st.bar_chart(df_tx['payment_method'].value_counts())
    else:
        st.info("Belum ada data transaksi yang tercatat.")

# ---------------------------------------------------------
# MENU 5: PENGATURAN STRUK & PRINTER
# ---------------------------------------------------------
elif menu == "⚙️ Pengaturan Struk & Printer":
    st.header("⚙️ Custom Struk Penjualan")
    
    c.execute("SELECT value FROM settings WHERE key='receipt_header'")
    header_val = c.fetchone()[0]
    c.execute("SELECT value FROM settings WHERE key='receipt_footer'")
    footer_val = c.fetchone()[0]
    
    new_header = st.text_area("Header Struk (Tulisan Bagian Atas Struk)", value=header_val)
    new_footer = st.text_area("Footer Struk (Tulisan Bagian Bawah Struk)", value=footer_val)
    
    if st.button("💾 Simpan Pengaturan Struk"):
        c.execute("UPDATE settings SET value=? WHERE key='receipt_header'", (new_header,))
        c.execute("UPDATE settings SET value=? WHERE key='receipt_footer'", (new_footer,))
        conn.commit()
        st.success("Pengaturan tulisan struk berhasil diperbarui!")

# ---------------------------------------------------------
# MENU 6: KELOLA USER
# ---------------------------------------------------------
elif menu == "👥 Kelola User":
    if st.session_state['role'] != 'Admin':
        st.error("Akses ditolak. Menu ini hanya dapat diakses oleh Admin.")
    else:
        st.header("👥 Manajemen Pengguna")
        col_u1, col_u2 = st.columns(2)
        with col_u1:
            new_user = st.text_input("Username Baru")
            new_pass = st.text_input("Password Baru", type="password")
            new_role = st.selectbox("Role / Hak Akses", ["Kasir", "Admin"])
            
            if st.button("➕ Tambah User Baru"):
                if new_user and new_pass:
                    c.execute("INSERT INTO users (username, password, role) VALUES (?, ?, ?)", (new_user, new_pass, new_role))
                    conn.commit()
                    st.success(f"User '{new_user}' berhasil ditambahkan!")
                    st.rerun()
                else:
                    st.error("Lengkapi username dan password!")
                    
        with col_u2:
            st.subheader("Daftar Pengguna Aplikasi")
            users_df = pd.read_sql("SELECT id, username, role FROM users", conn)
            st.dataframe(users_df, hide_index=True, use_container_width=True)
