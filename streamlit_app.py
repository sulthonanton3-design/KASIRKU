import streamlit as st
import sqlite3
import pandas as pd
from datetime import datetime
import os

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
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, name TEXT, price REAL, hpp REAL, stock REAL DEFAULT 100, image TEXT)''')
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
st.set_page_config(page_title="Sistem POS & HPP Modern", layout="wide")

if 'logged_in' not in st.session_state:
    st.session_state['logged_in'] = False
    st.session_state['username'] = ''
    st.session_state['role'] = ''

def login():
    st.title("🔑 Login Kasir & Manajemen POS")
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
    "📝 Kelola & Edit Produk",
    "📦 Input & Stok Bahan Baku",
    "🍔 Buat Produk & Kalkulasi HPP",
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
# MENU 1: KASIR (POS LAYOUT MODERN)
# ---------------------------------------------------------
if menu == "🛒 Kasir (POS)":
    col_catalog, col_cart = st.columns([2.5, 1.2])
    
    with col_catalog:
        search_query = st.text_input("🔍 Scan barcode / cari nama produk...", placeholder="Ketik nama produk untuk mencari...")
        
        products = pd.read_sql("SELECT * FROM products", conn)
        
        if search_query:
            products = products[products['name'].str.contains(search_query, case=False, na=False)]
            
        if 'cart' not in st.session_state:
            st.session_state['cart'] = []

        if products.empty:
            st.info("Tidak ada produk ditemukan.")
        else:
            cols = st.columns(4)
            for idx, row in products.reset_index(drop=True).iterrows():
                with cols[idx % 4]:
                    with st.container(border=True):
                        if row['image'] and os.path.exists(row['image']):
                            st.image(row['image'], use_column_width=True)
                        else:
                            st.write("🖼️ *Tanpa Gambar*")
                        st.markdown(f"**{row['name']}**")
                        st.markdown(f"<h5 style='color: #1E88E5; margin:0;'>Rp {row['price']:,.0f}</h5>", unsafe_allow_html=True)
                        st.caption(f"Stok: {row['stock']}")
                        
                        if st.button(f"➕ Tambah", key=f"btn_add_{row['id']}", use_container_width=True):
                            st.session_state['cart'].append({"id": row['id'], "name": row['name'], "price": row['price']})
                            st.rerun()

    with col_cart:
        with st.container(border=True):
            st.markdown("### 🛒 Keranjang")
            if st.session_state['cart']:
                cart_df = pd.DataFrame(st.session_state['cart'])
                summary = cart_df.groupby(['id', 'name', 'price']).size().reset_index(name='qty')
                summary['subtotal'] = summary['price'] * summary['qty']
                
                for _, item in summary.iterrows():
                    c_info, c_btn = st.columns([3, 1])
                    with c_info:
                        st.write(f"**{item['name']}** x {item['qty']}")
                        st.caption(f"Rp {item['price']:,.0f} = Rp {item['subtotal']:,.0f}")
                    with c_btn:
                        if st.button("❌", key=f"del_{item['id']}"):
                            st.session_state['cart'] = [x for x in st.session_state['cart'] if x['id'] != item['id']]
                            st.rerun()
                    st.divider()
                
                subtotal = summary['subtotal'].sum()
                st.write(f"**Subtotal:** Rp {subtotal:,.0f}")
                
                discount = st.number_input("Diskon (Rp)", min_value=0.0, value=0.0, step=1000.0)
                total = max(0.0, subtotal - discount)
                
                st.markdown(f"## **TOTAL: Rp {total:,.0f}**")
                
                pay_method = st.selectbox("Metode Pembayaran", ["Cash", "Transfer Bank", "E-Wallet (QRIS)"])
                
                if st.button("💳 BAYAR SEKARANG", type="primary", use_container_width=True):
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute("INSERT INTO transactions (date, total, payment_method, user) VALUES (?, ?, ?, ?)",
                              (now, total, pay_method, st.session_state['username']))
                    
                    for _, item in summary.iterrows():
                        c.execute("UPDATE products SET stock = stock - ? WHERE id=?", (item['qty'], item['id']))
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
                    
                if st.button("🗑️ Kosongkan Keranjang", use_container_width=True):
                    st.session_state['cart'] = []
                    st.rerun()
            else:
                st.info("Keranjang kosong. Klik produk di sebelah kiri untuk menambahkan.")

# ---------------------------------------------------------
# MENU 2: KELOLA & EDIT PRODUK (FITUR BARU)
# ---------------------------------------------------------
elif menu == "📝 Kelola & Edit Produk":
    st.header("📝 Daftar & Adjustment Produk")
    st.caption("Gunakan menu ini untuk mengubah nama, harga, stok, atau menghapus produk yang terinput.")
    
    df_products = pd.read_sql("SELECT * FROM products", conn)
    
    if not df_products.empty:
        df_display = df_products.copy()
        df_display['price_fmt'] = df_display['price'].apply(lambda x: f"Rp {x:,.0f}")
        df_display['hpp_fmt'] = df_display['hpp'].apply(lambda x: f"Rp {x:,.2f}")
        
        st.subheader("📋 Daftar Produk Saat Ini")
        st.dataframe(
            df_display[['id', 'name', 'price_fmt', 'hpp_fmt', 'stock', 'image']],
            column_config={
                "id": "ID",
                "name": "Nama Produk",
                "price_fmt": "Harga Jual",
                "hpp_fmt": "HPP",
                "stock": "Stok Produk",
                "image": "Gambar Path"
            },
            hide_index=True,
            use_container_width=True
        )
        
        st.markdown("---")
        st.subheader("⚙️ Adjust / Edit / Hapus Produk")
        selected_prod_id = st.selectbox(
            "Pilih Produk yang Ingin Diubah",
            df_products['id'].tolist(),
            format_func=lambda x: df_products[df_products['id'] == x]['name'].values[0]
        )
        
        prod_data = df_products[df_products['id'] == selected_prod_id].iloc[0]
        
        col_ed1, col_ed2 = st.columns(2)
        with col_ed1:
            edit_name = st.text_input("Nama Produk", value=prod_data['name'])
            edit_price = st.number_input("Harga Jual (Rp)", value=float(prod_data['price']), step=1000.0)
            edit_hpp = st.number_input("HPP Produk (Rp)", value=float(prod_data['hpp']), step=500.0)
        with col_ed2:
            edit_stock = st.number_input("Jumlah Stok", value=float(prod_data['stock']), step=1.0)
            edit_img = st.file_uploader("Ganti Foto Produk (Opsional)", type=["jpg", "png", "jpeg"])
            if prod_data['image'] and os.path.exists(prod_data['image']):
                st.image(prod_data['image'], width=100, caption="Foto Saat Ini")
        
        col_act1, col_act2 = st.columns(2)
        with col_act1:
            if st.button("💾 Simpan Perubahan Produk", type="primary", use_container_width=True):
                if edit_img is not None:
                    img_path = save_uploaded_file(edit_img)
                else:
                    img_path = prod_data['image']
                    
                c.execute("UPDATE products SET name=?, price=?, hpp=?, stock=?, image=? WHERE id=?",
                          (edit_name, edit_price, edit_hpp, edit_stock, img_path, selected_prod_id))
                conn.commit()
                st.success(f"Produk '{edit_name}' berhasil diperbarui!")
                st.rerun()
        with col_act2:
            if st.button("🗑️ Hapus Produk Ini", use_container_width=True):
                c.execute("DELETE FROM products WHERE id=?", (selected_prod_id,))
                c.execute("DELETE FROM recipes WHERE product_id=?", (selected_prod_id,))
                conn.commit()
                st.warning("Produk dan resep terkait berhasil dihapus!")
                st.rerun()
    else:
        st.info("Belum ada produk terdaftar.")

# ---------------------------------------------------------
# MENU 3: INPUT & STOK BAHAN BAKU
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

        low_stock = df_mats[df_mats['stock'] < 10]
        if not low_stock.empty:
            st.warning("⚠️ **Peringatan Bahan Baku Menipis (< 10 unit):**")
            st.dataframe(low_stock[['name', 'stock', 'unit']], hide_index=True)
    else:
        st.info("Belum ada data bahan baku.")

# ---------------------------------------------------------
# MENU 4: BUAT PRODUK & PERHITUNGAN HPP
# ---------------------------------------------------------
elif menu == "🍔 Buat Produk & Kalkulasi HPP":
    st.header("🍔 Buat Produk Baru & Kalkulasi HPP")
    
    st.subheader("1. Input Biaya Operasional (Overhead)")
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
    st.subheader("2. Resep Adonan & Input Produk")
    
    col_p1, col_p2 = st.columns(2)
    with col_p1:
        p_name = st.text_input("Nama Produk Jualan")
        p_price = st.number_input("Harga Jual Produk (Rp)", min_value=0.0)
        p_stock = st.number_input("Stok Awal Jualan (Pcs)", min_value=1.0, value=100.0)
    with col_p2:
        p_img = st.file_uploader("Upload Foto Produk (Opsional)", type=["jpg", "png", "jpeg"])

    st.markdown("#### 🥣 Perhitungan Resep Sekali Buat (Batch/Adonan)")
    yield_qty = st.number_input("Sekali buat resep ini, jadi berapa porsi/pcs?", min_value=1.0, value=1.0, step=1.0)

    mats_df = pd.read_sql("SELECT id, name, unit, cost_per_unit FROM raw_materials", conn)
    
    selected_recipe_per_portion = []
    total_batch_cost = 0.0
    
    st.write("**Bahan Baku yang Digunakan untuk Sekali Buat (1 Batch):**")
    if not mats_df.empty:
        for idx, row in mats_df.iterrows():
            batch_qty = st.number_input(f"Bahan {row['name']} ({row['unit']}) yang dipakai sekali buat", min_value=0.0, key=f"mat_{row['id']}")
            if batch_qty > 0:
                cost_material = batch_qty * row['cost_per_unit']
                total_batch_cost += cost_material
                qty_per_portion = batch_qty / yield_qty
                selected_recipe_per_portion.append((row['id'], qty_per_portion))
                
        # Perhitungan HPP per Porsi
        hpp_bahan_per_porsi = total_batch_cost / yield_qty
        total_hpp_satuan = hpp_bahan_per_porsi + overhead_per_pcs
        profit_per_porsi = p_price - total_hpp_satuan
        margin_percent = (profit_per_porsi / p_price * 100) if p_price > 0 else 0.0
        
        st.markdown("---")
        st.subheader("📊 3. Ringkasan Kalkulasi HPP & Margin Keuntungan")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("HPP Bahan / Porsi", f"Rp {hpp_bahan_per_porsi:,.2f}")
        c_m2.metric("Overhead / Porsi", f"Rp {overhead_per_pcs:,.2f}")
        c_m3.metric("TOTAL HPP PER PORSI", f"Rp {total_hpp_satuan:,.2f}")
        
        c_m4, c_m5 = st.columns(2)
        c_m4.metric("Profit (Rp) / Porsi", f"Rp {profit_per_porsi:,.2f}")
        c_m5.metric("Persentase Keuntungan (Margin %)", f"{margin_percent:.2f}%")

        st.markdown("---")
        st.subheader("🎯 4. Simulasi Target Profit & Estimasi Modal")
        
        sim_col1, sim_col2 = st.columns(2)
        with sim_col1:
            st.markdown("##### 📌 Opsi A: Berdasarkan Target Profit Bulanan")
            target_profit_monthly = st.number_input("Target Profit Bersih / Bulan (Rp)", value=5000000, step=500000)
            if profit_per_porsi > 0:
                pcs_needed = target_profit_monthly / profit_per_porsi
                omset_needed = pcs_needed * p_price
                capital_needed = pcs_needed * hpp_bahan_per_porsi
                
                st.write(f"* Untuk profit **Rp {target_profit_monthly:,.0f}/bulan**:")
                st.write(f"  - Wajib Terjual: **{pcs_needed:,.0f} Pcs/Bulan** (~{pcs_needed/30:,.0f} pcs/hari)")
                st.write(f"  - Target Omset: **Rp {omset_needed:,.0f}**")
                st.write(f"  - Estimasi Modal Bahan: **Rp {capital_needed:,.0f}**")
            else:
                st.warning("Harga jual harus lebih tinggi dari HPP untuk menghitung target!")

        with sim_col2:
            st.markdown("##### 📌 Opsi B: Estimasi Modal Berdasarkan Rencana Produksi")
            plan_pcs = st.number_input("Rencana Jumlah Produksi (Pcs)", value=500, step=50)
            modal_bahan = plan_pcs * hpp_bahan_per_porsi
            est_omset = plan_pcs * p_price
            est_profit = plan_pcs * profit_per_porsi
            
            st.write(f"* Untuk produksi **{plan_pcs:,.0f} Pcs**:")
            st.write(f"  - **Estimasi Modal Bahan:** **Rp {modal_bahan:,.0f}**")
            st.write(f"  - Potensi Omset: **Rp {est_omset:,.0f}**")
            st.write(f"  - Potensi Profit Bersih: **Rp {est_profit:,.0f}**")

        st.markdown("---")
        if st.button("💾 Simpan Produk Jualan", type="primary"):
            if p_name and p_price > 0:
                img_path = save_uploaded_file(p_img)
                c.execute("INSERT INTO products (name, price, hpp, stock, image) VALUES (?, ?, ?, ?, ?)",
                          (p_name, p_price, total_hpp_satuan, p_stock, img_path))
                p_id = c.lastrowid
                for m_id, q_per_porsi in selected_recipe_per_portion:
                    c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_id, m_id, q_per_porsi))
                conn.commit()
                st.success(f"Produk '{p_name}' berhasil disimpan!")
                st.rerun()
            else:
                st.error("Isi nama produk dan harga jual terlebih dahulu!")
    else:
        st.warning("Tambahkan bahan baku terlebih dahulu di menu Bahan Baku!")

# ---------------------------------------------------------
# MENU 5: LAPORAN TRANSAKSI
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
# MENU 6: PENGATURAN STRUK
# ---------------------------------------------------------
elif menu == "⚙️ Pengaturan Struk & Printer":
    st.header("⚙️ Custom Struk Penjualan")
    c.execute("SELECT value FROM settings WHERE key='receipt_header'")
    header_val = c.fetchone()[0]
    c.execute("SELECT value FROM settings WHERE key='receipt_footer'")
    footer_val = c.fetchone()[0]
    
    new_header = st.text_area("Header Struk", value=header_val)
    new_footer = st.text_area("Footer Struk", value=footer_val)
    
    if st.button("💾 Simpan Pengaturan Struk"):
        c.execute("UPDATE settings SET value=? WHERE key='receipt_header'", (new_header,))
        c.execute("UPDATE settings SET value=? WHERE key='receipt_footer'", (new_footer,))
        conn.commit()
        st.success("Pengaturan tulisan struk berhasil diperbarui!")

# ---------------------------------------------------------
# MENU 7: KELOLA USER
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
