<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KASIRKU - Dashboard & POS System</title>
    <!-- Tailwind CSS CDN -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .active-menu {
            background-color: #3b82f6;
            color: #ffffff !important;
        }
        .active-menu i {
            color: #ffffff !important;
        }
    </style>
</head>
<body class="bg-slate-100 font-sans text-slate-800">

    <div class="flex h-screen overflow-hidden">

        <!-- SIDEBAR NAVIGASI -->
        <aside class="w-64 bg-white border-r border-slate-200 flex flex-col justify-between shadow-sm">
            <div>
                <!-- Brand Header -->
                <div class="p-4 border-b border-slate-100 flex items-center gap-3">
                    <div class="p-2 bg-blue-600 text-white rounded-lg">
                        <i data-lucide="store" class="w-6 h-6"></i>
                    </div>
                    <div>
                        <h1 class="font-bold text-lg text-slate-800 leading-none">KASIRKU</h1>
                        <span class="text-xs text-slate-400">Point of Sale System</span>
                    </div>
                </div>

                <!-- MENU UTAMA -->
                <div class="p-3 space-y-4">
                    
                    <!-- MENU KASIR (Tombol Khusus Paling Atas) -->
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
                        <!-- Master Data -->
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

                        <!-- Inventory -->
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-3">Inventory</div>
                        <button onclick="switchTab('inv-product')" id="btn-inv-product" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="archive" class="w-4 h-4"></i> Stock Product
                        </button>
                        <button onclick="switchTab('inv-bahan')" id="btn-inv-bahan" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="layers" class="w-4 h-4"></i> Akumulasi Stock Bahan
                        </button>
                        <button onclick="switchTab('inv-opname')" id="btn-inv-opname" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="clipboard-check" class="w-4 h-4"></i> Stock Opname
                        </button>

                        <!-- Laporan -->
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-3">Laporan</div>
                        <button onclick="switchTab('lap-cashflow')" id="btn-lap-cashflow" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="arrow-left-right" class="w-4 h-4"></i> Cashflow
                        </button>
                        <button onclick="switchTab('lap-penjualan-harian')" id="btn-lap-penjualan-harian" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="receipt" class="w-4 h-4"></i> Penjualan Harian
                        </button>
                        <button onclick="switchTab('lap-sales')" id="btn-lap-sales" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="trending-up" class="w-4 h-4"></i> Sales Transaction
                        </button>
                        <button onclick="switchTab('lap-pnl')" id="btn-lap-pnl" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="pie-chart" class="w-4 h-4"></i> Laporan PnL
                        </button>

                        <!-- Pengaturan -->
                        <div class="text-xs font-semibold text-slate-400 uppercase tracking-wider px-3 pt-3">Pengaturan</div>
                        <button onclick="switchTab('set-overhead')" id="btn-set-overhead" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="percent" class="w-4 h-4"></i> Overhead & PPN
                        </button>
                        <button onclick="switchTab('set-akun')" id="btn-set-akun" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="sliders" class="w-4 h-4"></i> Akun & Branding
                        </button>
                        <button onclick="switchTab('set-struk')" id="btn-set-struk" class="nav-btn w-full flex items-center gap-3 px-3 py-2 rounded-lg text-sm text-slate-600 hover:bg-slate-100 transition">
                            <i data-lucide="printer" class="w-4 h-4"></i> Configuration Struk
                        </button>
                    </div>
                </div>
            </div>

            <!-- Footer User Profile -->
            <div class="p-3 border-t border-slate-100 flex items-center justify-between">
                <div class="flex items-center gap-2">
                    <div class="w-8 h-8 rounded-full bg-slate-200 flex items-center justify-center font-bold text-slate-600 text-xs">
                        KS
                    </div>
                    <div>
                        <p class="text-xs font-semibold text-slate-700">Kasir Shift 1</p>
                        <p class="text-[10px] text-slate-400">Kasir Utama</p>
                    </div>
                </div>
                <button class="text-slate-400 hover:text-red-500 transition">
                    <i data-lucide="log-out" class="w-4 h-4"></i>
                </button>
            </div>
        </aside>

        <!-- KONTEN UTAMA -->
        <main class="flex-1 overflow-y-auto bg-slate-50 p-6" id="main-content">

            <!-- TAB 1: KASIR / POS -->
            <section id="tab-kasir" class="tab-content hidden">
                <div class="flex justify-between items-center mb-6">
                    <h2 class="text-2xl font-bold text-slate-800">Menu Pengkasiran</h2>
                    <span class="text-sm bg-blue-50 text-blue-600 px-3 py-1 rounded-full border border-blue-200">Mode Transaksi On</span>
                </div>
                <div class="grid grid-cols-3 gap-6">
                    <!-- Area Pilih Produk -->
                    <div class="col-span-2 space-y-4">
                        <div class="flex gap-2">
                            <input type="text" placeholder="Cari nama atau barcode produk..." class="w-full px-4 py-2 bg-white border border-slate-200 rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                            <select class="px-3 py-2 bg-white border border-slate-200 rounded-lg text-sm">
                                <option>Semua Kategori</option>
                                <option>Makanan</option>
                                <option>Minuman</option>
                            </select>
                        </div>
                        <div class="grid grid-cols-3 gap-4">
                            <!-- Contoh Card Produk -->
                            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                                <div>
                                    <span class="text-[10px] font-semibold bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded">Ready</span>
                                    <h4 class="font-bold text-slate-800 mt-2">Kopi Susu Gula Aren</h4>
                                    <p class="text-xs text-slate-400">Minuman</p>
                                </div>
                                <div class="mt-4 flex justify-between items-center">
                                    <span class="font-bold text-blue-600">Rp 18.000</span>
                                    <button class="px-3 py-1 bg-blue-600 text-white rounded-lg text-xs hover:bg-blue-700">+ Tambah</button>
                                </div>
                            </div>
                            <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between opacity-60">
                                <div>
                                    <span class="text-[10px] font-semibold bg-red-100 text-red-700 px-2 py-0.5 rounded">Habis</span>
                                    <h4 class="font-bold text-slate-800 mt-2">Roti Bakar Cokelat</h4>
                                    <p class="text-xs text-slate-400">Makanan</p>
                                </div>
                                <div class="mt-4 flex justify-between items-center">
                                    <span class="font-bold text-slate-500">Rp 15.000</span>
                                    <button disabled class="px-3 py-1 bg-slate-300 text-white rounded-lg text-xs cursor-not-allowed">Habis</button>
                                </div>
                            </div>
                        </div>
                    </div>
                    <!-- Area Cart / Keranjang -->
                    <div class="bg-white p-4 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between h-[500px]">
                        <div>
                            <h3 class="font-bold border-b pb-2 text-slate-700">Detail Pesanan</h3>
                            <div class="py-4 text-center text-sm text-slate-400">
                                Belum ada item dipilih
                            </div>
                        </div>
                        <div class="border-t pt-3 space-y-2">
                            <div class="flex justify-between text-sm">
                                <span>Subtotal</span>
                                <span>Rp 0</span>
                            </div>
                            <div class="flex justify-between text-sm">
                                <span>PPN (11%)</span>
                                <span>Rp 0</span>
                            </div>
                            <div class="flex justify-between font-bold text-base border-t pt-2">
                                <span>Total</span>
                                <span class="text-blue-600">Rp 0</span>
                            </div>
                            <button class="w-full bg-emerald-600 text-white font-semibold py-3 rounded-xl hover:bg-emerald-700 transition mt-2">Bayar Sekarang</button>
                        </div>
                    </div>
                </div>
            </section>

            <!-- TAB 2: MASTER DATA - PRODUCT -->
            <section id="tab-master-product" class="tab-content hidden">
                <div class="flex justify-between items-center mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-slate-800">Master Data Produk</h2>
                        <p class="text-sm text-slate-500">Kelola semua produk yang siap jual maupun yang sudah habis.</p>
                    </div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold flex items-center gap-2">
                        <i data-lucide="plus" class="w-4 h-4"></i> Tambah Produk
                    </button>
                </div>
                <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                    <table class="w-full text-left border-collapse">
                        <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                            <tr>
                                <th class="p-4">Nama Produk</th>
                                <th class="p-4">Kategori</th>
                                <th class="p-4">Harga Jual</th>
                                <th class="p-4">Status</th>
                                <th class="p-4 text-right">Aksi</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y text-sm">
                            <tr>
                                <td class="p-4 font-semibold">Kopi Susu Gula Aren</td>
                                <td class="p-4 text-slate-500">Minuman</td>
                                <td class="p-4">Rp 18.000</td>
                                <td class="p-4"><span class="bg-emerald-100 text-emerald-700 px-2.5 py-1 rounded-full text-xs">Ready</span></td>
                                <td class="p-4 text-right space-x-2">
                                    <button class="text-blue-600 hover:underline">Edit</button>
                                    <button class="text-red-600 hover:underline">Hapus</button>
                                </td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 3: MASTER DATA - INPUT BAHAN BAKU -->
            <section id="tab-master-bahan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Input Bahan Baku</h2>
                <p class="text-sm text-slate-500 mb-6">Master data bahan baku mentah dasar pembuatan produk.</p>
                <div class="bg-white p-6 rounded-xl border border-slate-200 max-w-xl shadow-sm space-y-4">
                    <div>
                        <label class="block text-sm font-medium text-slate-700 mb-1">Nama Bahan Baku</label>
                        <input type="text" placeholder="Contoh: Biji Kopi Arabika, Susu UHT" class="w-full border rounded-lg p-2.5 text-sm">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Satuan Dasar</label>
                            <select class="w-full border rounded-lg p-2.5 text-sm">
                                <option>Gram (g)</option>
                                <option>Milliliter (ml)</option>
                                <option>Pcs / Biji</option>
                            </select>
                        </div>
                        <div>
                            <label class="block text-sm font-medium text-slate-700 mb-1">Harga Beli per Satuan</label>
                            <input type="number" placeholder="Rp" class="w-full border rounded-lg p-2.5 text-sm">
                        </div>
                    </div>
                    <button class="w-full bg-blue-600 text-white font-medium py-2.5 rounded-lg text-sm">Simpan Bahan Baku</button>
                </div>
            </section>

            <!-- TAB 4: MASTER DATA - PEMBUATAN PRODUCT -->
            <section id="tab-master-racikan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Pembuatan Product (Resep/BOM)</h2>
                <p class="text-sm text-slate-500 mb-6">Hubungkan produk jadi dengan konsumsi kebutuhan bahan bakunya.</p>
                <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm space-y-4">
                    <div class="max-w-md">
                        <label class="block text-sm font-medium mb-1">Pilih Produk Jadi</label>
                        <select class="w-full border rounded-lg p-2.5 text-sm">
                            <option>-- Pilih Produk --</option>
                            <option>Kopi Susu Gula Aren</option>
                        </select>
                    </div>
                    <div class="border-t pt-4">
                        <h4 class="font-bold text-sm mb-3">Komposisi Bahan Baku</h4>
                        <div class="flex gap-4 items-center mb-2">
                            <select class="flex-1 border rounded-lg p-2 text-sm">
                                <option>Biji Kopi Espreso</option>
                                <option>Susu Cair UHT</option>
                                <option>Sirup Gula Aren</option>
                            </select>
                            <input type="number" placeholder="Jumlah" class="w-32 border rounded-lg p-2 text-sm">
                            <span class="text-xs text-slate-400">Gram / ML</span>
                            <button class="text-red-500 p-2"><i data-lucide="trash-2" class="w-4 h-4"></i></button>
                        </div>
                        <button class="text-sm text-blue-600 font-semibold mt-2">+ Tambah Bahan Resep</button>
                    </div>
                </div>
            </section>

            <!-- TAB 5: INVENTORY - STOCK PRODUCT -->
            <section id="tab-inv-product" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Stock Product (Belum Terjual)</h2>
                <div class="bg-white rounded-xl border p-4 shadow-sm">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-50 border-b text-xs text-slate-500 uppercase">
                            <tr>
                                <th class="p-3">Nama Produk</th>
                                <th class="p-3">Kategori</th>
                                <th class="p-3">Stok Saat Ini</th>
                                <th class="p-3">Status</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr class="border-b">
                                <td class="p-3 font-semibold">Kopi Susu Gula Aren</td>
                                <td class="p-3">Minuman</td>
                                <td class="p-3 font-bold text-blue-600">45 Cup</td>
                                <td class="p-3"><span class="bg-emerald-100 text-emerald-700 px-2 py-0.5 rounded text-xs">Aman</span></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 6: INVENTORY - AKUMULASI STOCK BAHAN BAKU -->
            <section id="tab-inv-bahan" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Akumulasi Stock Bahan Baku</h2>
                <div class="grid grid-cols-3 gap-4">
                    <div class="bg-white p-4 rounded-xl border border-slate-200">
                        <span class="text-xs text-slate-400">Total Biji Kopi</span>
                        <h3 class="text-xl font-bold text-slate-800 mt-1">2.500 Gram</h3>
                        <p class="text-xs text-emerald-600 mt-2">Setara ~ 138 Cangkir</p>
                    </div>
                    <div class="bg-white p-4 rounded-xl border border-slate-200">
                        <span class="text-xs text-slate-400">Susu UHT</span>
                        <h3 class="text-xl font-bold text-slate-800 mt-1">5.000 ML</h3>
                        <p class="text-xs text-emerald-600 mt-2">Setara ~ 50 Porsi</p>
                    </div>
                </div>
            </section>

            <!-- TAB 7: INVENTORY - STOCK OPNAME -->
            <section id="tab-inv-opname" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Stock Opname</h2>
                <p class="text-sm text-slate-500 mb-6">Pencocokan perbandingan ketersediaan stok bahan baku di Sistem vs Fisik.</p>
                <div class="bg-white rounded-xl border overflow-hidden">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-50 border-b text-xs text-slate-500 uppercase">
                            <tr>
                                <th class="p-3">Bahan Baku</th>
                                <th class="p-3">Stok Sistem</th>
                                <th class="p-3">Stok Fisik</th>
                                <th class="p-3">Selisih</th>
                                <th class="p-3">Keterangan</th>
                            </tr>
                        </thead>
                        <tbody class="divide-y">
                            <tr>
                                <td class="p-3 font-semibold">Biji Kopi Arabika</td>
                                <td class="p-3">2.500 g</td>
                                <td class="p-3"><input type="number" value="2400" class="w-24 border rounded p-1 text-center"> g</td>
                                <td class="p-3 text-red-600 font-bold">-100 g</td>
                                <td class="p-3"><input type="text" placeholder="Catatan..." class="border rounded p-1 text-xs w-full"></td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 8: LAPORAN - CASHFLOW -->
            <section id="tab-lap-cashflow" class="tab-content hidden">
                <div class="flex justify-between items-center mb-6">
                    <div>
                        <h2 class="text-2xl font-bold text-slate-800">Cashflow / Pengeluaran</h2>
                        <p class="text-sm text-slate-500">Input belanja bahan baku, operasional, dan belanja aset dapur.</p>
                    </div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">+ Catat Pengeluaran</button>
                </div>
                <!-- Filter -->
                <div class="bg-white p-4 rounded-xl border mb-6 flex gap-4">
                    <input type="date" class="border rounded-lg p-2 text-sm">
                    <select class="border rounded-lg p-2 text-sm">
                        <option>Semua Kategori</option>
                        <option>Belanja Bahan Baku</option>
                        <option>Operasional</option>
                        <option>Asset Dapur</option>
                    </select>
                    <button class="bg-slate-800 text-white px-4 py-2 rounded-lg text-sm">Filter</button>
                </div>
            </section>

            <!-- TAB 9: LAPORAN - PENJUALAN HARIAN -->
            <section id="tab-lap-penjualan-harian" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Penjualan Harian</h2>
                <p class="text-sm text-slate-500 mb-6">Rincian detail barang dan item yang terjual.</p>
                <div class="bg-white p-4 rounded-xl border mb-4 flex gap-3">
                    <input type="text" placeholder="Search nama produk..." class="border p-2 rounded-lg text-sm flex-1">
                    <input type="date" class="border p-2 rounded-lg text-sm">
                </div>
                <div class="bg-white rounded-xl border overflow-hidden">
                    <table class="w-full text-left text-sm">
                        <thead class="bg-slate-50 border-b text-xs text-slate-500 uppercase">
                            <tr>
                                <th class="p-3">Waktu</th>
                                <th class="p-3">Nama Produk</th>
                                <th class="p-3">Kategori</th>
                                <th class="p-3">Qty Terjual</th>
                                <th class="p-3">Total Jual</th>
                            </tr>
                        </thead>
                        <tbody>
                            <tr>
                                <td class="p-3 text-slate-400">14:20 WIB</td>
                                <td class="p-3 font-semibold">Kopi Susu Gula Aren</td>
                                <td class="p-3">Minuman</td>
                                <td class="p-3">2 Cup</td>
                                <td class="p-3">Rp 36.000</td>
                            </tr>
                        </tbody>
                    </table>
                </div>
            </section>

            <!-- TAB 10: LAPORAN - SALES -->
            <section id="tab-lap-sales" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Laporan Sales Transaction</h2>
                <p class="text-sm text-slate-500 mb-6">Ringkasan transaksi kasir mencakup Omset, HPP Bahan Baku, Overhead, dan Profit.</p>
                <div class="grid grid-cols-4 gap-4 mb-6">
                    <div class="bg-white p-4 rounded-xl border">
                        <span class="text-xs text-slate-400">Omset Penjualan</span>
                        <h4 class="text-lg font-bold text-slate-800 mt-1">Rp 1.500.000</h4>
                    </div>
                    <div class="bg-white p-4 rounded-xl border">
                        <span class="text-xs text-slate-400">Modal Bahan Baku</span>
                        <h4 class="text-lg font-bold text-slate-800 mt-1">Rp 600.000</h4>
                    </div>
                    <div class="bg-white p-4 rounded-xl border">
                        <span class="text-xs text-slate-400">Modal Overhead</span>
                        <h4 class="text-lg font-bold text-slate-800 mt-1">Rp 150.000</h4>
                    </div>
                    <div class="bg-white p-4 rounded-xl border">
                        <span class="text-xs text-slate-400">Gross Profit</span>
                        <h4 class="text-lg font-bold text-emerald-600 mt-1">Rp 750.000</h4>
                    </div>
                </div>
            </section>

            <!-- TAB 11: LAPORAN - PNL -->
            <section id="tab-lap-pnl" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-2">Laporan Profit & Loss (PnL)</h2>
                <p class="text-sm text-slate-500 mb-6">Keseluruhan kondisi data keuangan bisnis secara menyeluruh.</p>
                <div class="bg-white p-6 rounded-xl border space-y-3 max-w-2xl">
                    <div class="flex justify-between border-b pb-2 text-sm">
                        <span>Modal Bahan Baku (Belum Terolah)</span>
                        <span class="font-medium">Rp 2.000.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm">
                        <span>Modal Barang Jadi (Belum Terjual)</span>
                        <span class="font-medium">Rp 500.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm text-blue-600 font-bold">
                        <span>Omset Penjualan</span>
                        <span>Rp 10.000.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm text-red-500">
                        <span>(-) Modal Bahan Baku Terjual</span>
                        <span>Rp 4.000.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm text-red-500">
                        <span>(-) Modal Overhead Terjual</span>
                        <span>Rp 1.000.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm font-bold bg-slate-50 p-2 rounded">
                        <span>PROFIT KOTOR</span>
                        <span class="text-emerald-600">Rp 5.000.000</span>
                    </div>
                    <div class="flex justify-between border-b pb-2 text-sm text-red-500">
                        <span>(-) Belanja Operasional</span>
                        <span>Rp 1.500.000</span>
                    </div>
                    <div class="flex justify-between text-base font-bold bg-emerald-50 text-emerald-800 p-3 rounded-lg border border-emerald-200">
                        <span>PROFIT BERSIH (NET PROFIT)</span>
                        <span>Rp 3.500.000</span>
                    </div>
                </div>
            </section>

            <!-- TAB 12: PENGATURAN - OVERHEAD & PPN -->
            <section id="tab-set-overhead" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Pengaturan Persentase Overhead & PPN</h2>
                <div class="bg-white p-6 rounded-xl border max-w-md space-y-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">Persentase Overhead (%)</label>
                        <input type="number" value="10" class="w-full border rounded-lg p-2 text-sm">
                        <span class="text-xs text-slate-400">Digunakan untuk estimasi biaya listrik, air, dan kemasan per porsi.</span>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Pajak PPN (%)</label>
                        <input type="number" value="11" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">Simpan Pengaturan</button>
                </div>
            </section>

            <!-- TAB 13: PENGATURAN - AKUN & BRANDING -->
            <section id="tab-set-akun" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Konfigurasi Toko & Branding</h2>
                <div class="bg-white p-6 rounded-xl border max-w-xl space-y-4">
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-1">Nama Toko / Outlet</label>
                            <input type="text" value="Kedai Kopi Utama" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1">Warna Brand Aplikasi</label>
                            <input type="color" value="#3b82f6" class="w-full h-10 border rounded-lg p-1">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Tagline Toko</label>
                        <input type="text" value="Nikmatnya Kopi Asli Indonesia" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <div class="grid grid-cols-2 gap-4">
                        <div>
                            <label class="block text-sm font-medium mb-1">No. Telepon</label>
                            <input type="text" value="021-12345678" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                        <div>
                            <label class="block text-sm font-medium mb-1">WhatsApp</label>
                            <input type="text" value="081234567890" class="w-full border rounded-lg p-2 text-sm">
                        </div>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Alamat Lengkap</label>
                        <textarea class="w-full border rounded-lg p-2 text-sm" rows="3">Jl. Raya Merdeka No. 123, Jakarta Pusat</textarea>
                    </div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">Update Profil Toko</button>
                </div>
            </section>

            <!-- TAB 14: PENGATURAN - STRUK -->
            <section id="tab-set-struk" class="tab-content hidden">
                <h2 class="text-2xl font-bold text-slate-800 mb-6">Pengaturan Struk Pembayaran</h2>
                <div class="bg-white p-6 rounded-xl border max-w-md space-y-4">
                    <div>
                        <label class="block text-sm font-medium mb-1">Lebar Kertas</label>
                        <select class="w-full border rounded-lg p-2 text-sm">
                            <option>58 mm (Thermal Mini)</option>
                            <option>80 mm (Standard POS)</option>
                            <option>Custom Size</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Font Size</label>
                        <select class="w-full border rounded-lg p-2 text-sm">
                            <option>Kecil (Small)</option>
                            <option selected>Normal</option>
                            <option>Besar (Large)</option>
                        </select>
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Pesan Header Struk</label>
                        <input type="text" value="Selamat Datang di Kedai Kopi!" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <div>
                        <label class="block text-sm font-medium mb-1">Pesan Footer Struk</label>
                        <input type="text" value="Terima Kasih Atas Kunjungan Anda" class="w-full border rounded-lg p-2 text-sm">
                    </div>
                    <button class="bg-blue-600 text-white px-4 py-2 rounded-lg text-sm font-semibold">Simpan Template Struk</button>
                </div>
            </section>

        </main>
    </div>

    <!-- LOGIKA SCRIPT JAVASCRIPT -->
    <script>
        // Inisialisasi Icon Lucide
        lucide.createIcons();

        // Fungsi Switch Navigasi Tab
        function switchTab(tabId) {
            // Sembunyikan semua tab konten
            const contents = document.querySelectorAll('.tab-content');
            contents.forEach(content => content.classList.add('hidden'));

            // Hapus status aktif dari semua tombol navigasi
            const buttons = document.querySelectorAll('.nav-btn');
            buttons.forEach(btn => btn.classList.remove('active-menu'));

            // Tampilkan tab yang dipilih
            const selectedTab = document.getElementById('tab-' + tabId);
            if (selectedTab) {
                selectedTab.classList.remove('hidden');
            }

            // Tandai tombol yang aktif (jika bukan tombol utama Kasir)
            const selectedBtn = document.getElementById('btn-' + tabId);
            if (selectedBtn && tabId !== 'kasir') {
                selectedBtn.classList.add('active-menu');
            }
        }

        // Jalankan default tab saat pertama dimuat (default: Kasir POS)
        document.addEventListener('DOMContentLoaded', () => {
            switchTab('kasir');
        });
    </script>
</body>
</html>
