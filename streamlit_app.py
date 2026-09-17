import streamlit as st
import pandas as pd
from datetime import datetime

# Konfigurasi Halaman (Agar responsif di HP & PC)
st.set_page_config(
    page_title="POS & Dashboard Analisis Toko",
    page_icon="☕",
    layout="wide"
)

# Inisialisasi Session State untuk Simulasi Data & Keranjang
if 'cart' not in st.session_state:
    st.session_state.cart = []
if 'logged_in' not in st.session_state:
    st.session_state.logged_in = False
if 'role' not in st.session_state:
    st.session_state.role = ""
if 'username' not in st.session_state:
    st.session_state.username = ""
if 'cash_drawer' not in st.session_state:
    st.session_state.cash_drawer = 500000  # Modal awal kasir

# Dummy Data Produk (Bisa dikoneksikan ke Database/CSV nanti)
if 'products' not in st.session_state:
    st.session_state.products = [
        {"id": 1, "name": "Kopi Susu Gula Aren", "category": "Kopi", "price": 18000, "hpp": 10000, "stock": 15, "status": "safe"},
        {"id": 2, "name": "Matcha Latte", "category": "Non-Kopi", "price": 22000, "hpp": 13000, "stock": 3, "status": "warning"},
        {"id": 3, "name": "Croissant", "category": "Dessert", "price": 25000, "hpp": 16000, "stock": 0, "status": "empty"},
    ]

# 1. HALAMAN LOGIN
def login_page():
    st.title("🔐 Login Sistem Kasir & Admin")
    st.markdown("Silakan masuk menggunakan kredensial Anda.")
    
    with st.form("login_form"):
        u_input = st.text_input("Username / Email")
        p_input = st.text_input("Password", type="password")
        submit = st.form_submit_button("Login")
        
        if submit:
            if u_input == "admin" and p_input == "admin":
                st.session_state.logged_in = True
                st.session_state.role = "admin"
                st.session_state.username = "Owner / Admin"
                st.success("Login Berhasil sebagai Admin!")
                st.rerun()
            elif u_input == "kasir" and p_input == "kasir":
                st.session_state.logged_in = True
                st.session_state.role = "kasir"
                st.session_state.username = "Staff Kasir"
                st.success("Login Berhasil sebagai Kasir!")
                st.rerun()
            else:
                st.error("Username atau Password salah! (Gunakan admin/admin atau kasir/kasir)")

# 2. HALAMAN KASIR (POS)
def kasir_page():
    st.sidebar.title(f"👤 {st.session_state.username}")
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()
        
    if st.session_state.role == "admin":
        if st.sidebar.button("⬅️ Masuk ke Dashboard Admin"):
            st.session_state.current_view = "admin"
            st.rerun()

    st.title("🛒 Kasir / POS - NGE' CAFE")
    
    col1, col2 = st.columns([1.2, 1.8])
    
    with col1:
        st.subheader("Detail Pesanan")
        
        # Tampilkan isi keranjang
        if len(st.session_state.cart) == 0:
            st.info("Belum ada produk dipilih.")
        else:
            total_belanja = 0
            for idx, item in enumerate(st.session_state.cart):
                sub = item['price'] * item['qty']
                total_belanja += sub
                c_a, c_b, c_c = st.columns([3, 2, 1])
                c_a.text(f"{item['name']}")
                c_b.text(f"{item['qty']}x Rp {item['price']:,}")
                if c_c.button("❌", key=f"del_{idx}"):
                    st.session_state.cart.pop(idx)
                    st.rerun()
            
            st.divider()
            st.markdown(f"### **Total: Rp {total_belanja:,}**")
            
            # Metode Pembayaran
            pay_method = st.selectbox("Metode Pembayaran", ["Cash", "TF Bank", "QRIS"])
            cash_given = 0
            if pay_method == "Cash":
                cash_given = st.number_input("Nominal Uang Tunai (Rp)", min_value=0, step=1000)
                if cash_given >= total_belanja and cash_given > 0:
                    change = cash_given - total_belanja
                    st.success(f"Kembalian: **Rp {change:,}**")
                elif cash_given > 0:
                    st.warning("Uang tunai kurang dari total belanja!")

            if st.button("Proses Pembayaran & Cetak Struk", type="primary", use_container_width=True):
                if total_belanja > 0:
                    st.success("Transaksi Berhasil! Laci kasir terbuka & Struk tercetak.")
                    st.session_state.cash_drawer += total_belanja
                    st.session_state.cart = []
                    st.rerun()
                else:
                    st.warning("Keranjang masih kosong.")

    with col2:
        st.subheader("Katalog Produk")
        search_query = st.text_input("🔍 Cari Produk...", "")
        
        # Grid Produk
        cols = st.columns(3)
        for i, p in enumerate(st.session_state.products):
            if search_query.lower() in p['name'].lower():
                with cols[i % 3]:
                    # Warna Indikator Stok
                    badge_color = "🟢 Aman" if p['status'] == 'safe' else ("🟡 Kritis" if p['status'] == 'warning' else "🔴 Habis")
                    st.markdown(f"""
                    <div style="border:1px solid #ddd; padding:10px; border-radius:10px; margin-bottom:10px; background:white;">
                        <small>{p['category']}</small><br>
                        <b>{p['name']}</b><br>
                        <span style="color:blue; font-weight:bold;">Rp {p['price']:,}</span><br>
                        <small>Stok: {p['stock']} ({badge_color})</small>
                    </div>
                    """, unsafe_allow_html=True)
                    
                    if p['stock'] > 0:
                        if st.button("Pilih", key=f"prod_{p['id']}"):
                            # Masukkan ke keranjang
                            found = False
                            for item in st.session_state.cart:
                                if item['id'] == p['id']:
                                    item['qty'] += 1
                                    found = True
                                    break
                            if not found:
                                st.session_state.cart.append({**p, 'qty': 1})
                            st.rerun()
                    else:
                        st.button("Habis", disabled=True, key=f"empty_{p['id']}")

# 3. DASHBOARD ADMIN
def admin_page():
    st.sidebar.title("🛠️ Menu Admin")
    if st.sidebar.button("🔙 Kembali ke Mode Kasir"):
        st.session_state.current_view = "kasir"
        st.rerun()
    if st.sidebar.button("Logout"):
        st.session_state.logged_in = False
        st.rerun()

    menu = st.sidebar.radio("Navigasi Admin", ["Master Data Produk", "Laporan Penjualan & PnL", "Pengaturan Akun & Akses"])

    if menu == "Master Data Produk":
        st.title("📦 Master Data Produk & Stok")
        
        # Tambah Produk Baru
        with st.expander("➕ Tambah Produk / Resep Baru"):
            with st.form("add_product"):
                p_name = st.text_input("Nama Produk")
                p_cat = st.selectbox("Kategori", ["Kopi", "Non-Kopi", "Dessert", "Main Course"])
                p_price = st.number_input("Harga Jual (Rp)", min_value=0)
                p_hpp = st.number_input("HPP / Modal (Rp)", min_value=0)
                p_stock = st.number_input("Stok Awal", min_value=0)
                submitted = st.form_submit_button("Simpan Produk")
                if submitted:
                    new_id = len(st.session_state.products) + 1
                    status = "safe" if p_stock > 5 else ("warning" if p_stock > 0 else "empty")
                    st.session_state.products.append({
                        "id": new_id, "name": p_name, "category": p_cat, 
                        "price": p_price, "hpp": p_hpp, "stock": p_stock, "status": status
                    })
                    st.success("Produk berhasil ditambahkan!")
                    st.rerun()

        # Tabel Data Produk
        df_prod = pd.DataFrame(st.session_state.products)
        st.dataframe(df_prod, use_container_width=True)

    elif menu == "Laporan Penjualan & PnL":
        st.title("📊 Laporan Penjualan & Laba Rugi (PnL)")
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Omset Hari Ini", "Rp 1.450.000", "+12%")
        col2.metric("Total Transaksi", "45 Struk", "+5")
        col3.metric("Estimasi Net Profit", "Rp 580.000", "+8%")
        
        st.subheader("Ringkasan Arus Kas & Kasir")
        st.info(f"Uang Aktual di Laci Kasir Saat Ini: **Rp {st.session_state.cash_drawer:,}**")
        
        st.subheader("Riwayat PnL Singkat")
        pnl_data = pd.DataFrame([
            {"Tanggal": str(datetime.now().date()), "Omset": 1450000, "HPP Bahan": 650000, "Overhead": 120000, "Net Profit": 680000}
        ])
        st.dataframe(pnl_data, use_container_width=True)

    elif menu == "Pengaturan Akun & Akses":
        st.title("⚙️ Pengaturan Akun & Hak Akses Staff")
        st.markdown("Kelola email atau akun staff yang diizinkan masuk ke sistem.")
        
        users_df = pd.DataFrame([
            {"Email / Username": "admin@store.com", "Role": "Owner / Admin", "Akses Menu": "Full Akses"},
            {"Email / Username": "kasir1@store.com", "Role": "Staff Kasir", "Akses Menu": "Halaman Kasir Saja"},
            {"Email / Username": "kasir2@store.com", "Role": "Staff Kasir", "Akses Menu": "Halaman Kasir Saja"},
        ])
        st.dataframe(users_df, use_container_width=True)
        
        st.subheader("Tambah Akses Staff Baru")
        with st.form("new_access"):
            st.text_input("Email Google / Username Staff")
            st.selectbox("Hak Akses", ["Kasir Saja", "Admin & Kasir (Full)"])
            if st.form_submit_button("Berikan Akses"):
                st.success("Akses berhasil disimpan!")

# Logika Kontrol Navigasi Utama Aplikasi
if 'current_view' not in st.session_state:
    st.session_state.current_view = "kasir"

if not st.session_state.logged_in:
    login_page()
else:
    if st.session_state.role == "admin" and st.session_state.current_view == "admin":
        admin_page()
    else:
        kasir_page()
