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

c.execute('''CREATE TABLE IF NOT EXISTS users (id INTEGER PRIMARY KEY, username TEXT, password TEXT, role TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS raw_materials (id INTEGER PRIMARY KEY, name TEXT, unit TEXT, stock REAL, cost_per_unit REAL, image TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS products (id INTEGER PRIMARY KEY, sku TEXT, name TEXT, category TEXT, price REAL, hpp REAL, stock REAL DEFAULT 100, image TEXT, is_draft INTEGER DEFAULT 0)''')
c.execute('''CREATE TABLE IF NOT EXISTS recipes (id INTEGER PRIMARY KEY, product_id INT, material_id INT, qty REAL)''')
c.execute('''CREATE TABLE IF NOT EXISTS transactions (id INTEGER PRIMARY KEY, date TEXT, total REAL, payment_method TEXT, user TEXT)''')
c.execute('''CREATE TABLE IF NOT EXISTS settings (key TEXT PRIMARY KEY, value TEXT)''')
conn.commit()

# Autoupdate skema database
try:
    c.execute("ALTER TABLE products ADD COLUMN sku TEXT")
except:
    pass

try:
    c.execute("ALTER TABLE products ADD COLUMN category TEXT")
except:
    pass

try:
    c.execute("ALTER TABLE products ADD COLUMN is_draft INTEGER DEFAULT 0")
except:
    pass
conn.commit()

# Default Settings & Admin
c.execute("INSERT OR IGNORE INTO users VALUES (1, 'admin', 'admin123', 'Admin')")
c.execute("INSERT OR IGNORE INTO settings VALUES ('receipt_header', 'SELAMAT DATANG DI NGE CAFE')")
c.execute("INSERT OR IGNORE INTO settings VALUES ('receipt_footer', 'Terima Kasih Atas Kunjungan Anda!')")
c.execute("INSERT OR IGNORE INTO settings VALUES ('overhead_percent', '20')")
conn.commit()

# Daftar Kategori Terbaru
LIST_KATEGORI = ["Kopi", "Non Kopi", "Dessert", "Main Course", "Lain-lain"]

# ---------------------------------------------------------
# AUTHENTICATION & CONFIG
# ---------------------------------------------------------
st.set_page_config(page_title="Sistem POS & HPP NGE' CAFE", layout="wide")

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
    "⚙️ Pengaturan System & Overhead",
    "👥 Kelola User"
])

if st.sidebar.button("Logout"):
    st.session_state['logged_in'] = False
    st.rerun()

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
    col_catalog, col_cart = st.columns([2.5, 1.2])
    
    with col_catalog:
        search_query = st.text_input("🔍 Scan barcode / cari nama produk...", placeholder="Ketik nama atau SKU...")
        
        products = pd.read_sql("SELECT * FROM products WHERE is_draft = 0 OR is_draft IS NULL", conn)
        
        if search_query and not products.empty:
            products = products[
                products['name'].str.contains(search_query, case=False, na=False) |
                products['sku'].astype(str).str.contains(search_query, case=False, na=False)
            ]
            
        if 'cart' not in st.session_state:
            st.session_state['cart'] = []

        if products.empty:
            st.info("Tidak ada produk aktif ditemukan.")
        else:
            cols = st.columns(4)
            for idx, row in products.reset_index(drop=True).iterrows():
                with cols[idx % 4]:
                    with st.container(border=True):
                        if row['image'] and os.path.exists(row['image']):
                            st.image(row['image'], use_container_width=True)
                        else:
                            st.write("🖼️ *Tanpa Gambar*")
                        st.markdown(f"**{row['name']}**")
                        st.markdown(f"<h5 style='color: #1E88E5; margin:0;'>Rp {row['price']:,.0f}</h5>", unsafe_allow_html=True)
                        
                        stock_val = row.get('stock', 100) if pd.notnull(row.get('stock')) else 100
                        st.caption(f"Stok: {stock_val:g}")
                        
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
                
                paid_amount = total
                change = 0.0
                can_process = True

                if pay_method == "Cash":
                    paid_amount = st.number_input("Nominal Pembayaran (Rp)", min_value=0.0, value=float(total), step=5000.0)
                    change = paid_amount - total
                    if change >= 0:
                        st.success(f"💵 **Kembalian: Rp {change:,.0f}**")
                    else:
                        st.error(f"⚠️ Pembayaran kurang Rp {abs(change):,.0f}")
                        can_process = False

                if st.button("💳 BAYAR SEKARANG", type="primary", use_container_width=True, disabled=not can_process):
                    now = datetime.now().strftime("%Y-%m-%d %H:%M:%S")
                    c.execute("INSERT INTO transactions (date, total, payment_method, user) VALUES (?, ?, ?, ?)",
                              (now, total, pay_method, st.session_state['username']))
                    
                    for _, item in summary.iterrows():
                        c.execute("UPDATE products SET stock = COALESCE(stock, 0) - ? WHERE id=?", (item['qty'], item['id']))
                            
                        c.execute("SELECT material_id, qty FROM recipes WHERE product_id=?", (item['id'],))
                        recipes = c.fetchall()
                        for mat_id, req_qty in recipes:
                            total_deduct = req_qty * item['qty']
                            c.execute("UPDATE raw_materials SET stock = COALESCE(stock, 0) - ? WHERE id=?", (total_deduct, mat_id))
                    
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
# MENU 2: KELOLA & EDIT PRODUK
# ---------------------------------------------------------
elif menu == "📝 Kelola & Edit Produk":
    col_hdr1, col_hdr2 = st.columns([3, 1])
    with col_hdr1:
        st.title("Produk")
        st.caption("Kelola produk, barcode, harga jual & HPP")
    with col_hdr2:
        df_export = pd.read_sql("SELECT * FROM products", conn)
        if not df_export.empty:
            csv_data = df_export.to_csv(index=False).encode('utf-8')
            st.download_button("⬇️ Export CSV", data=csv_data, file_name="data_produk.csv", mime="text/csv", use_container_width=True)

    st.markdown("---")

    f_col1, f_col2, f_col3 = st.columns([4, 2, 2])
    with f_col1:
        search_kw = st.text_input("Cari", placeholder="🔍 Cari nama, SKU, barcode...", label_visibility="collapsed")
    with f_col2:
        cat_filter = st.selectbox("Kategori", ["Semua Kategori"] + LIST_KATEGORI, label_visibility="collapsed")
    with f_col3:
        status_filter = st.selectbox("Status", ["Semua Status", "Aktif", "Draft"], label_visibility="collapsed")

    # PANEL EDIT PRODUK & BAHAN BAKU / DRAFT
    if 'edit_product_id' in st.session_state:
        st.markdown("---")
        st.subheader("✏️ Edit Data Produk & Resep Bahan Baku")
        p_edit_id = st.session_state['edit_product_id']
        c.execute("SELECT * FROM products WHERE id=?", (p_edit_id,))
        p_data = c.fetchone()
        
        if p_data:
            c.execute("SELECT value FROM settings WHERE key='overhead_percent'")
            res_ovh = c.fetchone()
            overhead_pct = float(res_ovh[0]) if res_ovh else 20.0

            c.execute("SELECT material_id, qty FROM recipes WHERE product_id=?", (p_edit_id,))
            old_recipes = dict(c.fetchall())

            with st.container(border=True):
                col_e1, col_e2, col_e3 = st.columns(3)
                with col_e1:
                    e_name = st.text_input("Nama Produk", value=p_data[2])
                    e_sku = st.text_input("SKU / Barcode", value=p_data[1] if p_data[1] else "")
                    e_img = st.file_uploader("Ganti Foto Produk (Opsional)", type=["jpg", "png", "jpeg"])
                with col_e2:
                    curr_cat_idx = LIST_KATEGORI.index(p_data[3]) if p_data[3] in LIST_KATEGORI else 0
                    e_category = st.selectbox("Kategori Produk", LIST_KATEGORI, index=curr_cat_idx)
                    e_price = st.number_input("Harga Jual (Rp)", value=float(p_data[4]))
                with col_e3:
                    e_stock = st.number_input("Stok Jual", value=float(p_data[6]) if p_data[6] is not None else 0.0)
                    e_status = st.selectbox("Status Produk", ["Draft", "Aktif"], index=0 if p_data[8] == 1 else 1)
                    if p_data[7] and os.path.exists(p_data[7]):
                        st.caption("Gambar Saat Ini:")
                        st.image(p_data[7], width=70)

                st.markdown("---")
                st.subheader("🥣 Edit Bahan Baku / Resep Porsi")
                
                mats_df = pd.read_sql("SELECT id, name, unit, cost_per_unit FROM raw_materials", conn)
                updated_recipes = []
                total_bahan_cost = 0.0

                if not mats_df.empty:
                    st.caption("Masukkan takaran bahan baku per porsi/satuan:")
                    for idx, row in mats_df.iterrows():
                        old_qty = old_recipes.get(row['id'], 0.0)
                        req_qty = st.number_input(f"Takaran {row['name']} ({row['unit']})", min_value=0.0, value=float(old_qty), key=f"edit_mat_{row['id']}")
                        if req_qty > 0:
                            total_bahan_cost += req_qty * row['cost_per_unit']
                            updated_recipes.append((row['id'], req_qty))

                overhead_val = total_bahan_cost * (overhead_pct / 100.0)
                new_hpp_satuan = total_bahan_cost + overhead_val
                new_profit = e_price - new_hpp_satuan
                new_margin = (new_profit / e_price * 100) if e_price > 0 else 0.0

                st.markdown("---")
                st.markdown("#### 📊 Kalkulasi HPP Terbaru")
                cm1, cm2, cm3, cm4 = st.columns(4)
                cm1.metric("HPP Bahan", f"Rp {total_bahan_cost:,.2f}")
                cm2.metric(f"Overhead ({overhead_pct}%)", f"Rp {overhead_val:,.2f}")
                cm3.metric("TOTAL HPP PER PORSI", f"Rp {new_hpp_satuan:,.2f}")
                cm4.metric("Margin Profit", f"{new_margin:.2f}% (Rp {new_profit:,.0f})")

                st.markdown("---")
                btn_c1, btn_c2, btn_c3 = st.columns(3)
                
                img_path = save_uploaded_file(e_img) if e_img else p_data[7]

                with btn_c1:
                    if st.button("🚀 Simpan & Aktifkan Produk", type="primary", use_container_width=True):
                        c.execute("UPDATE products SET name=?, sku=?, category=?, price=?, hpp=?, stock=?, image=?, is_draft=0 WHERE id=?", 
                                  (e_name, e_sku, e_category, e_price, new_hpp_satuan, e_stock, img_path, p_edit_id))
                        c.execute("DELETE FROM recipes WHERE product_id=?", (p_edit_id,))
                        for m_id, q_qty in updated_recipes:
                            c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_edit_id, m_id, q_qty))
                        conn.commit()
                        del st.session_state['edit_product_id']
                        st.success(f"Produk '{e_name}' berhasil direvisi & DIPUBLIKASIKAN (AKTIF)!")
                        st.rerun()

                with btn_c2:
                    if st.button("💾 Simpan Perubahan (Tetap Draft)", use_container_width=True):
                        is_draft_code = 1 if e_status == "Draft" else 0
                        c.execute("UPDATE products SET name=?, sku=?, category=?, price=?, hpp=?, stock=?, image=?, is_draft=? WHERE id=?", 
                                  (e_name, e_sku, e_category, e_price, new_hpp_satuan, e_stock, img_path, is_draft_code, p_edit_id))
                        c.execute("DELETE FROM recipes WHERE product_id=?", (p_edit_id,))
                        for m_id, q_qty in updated_recipes:
                            c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_edit_id, m_id, q_qty))
                        conn.commit()
                        del st.session_state['edit_product_id']
                        st.success(f"Perubahan produk '{e_name}' berhasil disimpan!")
                        st.rerun()

                with btn_c3:
                    if st.button("❌ Batal Edit", use_container_width=True):
                        del st.session_state['edit_product_id']
                        st.rerun()

    st.markdown("<br>", unsafe_allow_html=True)
    df_products = pd.read_sql("SELECT * FROM products", conn)

    if df_products.empty:
        st.info("Belum ada data produk terdaftar.")
    else:
        if status_filter == "Aktif":
            df_products = df_products[(df_products['is_draft'] == 0) | (df_products['is_draft'].isna())]
        elif status_filter == "Draft":
            df_products = df_products[df_products['is_draft'] == 1]

        if cat_filter != "Semua Kategori":
            df_products = df_products[df_products['category'] == cat_filter]

        if search_kw:
            df_products = df_products[
                df_products['name'].str.contains(search_kw, case=False, na=False) |
                df_products['sku'].astype(str).str.contains(search_kw, case=False, na=False)
            ]

        h1, h2, h3, h4, h5, h6, h7, h8, h9 = st.columns([0.8, 1.5, 2.5, 1.8, 1.5, 1.5, 1.0, 1.0, 1.5])
        with h1: st.caption("**GAMBAR**")
        with h2: st.caption("**SKU/BARCODE**")
        with h3: st.caption("**NAMA**")
        with h4: st.caption("**KATEGORI**")
        with h5: st.caption("**HARGA**")
        with h6: st.caption("**HPP**")
        with h7: st.caption("**STOK**")
        with h8: st.caption("**STATUS**")
        with h9: st.caption("**AKSI**")

        st.divider()

        for idx, row in df_products.iterrows():
            c1, c2, c3, c4, c5, c6, c7, c8, c9 = st.columns([0.8, 1.5, 2.5, 1.8, 1.5, 1.5, 1.0, 1.0, 1.5])
            
            with c1:
                if row['image'] and os.path.exists(row['image']):
                    st.image(row['image'], width=45)
                else:
                    st.markdown("🖼️")

            with c2:
                sku_val = row.get('sku') if pd.notnull(row.get('sku')) and row.get('sku') != '' else f"DPT-{row['id']:06d}"
                st.caption(f"`{sku_val}`")

            with c3:
                st.markdown(f"**{row['name'] if row['name'] else '(Tanpa Nama)'}**")

            with c4:
                cat_val = row.get('category') if pd.notnull(row.get('category')) and row.get('category') != '' else "Umum"
                st.write(cat_val)

            with c5:
                st.markdown(f"**Rp {row['price']:,.0f}**")

            with c6:
                hpp_val = row['hpp'] if pd.notnull(row['hpp']) else 0
                st.caption(f"Rp {hpp_val:,.0f} ⚙️")

            with c7:
                st_val = row.get('stock', 0) if pd.notnull(row.get('stock')) else 0
                st.write(f"{st_val:g} pcs")

            with c8:
                if row.get('is_draft') == 1:
                    st.markdown("<span style='background-color:#FFF3CD; color:#856404; padding:3px 8px; border-radius:12px; font-size:12px; font-weight:bold;'>Draft</span>", unsafe_allow_html=True)
                else:
                    st.markdown("<span style='background-color:#D4EDDA; color:#155724; padding:3px 8px; border-radius:12px; font-size:12px; font-weight:bold;'>Aktif</span>", unsafe_allow_html=True)

            with c9:
                act_col1, act_col2 = st.columns(2)
                with act_col1:
                    if st.button("Edit", key=f"edt_{row['id']}"):
                        st.session_state['edit_product_id'] = row['id']
                        st.rerun()
                with act_col2:
                    if st.button("❌", key=f"del_{row['id']}"):
                        c.execute("DELETE FROM products WHERE id=?", (row['id'],))
                        c.execute("DELETE FROM recipes WHERE product_id=?", (row['id'],))
                        conn.commit()
                        st.rerun()

            st.markdown("<hr style='margin: 4px 0; border: 0.5px solid #f0f2f6;'>", unsafe_allow_html=True)

# ---------------------------------------------------------
# MENU 3: INPUT & STOK BAHAN BAKU
# ---------------------------------------------------------
elif menu == "📦 Input & Stok Bahan Baku":
    st.header("📦 Manajemen Bahan Baku, Restock & Modal Terendap")

    # AKUMULASI DRAFT DATA MODAL BELUM TEROLAH
    df_mats_all = pd.read_sql("SELECT * FROM raw_materials", conn)
    total_modal_terendap = 0.0
    if not df_mats_all.empty:
        df_mats_all['nilai_modal'] = df_mats_all['stock'] * df_mats_all['cost_per_unit']
        total_modal_terendap = df_mats_all['nilai_modal'].sum()

    st.metric(label="💰 **TOTAL MODAL BAHAN BAKU BELUM TEROLAH (SISA STOK)**", value=f"Rp {total_modal_terendap:,.2f}")
    st.markdown("---")
    
    # FORM INPUT / RESTOCK BAHAN BAKU DENGAN AUTO RESET ST-FORM
    with st.expander("➕ Input Bahan Baku Baru / Restock Barang Datang", expanded=True):
        with st.form("form_tambah_bahan", clear_on_submit=True):
            col1, col2 = st.columns(2)
            with col1:
                name = st.text_input("Nama Bahan Baku (Contoh: Biji Kopi, Susu UHT)")
                unit = st.selectbox("Satuan Unit", ["Gram", "ML", "Pcs", "Kg", "Liter"])
                img_file = st.file_uploader("Upload Gambar Bahan Baku (Opsional)", type=["jpg", "png", "jpeg"])
            with col2:
                stock_input = st.number_input("Jumlah Stok Masuk / Datang Baru", min_value=0.0, step=1.0)
                cost_total_input = st.number_input("Total Nominal Belanja Pembelian Ini (Rp)", min_value=0.0, step=1000.0)
            
            btn_submit = st.form_submit_button("💾 Simpan Bahan Baku Datang", type="primary", use_container_width=True)

        if btn_submit:
            if stock_input > 0 and name:
                new_cost_per_unit = cost_total_input / stock_input if stock_input > 0 else 0
                img_path = save_uploaded_file(img_file)

                # CEK APAKAH BAHAN BAKU SUDAH ADA SEBELUMNYA (RESTOCK)
                c.execute("SELECT id, stock, cost_per_unit, image FROM raw_materials WHERE LOWER(name)=LOWER(?)", (name.strip(),))
                existing_item = c.fetchone()

                if existing_item:
                    # AKUMULASI STOK & HARGA UNTUK ITEM LAMA
                    old_id, old_stock, old_cost, old_img = existing_item
                    accumulated_stock = old_stock + stock_input
                    final_img = img_path if img_path else old_img
                    
                    c.execute("UPDATE raw_materials SET stock=?, cost_per_unit=?, image=? WHERE id=?", 
                              (accumulated_stock, new_cost_per_unit, final_img, old_id))
                    conn.commit()
                    st.success(f"✅ **Restock Berhasil!** Stok '{name}' otomatis bertambah +{stock_input} {unit} (Total Stok: {accumulated_stock:g} {unit}). Total Belanja Transaksi Ini: Rp {cost_total_input:,.0f}")
                else:
                    # INPUT SEBAGAI ITEM BAHAN BAKU BARU
                    c.execute("INSERT INTO raw_materials (name, unit, stock, cost_per_unit, image) VALUES (?, ?, ?, ?, ?)",
                              (name.strip(), unit, stock_input, new_cost_per_unit, img_path))
                    conn.commit()
                    st.success(f"✅ Bahan baku baru '{name}' berhasil tersimpan dengan total belanja Rp {cost_total_input:,.0f}!")
                st.rerun()
            else:
                st.error("Nama bahan dan jumlah stok harus diisi!")

    # PANEL EDIT BAHAN BAKU SISI SAMPING (JIKA AKSI EDIT DIKLIK)
    if 'edit_material_id' in st.session_state:
        m_id = st.session_state['edit_material_id']
        c.execute("SELECT * FROM raw_materials WHERE id=?", (m_id,))
        m_curr = c.fetchone()
        
        if m_curr:
            st.markdown("---")
            with st.container(border=True):
                st.subheader(f"✏️ Edit Bahan Baku: {m_curr[1]}")
                col_em1, col_em2, col_em3 = st.columns(3)
                with col_em1:
                    e_m_name = st.text_input("Nama Bahan Baku", value=m_curr[1])
                    e_m_unit = st.selectbox("Satuan", ["Gram", "ML", "Pcs", "Kg", "Liter"], index=["Gram", "ML", "Pcs", "Kg", "Liter"].index(m_curr[2]) if m_curr[2] in ["Gram", "ML", "Pcs", "Kg", "Liter"] else 0)
                with col_em2:
                    e_m_stock = st.number_input("Sisa Stok", value=float(m_curr[3]))
                    e_m_cost = st.number_input("Harga Per Satuan / Cost per Unit (Rp)", value=float(m_curr[4]))
                with col_em3:
                    e_m_img = st.file_uploader("Ganti Gambar", type=["jpg", "png", "jpeg"])
                    if m_curr[5] and os.path.exists(m_curr[5]):
                        st.image(m_curr[5], width=60)
                
                b1, b2 = st.columns(2)
                with b1:
                    if st.button("💾 Simpan Perubahan Bahan", type="primary", use_container_width=True):
                        new_m_img = save_uploaded_file(e_m_img) if e_m_img else m_curr[5]
                        c.execute("UPDATE raw_materials SET name=?, unit=?, stock=?, cost_per_unit=?, image=? WHERE id=?",
                                  (e_m_name, e_m_unit, e_m_stock, e_m_cost, new_m_img, m_id))
                        conn.commit()
                        del st.session_state['edit_material_id']
                        st.success("Bahan baku berhasil diperbarui!")
                        st.rerun()
                with b2:
                    if st.button("Batal Edit Bahan", use_container_width=True):
                        del st.session_state['edit_material_id']
                        st.rerun()

    st.markdown("---")
    st.subheader("📋 Daftar & Nilai Modal Bahan Baku Terendap")
    df_mats = pd.read_sql("SELECT * FROM raw_materials", conn)
    
    if not df_mats.empty:
        df_mats['nilai_terendap'] = df_mats['stock'] * df_mats['cost_per_unit']

        # HEADER TABEL BAHAN BAKU
        h_m1, h_m2, h_m3, h_m4, h_m5, h_m6, h_m7 = st.columns([0.8, 2.0, 1.0, 1.2, 1.5, 1.8, 1.2])
        with h_m1: st.caption("**GAMBAR**")
        with h_m2: st.caption("**NAMA BAHAN**")
        with h_m3: st.caption("**SATUAN**")
        with h_m4: st.caption("**SISA STOK**")
        with h_m5: st.caption("**HARGA SATUAN**")
        with h_m6: st.caption("**MODAL TERENDAP**")
        with h_m7: st.caption("**AKSI**")
        
        st.divider()

        # BARIS PER PRODUCT BAHAN BAKU DENGAN TOOLS DI KOLOM PALING UJUNG
        for idx, row in df_mats.iterrows():
            c_m1, c_m2, c_m3, c_m4, c_m5, c_m6, c_m7 = st.columns([0.8, 2.0, 1.0, 1.2, 1.5, 1.8, 1.2])
            
            with c_m1:
                if row['image'] and os.path.exists(row['image']):
                    st.image(row['image'], width=40)
                else:
                    st.markdown("📦")

            with c_m2:
                st.markdown(f"**{row['name']}**")

            with c_m3:
                st.write(row['unit'])

            with c_m4:
                st.write(f"{row['stock']:g}")

            with c_m5:
                cost_val = row['cost_per_unit'] if pd.notnull(row['cost_per_unit']) else 0
                st.write(f"Rp {cost_val:,.2f}")

            with c_m6:
                nilai_terendap_val = row['nilai_terendap'] if pd.notnull(row['nilai_terendap']) else 0
                st.markdown(f"**Rp {nilai_terendap_val:,.2f}**")

            with c_m7:
                act_m1, act_m2 = st.columns(2)
                with act_m1:
                    if st.button("✏️", key=f"edit_mat_btn_{row['id']}"):
                        st.session_state['edit_material_id'] = row['id']
                        st.rerun()
                with act_m2:
                    if st.button("❌", key=f"del_mat_btn_{row['id']}"):
                        c.execute("DELETE FROM raw_materials WHERE id=?", (row['id'],))
                        conn.commit()
                        st.rerun()

            st.markdown("<hr style='margin: 4px 0; border: 0.5px solid #f0f2f6;'>", unsafe_allow_html=True)

        low_stock = df_mats[df_mats['stock'] < 10]
        if not low_stock.empty:
            st.warning("⚠️ **Peringatan Bahan Baku Menipis (< 10 unit):**")
            st.dataframe(low_stock[['name', 'stock', 'unit']], hide_index=True)
    else:
        st.info("Belum ada data bahan baku.")

# ---------------------------------------------------------
# MENU 4: BUAT PRODUK & KALKULASI HPP
# ---------------------------------------------------------
elif menu == "🍔 Buat Produk & Kalkulasi HPP":
    st.header("🍔 Buat Produk Baru & Kalkulasi HPP")
    
    c.execute("SELECT value FROM settings WHERE key='overhead_percent'")
    res_ovh = c.fetchone()
    overhead_pct = float(res_ovh[0]) if res_ovh else 20.0

    st.info(f"💡 **Persentase Overhead Otomatis Aktif:** {overhead_pct}% (Dapat diubah di menu Pengaturan)")

    st.markdown("---")
    st.subheader("1. Informasi Produk Jualan")
    
    col_p1, col_p2, col_p3 = st.columns(3)
    with col_p1:
        p_sku = st.text_input("SKU / Barcode", placeholder="Contoh: DPT-000036 (Opsional)")
        p_name = st.text_input("Nama Produk Jualan")
    with col_p2:
        p_category = st.selectbox("Kategori Produk", LIST_KATEGORI)
        p_price = st.number_input("Harga Jual Produk (Rp)", min_value=0.0)
    with col_p3:
        p_stock = st.number_input("Stok Awal Jualan (Pcs)", min_value=1.0, value=100.0)
        p_img = st.file_uploader("Upload Foto Produk (Opsional)", type=["jpg", "png", "jpeg"])

    st.markdown("---")
    st.subheader("2. Resep Adonan & Bahan Baku")
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
                
        hpp_bahan_per_porsi = total_batch_cost / yield_qty
        overhead_per_porsi = hpp_bahan_per_porsi * (overhead_pct / 100.0)
        total_hpp_satuan = hpp_bahan_per_porsi + overhead_per_porsi
        
        profit_per_porsi = p_price - total_hpp_satuan
        margin_percent = (profit_per_porsi / p_price * 100) if p_price > 0 else 0.0
        
        st.markdown("---")
        st.subheader("📊 3. Ringkasan Kalkulasi HPP & Margin Keuntungan")
        
        c_m1, c_m2, c_m3 = st.columns(3)
        c_m1.metric("HPP Bahan / Porsi", f"Rp {hpp_bahan_per_porsi:,.2f}")
        c_m2.metric(f"Biaya Overhead ({overhead_pct}%)", f"Rp {overhead_per_porsi:,.2f}")
        c_m3.metric("TOTAL HPP PER PORSI", f"Rp {total_hpp_satuan:,.2f}")
        
        c_m4, c_m5 = st.columns(2)
        c_m4.metric("Profit (Rp) / Porsi", f"Rp {profit_per_porsi:,.2f}")
        c_m5.metric("Persentase Keuntungan (Margin %)", f"{margin_percent:.2f}%")

        st.markdown("---")
        
        btn_col1, btn_col2 = st.columns(2)
        with btn_col1:
            if st.button("💾 Simpan Produk Jualan (Aktif)", type="primary", use_container_width=True):
                if p_name and p_price > 0:
                    img_path = save_uploaded_file(p_img)
                    final_sku = p_sku if p_sku else f"DPT-{int(datetime.now().timestamp())}"
                    
                    c.execute("""
                        INSERT INTO products (sku, name, category, price, hpp, stock, image, is_draft) 
                        VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                    """, (final_sku, p_name, p_category, p_price, total_hpp_satuan, p_stock, img_path, 0))
                                  
                    p_id = c.lastrowid
                    for m_id, q_per_porsi in selected_recipe_per_portion:
                        c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_id, m_id, q_per_porsi))
                    conn.commit()
                    st.success(f"Produk '{p_name}' berhasil dipublikasikan & siap dijual!")
                    st.rerun()
                else:
                    st.error("Isi nama produk dan harga jual terlebih dahulu!")

        with btn_col2:
            if st.button("📝 Simpan Sebagai Draft", use_container_width=True):
                draft_name = p_name if p_name else "Draft Produk (Belum Selesai)"
                img_path = save_uploaded_file(p_img)
                final_sku = p_sku if p_sku else f"DPT-{int(datetime.now().timestamp())}"
                
                c.execute("""
                    INSERT INTO products (sku, name, category, price, hpp, stock, image, is_draft) 
                    VALUES (?, ?, ?, ?, ?, ?, ?, ?)
                """, (final_sku, draft_name, p_category, p_price, total_hpp_satuan, p_stock, img_path, 1))
                              
                p_id = c.lastrowid
                for m_id, q_per_porsi in selected_recipe_per_portion:
                    c.execute("INSERT INTO recipes (product_id, material_id, qty) VALUES (?, ?, ?)", (p_id, m_id, q_per_porsi))
                conn.commit()
                st.warning(f"Produk '{draft_name}' berhasil disimpan ke Draft.")
                st.rerun()
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
# MENU 6: PENGATURAN SYSTEM & OVERHEAD
# ---------------------------------------------------------
elif menu == "⚙️ Pengaturan System & Overhead":
    st.header("⚙️ Pengaturan Sistem & Overhead")
    
    st.subheader("💡 1. Pengaturan Overhead Global")
    c.execute("SELECT value FROM settings WHERE key='overhead_percent'")
    res_ovh = c.fetchone()
    current_ovh = float(res_ovh[0]) if res_ovh else 20.0
    
    new_ovh = st.number_input("Persentase Overhead Otomatis dari HPP Bahan Baku (%)", value=current_ovh, step=1.0, min_value=0.0)
    
    if st.button("💾 Simpan Persentase Overhead"):
        c.execute("UPDATE settings SET value=? WHERE key='overhead_percent'", (str(new_ovh),))
        conn.commit()
        st.success(f"Persentase Overhead berhasil diperbarui menjadi {new_ovh}%!")
        st.rerun()

    st.markdown("---")
    
    st.subheader("🧾 2. Custom Struk Penjualan")
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
