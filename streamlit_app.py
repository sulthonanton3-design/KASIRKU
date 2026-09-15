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

# Kode HTML, CSS, dan JavaScript Aplikasi POS KASIRKU
html_code = """
<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KASIRKU - POS System</title>
    <script src="https://cdn.tailwindcss.com"></script>
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .active-menu { background-color: #3b82f6; color: #ffffff !important; }
        .active-menu i { color: #ffffff !important; }
    </style>
</head>
<body class="bg-slate-100 font-sans text-slate-800">

    <div class="flex h-screen overflow-hidden">

        <!-- SIDEBAR NAVIGASI -->
        <aside class="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shadow-sm flex-shrink-0">
            <div>
                <div class="p-4 border-b border-slate-100 flex items-center gap-3">
                    <div class="p-2 bg-blue-600 text-white rounded-lg">
                        <i data-lucide="store" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h1 class="font-bold text-lg text-slate-800 leading-none">KASIRKU</h1>
                        <span class="text-xs text-slate-400">POS & Management System</span>
                    </div>
                </div>

                <div class="p-3 space-y-3 overflow-y-auto max-h-[calc(100vh-120px)]">
                    <div>
                        <button onclick="switchTab('kasir')" id="btn-kasir" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 px-4 rounded-xl shadow-md transition flex items-center justify-between border-2 border-emerald-500">
                            <div class="flex items-center gap-3">
                                <i data-lucide="shopping-cart" class="w-5 h-5"></i>
                                <span>KASIR / POS</span>
                            </div>
                            <span class="bg-emerald-800 text-xs px-2 py-0.5 rounded-full">UTAMA</span>
                        </button>
                    </div>

                    <!-- MASTER DATA -->
                    <div class="space-y-1">
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-2">Master Data</div>
                        <button onclick="switchTab('master-product')" id="btn-master-product" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="package" class="w-4 h-4"></i> Product (Ready/Habis)
                        </button>
                        <button onclick="switchTab('master-bahan')" id="btn-master-bahan" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="boxes" class="w-4 h-4"></i> Input Bahan Baku
                        </button>
                        <button onclick="switchTab('master-racikan')" id="btn-master-racikan" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="chef-hat" class="w-4 h-4"></i> Pembuatan Product
                        </button>
                    </div>

                    <!-- INVENTORY -->
                    <div class="space-y-1">
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-2">Inventory</div>
                        <button onclick="switchTab('stock-product')" id="btn-stock-product" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="archive" class="w-4 h-4"></i> Stock Product
                        </button>
                        <button onclick="switchTab('stock-bahan')" id="btn-stock-bahan" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="layers" class="w-4 h-4"></i> Akumulasi Stock Bahan
                        </button>
                    </div>

                    <!-- LAPORAN -->
                    <div class="space-y-1">
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-2">Laporan</div>
                        <button onclick="switchTab('report-daily')" id="btn-report-daily" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="calendar" class="w-4 h-4"></i> Penjualan Harian
                        </button>
                        <button onclick="switchTab('report-tx')" id="btn-report-tx" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="receipt" class="w-4 h-4"></i> Transaksi (Metode)
                        </button>
                        <button onclick="switchTab('report-cashflow')" id="btn-report-cashflow" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="arrow-left-right" class="w-4 h-4"></i> Cashflow & Pengeluaran
                        </button>
                        <button onclick="switchTab('report-pnl')" id="btn-report-pnl" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="pie-chart" class="w-4 h-4"></i> Laporan PnL Lengkap
                        </button>
                    </div>

                    <!-- PENGATURAN -->
                    <div class="space-y-1">
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-2">Pengaturan</div>
                        <button onclick="switchTab('set-overhead')" id="btn-set-overhead" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="percent" class="w-4 h-4"></i> Overhead & PPN
                        </button>
                    </div>
                </div>
            </div>
            
            <div class="p-3 border-t border-slate-100 flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600 text-xs">KS</div>
                    <div>
                        <p class="text-xs font-semibold text-slate-700">Kasir Shift 1</p>
                        <p class="text-[10px] text-slate-400">Kasir Utama</p>
                    </div>
                </div>
            </div>
        </aside>

        <!-- MAIN CONTENT AREA -->
        <main class="flex-1 overflow-y-auto bg-slate-50 p-6" id="main-content">

            <!-- TAB 1: KASIR / POS -->
            <section id="tab-kasir" class="tab-content">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Menu Pengkasiran</h2>
                    <span class="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded-full border border-blue-200">Mode Transaksi On</span>
                </div>
                <div class="grid grid-cols-3 gap-6">
                    <div class="col-span-2 space-y-4">
                        <input type="text" id="pos-search" onkeyup="filterPosProducts()" placeholder="Cari nama produk..." class="w-full px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        <div class="grid grid-cols-3 gap-4" id="pos-products-grid"></div>
                    </div>

                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between h-[620px]">
                        <div>
                            <h3 class="font-bold border-b pb-2 text-slate-700 flex justify-between">
                                <span>Detail Pesanan</span>
                                <button onclick="clearCart()" class="text-xs text-red-500 font-normal hover:underline">Reset</button>
                            </h3>
                            <div id="cart-items" class="py-2 overflow-y-auto max-h-[220px] divide-y text-sm">
                                <p class="text-center text-xs text-slate-400 py-6">Belum ada item dipilih</p>
                            </div>
                        </div>

                        <div class="border-t pt-3 space-y-3">
                            <div class="space-y-1 text-sm">
                                <div class="flex justify-between">
                                    <span class="text-slate-500">Subtotal</span>
                                    <span id="pos-subtotal" class="font-semibold">Rp 0</span>
                                </div>
                                <div class="flex justify-between">
                                    <span class="text-slate-500">PPN (<span id="pos-ppn-rate">11</span>%)</span>
                                    <span id="pos-ppn" class="font-semibold">Rp 0</span>
                                </div>
                                <div class="flex justify-between font-bold text-base border-t pt-1">
                                    <span>Total</span>
                                    <span id="pos-total" class="text-blue-600">Rp 0</span>
                                </div>
                            </div>

                            <div class="space-y-2 border-t pt-2">
                                <label class="block text-xs font-medium text-slate-600">Metode Pembayaran</label>
                                <div class="grid grid-cols-3 gap-1">
                                    <button type="button" onclick="setPaymentMethod('cash')" id="pay-btn-cash" class="pay-method-btn bg-blue-600 text-white text-xs py-1.5 rounded font-medium">Cash</button>
                                    <button type="button" onclick="setPaymentMethod('transfer')" id="pay-btn-transfer" class="pay-method-btn bg-slate-100 text-slate-600 text-xs py-1.5 rounded font-medium">Transfer</button>
                                    <button type="button" onclick="setPaymentMethod('ewallet')" id="pay-btn-ewallet" class="pay-method-btn bg-slate-100 text-slate-600 text-xs py-1.5 rounded font-medium">E-Wallet</button>
                                </div>
                            </div>

                            <div id="cash-payment-section" class="space-y-1">
                                <label class="block text-xs font-medium text-slate-600">Uang Terbayar (Cash)</label>
                                <input type="number" id="cash-paid" oninput="calculateChange()" placeholder="Rp 0" class="w-full border rounded-lg p-2 text-sm focus:ring-1 focus:ring-blue-500">
                                <div class="flex justify-between text-xs pt-1">
                                    <span class="text-slate-500">Kembalian:</span>
                                    <span id="cash-change" class="font-bold text-emerald-600">Rp 0</span>
                                </div>
                            </div>

                            <button onclick="processTransaction()" class="w-full bg-emerald-600 text-white font-semibold py-2.5 rounded-xl hover:bg-emerald-700 transition">Selesaikan Transaksi</button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 2: MASTER PRODUCT -->
            <section id="tab-master-product" class="tab-content hidden">
                <div class="flex justify-between items-center mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-slate-800">Master Data Produk</h2>
                        <p class="text-sm text-slate-500">Kelola daftar produk, gambar, harga, dan status ketersediaan.</p>
                    </div>
                    <button onclick="openProductModal()" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2">
                        <i data-lucide="plus" class="w-4 h-4"></i> Tambah Produk
                    </button>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">Gambar</th>
                                <th class="p-4">Nama Produk</th>
                                <th class="p-4">Kategori</th>
                                <th class="p-4">Harga Jual</th>
                                <th class="p-4">Status</th>
                                <th class="p-4 text-right">Aksi</th>
                            </tr>
                        </thead>
                        <tbody id="product-table-body" class="divide-y text-sm"></tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 3: INPUT BAHAN BAKU -->
            <section id="tab-master-bahan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Input Bahan Baku</h2>
                <p class="text-sm text-slate-500 mb-6">Input master bahan baku mentah dasar untuk akumulasi stok dan modal.</p>
                <div class="bg-white p-6 rounded-xl border border-slate-200 max-w-xl shadow-sm space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Nama Bahan Baku</label>
                        <input type="text" id="bahan-nama" placeholder="Contoh: Biji Kopi Arabika, Susu UHT" class="w-full border rounded-lg p-2.5 text-sm">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Satuan Dasar</label>
                            <select id="bahan-satuan" class="w-full border rounded-lg p-2.5 text-sm">
                                <option value="Gram">Gram (g)</option>
                                <option value="ML">Milliliter (ml)</option>
                                <option value="Pcs">Pcs / Biji</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Volume/Berat per Pack</label>
                            <input type="number" id="bahan-volume" oninput="calcBahanGlobal()" placeholder="Contoh: 1000" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Qty Terbeli (Bungkus)</label>
                            <input type="number" id="bahan-qty" oninput="calcBahanGlobal()" placeholder="Contoh: 5" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Harga Beli per Bungkus</label>
                            <input type="number" id="bahan-harga-pack" oninput="calcBahanGlobal()" placeholder="Rp" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                    </div>

                    <div class="bg-slate-50 p-3 rounded-lg border space-y-1 text-xs text-slate-600">
                        <div class="flex justify-between">
                            <span>Total Nominal Pembelian:</span>
                            <span id="bahan-total-spend" class="font-bold text-slate-800">Rp 0</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Harga Beli Global / Satuan:</span>
                            <span id="bahan-harga-global" class="font-bold text-blue-600">Rp 0 / Satuan</span>
                        </div>
                    </div>

                    <button onclick="saveBahanBaku()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg text-sm transition">Simpan Bahan Baku</button>
                </div>
            </section>

            <!-- TAB 4: PEMBUATAN PRODUCT -->
            <section id="tab-master-racikan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Pembuatan Product (Proses Produksi)</h2>
                <p class="text-sm text-slate-500 mb-6">Racik bahan baku menjadi produk siap jual. Hasil pembuatan akan menambah Stock Product.</p>
                
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6 mb-8">
                    <div class="grid grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium mb-1">Pilih Produk Jadi</label>
                            <select id="recipe-product-select" onchange="calculateHPP()" class="w-full border rounded-lg p-2.5 text-sm">
                                <option value="">-- Pilih Produk --</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1">Jumlah Porsi Diproduksi (Ditambah ke Stok Produk)</label>
                            <input type="number" id="recipe-portion" value="10" min="1" oninput="calculateHPP()" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                    </div>

                    <div class="border-t pt-4">
                        <div class="flex justify-between items-center mb-3">
                            <h4 class="font-bold text-sm">Komposisi Resep Bahan Baku / Porsi</h4>
                            <button onclick="addRecipeRow()" class="text-xs bg-slate-100 hover:bg-slate-200 text-blue-600 px-3 py-1.5 rounded-lg font-semibold border">+ Tambah Bahan Manual</button>
                        </div>
                        <div id="recipe-rows-container" class="space-y-3"></div>
                    </div>

                    <div class="grid grid-cols-2 gap-4 border-t pt-4">
                        <div class="bg-blue-50/50 p-4 rounded-xl border border-blue-100 space-y-2 text-sm">
                            <h5 class="font-bold text-blue-900 border-b border-blue-200 pb-1">Kalkulasi Biaya & HPP</h5>
                            <div class="flex justify-between text-slate-600">
                                <span>HPP Bahan Mentah / Porsi:</span>
                                <span id="hpp-bahan-raw" class="font-semibold">Rp 0</span>
                            </div>
                            <div class="flex justify-between text-slate-600">
                                <span>Overhead (<span id="overhead-rate-display">10</span>%):</span>
                                <span id="hpp-overhead-val" class="font-semibold">Rp 0</span>
                            </div>
                            <div class="flex justify-between font-bold text-base border-t border-blue-200 pt-2 text-slate-800">
                                <span>Total HPP / Porsi:</span>
                                <span id="hpp-total-final" class="text-blue-600">Rp 0</span>
                            </div>
                        </div>

                        <div class="bg-emerald-50/50 p-4 rounded-xl border border-emerald-100 space-y-2 text-sm">
                            <h5 class="font-bold text-emerald-900 border-b border-emerald-200 pb-1">Analisis Profit & Margin</h5>
                            <div class="flex justify-between text-slate-600">
                                <span>Harga Jual Produk:</span>
                                <span id="margin-harga-jual" class="font-semibold text-slate-800">Rp 0</span>
                            </div>
                            <div class="flex justify-between text-slate-600">
                                <span>Laba Kotor / Porsi:</span>
                                <span id="margin-laba-nominal" class="font-semibold text-emerald-700">Rp 0</span>
                            </div>
                            <div class="flex justify-between font-bold text-base border-t border-emerald-200 pt-2 text-slate-800">
                                <span>Profit Margin (%):</span>
                                <span id="margin-persen" class="text-emerald-600">0%</span>
                            </div>
                        </div>
                    </div>

                    <button onclick="saveRecipeAndProduce()" class="w-full bg-emerald-600 text-white font-semibold py-3 rounded-lg text-sm hover:bg-emerald-700 transition">Proses Pembuatan & Tambah ke Stok Siap Jual</button>
                </div>
            </section>

            <!-- TAB 5: INVENTORY - STOCK PRODUCT -->
            <section id="tab-stock-product" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Stock Product (Siap Jual)</h2>
                    <p class="text-sm text-slate-500">Produk yang telah melalui proses pembuatan dan siap dijual melalui POS. Anda dapat mengedit stok atau menghapus data produk di sini.</p>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">Produk</th>
                                <th class="p-4">Kategori</th>
                                <th class="p-4">Stok Tersedia</th>
                                <th class="p-4">Harga Jual</th>
                                <th class="p-4">Status POS</th>
                                <th class="p-4 text-right">Aksi Inventory</th>
                            </tr>
                        </thead>
                        <tbody id="stock-product-table-body" class="divide-y text-sm"></tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 6: INVENTORY - AKUMULASI STOCK BAHAN -->
            <section id="tab-stock-bahan" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Akumulasi Stock Bahan Baku</h2>
                    <p class="text-sm text-slate-500">Kelola stok bahan mentah. Anda dapat mengedit sisa stok atau menghapus bahan baku dari sistem.</p>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">Nama Bahan</th>
                                <th class="p-4">Total Awal Belanja</th>
                                <th class="p-4">Sisa Stok Bahan</th>
                                <th class="p-4">Harga Global / Satuan</th>
                                <th class="p-4">Total Value Stok</th>
                                <th class="p-4 text-right">Aksi Inventory</th>
                            </tr>
                        </thead>
                        <tbody id="stock-bahan-table-body" class="divide-y text-sm"></tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 7: LAPORAN PENJUALAN HARIAN -->
            <section id="tab-report-daily" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Laporan Penjualan Harian</h2>
                    <p class="text-sm text-slate-500">Ringkasan transaksi berdasarkan tanggal dengan opsi filter fleksibel.</p>
                </div>

                <!-- COMPONENT FILTER HARIAN -->
                <div class="bg-white p-4 rounded-xl border border-slate-200 mb-6 shadow-sm flex flex-wrap gap-4 items-end">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Dari Tanggal</label>
                        <input type="date" id="filter-daily-start" onchange="renderDailyReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Sampai Tanggal</label>
                        <input type="date" id="filter-daily-end" onchange="renderDailyReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Bulan & Tahun</label>
                        <input type="month" id="filter-daily-month" onchange="renderDailyReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <button onclick="resetDailyFilters()" class="bg-slate-100 hover:bg-slate-200 text-slate-600 px-3 py-2 rounded-lg text-xs font-semibold">Reset Filter</button>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">Tanggal</th>
                                <th class="p-4">Jumlah Transaksi</th>
                                <th class="p-4">Item Terjual</th>
                                <th class="p-4">Total Omset (Rp)</th>
                            </tr>
                        </thead>
                        <tbody id="daily-report-table-body" class="divide-y text-sm"></tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 8: LAPORAN TRANSAKSI DETAIL -->
            <section id="tab-report-tx" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Laporan Transaksi Pembayaran</h2>
                    <p class="text-sm text-slate-500">Rincian metode pembayaran Cash, Transfer, dan E-Wallet.</p>
                </div>

                <!-- COMPONENT FILTER TRANSAKSI -->
                <div class="bg-white p-4 rounded-xl border border-slate-200 mb-6 shadow-sm flex flex-wrap gap-4 items-end">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Dari Tanggal</label>
                        <input type="date" id="filter-tx-start" onchange="renderTxReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Sampai Tanggal</label>
                        <input type="date" id="filter-tx-end" onchange="renderTxReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Bulan & Tahun</label>
                        <input type="month" id="filter-tx-month" onchange="renderTxReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Jenis / Metode Bayar</label>
                        <select id="filter-tx-method" onchange="renderTxReport()" class="border rounded-lg p-2 text-xs">
                            <option value="all">Semua Metode</option>
                            <option value="cash">Cash</option>
                            <option value="transfer">Transfer</option>
                            <option value="ewallet">E-Wallet</option>
                        </select>
                    </div>
                    <button onclick="resetTxFilters()" class="bg-slate-100 hover:bg-slate-200 text-slate-600 px-3 py-2 rounded-lg text-xs font-semibold">Reset Filter</button>
                </div>

                <div class="grid grid-cols-3 gap-4 mb-6">
                    <div class="bg-white p-4 rounded-xl border shadow-sm">
                        <p class="text-xs text-slate-400 font-semibold">TOTAL CASH</p>
                        <p id="tx-total-cash" class="text-xl font-bold text-emerald-600 mt-1">Rp 0</p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border shadow-sm">
                        <p class="text-xs text-slate-400 font-semibold">TOTAL TRANSFER</p>
                        <p id="tx-total-transfer" class="text-xl font-bold text-blue-600 mt-1">Rp 0</p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border shadow-sm">
                        <p class="text-xs text-slate-400 font-semibold">TOTAL E-WALLET</p>
                        <p id="tx-total-ewallet" class="text-xl font-bold text-purple-600 mt-1">Rp 0</p>
                    </div>
                </div>

                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">ID / Waktu</th>
                                <th class="p-4">Detail Items</th>
                                <th class="p-4">Metode</th>
                                <th class="p-4">Subtotal</th>
                                <th class="p-4">PPN</th>
                                <th class="p-4">Total Bayar</th>
                            </tr>
                        </thead>
                        <tbody id="tx-report-table-body" class="divide-y text-sm"></tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 9: LAPORAN CASHFLOW & PENGELUARAN -->
            <section id="tab-report-cashflow" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Cashflow & Input Pengeluaran</h2>
                    <p class="text-sm text-slate-500">Pencatatan pengeluaran operasional, belanja bahan baku, dan pembelian aset.</p>
                </div>
                <div class="grid grid-cols-3 gap-6">
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
                        <h3 class="font-bold border-b pb-2 text-slate-800">Input Pengeluaran Baru</h3>
                        <div>
                            <label class="block text-xs font-semibold mb-1">Tanggal Pengeluaran</label>
                            <input type="date" id="expense-date" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold mb-1">Kategori Pengeluaran</label>
                            <select id="expense-category" class="w-full border rounded-lg p-2 text-sm">
                                <option value="Bahan Baku">Belanja Bahan Baku</option>
                                <option value="Operasional">Operasional (Gaji, Listrik, Sewa, dll)</option>
                                <option value="Asset">Pembelian Asset / Peralatan</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-xs font-semibold mb-1">Deskripsi / Keterangan</label>
                            <input type="text" id="expense-desc" placeholder="Contoh: Bayar Listrik Bulan Ini" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-xs font-semibold mb-1">Nominal (Rp)</label>
                            <input type="number" id="expense-amount" placeholder="Rp 0" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                        <button onclick="saveExpense()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-semibold py-2.5 rounded-lg text-sm transition">Simpan Pengeluaran</button>
                    </div>

                    <div class="col-span-2 space-y-4">
                        <!-- COMPONENT FILTER CASHFLOW -->
                        <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-wrap gap-3 items-end">
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Dari Tanggal</label>
                                <input type="date" id="filter-exp-start" onchange="renderExpenseTable()" class="border rounded-lg p-2 text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Sampai Tanggal</label>
                                <input type="date" id="filter-exp-end" onchange="renderExpenseTable()" class="border rounded-lg p-2 text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Bulan & Tahun</label>
                                <input type="month" id="filter-exp-month" onchange="renderExpenseTable()" class="border rounded-lg p-2 text-xs">
                            </div>
                            <div>
                                <label class="block text-xs font-semibold text-slate-600 mb-1">Jenis Kategori</label>
                                <select id="filter-exp-cat" onchange="renderExpenseTable()" class="border rounded-lg p-2 text-xs">
                                    <option value="all">Semua Kategori</option>
                                    <option value="Bahan Baku">Bahan Baku</option>
                                    <option value="Operasional">Operasional</option>
                                    <option value="Asset">Asset</option>
                                </select>
                            </div>
                            <button onclick="resetExpFilters()" class="bg-slate-100 hover:bg-slate-200 text-slate-600 px-3 py-2 rounded-lg text-xs font-semibold">Reset</button>
                        </div>

                        <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                            <div class="p-4 border-b font-bold text-slate-800 flex justify-between items-center">
                                <span>Riwayat Pengeluaran (Arus Kas Keluar)</span>
                                <span id="exp-filtered-total" class="text-xs bg-red-50 text-red-600 px-2.5 py-1 rounded-full border border-red-200">Total: Rp 0</span>
                            </div>
                            <table class="w-full text-left border-collapse">
                                <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                                    <tr>
                                        <th class="p-3">Tanggal</th>
                                        <th class="p-3">Kategori</th>
                                        <th class="p-3">Keterangan</th>
                                        <th class="p-3 text-right">Nominal</th>
                                    </tr>
                                </thead>
                                <tbody id="expense-table-body" class="divide-y text-sm"></tbody>
                            </table>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 10: LAPORAN PnL -->
            <section id="tab-report-pnl" class="tab-content hidden">
                <div class="mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Laporan PnL (Laba & Rugi Transparan)</h2>
                    <p class="text-sm text-slate-500">Evaluasi total aset, modal terpakai, biaya operasional, dan laba bersih usaha.</p>
                </div>

                <!-- COMPONENT FILTER PnL -->
                <div class="bg-white p-4 rounded-xl border border-slate-200 mb-6 shadow-sm flex flex-wrap gap-4 items-end">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Dari Tanggal</label>
                        <input type="date" id="filter-pnl-start" onchange="renderPnLReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Sampai Tanggal</label>
                        <input type="date" id="filter-pnl-end" onchange="renderPnLReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 mb-1">Bulan & Tahun</label>
                        <input type="month" id="filter-pnl-month" onchange="renderPnLReport()" class="border rounded-lg p-2 text-xs">
                    </div>
                    <button onclick="resetPnLFilters()" class="bg-slate-100 hover:bg-slate-200 text-slate-600 px-3 py-2 rounded-lg text-xs font-semibold">Reset Filter</button>
                </div>

                <div class="grid grid-cols-2 gap-6">
                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-3">
                        <h3 class="font-bold text-slate-800 border-b pb-2">1. Nilai Persediaan / Stok (Asset Tersimpan)</h3>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Nilai Bahan Baku Belum Terolah:</span>
                            <span id="pnl-raw-value" class="font-bold text-slate-800">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Nilai Produk Siap Jual (Belum Terjual):</span>
                            <span id="pnl-unsold-product-value" class="font-bold text-slate-800">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm border-t pt-2 font-bold text-blue-600">
                            <span>Total Portfolio Stok:</span>
                            <span id="pnl-total-asset-value">Rp 0</span>
                        </div>
                    </div>

                    <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-3">
                        <h3 class="font-bold text-slate-800 border-b pb-2">2. Pendapatan (Penjualan Terrealisasi)</h3>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Total Omset Penjualan Bersih (Tanpa PPN):</span>
                            <span id="pnl-omset" class="font-bold text-emerald-600">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Modal Bahan Baku Produk Terjual (COGS):</span>
                            <span id="pnl-cogs" class="font-semibold text-red-500">- Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Alokasi Biaya Overhead HPP:</span>
                            <span id="pnl-overhead" class="font-semibold text-amber-600">- Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm border-t pt-2 font-bold text-slate-800">
                            <span>Laba Kotor Penjualan:</span>
                            <span id="pnl-gross-profit" class="text-emerald-700">Rp 0</span>
                        </div>
                    </div>
                </div>

                <div class="mt-6 bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
                    <h3 class="font-bold text-slate-800 border-b pb-2">3. Pengeluaran Tambahan & Profit Bersih</h3>
                    <div class="grid grid-cols-3 gap-4 text-sm">
                        <div class="p-3 bg-slate-50 rounded-lg">
                            <span class="text-slate-500 text-xs">Belanja Bahan Baku</span>
                            <p id="pnl-exp-bahan" class="font-bold text-slate-700 mt-1">Rp 0</p>
                        </div>
                        <div class="p-3 bg-slate-50 rounded-lg">
                            <span class="text-slate-500 text-xs">Biaya Operasional</span>
                            <p id="pnl-exp-ops" class="font-bold text-slate-700 mt-1">Rp 0</p>
                        </div>
                        <div class="p-3 bg-slate-50 rounded-lg">
                            <span class="text-slate-500 text-xs">Pembelian Asset</span>
                            <p id="pnl-exp-asset" class="font-bold text-slate-700 mt-1">Rp 0</p>
                        </div>
                    </div>

                    <div class="border-t pt-4 flex justify-between items-center">
                        <div>
                            <p class="text-lg font-bold text-slate-800">NET PROFIT / LABA BERSIH</p>
                            <p class="text-xs text-slate-400">Laba Kotor Penjualan dikurangi Pengeluaran Operasional & Aset</p>
                        </div>
                        <span id="pnl-net-profit" class="text-3xl font-extrabold text-blue-600">Rp 0</span>
                    </div>
                </div>
            </section>

            <!-- TAB 11: PENGATURAN OVERHEAD -->
            <section id="tab-set-overhead" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Pengaturan Persentase Overhead & PPN</h2>
                <div class="bg-white p-6 rounded-xl border max-w-md space-y-4 shadow-sm">
                    <div>
                        <label class="block text-sm font-medium mb-1">Persentase Overhead (%)</label>
                        <input type="number" id="set-overhead-rate" value="10" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Pajak PPN (%)</label>
                        <input type="number" id="set-ppn-rate" value="11" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <button onclick="saveSettings()" class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold hover:bg-blue-700">Simpan Pengaturan</button>
                </div>
            </section>
        </main>
    </div>

    <!-- MODAL EDIT / TAMBAH PRODUK -->
    <div id="product-modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center z-50">
        <div class="bg-white w-full max-w-md p-6 rounded-xl shadow-lg space-y-4">
            <h3 id="modal-title" class="text-lg font-bold border-b pb-2">Tambah / Edit Produk</h3>
            <input type="hidden" id="modal-product-id">
            <div>
                <label class="block text-xs font-semibold mb-1">Nama Produk</label>
                <input type="text" id="modal-nama" class="w-full border rounded p-2 text-sm">
            </div>
            <div>
                <label class="block text-xs font-semibold mb-1">Kategori</label>
                <select id="modal-kategori" class="w-full border rounded p-2 text-sm">
                    <option value="Makanan">Makanan</option>
                    <option value="Minuman">Minuman</option>
                    <option value="Snack">Snack</option>
                </select>
            </div>
            <div>
                <label class="block text-xs font-semibold mb-1">Harga Jual (Rp)</label>
                <input type="number" id="modal-harga" class="w-full border rounded p-2 text-sm">
            </div>
            <div>
                <label class="block text-xs font-semibold mb-1">Stok Siap Jual</label>
                <input type="number" id="modal-stok" class="w-full border rounded p-2 text-sm">
            </div>
            <div>
                <label class="block text-xs font-semibold mb-1">URL Gambar Produk</label>
                <input type="text" id="modal-gambar" placeholder="https://..." class="w-full border rounded p-2 text-sm">
            </div>
            <div>
                <label class="block text-xs font-semibold mb-1">Status</label>
                <select id="modal-status" class="w-full border rounded p-2 text-sm">
                    <option value="Ready">Ready</option>
                    <option value="Habis">Habis</option>
                </select>
            </div>
            <div class="flex justify-end gap-2 pt-2 border-t">
                <button onclick="closeProductModal()" class="px-4 py-2 bg-slate-200 text-xs font-semibold rounded-lg">Batal</button>
                <button onclick="saveProductForm()" class="px-4 py-2 bg-blue-600 text-white text-xs font-semibold rounded-lg">Simpan Produk</button>
            </div>
        </div>
    </div>

    <!-- MODAL EDIT INVENTORY STOK BAHAN BAKU -->
    <div id="bahan-modal" class="fixed inset-0 bg-black/40 hidden items-center justify-center z-50">
        <div class="bg-white w-full max-w-md p-6 rounded-xl shadow-lg space-y-4">
            <h3 class="text-lg font-bold border-b pb-2">Edit Inventory Bahan Baku</h3>
            <input type="hidden" id="modal-bahan-id">
            <div>
                <label class="block text-xs font-semibold mb-1">Nama Bahan Baku</label>
                <input type="text" id="modal-bahan-nama" class="w-full border rounded p-2 text-sm">
            </div>
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-semibold mb-1">Satuan</label>
                    <input type="text" id="modal-bahan-satuan" class="w-full border rounded p-2 text-sm">
                </div>
                <div>
                    <label class="block text-xs font-semibold mb-1">Harga Global/Satuan (Rp)</label>
                    <input type="number" id="modal-bahan-harga" class="w-full border rounded p-2 text-sm">
                </div>
            </div>
            <div class="grid grid-cols-2 gap-3">
                <div>
                    <label class="block text-xs font-semibold mb-1">Total Awal Belanja</label>
                    <input type="number" id="modal-bahan-totalstok" class="w-full border rounded p-2 text-sm">
                </div>
                <div>
                    <label class="block text-xs font-semibold mb-1">Sisa Stok Sekarang</label>
                    <input type="number" id="modal-bahan-sisastok" class="w-full border rounded p-2 text-sm">
                </div>
            </div>
            <div class="flex justify-end gap-2 pt-2 border-t">
                <button onclick="closeBahanModal()" class="px-4 py-2 bg-slate-200 text-xs font-semibold rounded-lg">Batal</button>
                <button onclick="saveBahanEditForm()" class="px-4 py-2 bg-blue-600 text-white text-xs font-semibold rounded-lg">Simpan Stok Bahan</button>
            </div>
        </div>
    </div>

    <script>
        let overheadRate = 10;
        let ppnRate = 11;
        let selectedPayMethod = 'cash';
        let cart = [];

        let transactionsList = [
            {
                id: 'TRX-1700000000000',
                tanggal: '2026-03-15',
                waktu: '10:30:00',
                items: [{ id: 1, nama: 'Kopi Susu Gula Aren', harga: 18000, qty: 2 }],
                metode: 'cash',
                subtotal: 36000,
                ppn: 3960,
                total: 39960,
                cogs: 6600,
                overhead: 660
            }
        ];

        let expensesList = [
            { tanggal: '2026-03-15', kategori: 'Bahan Baku', keterangan: 'Beli Biji Kopi Arabika (2 pack)', nominal: 300000 }
        ];

        let products = [
            { id: 1, nama: 'Kopi Susu Gula Aren', kategori: 'Minuman', harga: 18000, stok: 25, status: 'Ready', gambar: 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=300' },
            { id: 2, nama: 'Roti Bakar Cokelat', kategori: 'Makanan', harga: 15000, stok: 0, status: 'Habis', gambar: 'https://images.unsplash.com/photo-1584776296944-ab6fb57b0bff?w=300' }
        ];

        let bahanBakuList = [
            { id: 1, nama: 'Biji Kopi Arabika', satuan: 'Gram', totalStok: 2000, sisaStok: 2000, hargaGlobal: 150 },
            { id: 2, nama: 'Susu UHT', satuan: 'ML', totalStok: 10000, sisaStok: 10000, hargaGlobal: 18 },
            { id: 3, nama: 'Gula Aren', satuan: 'ML', totalStok: 5000, sisaStok: 5000, hargaGlobal: 21 }
        ];

        let recipesList = [
            {
                productId: 1,
                komposisi: [
                    { bahanId: 1, qty: 12 },
                    { bahanId: 2, qty: 100 },
                    { bahanId: 3, qty: 15 }
                ]
            }
        ];

        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.nav-btn').forEach(btn => btn.classList.remove('active-menu'));

            const targetTab = document.getElementById('tab-' + tabId);
            if (targetTab) targetTab.classList.remove('hidden');

            const activeBtn = document.getElementById('btn-' + tabId);
            if (activeBtn && tabId !== 'kasir') activeBtn.classList.add('active-menu');

            if (tabId === 'kasir') renderPosProducts();
            if (tabId === 'master-product') renderProductTable();
            if (tabId === 'master-racikan') initRacikanTab();
            if (tabId === 'stock-product') renderStockProductTable();
            if (tabId === 'stock-bahan') renderStockBahanTable();
            if (tabId === 'report-daily') renderDailyReport();
            if (tabId === 'report-tx') renderTxReport();
            if (tabId === 'report-cashflow') {
                document.getElementById('expense-date').value = new Date().toISOString().split('T')[0];
                renderExpenseTable();
            }
            if (tabId === 'report-pnl') renderPnLReport();
        }

        // --- POS FUNCTIONS ---
        function renderPosProducts(filter = "") {
            const grid = document.getElementById('pos-products-grid');
            grid.innerHTML = "";
            products.filter(p => p.nama.toLowerCase().includes(filter.toLowerCase())).forEach(p => {
                const isReady = p.status === 'Ready' && p.stok > 0;
                const card = document.createElement('div');
                card.className = `bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between ${!isReady ? 'opacity-50' : ''}`;
                card.innerHTML = `
                    <div>
                        <img src="${p.gambar || 'https://via.placeholder.com/150'}" class="w-full h-28 object-cover rounded-lg mb-2 border">
                        <div class="flex justify-between items-center">
                            <span class="text-[10px] font-semibold ${isReady ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'} px-2 py-0.5 rounded">${isReady ? 'Stok: ' + p.stok : 'Habis'}</span>
                            <span class="text-[10px] text-slate-400">${p.kategori}</span>
                        </div>
                        <h4 class="font-bold text-slate-800 text-sm mt-1">${p.nama}</h4>
                    </div>
                    <div class="mt-3 flex justify-between items-center">
                        <span class="font-bold text-blue-600 text-sm">Rp ${p.harga.toLocaleString('id-ID')}</span>
                        <button onclick="addToCart(${p.id})" ${!isReady ? 'disabled' : ''} class="px-3 py-1 ${isReady ? 'bg-blue-600 hover:bg-blue-700' : 'bg-slate-300 cursor-not-allowed'} text-white rounded-lg text-xs font-semibold">+ Tambah</button>
                    </div>
                `;
                grid.appendChild(card);
            });
        }

        function filterPosProducts() {
            renderPosProducts(document.getElementById('pos-search').value);
        }

        function addToCart(productId) {
            const product = products.find(p => p.id === productId);
            if (!product || product.stok <= 0) return;
            const item = cart.find(c => c.id === productId);
            if (item) {
                if (item.qty < product.stok) item.qty++;
                else alert("Stok produk tidak mencukupi!");
            } else {
                cart.push({ ...product, qty: 1 });
            }
            renderCart();
        }

        function updateCartQty(productId, change) {
            const item = cart.find(c => c.id === productId);
            const product = products.find(p => p.id === productId);
            if (item) {
                if (change > 0 && item.qty >= product.stok) {
                    alert("Jumlah melebihi stok yang tersedia!");
                    return;
                }
                item.qty += change;
                if (item.qty <= 0) cart = cart.filter(c => c.id !== productId);
            }
            renderCart();
        }

        function clearCart() {
            cart = [];
            renderCart();
        }

        function renderCart() {
            const cartContainer = document.getElementById('cart-items');
            if (cart.length === 0) {
                cartContainer.innerHTML = `<p class="text-center text-xs text-slate-400 py-6">Belum ada item dipilih</p>`;
            } else {
                cartContainer.innerHTML = cart.map(item => `
                    <div class="py-2 flex justify-between items-center">
                        <div>
                            <p class="font-semibold text-slate-700 text-xs">${item.nama}</p>
                            <p class="text-[10px] text-slate-400">Rp ${item.harga.toLocaleString('id-ID')} x ${item.qty}</p>
                        </div>
                        <div class="flex items-center gap-2">
                            <button onclick="updateCartQty(${item.id}, -1)" class="w-5 h-5 bg-slate-200 rounded text-xs font-bold flex items-center justify-center">-</button>
                            <span class="text-xs font-semibold">${item.qty}</span>
                            <button onclick="updateCartQty(${item.id}, 1)" class="w-5 h-5 bg-slate-200 rounded text-xs font-bold flex items-center justify-center">+</button>
                        </div>
                    </div>
                `).join('');
            }

            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const ppn = subtotal * (ppnRate / 100);
            const total = subtotal + ppn;

            document.getElementById('pos-subtotal').innerText = 'Rp ' + subtotal.toLocaleString('id-ID');
            document.getElementById('pos-ppn-rate').innerText = ppnRate;
            document.getElementById('pos-ppn').innerText = 'Rp ' + ppn.toLocaleString('id-ID');
            document.getElementById('pos-total').innerText = 'Rp ' + total.toLocaleString('id-ID');

            calculateChange();
        }

        function setPaymentMethod(method) {
            selectedPayMethod = method;
            document.querySelectorAll('.pay-method-btn').forEach(btn => {
                btn.className = "pay-method-btn bg-slate-100 text-slate-600 text-xs py-1.5 rounded font-medium";
            });
            const activeBtn = document.getElementById('pay-btn-' + method);
            if (activeBtn) activeBtn.className = "pay-method-btn bg-blue-600 text-white text-xs py-1.5 rounded font-medium";

            const cashSection = document.getElementById('cash-payment-section');
            if (method === 'cash') cashSection.classList.remove('hidden');
            else cashSection.classList.add('hidden');
        }

        function calculateChange() {
            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const total = subtotal + (subtotal * (ppnRate / 100));
            const cashPaid = parseFloat(document.getElementById('cash-paid').value) || 0;
            const change = cashPaid - total;

            document.getElementById('cash-change').innerText = 'Rp ' + (change > 0 ? change.toLocaleString('id-ID') : '0');
        }

        function processTransaction() {
            if (cart.length === 0) {
                alert("Keranjang masih kosong!");
                return;
            }

            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const ppn = subtotal * (ppnRate / 100);
            const total = subtotal + ppn;

            if (selectedPayMethod === 'cash') {
                const cashPaid = parseFloat(document.getElementById('cash-paid').value) || 0;
                if (cashPaid < total) {
                    alert("Uang pembayaran kurang!");
                    return;
                }
            }

            let txCogs = 0;
            let txOverhead = 0;

            cart.forEach(item => {
                const prod = products.find(p => p.id === item.id);
                if (prod) {
                    prod.stok -= item.qty;
                    if (prod.stok <= 0) {
                        prod.stok = 0;
                        prod.status = 'Habis';
                    }
                }

                const recipe = recipesList.find(r => r.productId === item.id);
                if (recipe) {
                    let itemRawHpp = 0;
                    recipe.komposisi.forEach(comp => {
                        const bahan = bahanBakuList.find(b => b.id === comp.bahanId);
                        if (bahan) {
                            itemRawHpp += (bahan.hargaGlobal * comp.qty);
                            bahan.sisaStok -= (comp.qty * item.qty);
                            if (bahan.sisaStok < 0) bahan.sisaStok = 0;
                        }
                    });
                    txCogs += (itemRawHpp * item.qty);
                    txOverhead += (itemRawHpp * (overheadRate / 100) * item.qty);
                }
            });

            const today = new Date().toISOString().split('T')[0];
            const now = new Date().toLocaleTimeString('id-ID');

            transactionsList.push({
                id: 'TRX-' + Date.now(),
                tanggal: today,
                waktu: now,
                items: JSON.parse(JSON.stringify(cart)),
                metode: selectedPayMethod,
                subtotal: subtotal,
                ppn: ppn,
                total: total,
                cogs: txCogs,
                overhead: txOverhead
            });

            alert("Transaksi Berhasil Diproses!");
            clearCart();
            document.getElementById('cash-paid').value = "";
            renderPosProducts();
        }

        // --- MASTER PRODUCT & INVENTORY MANAGEMENT ---
        function renderProductTable() {
            const tbody = document.getElementById('product-table-body');
            tbody.innerHTML = products.map(p => `
                <tr class="hover:bg-slate-50">
                    <td class="p-4"><img src="${p.gambar || 'https://via.placeholder.com/50'}" class="w-12 h-12 object-cover rounded-lg border"></td>
                    <td class="p-4 font-semibold text-slate-800">${p.nama}</td>
                    <td class="p-4 text-slate-500">${p.kategori}</td>
                    <td class="p-4 font-medium text-slate-700">Rp ${p.harga.toLocaleString('id-ID')}</td>
                    <td class="p-4"><span class="text-xs px-2.5 py-1 rounded-full font-semibold ${p.status === 'Ready' && p.stok > 0 ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}">${p.status === 'Ready' && p.stok > 0 ? 'Ready (' + p.stok + ')' : 'Habis'}</span></td>
                    <td class="p-4 text-right">
                        <button onclick="openProductModal(${p.id})" class="text-blue-600 hover:underline text-xs font-semibold mr-2">Edit</button>
                        <button onclick="deleteProduct(${p.id})" class="text-red-600 hover:underline text-xs font-semibold">Hapus</button>
                    </td>
                </tr>
            `).join('');
        }

        function openProductModal(productId = null) {
            const modal = document.getElementById('product-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');

            if (productId) {
                const p = products.find(item => item.id === productId);
                document.getElementById('modal-title').innerText = "Edit Produk & Stok";
                document.getElementById('modal-product-id').value = p.id;
                document.getElementById('modal-nama').value = p.nama;
                document.getElementById('modal-kategori').value = p.kategori;
                document.getElementById('modal-harga').value = p.harga;
                document.getElementById('modal-stok').value = p.stok;
                document.getElementById('modal-gambar').value = p.gambar;
                document.getElementById('modal-status').value = p.status;
            } else {
                document.getElementById('modal-title').innerText = "Tambah Produk Baru";
                document.getElementById('modal-product-id').value = "";
                document.getElementById('modal-nama').value = "";
                document.getElementById('modal-harga').value = "";
                document.getElementById('modal-stok').value = 0;
                document.getElementById('modal-gambar').value = "";
                document.getElementById('modal-status').value = "Ready";
            }
        }

        function closeProductModal() {
            const modal = document.getElementById('product-modal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }

        function saveProductForm() {
            const id = document.getElementById('modal-product-id').value;
            const nama = document.getElementById('modal-nama').value;
            const kategori = document.getElementById('modal-kategori').value;
            const harga = parseFloat(document.getElementById('modal-harga').value) || 0;
            const stok = parseInt(document.getElementById('modal-stok').value) || 0;
            const gambar = document.getElementById('modal-gambar').value;
            let status = document.getElementById('modal-status').value;

            if (!nama || harga <= 0) {
                alert("Harap isi nama dan harga produk dengan benar!");
                return;
            }

            if (stok <= 0) status = 'Habis';

            if (id) {
                const p = products.find(item => item.id == id);
                if (p) {
                    p.nama = nama; p.kategori = kategori; p.harga = harga; p.stok = stok; p.gambar = gambar; p.status = status;
                }
            } else {
                const newId = products.length ? Math.max(...products.map(p => p.id)) + 1 : 1;
                products.push({ id: newId, nama, kategori, harga, stok, status, gambar });
            }

            closeProductModal();
            renderProductTable();
            renderStockProductTable();
        }

        function deleteProduct(productId) {
            if (confirm("Apakah Anda yakin ingin menghapus produk ini dari inventory?")) {
                products = products.filter(p => p.id !== productId);
                recipesList = recipesList.filter(r => r.productId !== productId);
                renderProductTable();
                renderStockProductTable();
            }
        }

        function renderStockProductTable() {
            const tbody = document.getElementById('stock-product-table-body');
            tbody.innerHTML = products.map(p => `
                <tr class="hover:bg-slate-50">
                    <td class="p-4 font-semibold text-slate-800">${p.nama}</td>
                    <td class="p-4 text-slate-500">${p.kategori}</td>
                    <td class="p-4 font-bold text-blue-600">${p.stok} Porsi</td>
                    <td class="p-4 text-slate-700">Rp ${p.harga.toLocaleString('id-ID')}</td>
                    <td class="p-4"><span class="text-xs px-2.5 py-1 rounded-full font-semibold ${p.status === 'Ready' && p.stok > 0 ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}">${p.status === 'Ready' && p.stok > 0 ? 'Tersedia' : 'Habis / Non-aktif'}</span></td>
                    <td class="p-4 text-right">
                        <button onclick="openProductModal(${p.id})" class="text-blue-600 hover:underline text-xs font-semibold mr-2">Edit Stok</button>
                        <button onclick="deleteProduct(${p.id})" class="text-red-600 hover:underline text-xs font-semibold">Hapus</button>
                    </td>
                </tr>
            `).join('');
        }

        // --- BAHAN BAKU INVENTORY MANAGEMENT ---
        function calcBahanGlobal() {
            const volume = parseFloat(document.getElementById('bahan-volume').value) || 0;
            const qty = parseFloat(document.getElementById('bahan-qty').value) || 0;
            const hargaPack = parseFloat(document.getElementById('bahan-harga-pack').value) || 0;

            const totalSpend = qty * hargaPack;
            const totalVolume = volume * qty;
            const hargaGlobal = totalVolume > 0 ? totalSpend / totalVolume : 0;

            document.getElementById('bahan-total-spend').innerText = 'Rp ' + totalSpend.toLocaleString('id-ID');
            document.getElementById('bahan-harga-global').innerText = 'Rp ' + Math.round(hargaGlobal).toLocaleString('id-ID') + ' / Satuan';
        }

        function saveBahanBaku() {
            const nama = document.getElementById('bahan-nama').value;
            const satuan = document.getElementById('bahan-satuan').value;
            const volume = parseFloat(document.getElementById('bahan-volume').value) || 0;
            const qty = parseFloat(document.getElementById('bahan-qty').value) || 0;
            const hargaPack = parseFloat(document.getElementById('bahan-harga-pack').value) || 0;

            if (!nama || volume <= 0 || qty <= 0 || hargaPack <= 0) {
                alert("Harap lengkapi semua data bahan baku dengan benar!");
                return;
            }

            const totalVolume = volume * qty;
            const hargaGlobal = (qty * hargaPack) / totalVolume;
            const newId = bahanBakuList.length ? Math.max(...bahanBakuList.map(b => b.id)) + 1 : 1;

            bahanBakuList.push({
                id: newId,
                nama: nama,
                satuan: satuan,
                totalStok: totalVolume,
                sisaStok: totalVolume,
                hargaGlobal: hargaGlobal
            });

            const today = new Date().toISOString().split('T')[0];
            expensesList.push({
                tanggal: today,
                kategori: 'Bahan Baku',
                keterangan: `Beli ${nama} (${qty} pack)`,
                nominal: qty * hargaPack
            });

            alert("Bahan Baku Berhasil Disimpan & Dicatat ke Cashflow!");
            document.getElementById('bahan-nama').value = "";
            document.getElementById('bahan-volume').value = "";
            document.getElementById('bahan-qty').value = "";
            document.getElementById('bahan-harga-pack').value = "";
            calcBahanGlobal();
        }

        function renderStockBahanTable() {
            const tbody = document.getElementById('stock-bahan-table-body');
            tbody.innerHTML = bahanBakuList.map(b => {
                const totalValue = b.sisaStok * b.hargaGlobal;
                return `
                    <tr class="hover:bg-slate-50">
                        <td class="p-4 font-semibold text-slate-800">${b.nama}</td>
                        <td class="p-4 text-slate-500">${b.totalStok.toLocaleString('id-ID')} ${b.satuan}</td>
                        <td class="p-4 font-bold ${b.sisaStok < (b.totalStok * 0.2) ? 'text-red-600' : 'text-emerald-600'}">${b.sisaStok.toLocaleString('id-ID')} ${b.satuan}</td>
                        <td class="p-4 text-slate-600 text-xs">Rp ${Math.round(b.hargaGlobal).toLocaleString('id-ID')} / ${b.satuan}</td>
                        <td class="p-4 font-semibold text-slate-700">Rp ${Math.round(totalValue).toLocaleString('id-ID')}</td>
                        <td class="p-4 text-right">
                            <button onclick="openBahanModal(${b.id})" class="text-blue-600 hover:underline text-xs font-semibold mr-2">Edit</button>
                            <button onclick="deleteBahanBaku(${b.id})" class="text-red-600 hover:underline text-xs font-semibold">Hapus</button>
                        </td>
                    </tr>
                `;
            }).join('');
        }

        function openBahanModal(id) {
            const b = bahanBakuList.find(item => item.id === id);
            if (!b) return;
            document.getElementById('modal-bahan-id').value = b.id;
            document.getElementById('modal-bahan-nama').value = b.nama;
            document.getElementById('modal-bahan-satuan').value = b.satuan;
            document.getElementById('modal-bahan-harga').value = Math.round(b.hargaGlobal);
            document.getElementById('modal-bahan-totalstok').value = b.totalStok;
            document.getElementById('modal-bahan-sisastok').value = b.sisaStok;

            const modal = document.getElementById('bahan-modal');
            modal.classList.remove('hidden');
            modal.classList.add('flex');
        }

        function closeBahanModal() {
            const modal = document.getElementById('bahan-modal');
            modal.classList.add('hidden');
            modal.classList.remove('flex');
        }

        function saveBahanEditForm() {
            const id = parseInt(document.getElementById('modal-bahan-id').value);
            const nama = document.getElementById('modal-bahan-nama').value;
            const satuan = document.getElementById('modal-bahan-satuan').value;
            const hargaGlobal = parseFloat(document.getElementById('modal-bahan-harga').value) || 0;
            const totalStok = parseFloat(document.getElementById('modal-bahan-totalstok').value) || 0;
            const sisaStok = parseFloat(document.getElementById('modal-bahan-sisastok').value) || 0;

            const b = bahanBakuList.find(item => item.id === id);
            if (b) {
                b.nama = nama;
                b.satuan = satuan;
                b.hargaGlobal = hargaGlobal;
                b.totalStok = totalStok;
                b.sisaStok = sisaStok;
            }

            closeBahanModal();
            renderStockBahanTable();
        }

        function deleteBahanBaku(id) {
            if (confirm("Apakah Anda yakin ingin menghapus bahan baku ini dari inventory?")) {
                bahanBakuList = bahanBakuList.filter(b => b.id !== id);
                renderStockBahanTable();
            }
        }

        // --- RACIKAN / RESEP PRODUK ---
        function initRacikanTab() {
            const select = document.getElementById('recipe-product-select');
            select.innerHTML = `<option value="">-- Pilih Produk --</option>` + products.map(p => `<option value="${p.id}">${p.nama}</option>`).join('');
            document.getElementById('recipe-rows-container').innerHTML = "";
            calculateHPP();
        }

        function addRecipeRow(bahanId = "", qty = 0) {
            const container = document.getElementById('recipe-rows-container');
            const rowId = Date.now() + Math.random();
            const div = document.createElement('div');
            div.className = "flex items-center gap-3 recipe-row";
            div.id = 'row-' + rowId;

            const options = bahanBakuList.map(b => `<option value="${b.id}" ${b.id == bahanId ? 'selected' : ''}>${b.nama} (${b.satuan}) - Rp ${Math.round(b.hargaGlobal)}/${b.satuan}</option>`).join('');

            div.innerHTML = `
                <select class="recipe-bahan-select w-full border rounded-lg p-2 text-sm" onchange="calculateHPP()">
                    <option value="">-- Pilih Bahan Baku --</option>
                    ${options}
                </select>
                <input type="number" value="${qty}" placeholder="Qty/Porsi" oninput="calculateHPP()" class="recipe-qty-input w-32 border rounded-lg p-2 text-sm">
                <button onclick="removeRecipeRow('${rowId}')" class="text-red-500 font-bold px-2">X</button>
            `;
            container.appendChild(div);
            calculateHPP();
        }

        function removeRecipeRow(rowId) {
            const el = document.getElementById('row-' + rowId);
            if (el) el.remove();
            calculateHPP();
        }

        function calculateHPP() {
            document.getElementById('overhead-rate-display').innerText = overheadRate;
            const productId = parseInt(document.getElementById('recipe-product-select').value);
            const product = products.find(p => p.id === productId);

            let rawHpp = 0;
            document.querySelectorAll('.recipe-row').forEach(row => {
                const bahanId = parseInt(row.querySelector('.recipe-bahan-select').value);
                const qty = parseFloat(row.querySelector('.recipe-qty-input').value) || 0;
                const bahan = bahanBakuList.find(b => b.id === bahanId);
                if (bahan) {
                    rawHpp += (bahan.hargaGlobal * qty);
                }
            });

            const overheadVal = rawHpp * (overheadRate / 100);
            const totalHpp = rawHpp + overheadVal;

            document.getElementById('hpp-bahan-raw').innerText = 'Rp ' + Math.round(rawHpp).toLocaleString('id-ID');
            document.getElementById('hpp-overhead-val').innerText = 'Rp ' + Math.round(overheadVal).toLocaleString('id-ID');
            document.getElementById('hpp-total-final').innerText = 'Rp ' + Math.round(totalHpp).toLocaleString('id-ID');

            if (product) {
                const hargaJual = product.harga;
                const laba = hargaJual - totalHpp;
                const margin = hargaJual > 0 ? (laba / hargaJual) * 100 : 0;

                document.getElementById('margin-harga-jual').innerText = 'Rp ' + hargaJual.toLocaleString('id-ID');
                document.getElementById('margin-laba-nominal').innerText = 'Rp ' + Math.round(laba).toLocaleString('id-ID');
                document.getElementById('margin-persen').innerText = margin.toFixed(1) + '%';
            } else {
                document.getElementById('margin-harga-jual').innerText = 'Rp 0';
                document.getElementById('margin-laba-nominal').innerText = 'Rp 0';
                document.getElementById('margin-persen').innerText = '0%';
            }
        }

        function saveRecipeAndProduce() {
            const productId = parseInt(document.getElementById('recipe-product-select').value);
            const portion = parseInt(document.getElementById('recipe-portion').value) || 0;

            if (!productId || portion <= 0) {
                alert("Pilih produk dan masukkan jumlah porsi yang diproduksi!");
                return;
            }

            const komposisi = [];
            document.querySelectorAll('.recipe-row').forEach(row => {
                const bahanId = parseInt(row.querySelector('.recipe-bahan-select').value);
                const qty = parseFloat(row.querySelector('.recipe-qty-input').value) || 0;
                if (bahanId && qty > 0) {
                    komposisi.push({ bahanId, qty });
                }
            });

            if (komposisi.length === 0) {
                alert("Masukkan minimal satu bahan baku resep!");
                return;
            }

            const existingRecipeIndex = recipesList.findIndex(r => r.productId === productId);
            if (existingRecipeIndex > -1) {
                recipesList[existingRecipeIndex].komposisi = komposisi;
            } else {
                recipesList.push({ productId, komposisi });
            }

            const prod = products.find(p => p.id === productId);
            if (prod) {
                prod.stok += portion;
                prod.status = 'Ready';
            }

            alert(`Berhasil memproduksi ${portion} porsi ${prod.nama}! Stok produk telah ditambahkan.`);
        }

        // --- HELPER FILTER DATES ---
        function isDateInFilter(dateStr, startDate, endDate, monthStr) {
            if (startDate && dateStr < startDate) return false;
            if (endDate && dateStr > endDate) return false;
            if (monthStr && !dateStr.startsWith(monthStr)) return false;
            return true;
        }

        // --- LAPORAN 1: PENJUALAN HARIAN ---
        function renderDailyReport() {
            const tbody = document.getElementById('daily-report-table-body');
            const startDate = document.getElementById('filter-daily-start').value;
            const endDate = document.getElementById('filter-daily-end').value;
            const monthStr = document.getElementById('filter-daily-month').value;

            const dailyData = {};

            transactionsList.forEach(tx => {
                if (isDateInFilter(tx.tanggal, startDate, endDate, monthStr)) {
                    if (!dailyData[tx.tanggal]) {
                        dailyData[tx.tanggal] = { txCount: 0, itemsCount: 0, totalOmset: 0 };
                    }
                    dailyData[tx.tanggal].txCount += 1;
                    dailyData[tx.tanggal].itemsCount += tx.items.reduce((sum, item) => sum + item.qty, 0);
                    dailyData[tx.tanggal].totalOmset += tx.subtotal;
                }
            });

            const dates = Object.keys(dailyData);
            if (dates.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-400">Tidak ada transaksi ditemukan</td></tr>`;
                return;
            }

            tbody.innerHTML = dates.map(date => `
                <tr class="hover:bg-slate-50">
                    <td class="p-4 font-semibold text-slate-800">${date}</td>
                    <td class="p-4 text-slate-600">${dailyData[date].txCount} Transaksi</td>
                    <td class="p-4 text-slate-600">${dailyData[date].itemsCount} Porsi</td>
                    <td class="p-4 font-bold text-emerald-600">Rp ${dailyData[date].totalOmset.toLocaleString('id-ID')}</td>
                </tr>
            `).join('');
        }

        function resetDailyFilters() {
            document.getElementById('filter-daily-start').value = "";
            document.getElementById('filter-daily-end').value = "";
            document.getElementById('filter-daily-month').value = "";
            renderDailyReport();
        }

        // --- LAPORAN 2: TRANSAKSI METHOD ---
        function renderTxReport() {
            const tbody = document.getElementById('tx-report-table-body');
            const startDate = document.getElementById('filter-tx-start').value;
            const endDate = document.getElementById('filter-tx-end').value;
            const monthStr = document.getElementById('filter-tx-month').value;
            const methodFilter = document.getElementById('filter-tx-method').value;

            let totalCash = 0, totalTransfer = 0, totalEwallet = 0;

            const filteredTx = transactionsList.filter(tx => {
                const passDate = isDateInFilter(tx.tanggal, startDate, endDate, monthStr);
                const passMethod = (methodFilter === 'all' || tx.metode === methodFilter);
                return passDate && passMethod;
            });

            filteredTx.forEach(tx => {
                if (tx.metode === 'cash') totalCash += tx.total;
                if (tx.metode === 'transfer') totalTransfer += tx.total;
                if (tx.metode === 'ewallet') totalEwallet += tx.total;
            });

            document.getElementById('tx-total-cash').innerText = 'Rp ' + totalCash.toLocaleString('id-ID');
            document.getElementById('tx-total-transfer').innerText = 'Rp ' + totalTransfer.toLocaleString('id-ID');
            document.getElementById('tx-total-ewallet').innerText = 'Rp ' + totalEwallet.toLocaleString('id-ID');

            if (filteredTx.length === 0) {
                tbody.innerHTML = `<tr><td colspan="6" class="p-4 text-center text-slate-400">Tidak ada data transaksi cocok</td></tr>`;
                return;
            }

            tbody.innerHTML = filteredTx.map(tx => {
                const itemList = tx.items.map(i => `${i.nama} (${i.qty})`).join(', ');
                const methodBadge = tx.metode === 'cash' ? 'bg-emerald-100 text-emerald-700' : (tx.metode === 'transfer' ? 'bg-blue-100 text-blue-700' : 'bg-purple-100 text-purple-700');

                return `
                    <tr class="hover:bg-slate-50">
                        <td class="p-4"><p class="font-bold text-slate-800 text-xs">${tx.id}</p><p class="text-[10px] text-slate-400">${tx.tanggal} ${tx.waktu}</p></td>
                        <td class="p-4 text-xs text-slate-600">${itemList}</td>
                        <td class="p-4"><span class="text-xs px-2 py-0.5 rounded font-semibold uppercase ${methodBadge}">${tx.metode}</span></td>
                        <td class="p-4 text-slate-600 text-xs">Rp ${tx.subtotal.toLocaleString('id-ID')}</td>
                        <td class="p-4 text-slate-600 text-xs">Rp ${tx.ppn.toLocaleString('id-ID')}</td>
                        <td class="p-4 font-bold text-slate-800 text-xs">Rp ${tx.total.toLocaleString('id-ID')}</td>
                    </tr>
                `;
            }).join('');
        }

        function resetTxFilters() {
            document.getElementById('filter-tx-start').value = "";
            document.getElementById('filter-tx-end').value = "";
            document.getElementById('filter-tx-month').value = "";
            document.getElementById('filter-tx-method').value = "all";
            renderTxReport();
        }

        // --- LAPORAN 3: CASHFLOW & PENGELUARAN ---
        function saveExpense() {
            const date = document.getElementById('expense-date').value || new Date().toISOString().split('T')[0];
            const kategori = document.getElementById('expense-category').value;
            const keterangan = document.getElementById('expense-desc').value;
            const nominal = parseFloat(document.getElementById('expense-amount').value) || 0;

            if (!keterangan || nominal <= 0) {
                alert("Lengkapi keterangan dan nominal pengeluaran!");
                return;
            }

            expensesList.push({ tanggal: date, kategori, keterangan, nominal });

            alert("Pengeluaran Berhasil Dicatat!");
            document.getElementById('expense-desc').value = "";
            document.getElementById('expense-amount').value = "";
            renderExpenseTable();
        }

        function renderExpenseTable() {
            const tbody = document.getElementById('expense-table-body');
            const startDate = document.getElementById('filter-exp-start').value;
            const endDate = document.getElementById('filter-exp-end').value;
            const monthStr = document.getElementById('filter-exp-month').value;
            const catFilter = document.getElementById('filter-exp-cat').value;

            const filteredExp = expensesList.filter(exp => {
                const passDate = isDateInFilter(exp.tanggal, startDate, endDate, monthStr);
                const passCat = (catFilter === 'all' || exp.kategori === catFilter);
                return passDate && passCat;
            });

            const totalExp = filteredExp.reduce((sum, item) => sum + item.nominal, 0);
            document.getElementById('exp-filtered-total').innerText = 'Total: Rp ' + totalExp.toLocaleString('id-ID');

            if (filteredExp.length === 0) {
                tbody.innerHTML = `<tr><td colspan="4" class="p-4 text-center text-slate-400">Tidak ada pengeluaran dicatat</td></tr>`;
                return;
            }

            tbody.innerHTML = filteredExp.map(exp => `
                <tr class="hover:bg-slate-50">
                    <td class="p-3 text-slate-500 text-xs">${exp.tanggal}</td>
                    <td class="p-3 font-semibold text-slate-700 text-xs">${exp.kategori}</td>
                    <td class="p-3 text-slate-600 text-xs">${exp.keterangan}</td>
                    <td class="p-3 font-bold text-red-600 text-xs text-right">Rp ${exp.nominal.toLocaleString('id-ID')}</td>
                </tr>
            `).join('');
        }

        function resetExpFilters() {
            document.getElementById('filter-exp-start').value = "";
            document.getElementById('filter-exp-end').value = "";
            document.getElementById('filter-exp-month').value = "";
            document.getElementById('filter-exp-cat').value = "all";
            renderExpenseTable();
        }

        // --- LAPORAN 4: PnL ---
        function renderPnLReport() {
            const startDate = document.getElementById('filter-pnl-start').value;
            const endDate = document.getElementById('filter-pnl-end').value;
            const monthStr = document.getElementById('filter-pnl-month').value;

            let rawMaterialValue = 0;
            bahanBakuList.forEach(b => {
                rawMaterialValue += (b.sisaStok * b.hargaGlobal);
            });

            let unsoldProductValue = 0;
            products.forEach(p => {
                const recipe = recipesList.find(r => r.productId === p.id);
                let productHpp = 0;
                if (recipe) {
                    recipe.komposisi.forEach(comp => {
                        const bahan = bahanBakuList.find(b => b.id === comp.bahanId);
                        if (bahan) productHpp += (bahan.hargaGlobal * comp.qty);
                    });
                }
                unsoldProductValue += (p.stok * productHpp);
            });

            const totalAssetStock = rawMaterialValue + unsoldProductValue;

            let totalOmset = 0;
            let totalCogs = 0;
            let totalOverhead = 0;

            transactionsList.forEach(tx => {
                if (isDateInFilter(tx.tanggal, startDate, endDate, monthStr)) {
                    totalOmset += tx.subtotal;
                    totalCogs += tx.cogs;
                    totalOverhead += tx.overhead;
                }
            });

            const grossProfit = totalOmset - totalCogs - totalOverhead;

            let expBahan = 0, expOps = 0, expAsset = 0;
            expensesList.forEach(e => {
                if (isDateInFilter(e.tanggal, startDate, endDate, monthStr)) {
                    if (e.kategori === 'Bahan Baku') expBahan += e.nominal;
                    if (e.kategori === 'Operasional') expOps += e.nominal;
                    if (e.kategori === 'Asset') expAsset += e.nominal;
                }
            });

            const netProfit = grossProfit - expOps - expAsset;

            document.getElementById('pnl-raw-value').innerText = 'Rp ' + Math.round(rawMaterialValue).toLocaleString('id-ID');
            document.getElementById('pnl-unsold-product-value').innerText = 'Rp ' + Math.round(unsoldProductValue).toLocaleString('id-ID');
            document.getElementById('pnl-total-asset-value').innerText = 'Rp ' + Math.round(totalAssetStock).toLocaleString('id-ID');

            document.getElementById('pnl-omset').innerText = 'Rp ' + Math.round(totalOmset).toLocaleString('id-ID');
            document.getElementById('pnl-cogs').innerText = '- Rp ' + Math.round(totalCogs).toLocaleString('id-ID');
            document.getElementById('pnl-overhead').innerText = '- Rp ' + Math.round(totalOverhead).toLocaleString('id-ID');
            document.getElementById('pnl-gross-profit').innerText = 'Rp ' + Math.round(grossProfit).toLocaleString('id-ID');

            document.getElementById('pnl-exp-bahan').innerText = 'Rp ' + Math.round(expBahan).toLocaleString('id-ID');
            document.getElementById('pnl-exp-ops').innerText = 'Rp ' + Math.round(expOps).toLocaleString('id-ID');
            document.getElementById('pnl-exp-asset').innerText = 'Rp ' + Math.round(expAsset).toLocaleString('id-ID');

            document.getElementById('pnl-net-profit').innerText = 'Rp ' + Math.round(netProfit).toLocaleString('id-ID');
        }

        function resetPnLFilters() {
            document.getElementById('filter-pnl-start').value = "";
            document.getElementById('filter-pnl-end').value = "";
            document.getElementById('filter-pnl-month').value = "";
            renderPnLReport();
        }

        function saveSettings() {
            overheadRate = parseFloat(document.getElementById('set-overhead-rate').value) || 0;
            ppnRate = parseFloat(document.getElementById('set-ppn-rate').value) || 0;
            alert("Pengaturan Overhead & PPN berhasil disimpan!");
        }

        document.addEventListener("DOMContentLoaded", function() {
            lucide.createIcons();
            renderPosProducts();
        });
    </script>
</body>
</html>
"""

# Menampilkan aplikasi web HTML di dalam Streamlit
components.html(html_code, height=950, scrolling=True)
