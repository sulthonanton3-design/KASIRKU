import streamlit as st
import streamlit.components.v1 as components

# Konfigurasi Tampilan Halaman Streamlit
st.set_page_config(
    page_title="KASIRKU - POS System",
    page_icon="🛒",
    layout="wide",
    initial_sidebar_state="collapsed"
)

# Menghilangkan padding default Streamlit agar tampilan HTML full screen
st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        header { visibility: hidden; }
        footer { visibility: hidden; }
    </style>
""", unsafe_allow_html=True)

html_content = """<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>Kasirku - Pembuatan Product (Proses Produksi)</title>
    <style>
        * {
            box-sizing: border-box;
            font-family: -apple-system, BlinkMacSystemFont, "Segoe UI", Roboto, Helvetica, Arial, sans-serif;
            margin: 0;
            padding: 0;
        }

        body {
            background-color: #f4f6f9;
            color: #333;
            display: flex;
            min-height: 100vh;
        }

        /* Sidebar Styles */
        .sidebar {
            width: 240px;
            background-color: #ffffff;
            border-right: 1px solid #e5e7eb;
            padding: 20px 15px;
            display: flex;
            flex-direction: column;
            gap: 15px;
        }

        .brand {
            font-size: 20px;
            font-weight: bold;
            color: #0d9488;
            margin-bottom: 10px;
        }

        .btn-pos {
            background-color: #059669;
            color: white;
            border: none;
            padding: 10px 15px;
            border-radius: 6px;
            font-weight: 600;
            cursor: pointer;
            display: flex;
            justify-content: space-between;
            align-items: center;
        }

        .menu-group {
            display: flex;
            flex-direction: column;
            gap: 5px;
        }

        .menu-title {
            font-size: 11px;
            text-transform: uppercase;
            color: #9ca3af;
            font-weight: 700;
            margin-top: 10px;
            margin-bottom: 5px;
        }

        .menu-item {
            padding: 8px 12px;
            font-size: 13px;
            color: #4b5563;
            text-decoration: none;
            border-radius: 6px;
            cursor: pointer;
        }

        .menu-item.active {
            background-color: #2563eb;
            color: white;
        }

        /* Main Content Styles */
        .main-content {
            flex: 1;
            padding: 25px 30px;
        }

        .header-title {
            font-size: 22px;
            font-weight: 700;
            color: #111827;
        }

        .header-subtitle {
            font-size: 13px;
            color: #6b7280;
            margin-bottom: 20px;
        }

        /* Form Card */
        .card {
            background: white;
            border-radius: 8px;
            border: 1px solid #e5e7eb;
            padding: 20px;
            margin-bottom: 20px;
        }

        .form-row {
            display: flex;
            gap: 20px;
            margin-bottom: 20px;
        }

        .form-group {
            flex: 1;
        }

        .form-group label {
            display: block;
            font-size: 13px;
            font-weight: 600;
            margin-bottom: 6px;
            color: #374151;
        }

        .form-control {
            width: 100%;
            padding: 8px 12px;
            border: 1px solid #d1d5db;
            border-radius: 6px;
            font-size: 14px;
            outline: none;
        }

        .form-control:focus {
            border-color: #2563eb;
        }

        /* Ingredient List */
        .resep-header {
            display: flex;
            justify-content: space-between;
            align-items: center;
            margin-bottom: 12px;
        }

        .resep-title {
            font-size: 13px;
            font-weight: 700;
            color: #111827;
        }

        .btn-add-manual {
            background-color: #eff6ff;
            color: #2563eb;
            border: 1px solid #bfdbfe;
            padding: 4px 10px;
            font-size: 12px;
            border-radius: 4px;
            cursor: pointer;
        }

        .ingredient-row {
            display: flex;
            gap: 10px;
            align-items: center;
            margin-bottom: 10px;
        }

        .ingredient-row select {
            flex: 1;
        }

        .ingredient-row input {
            width: 80px;
            text-align: center;
        }

        .btn-delete {
            color: #ef4444;
            font-weight: bold;
            cursor: pointer;
            border: none;
            background: none;
            padding: 0 5px;
        }

        /* Grid Results */
        .result-grid {
            display: grid;
            grid-template-columns: 1fr 1fr;
            gap: 20px;
            margin-bottom: 20px;
        }

        .calc-box {
            border-radius: 8px;
            padding: 15px;
            font-size: 13px;
        }

        .calc-box-left {
            background-color: #f8fafc;
            border: 1px solid #e2e8f0;
        }

        .calc-box-right {
            background-color: #f0fdf4;
            border: 1px solid #dcfce7;
        }

        .box-title {
            font-weight: 700;
            margin-bottom: 12px;
            color: #0f172a;
        }

        .data-row {
            display: flex;
            justify-content: space-between;
            margin-bottom: 8px;
            color: #475569;
        }

        .data-row.total {
            font-weight: bold;
            border-top: 1px solid #cbd5e1;
            padding-top: 8px;
            margin-top: 10px;
        }

        .val-blue { color: #2563eb; }
        .val-danger { color: #dc2626; }

        .btn-submit {
            width: 100%;
            background-color: #059669;
            color: white;
            border: none;
            padding: 12px;
            border-radius: 6px;
            font-weight: 600;
            font-size: 14px;
            cursor: pointer;
        }

        .btn-submit:hover {
            background-color: #047857;
        }
    </style>
</head>
<body>

    <!-- Sidebar Menu -->
    <div class="sidebar">
        <div class="brand">KASIRKU</div>
        <button class="btn-pos">KASIR / POS <span>UTAMA</span></button>
        
        <div class="menu-group">
            <div class="menu-title">Master Data</div>
            <a class="menu-item">Product (Ready/Habis)</a>
            <a class="menu-item">Input Bahan Baku</a>
            <a class="menu-item active">Pembuatan Product</a>
        </div>

        <div class="menu-group">
            <div class="menu-title">Inventory</div>
            <a class="menu-item">Stock Product</a>
            <a class="menu-item">Akumulasi Stock Bahan</a>
        </div>

        <div class="menu-group">
            <div class="menu-title">Laporan</div>
            <a class="menu-item">Penjualan Harian</a>
            <a class="menu-item">Transaksi (Metode)</a>
            <a class="menu-item">Cashflow & Pengeluaran</a>
            <a class="menu-item">Laporan PnL Lengkap</a>
        </div>
    </div>

    <!-- Main Content -->
    <div class="main-content">
        <h1 class="header-title">Pembuatan Product (Proses Produksi)</h1>
        <p class="header-subtitle">Racik bahan baku menjadi produk siap jual. Hasil pembuatan akan menambah Stock Product.</p>

        <div class="card">
            <!-- Pilih Produk & Jumlah Porsi -->
            <div class="form-row">
                <div class="form-group">
                    <label for="produkSiapJual">Pilih Produk Jadi</label>
                    <select id="produkSiapJual" class="form-control">
                        <option value="12000">Tiramisu</option>
                    </select>
                </div>
                <div class="form-group">
                    <label for="jumlahPorsi">Jumlah Porsi Diproduksi (Ditambah ke Stok Produk)</label>
                    <input type="number" id="jumlahPorsi" class="form-control" value="8" min="1">
                </div>
            </div>

            <!-- Resep Bahan Baku -->
            <div class="resep-header">
                <span class="resep-title">Komposisi Resep Bahan Baku / Porsi</span>
                <button class="btn-add-manual" onclick="tambahBahanRow()">+ Tambah Bahan Manual</button>
            </div>

            <div id="containerBahan">
                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="120">
                        <option value="120">Kopi Robusta (Gram) - Rp 120/Gram</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="12">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>

                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="158">
                        <option value="158">Whipcream (Gram) - Rp 158/Gram</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="100">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>

                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="15400">
                        <option value="15400">Prochiz (Pcs) - Rp 15400/Pcs</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="1">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>

                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="1500">
                        <option value="1500">SKM (Pcs) - Rp 1500/Pcs</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="1">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>

                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="375">
                        <option value="375">Malkist (Pcs) - Rp 375/Pcs</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="15">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>

                <div class="ingredient-row">
                    <select class="form-control select-bahan" data-harga="1600">
                        <option value="1600">CUP 150ml (Pcs) - Rp 1600/Pcs</option>
                    </select>
                    <input type="number" class="form-control input-qty" value="8">
                    <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
                </div>
            </div>
        </div>

        <!-- Panel Hasil Kalkulasi -->
        <div class="result-grid">
            <div class="calc-box calc-box-left">
                <div class="box-title">Kalkulasi Biaya & HPP</div>
                <div class="data-row">
                    <span>HPP Bahan Mentah / Porsi:</span>
                    <span id="hppBahanPorsi">Rp 0</span>
                </div>
                <div class="data-row">
                    <span>Overhead (20%):</span>
                    <span id="overheadPorsi">Rp 0</span>
                </div>
                <div class="data-row total">
                    <span>Total HPP / Porsi:</span>
                    <span id="totalHppPorsi" class="val-blue">Rp 0</span>
                </div>
            </div>

            <div class="calc-box calc-box-right">
                <div class="box-title">Analisis Profit & Margin</div>
                <div class="data-row">
                    <span>Harga Jual Produk:</span>
                    <span id="hargaJualDisplay">Rp 12.000</span>
                </div>
                <div class="data-row">
                    <span>Laba Kotor / Porsi:</span>
                    <span id="labaKotorPorsi">Rp 0</span>
                </div>
                <div class="data-row total">
                    <span>Profit Margin (%):</span>
                    <span id="profitMarginDisplay">0%</span>
                </div>
            </div>
        </div>

        <button class="btn-submit">Proses Pembuatan & Tambah ke Stok Siap Jual</button>
    </div>

    <!-- Logic JavaScript -->
    <script>
        function formatRupiah(angka) {
            return "Rp " + Math.round(angka).toLocaleString('id-ID');
        }

        function hitungHPP() {
            const inputPorsi = parseFloat(document.getElementById('jumlahPorsi').value) || 1;
            const jumlahPorsi = inputPorsi > 0 ? inputPorsi : 1;

            let totalBiayaBatch = 0;
            const rows = document.querySelectorAll('.ingredient-row');

            rows.forEach(row => {
                const selectEl = row.querySelector('.select-bahan');
                const hargaSatuan = parseFloat(selectEl.getAttribute('data-harga')) || 0;
                const qty = parseFloat(row.querySelector('.input-qty').value) || 0;
                
                totalBiayaBatch += (hargaSatuan * qty);
            });

            // Pembagian total biaya batch dengan porsi
            const hppBahanPerPorsi = totalBiayaBatch / jumlahPorsi;

            const overheadPerPorsi = hppBahanPerPorsi * 0.20;
            const totalHppPerPorsi = hppBahanPerPorsi + overheadPerPorsi;

            const hargaJual = parseFloat(document.getElementById('produkSiapJual').value) || 12000;
            const labaKotor = hargaJual - totalHppPerPorsi;
            const marginPersen = hargaJual > 0 ? (labaKotor / hargaJual) * 100 : 0;

            document.getElementById('hppBahanPorsi').innerText = formatRupiah(hppBahanPerPorsi);
            document.getElementById('overheadPorsi').innerText = formatRupiah(overheadPerPorsi);
            document.getElementById('totalHppPorsi').innerText = formatRupiah(totalHppPerPorsi);
            
            document.getElementById('hargaJualDisplay').innerText = formatRupiah(hargaJual);
            
            const labaEl = document.getElementById('labaKotorPorsi');
            labaEl.innerText = formatRupiah(labaKotor);
            labaEl.className = labaKotor < 0 ? 'val-danger' : 'val-blue';

            const marginEl = document.getElementById('profitMarginDisplay');
            marginEl.innerText = marginPersen.toFixed(1) + '%';
            marginEl.className = marginPersen < 0 ? 'val-danger' : 'val-blue';
        }

        function hapusBahanRow(button) {
            button.parentElement.remove();
            hitungHPP();
        }

        function tambahBahanRow() {
            const container = document.getElementById('containerBahan');
            const div = document.createElement('div');
            div.className = 'ingredient-row';
            div.innerHTML = `
                <select class="form-control select-bahan" data-harga="100" onchange="updateHargaAttr(this)">
                    <option value="100" data-harga="100">Bahan Tambahan - Rp 100/Unit</option>
                </select>
                <input type="number" class="form-control input-qty" value="1">
                <button class="btn-delete" onclick="hapusBahanRow(this)">X</button>
            `;
            container.appendChild(div);
            attachListeners();
            hitungHPP();
        }

        function updateHargaAttr(select) {
            const selectedOption = select.options[select.selectedIndex];
            const harga = selectedOption.getAttribute('data-harga') || 0;
            select.setAttribute('data-harga', harga);
            hitungHPP();
        }

        function attachListeners() {
            document.getElementById('jumlahPorsi').addEventListener('input', hitungHPP);
            document.getElementById('produkSiapJual').addEventListener('change', hitungHPP);

            document.querySelectorAll('.input-qty').forEach(input => {
                input.removeEventListener('input', hitungHPP);
                input.addEventListener('input', hitungHPP);
            });

            document.querySelectorAll('.select-bahan').forEach(select => {
                select.removeEventListener('change', hitungHPP);
                select.addEventListener('change', hitungHPP);
            });
        }

        window.onload = function() {
            attachListeners();
            hitungHPP();
        };
    </script>
</body>
</html>
"""

# Simpan variabel HTML ke file menggunakan Python
with open("kasirku_pembuatan_produk.html", "w", encoding="utf-8") as file:
    file.write(html_content)
