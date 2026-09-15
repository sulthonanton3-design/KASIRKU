import streamlit as st
import streamlit.components.v1 as components

st.set_page_config(
    page_title="KASIRKU - POS System & Inventory",
    page_icon="🛒",
    layout="wide"
)

st.markdown("""
    <style>
        .block-container {
            padding: 0rem !important;
            max-width: 100% !important;
        }
        header {visibility: hidden;}
        footer {visibility: hidden;}
    </style>
""", unsafe_allow_html=True)

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
        <aside class="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shadow-sm">
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

                <div class="p-3 space-y-4 overflow-y-auto max-h-[calc(100vh-120px)]">
                    <div>
                        <button onclick="switchTab('kasir')" id="btn-kasir" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white font-semibold py-3 px-4 rounded-xl shadow-md transition flex items-center justify-between border-2 border-emerald-500">
                            <div class="flex items-center gap-3">
                                <i data-lucide="shopping-cart" class="w-5 h-5"></i>
                                <span>KASIR / POS</span>
                            </div>
                            <span class="bg-emerald-800 text-xs px-2 py-0.5 rounded-full">UTAMA</span>
                        </button>
                    </div>

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

                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-3">Pengaturan</div>
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
                        <div class="flex gap-2">
                            <input type="text" id="pos-search" onkeyup="filterPosProducts()" placeholder="Cari nama produk..." class="w-full px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                        </div>
                        <div class="grid grid-cols-3 gap-4" id="pos-products-grid">
                            <!-- Produk di-render dinamis -->
                        </div>
                    </div>

                    <!-- Detail Pesanan -->
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

            <!-- TAB 2: MASTER DATA - PRODUCT -->
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
                        <tbody id="product-table-body" class="divide-y text-sm">
                            <!-- Diisi via JS -->
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 3: MASTER DATA - INPUT BAHAN BAKU -->
            <section id="tab-master-bahan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Input Bahan Baku</h2>
                <p class="text-sm text-slate-500 mb-6">Input master bahan baku mentah dasar untuk perhitungan stok dan modal.</p>
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
                            <label class="block text-sm font-medium text-slate-700 mb-1">Volume/Berat per Bungkus</label>
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
                            <span>Total Nominal Terbelanjakan:</span>
                            <span id="bahan-total-spend" class="font-bold text-slate-800">Rp 0</span>
                        </div>
                        <div class="flex justify-between">
                            <span>Harga Beli Global per Satuan Dasar:</span>
                            <span id="bahan-harga-global" class="font-bold text-blue-600">Rp 0 / Satuan</span>
                        </div>
                    </div>

                    <button onclick="saveBahanBaku()" class="w-full bg-blue-600 hover:bg-blue-700 text-white font-medium py-2.5 rounded-lg text-sm transition">Simpan Bahan Baku</button>
                </div>
            </section>

            <!-- TAB 4: PEMBUATAN PRODUCT (RESEP & HPP + MARGIN) -->
            <section id="tab-master-racikan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Pembuatan Product (Resep, HPP & Margin)</h2>
                <p class="text-sm text-slate-500 mb-6">Racik bahan baku ke dalam produk untuk otomatisasi hitung HPP, Overhead, dan Analisis Profit Margin.</p>
                
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-6 mb-8">
                    <div class="grid grid-cols-2 gap-6">
                        <div>
                            <label class="block text-sm font-medium mb-1">Pilih Produk Jadi</label>
                            <select id="recipe-product-select" onchange="calculateHPP()" class="w-full border rounded-lg p-2.5 text-sm">
                                <option value="">-- Pilih Produk --</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1">Estimasi Porsi Terbuat (Per Racikan Batch)</label>
                            <input type="number" id="recipe-portion" value="1" min="1" oninput="calculateHPP()" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                    </div>

                    <div class="border-t pt-4">
                        <div class="flex justify-between items-center mb-3">
                            <h4 class="font-bold text-sm">Komposisi Resep Bahan Baku</h4>
                            <button onclick="addRecipeRow()" class="text-xs bg-slate-100 hover:bg-slate-200 text-blue-600 px-3 py-1.5 rounded-lg font-semibold border">+ Tambah Bahan Manual</button>
                        </div>
                        <div id="recipe-rows-container" class="space-y-3">
                            <!-- Rows di-generate via JS -->
                        </div>
                    </div>

                    <!-- Output Kalkulasi HPP & Margin -->
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
                                <span>Laba Kotor Nominal:</span>
                                <span id="margin-laba-nominal" class="font-semibold text-emerald-700">Rp 0</span>
                            </div>
                            <div class="flex justify-between font-bold text-base border-t border-emerald-200 pt-2 text-slate-800">
                                <span>Profit Margin (%):</span>
                                <span id="margin-persen" class="text-emerald-600">0%</span>
                            </div>
                        </div>
                    </div>

                    <button onclick="saveRecipe()" class="bg-emerald-600 text-white font-semibold px-6 py-2.5 rounded-lg text-sm hover:bg-emerald-700 transition">Simpan Resep & HPP Produk</button>
                </div>

                <!-- TABEL DAFTAR RESEP TERSIMPAN -->
                <div class="bg-white rounded-xl border border-slate-200 p-6 shadow-sm">
                    <h3 class="text-lg font-bold text-slate-800 mb-4">Daftar Resep Produk Tersimpan</h3>
                    <div class="overflow-x-auto">
                        <table class="w-full text-left border-collapse">
                            <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                                <tr>
                                    <th class="p-3">Nama Produk</th>
                                    <th class="p-3">Harga Jual</th>
                                    <th class="p-3">Total HPP / Porsi</th>
                                    <th class="p-3">Laba Kotor</th>
                                    <th class="p-3">Profit Margin</th>
                                    <th class="p-3">Komposisi Bahan</th>
                                </tr>
                            </thead>
                            <tbody id="recipe-table-body" class="divide-y text-sm">
                                <!-- Diisi via JS -->
                            </tbody>
                        </table>
                    </div>
                </div>
            </section>

            <!-- TAB PENGATURAN OVERHEAD -->
            <section id="tab-set-overhead" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Pengaturan Persentase Overhead & PPN</h2>
                <div class="bg-white p-6 rounded-xl border max-w-md space-y-4 shadow-sm">
                    <div>
                        <label class="block text-sm font-medium mb-1">Persentase Overhead (%)</label>
                        <input type="number" id="set-overhead-rate" value="10" class="w-full border rounded-lg p-2 text-sm">
                        <span class="text-xs text-slate-400">Estimasi biaya operasional, listrik, air, dan kemasan per produk.</span>
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

    <script>
        let overheadRate = 10;
        let ppnRate = 11;
        let selectedPayMethod = 'cash';
        let cart = [];

        let products = [
            { id: 1, nama: 'Kopi Susu Gula Aren', kategori: 'Minuman', harga: 18000, status: 'Ready', gambar: 'https://images.unsplash.com/photo-1541167760496-1628856ab772?w=300' },
            { id: 2, nama: 'Roti Bakar Cokelat', kategori: 'Makanan', harga: 15000, status: 'Habis', gambar: 'https://images.unsplash.com/photo-1584776296944-ab6fb57b0bff?w=300' }
        ];

        let bahanBakuList = [
            { id: 1, nama: 'Biji Kopi Arabika', satuan: 'Gram', volume: 1000, qty: 2, hargaPack: 150000, hargaGlobal: 150 },
            { id: 2, nama: 'Susu UHT', satuan: 'ML', volume: 1000, qty: 10, hargaPack: 18000, hargaGlobal: 18 },
            { id: 3, nama: 'Gula Aren', satuan: 'ML', volume: 1000, qty: 5, hargaPack: 21000, hargaGlobal: 21 },
            { id: 4, nama: 'Botol 250ml', satuan: 'Pcs', volume: 1, qty: 100, hargaPack: 1800, hargaGlobal: 1800 }
        ];

        let recipesList = [
            {
                productId: 1,
                productName: 'Kopi Susu Gula Aren',
                hargaJual: 18000,
                porsiBatch: 1,
                hppPerPorsi: 7885,
                labaNominal: 10115,
                marginPersen: 56.19,
                komposisiText: 'Kopi (12g), Susu UHT (100ml), Gula Aren (6ml), Botol (1 Pcs)'
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
        }

        // --- POS FUNCTIONS ---
        function renderPosProducts(filter = "") {
            const grid = document.getElementById('pos-products-grid');
            grid.innerHTML = "";
            products.filter(p => p.nama.toLowerCase().includes(filter.toLowerCase())).forEach(p => {
                const isReady = p.status === 'Ready';
                const card = document.createElement('div');
                card.className = `bg-white p-3 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between ${!isReady ? 'opacity-50' : ''}`;
                card.innerHTML = `
                    <div>
                        <img src="${p.gambar || 'https://via.placeholder.com/150'}" class="w-full h-28 object-cover rounded-lg mb-2 border">
                        <span class="text-[10px] font-semibold ${isReady ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'} px-2 py-0.5 rounded">${p.status}</span>
                        <h4 class="font-bold text-slate-800 text-sm mt-1">${p.nama}</h4>
                        <p class="text-xs text-slate-400">${p.kategori}</p>
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
            const query = document.getElementById('pos-search').value;
            renderPosProducts(query);
        }

        function addToCart(productId) {
            const product = products.find(p => p.id === productId);
            if (!product) return;
            const item = cart.find(c => c.id === productId);
            if (item) {
                item.qty++;
            } else {
                cart.push({ ...product, qty: 1 });
            }
            renderCart();
        }

        function updateCartQty(productId, change) {
            const item = cart.find(c => c.id === productId);
            if (item) {
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
                        <div class="flex items-center gap-1">
                            <button onclick="updateCartQty(${item.id}, -1)" class="w-5 h-5 bg-slate-200 rounded text-xs font-bold text-slate-600 hover:bg-slate-300">-</button>
                            <span class="text-xs font-semibold w-4 text-center">${item.qty}</span>
                            <button onclick="updateCartQty(${item.id}, 1)" class="w-5 h-5 bg-slate-200 rounded text-xs font-bold text-slate-600 hover:bg-slate-300">+</button>
                        </div>
                    </div>
                `).join('');
            }
            calculateTotals();
        }

        function setPaymentMethod(method) {
            selectedPayMethod = method;
            document.querySelectorAll('.pay-method-btn').forEach(btn => {
                btn.className = "pay-method-btn bg-slate-100 text-slate-600 text-xs py-1.5 rounded font-medium";
            });
            document.getElementById(`pay-btn-${method}`).className = "pay-method-btn bg-blue-600 text-white text-xs py-1.5 rounded font-medium";
            
            const cashSection = document.getElementById('cash-payment-section');
            if (method === 'cash') {
                cashSection.classList.remove('hidden');
            } else {
                cashSection.classList.add('hidden');
            }
        }

        function calculateTotals() {
            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const ppn = Math.round(subtotal * (ppnRate / 100));
            const total = subtotal + ppn;

            document.getElementById('pos-subtotal').innerText = `Rp ${subtotal.toLocaleString('id-ID')}`;
            document.getElementById('pos-ppn-rate').innerText = ppnRate;
            document.getElementById('pos-ppn').innerText = `Rp ${ppn.toLocaleString('id-ID')}`;
            document.getElementById('pos-total').innerText = `Rp ${total.toLocaleString('id-ID')}`;
            calculateChange();
        }

        function calculateChange() {
            const total = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0) * (1 + ppnRate / 100);
            const paid = parseFloat(document.getElementById('cash-paid').value) || 0;
            const change = paid - total;
            const changeDisplay = document.getElementById('cash-change');
            if (change >= 0) {
                changeDisplay.innerText = `Rp ${Math.round(change).toLocaleString('id-ID')}`;
                changeDisplay.className = "font-bold text-emerald-600";
            } else {
                changeDisplay.innerText = `Kurang Rp ${Math.abs(Math.round(change)).toLocaleString('id-ID')}`;
                changeDisplay.className = "font-bold text-red-500";
            }
        }

        function processTransaction() {
            if (cart.length === 0) {
                alert("Keranjang belanja masih kosong!");
                return;
            }
            alert("Transaksi berhasil diproses!");
            clearCart();
            document.getElementById('cash-paid').value = "";
            calculateChange();
        }

        // --- MASTER PRODUCT FUNCTIONS ---
        function renderProductTable() {
            const tbody = document.getElementById('product-table-body');
            tbody.innerHTML = products.map(p => `
                <tr class="hover:bg-slate-50">
                    <td class="p-4"><img src="${p.gambar || 'https://via.placeholder.com/50'}" class="w-10 h-10 object-cover rounded border"></td>
                    <td class="p-4 font-semibold text-slate-800">${p.nama}</td>
                    <td class="p-4 text-slate-500">${p.kategori}</td>
                    <td class="p-4 font-medium text-slate-700">Rp ${p.harga.toLocaleString('id-ID')}</td>
                    <td class="p-4"><span class="px-2.5 py-1 text-xs rounded-full font-semibold ${p.status === 'Ready' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'}">${p.status}</span></td>
                    <td class="p-4 text-right">
                        <button onclick="editProduct(${p.id})" class="text-blue-600 hover:underline text-xs font-semibold mr-2">Edit</button>
                        <button onclick="deleteProduct(${p.id})" class="text-red-500 hover:underline text-xs font-semibold">Hapus</button>
                    </td>
                </tr>
            `).join('');
        }

        function openProductModal() {
            document.getElementById('modal-product-id').value = "";
            document.getElementById('modal-nama').value = "";
            document.getElementById('modal-harga').value = "";
            document.getElementById('modal-gambar').value = "";
            document.getElementById('modal-title').innerText = "Tambah Produk Baru";
            document.getElementById('product-modal').classList.remove('hidden');
            document.getElementById('product-modal').classList.add('flex');
        }

        function closeProductModal() {
            document.getElementById('product-modal').classList.add('hidden');
            document.getElementById('product-modal').classList.remove('flex');
        }

        function editProduct(id) {
            const p = products.find(x => x.id === id);
            if (!p) return;
            document.getElementById('modal-product-id').value = p.id;
            document.getElementById('modal-nama').value = p.nama;
            document.getElementById('modal-kategori').value = p.kategori;
            document.getElementById('modal-harga').value = p.harga;
            document.getElementById('modal-gambar').value = p.gambar;
            document.getElementById('modal-status').value = p.status;
            document.getElementById('modal-title').innerText = "Edit Produk";
            document.getElementById('product-modal').classList.remove('hidden');
            document.getElementById('product-modal').classList.add('flex');
        }

        function saveProductForm() {
            const id = document.getElementById('modal-product-id').value;
            const nama = document.getElementById('modal-nama').value;
            const kategori = document.getElementById('modal-kategori').value;
            const harga = parseFloat(document.getElementById('modal-harga').value) || 0;
            const gambar = document.getElementById('modal-gambar').value;
            const status = document.getElementById('modal-status').value;

            if (!nama || harga <= 0) {
                alert("Mohon isi nama dan harga produk dengan benar.");
                return;
            }

            if (id) {
                const p = products.find(x => x.id == id);
                if (p) {
                    p.nama = nama;
                    p.kategori = kategori;
                    p.harga = harga;
                    p.gambar = gambar;
                    p.status = status;
                }
            } else {
                products.push({
                    id: Date.now(),
                    nama, kategori, harga, gambar, status
                });
            }
            closeProductModal();
            renderProductTable();
        }

        function deleteProduct(id) {
            if (confirm("Yakin ingin menghapus produk ini?")) {
                products = products.filter(p => p.id !== id);
                renderProductTable();
            }
        }

        // --- MASTER BAHAN BAKU FUNCTIONS ---
        function calcBahanGlobal() {
            const vol = parseFloat(document.getElementById('bahan-volume').value) || 0;
            const qty = parseFloat(document.getElementById('bahan-qty').value) || 0;
            const price = parseFloat(document.getElementById('bahan-harga-pack').value) || 0;
            const totalSpend = qty * price;
            const totalVol = vol * qty;
            const globalUnit = totalVol > 0 ? (totalSpend / totalVol) : 0;

            document.getElementById('bahan-total-spend').innerText = `Rp ${totalSpend.toLocaleString('id-ID')}`;
            document.getElementById('bahan-harga-global').innerText = `Rp ${globalUnit.toFixed(2)} / Satuan`;
        }

        function saveBahanBaku() {
            const nama = document.getElementById('bahan-nama').value;
            const satuan = document.getElementById('bahan-satuan').value;
            const vol = parseFloat(document.getElementById('bahan-volume').value) || 0;
            const qty = parseFloat(document.getElementById('bahan-qty').value) || 0;
            const price = parseFloat(document.getElementById('bahan-harga-pack').value) || 0;

            if (!nama || vol <= 0 || qty <= 0 || price <= 0) {
                alert("Mohon lengkapi seluruh formulir bahan baku.");
                return;
            }

            const totalVol = vol * qty;
            const hargaGlobal = (qty * price) / totalVol;

            bahanBakuList.push({
                id: Date.now(),
                nama, satuan, volume: vol, qty, hargaPack: price, hargaGlobal
            });

            alert("Bahan baku berhasil disimpan!");
            document.getElementById('bahan-nama').value = "";
            document.getElementById('bahan-volume').value = "";
            document.getElementById('bahan-qty').value = "";
            document.getElementById('bahan-harga-pack').value = "";
            calcBahanGlobal();
        }

        // --- RACIKAN / RESEP & HPP FUNCTIONS ---
        function initRacikanTab() {
            const select = document.getElementById('recipe-product-select');
            select.innerHTML = `<option value="">-- Pilih Produk --</option>` + products.map(p => `<option value="${p.id}">${p.nama}</option>`).join('');
            
            const container = document.getElementById('recipe-rows-container');
            if (container.children.length === 0) {
                addRecipeRow();
            }
            renderRecipeTable();
        }

        function addRecipeRow() {
            const container = document.getElementById('recipe-rows-container');
            const rowId = Date.now() + Math.random();
            const div = document.createElement('div');
            div.className = "flex items-center gap-3 recipe-row";
            div.id = `row-${rowId}`;
            div.innerHTML = `
                <select onchange="calculateHPP()" class="recipe-bahan-select flex-1 border rounded-lg p-2 text-sm">
                    <option value="">-- Pilih Bahan Baku --</option>
                    ${bahanBakuList.map(b => `<option value="${b.id}">${b.nama} (${b.satuan}) - Rp ${b.hargaGlobal.toFixed(1)}/${b.satuan}</option>`).join('')}
                </select>
                <input type="number" oninput="calculateHPP()" placeholder="Takaran" class="recipe-qty-input w-32 border rounded-lg p-2 text-sm">
                <button onclick="removeRecipeRow('row-${rowId}')" class="text-red-500 hover:text-red-700 font-bold px-2">✕</button>
            `;
            container.appendChild(div);
        }

        function removeRecipeRow(rowId) {
            const row = document.getElementById(rowId);
            if (row) row.remove();
            calculateHPP();
        }

        function calculateHPP() {
            const productId = document.getElementById('recipe-product-select').value;
            const portion = parseFloat(document.getElementById('recipe-portion').value) || 1;
            const product = products.find(p => p.id == productId);

            let totalRawCostBatch = 0;
            const rows = document.querySelectorAll('.recipe-row');

            rows.forEach(row => {
                const bahanId = row.querySelector('.recipe-bahan-select').value;
                const qty = parseFloat(row.querySelector('.recipe-qty-input').value) || 0;
                const bahan = bahanBakuList.find(b => b.id == bahanId);
                if (bahan) {
                    totalRawCostBatch += (bahan.hargaGlobal * qty);
                }
            });

            const rawCostPerPortion = totalRawCostBatch / portion;
            const overheadVal = rawCostPerPortion * (overheadRate / 100);
            const totalHppFinal = rawCostPerPortion + overheadVal;

            document.getElementById('hpp-bahan-raw').innerText = `Rp ${Math.round(rawCostPerPortion).toLocaleString('id-ID')}`;
            document.getElementById('overhead-rate-display').innerText = overheadRate;
            document.getElementById('hpp-overhead-val').innerText = `Rp ${Math.round(overheadVal).toLocaleString('id-ID')}`;
            document.getElementById('hpp-total-final').innerText = `Rp ${Math.round(totalHppFinal).toLocaleString('id-ID')}`;

            if (product) {
                const hargaJual = product.harga;
                const labaNominal = hargaJual - totalHppFinal;
                const marginPersen = hargaJual > 0 ? ((labaNominal / hargaJual) * 100) : 0;

                document.getElementById('margin-harga-jual').innerText = `Rp ${hargaJual.toLocaleString('id-ID')}`;
                document.getElementById('margin-laba-nominal').innerText = `Rp ${Math.round(labaNominal).toLocaleString('id-ID')}`;
                document.getElementById('margin-persen').innerText = `${marginPersen.toFixed(2)}%`;
            } else {
                document.getElementById('margin-harga-jual').innerText = `Rp 0`;
                document.getElementById('margin-laba-nominal').innerText = `Rp 0`;
                document.getElementById('margin-persen').innerText = `0%`;
            }
        }

        function saveRecipe() {
            const productId = document.getElementById('recipe-product-select').value;
            const portion = parseFloat(document.getElementById('recipe-portion').value) || 1;
            const product = products.find(p => p.id == productId);

            if (!product) {
                alert("Pilih produk terlebih dahulu!");
                return;
            }

            let komposisiArr = [];
            let totalRawCostBatch = 0;

            document.querySelectorAll('.recipe-row').forEach(row => {
                const bahanId = row.querySelector('.recipe-bahan-select').value;
                const qty = parseFloat(row.querySelector('.recipe-qty-input').value) || 0;
                const bahan = bahanBakuList.find(b => b.id == bahanId);
                if (bahan && qty > 0) {
                    totalRawCostBatch += (bahan.hargaGlobal * qty);
                    komposisiArr.push(`${bahan.nama} (${qty} ${bahan.satuan})`);
                }
            });

            const rawCostPerPortion = totalRawCostBatch / portion;
            const overheadVal = rawCostPerPortion * (overheadRate / 100);
            const totalHppFinal = rawCostPerPortion + overheadVal;
            const labaNominal = product.harga - totalHppFinal;
            const marginPersen = product.harga > 0 ? ((labaNominal / product.harga) * 100) : 0;

            recipesList = recipesList.filter(r => r.productId != productId);
            recipesList.push({
                productId: product.id,
                productName: product.nama,
                hargaJual: product.harga,
                porsiBatch: portion,
                hppPerPorsi: Math.round(totalHppFinal),
                labaNominal: Math.round(labaNominal),
                marginPersen: parseFloat(marginPersen.toFixed(2)),
                komposisiText: komposisiArr.join(', ') || 'Tanpa komposisi'
            });

            alert("Resep berhasil disimpan!");
            renderRecipeTable();
        }

        function renderRecipeTable() {
            const tbody = document.getElementById('recipe-table-body');
            tbody.innerHTML = recipesList.map(r => `
                <tr class="hover:bg-slate-50">
                    <td class="p-3 font-semibold text-slate-800">${r.productName}</td>
                    <td class="p-3 text-slate-600">Rp ${r.hargaJual.toLocaleString('id-ID')}</td>
                    <td class="p-3 font-medium text-blue-600">Rp ${r.hppPerPorsi.toLocaleString('id-ID')}</td>
                    <td class="p-3 font-medium text-emerald-600">Rp ${r.labaNominal.toLocaleString('id-ID')}</td>
                    <td class="p-3 font-bold text-emerald-700">${r.marginPersen}%</td>
                    <td class="p-3 text-xs text-slate-500 max-w-xs truncate" title="${r.komposisiText}">${r.komposisiText}</td>
                </tr>
            `).join('');
        }

        // --- SETTINGS FUNCTIONS ---
        function saveSettings() {
            overheadRate = parseFloat(document.getElementById('set-overhead-rate').value) || 0;
            ppnRate = parseFloat(document.getElementById('set-ppn-rate').value) || 0;
            alert("Pengaturan persentase Overhead & PPN berhasil diperbarui!");
            calculateTotals();
        }

        // Init App
        renderPosProducts();
        lucide.createIcons();
    </script>
</body>
</html>
"""

components.html(html_code, height=900, scrolling=True)
