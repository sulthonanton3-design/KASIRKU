<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <meta name="viewport" content="width=device-width, initial-scale=1.0">
    <title>KASIRKU - POS & Inventory System</title>
    <!-- Tailwind CSS -->
    <script src="https://cdn.tailwindcss.com"></script>
    <!-- Lucide Icons -->
    <script src="https://unpkg.com/lucide@latest"></script>
    <style>
        .active-tab {
            background-color: #3b82f6;
            color: #ffffff;
        }
        .active-tab:hover {
            background-color: #2563eb;
        }
    </style>
</head>
<body class="bg-slate-100 font-sans text-slate-800 antialiased min-h-screen flex">

    <!-- SIDEBAR -->
    <aside class="w-64 bg-slate-900 text-slate-300 flex flex-col justify-between shrink-0 h-screen sticky top-0">
        <div>
            <!-- Logo & Brand -->
            <div class="p-5 border-b border-slate-800 flex items-center space-x-3">
                <div class="bg-blue-600 text-white p-2 rounded-lg">
                    <i data-lucide="store" class="w-6 h-6"></i>
                </div>
                <div>
                    <h1 class="font-bold text-white text-lg leading-none">KASIRKU</h1>
                    <span class="text-xs text-slate-500">POS & Inventory System</span>
                </div>
            </div>

            <!-- Navigation Menu -->
            <nav class="p-4 space-y-1">
                <div class="px-3 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider">Penjualan</div>
                <button onclick="switchTab('pos')" id="btn-pos" class="tab-btn active-tab w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium transition">
                    <i data-lucide="shopping-cart" class="w-4 h-4"></i>
                    <span>Kasir / POS</span>
                </button>

                <div class="px-3 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mt-4">Manajemen Resep & HPP</div>
                <button onclick="switchTab('hpp')" id="btn-hpp" class="tab-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 hover:text-white transition">
                    <i data-lucide="calculator" class="w-4 h-4"></i>
                    <span>Kalkulator HPP</span>
                </button>
                <button onclick="switchTab('resep')" id="btn-resep" class="tab-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 hover:text-white transition">
                    <i data-lucide="chef-hat" class="w-4 h-4"></i>
                    <span>Resep Produk</span>
                </button>
                <button onclick="switchTab('bahan')" id="btn-bahan" class="tab-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 hover:text-white transition">
                    <i data-lucide="package" class="w-4 h-4"></i>
                    <span>Data Bahan Baku</span>
                </button>

                <div class="px-3 py-2 text-xs font-semibold text-slate-500 uppercase tracking-wider mt-4">Inventory</div>
                <button onclick="switchTab('inv-product')" id="btn-inv-product" class="tab-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 hover:text-white transition">
                    <i data-lucide="boxes" class="w-4 h-4"></i>
                    <span>Stok Produk</span>
                </button>
                <button onclick="switchTab('inv-bahan')" id="btn-inv-bahan" class="tab-btn w-full flex items-center space-x-3 px-3 py-2.5 rounded-lg text-sm font-medium hover:bg-slate-800 hover:text-white transition">
                    <i data-lucide="layers" class="w-4 h-4"></i>
                    <span>Akumulasi Bahan Baku</span>
                </button>
            </nav>
        </div>

        <!-- User Info -->
        <div class="p-4 border-t border-slate-800 flex items-center space-x-3">
            <div class="w-9 h-9 rounded-full bg-slate-700 flex items-center justify-center font-bold text-white">
                A
            </div>
            <div>
                <div class="text-sm font-medium text-white">Kasir Utama</div>
                <div class="text-xs text-slate-500">Shift 1 (Aktif)</div>
            </div>
        </div>
    </aside>

    <!-- MAIN CONTENT -->
    <main class="flex-1 p-8 overflow-y-auto h-screen">

        <!-- TAB 1: KASIR / POS -->
        <section id="tab-pos" class="tab-content">
            <div class="flex items-center justify-between mb-6">
                <div>
                    <h2 class="text-2xl font-bold text-slate-800">Kasir / Point of Sales</h2>
                    <p class="text-sm text-slate-500">Pilih produk dan selesaikan transaksi dengan cepat.</p>
                </div>
            </div>

            <div class="grid grid-cols-12 gap-6">
                <!-- Product List -->
                <div class="col-span-7 bg-white p-6 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex items-center justify-between mb-4">
                        <h3 class="font-bold text-slate-700">Daftar Produk</h3>
                        <input type="text" placeholder="Cari produk..." class="px-3 py-1.5 border rounded-lg text-sm focus:outline-none focus:ring-2 focus:ring-blue-500">
                    </div>
                    <div id="product-grid" class="grid grid-cols-3 gap-4">
                        <!-- Items rendered via JS -->
                    </div>
                </div>

                <!-- Cart / Summary -->
                <div class="col-span-5 bg-white p-6 rounded-xl border border-slate-200 shadow-sm flex flex-col justify-between">
                    <div>
                        <h3 class="font-bold text-slate-700 mb-4 border-b pb-2">Keranjang Belanja</h3>
                        <div id="cart-items" class="space-y-3 max-h-64 overflow-y-auto pr-1">
                            <p class="text-sm text-slate-400 text-center py-8">Keranjang masih kosong</p>
                        </div>
                    </div>

                    <div class="border-t pt-4 mt-6 space-y-2">
                        <div class="flex justify-between text-sm text-slate-600">
                            <span>Subtotal</span>
                            <span id="cart-subtotal" class="font-semibold">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm text-slate-600">
                            <span>PPN (11%)</span>
                            <span id="cart-tax" class="font-semibold">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-lg font-bold text-slate-800 border-t pt-2">
                            <span>Total</span>
                            <span id="cart-total" class="text-blue-600">Rp 0</span>
                        </div>
                        <button onclick="openCheckoutModal()" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-3 rounded-xl font-bold mt-4 transition shadow-lg shadow-blue-500/30">
                            Bayar Sekarang
                        </button>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 2: KALKULATOR HPP -->
        <section id="tab-hpp" class="tab-content hidden">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Kalkulator HPP Produk</h2>
            <p class="text-sm text-slate-500 mb-6">Hitung Harga Pokok Produksi berdasarkan resep dan estimasi margin keuntungan.</p>

            <div class="bg-white p-6 rounded-xl border border-slate-200 shadow-sm max-w-2xl">
                <div class="space-y-4">
                    <div>
                        <label class="block text-sm font-semibold text-slate-700 mb-1">Pilih Produk</label>
                        <select id="hpp-select-product" onchange="calculateHPP()" class="w-full border rounded-lg p-2.5 text-sm focus:ring-2 focus:ring-blue-500">
                            <!-- Options generated via JS -->
                        </select>
                    </div>

                    <div class="p-4 bg-slate-50 rounded-lg border border-slate-100 space-y-2">
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Total HPP Bahan Baku:</span>
                            <span id="hpp-cost-display" class="font-bold text-slate-800">Rp 0</span>
                        </div>
                        <div class="flex justify-between text-sm">
                            <span class="text-slate-600">Margin Keuntungan (Target):</span>
                            <span class="font-bold text-emerald-600">40%</span>
                        </div>
                        <div class="flex justify-between text-base font-bold border-t pt-2">
                            <span>Rekomendasi Harga Jual:</span>
                            <span id="hpp-recommended-price" class="text-blue-600">Rp 0</span>
                        </div>
                    </div>
                </div>
            </div>
        </section>

        <!-- TAB 3: RESEP PRODUK -->
        <section id="tab-resep" class="tab-content hidden">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Resep & Komposisi Produk</h2>
            <p class="text-sm text-slate-500 mb-6">Atur racikan dan pemakaian bahan untuk setiap porsi produk.</p>

            <div id="resep-list" class="grid grid-cols-2 gap-6">
                <!-- Dynamic Recipe Cards -->
            </div>
        </section>

        <!-- TAB 4: DATA BAHAN BAKU -->
        <section id="tab-bahan" class="tab-content hidden">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Data Bahan Baku</h2>
            <p class="text-sm text-slate-500 mb-6">Kelola daftar bahan mentah beserta skema pembelian globalnya.</p>

            <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                        <tr>
                            <th class="p-4">Nama Bahan Baku</th>
                            <th class="p-4">Volume / Pack</th>
                            <th class="p-4">Satuan</th>
                            <th class="p-4">Harga Beli Global</th>
                            <th class="p-4">Harga Per Satuan (HPP Unit)</th>
                        </tr>
                    </thead>
                    <tbody id="bahan-table-body" class="divide-y text-sm">
                        <!-- Dynamic Bahan Rows -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- TAB 5: INVENTORY - STOK PRODUK -->
        <section id="tab-inv-product" class="tab-content hidden">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Stok Produk Siap Jual</h2>
            <p class="text-sm text-slate-500 mb-6">Monitoring ketersediaan stok produk jadi di etalase/kasir.</p>

            <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                        <tr>
                            <th class="p-4">Nama Produk</th>
                            <th class="p-4">Kategori</th>
                            <th class="p-4">Status Ketersediaan</th>
                            <th class="p-4">Keterangan</th>
                        </tr>
                    </thead>
                    <tbody id="inv-product-table-body" class="divide-y text-sm">
                        <!-- Diisi via JS -->
                    </tbody>
                </table>
            </div>
        </section>

        <!-- TAB 6: INVENTORY - AKUMULASI STOK BAHAN -->
        <section id="tab-inv-bahan" class="tab-content hidden">
            <h2 class="text-2xl font-bold text-slate-800 mb-2">Akumulasi Stok Bahan Baku</h2>
            <p class="text-sm text-slate-500 mb-6">Daftar akumulasi total stok bahan baku mentah yang tersimpan di gudang.</p>

            <div class="bg-white rounded-xl border border-slate-200 overflow-hidden shadow-sm">
                <table class="w-full text-left border-collapse">
                    <thead class="bg-slate-50 border-b text-xs font-semibold text-slate-500 uppercase">
                        <tr>
                            <th class="p-4">Nama Bahan Baku</th>
                            <th class="p-4">Total Stok Tersedia</th>
                            <th class="p-4">Satuan</th>
                            <th class="p-4">Estimasi HPP Global</th>
                        </tr>
                    </thead>
                    <tbody id="inv-bahan-table-body" class="divide-y text-sm">
                        <!-- Diisi via JS -->
                    </tbody>
                </table>
            </div>
        </section>

    </main>

    <!-- CHECKOUT & INVOICE MODAL -->
    <div id="checkout-modal" class="fixed inset-0 bg-slate-900/50 backdrop-blur-sm hidden flex items-center justify-center p-4 z-50">
        <div class="bg-white rounded-2xl max-w-md w-full p-6 shadow-2xl relative">
            <button onclick="closeCheckoutModal()" class="absolute top-4 right-4 text-slate-400 hover:text-slate-600">
                <i data-lucide="x" class="w-5 h-5"></i>
            </button>

            <!-- Form Pembayaran -->
            <div id="checkout-form-view">
                <h3 class="text-xl font-bold text-slate-800 mb-1">Selesaikan Transaksi</h3>
                <p class="text-sm text-slate-500 mb-4">Masukkan nominal pembayaran dari pelanggan.</p>

                <div class="bg-slate-50 p-4 rounded-xl mb-4 space-y-1 text-sm border">
                    <div class="flex justify-between text-slate-600">
                        <span>Total Tagihan:</span>
                        <span id="modal-total-tagihan" class="font-bold text-slate-900">Rp 0</span>
                    </div>
                </div>

                <div class="space-y-3">
                    <div>
                        <label class="block text-xs font-semibold text-slate-600 uppercase mb-1">Uang Diterima (Rp)</label>
                        <input type="number" id="cash-received" oninput="calculateChange()" placeholder="0" class="w-full border rounded-xl p-3 font-bold text-lg focus:ring-2 focus:ring-blue-500 focus:outline-none">
                    </div>
                    <div class="flex justify-between text-sm font-semibold p-2">
                        <span>Kembalian:</span>
                        <span id="modal-kembalian" class="text-emerald-600 font-bold">Rp 0</span>
                    </div>
                    <button onclick="processPayment()" class="w-full bg-emerald-600 hover:bg-emerald-700 text-white py-3 rounded-xl font-bold transition shadow-lg shadow-emerald-600/20">
                        Proses & Cetak Struk
                    </button>
                </div>
            </div>

            <!-- Struk / Invoice Output (Muncul setelah bayar) -->
            <div id="receipt-view" class="hidden">
                <div class="text-center pb-4 border-b border-dashed border-slate-300">
                    <h4 class="font-bold text-slate-800">KASIRKU STORE</h4>
                    <p class="text-xs text-slate-500">Jl. Raya Resto No. 12, Jawa Timur</p>
                    <p id="receipt-date" class="text-[10px] text-slate-400 mt-1"></p>
                </div>

                <div id="receipt-items-list" class="py-4 space-y-2 text-xs divide-y divide-slate-100">
                    <!-- Items Struk -->
                </div>

                <div class="border-t border-dashed border-slate-300 pt-3 text-xs space-y-1">
                    <div class="flex justify-between font-semibold">
                        <span>Subtotal:</span>
                        <span id="receipt-subtotal">Rp 0</span>
                    </div>
                    <div class="flex justify-between text-slate-500">
                        <span>PPN (11%):</span>
                        <span id="receipt-tax">Rp 0</span>
                    </div>
                    <div class="flex justify-between font-bold text-sm text-slate-800 pt-1">
                        <span>Total:</span>
                        <span id="receipt-total">Rp 0</span>
                    </div>
                    <div class="flex justify-between text-slate-500">
                        <span>Bayar:</span>
                        <span id="receipt-cash">Rp 0</span>
                    </div>
                    <div class="flex justify-between font-semibold text-emerald-600">
                        <span>Kembali:</span>
                        <span id="receipt-change">Rp 0</span>
                    </div>
                </div>

                <div class="mt-6 space-y-2">
                    <button onclick="resetPOS()" class="w-full bg-blue-600 hover:bg-blue-700 text-white py-2.5 rounded-xl text-sm font-bold transition">
                        Transaksi Baru
                    </button>
                </div>
            </div>
        </div>
    </div>

    <!-- JAVASCRIPT LOGIC -->
    <script>
        // DATA MASTER
        const bahanBakuList = [
            { id: 'b1', nama: 'Kopi Espresso Blend', volume: 1000, satuan: 'gram', hargaGlobal: 180000, qty: 5 },
            { id: 'b2', nama: 'Susu UHT Full Cream', volume: 1000, satuan: 'ml', hargaGlobal: 20000, qty: 12 },
            { id: 'b3', nama: 'Syrup Aren Pure', volume: 500, satuan: 'ml', hargaGlobal: 35000, qty: 8 },
            { id: 'b4', nama: 'Matcha Powder Premium', volume: 500, satuan: 'gram', hargaGlobal: 120000, qty: 3 }
        ];

        const products = [
            {
                id: 'p1',
                nama: 'Kopi Kenangan Aren',
                harga: 18000,
                kategori: 'Minuman',
                status: 'Ready',
                resep: [
                    { bahanId: 'b1', jumlah: 18 },
                    { bahanId: 'b2', jumlah: 120 },
                    { bahanId: 'b3', jumlah: 25 }
                ]
            },
            {
                id: 'p2',
                nama: 'Matcha Latte',
                harga: 22000,
                kategori: 'Minuman',
                status: 'Ready',
                resep: [
                    { bahanId: 'b4', jumlah: 15 },
                    { bahanId: 'b2', jumlah: 150 }
                ]
            },
            {
                id: 'p3',
                nama: 'Americano Hot/Iced',
                harga: 15000,
                kategori: 'Minuman',
                status: 'Ready',
                resep: [
                    { bahanId: 'b1', jumlah: 18 }
                ]
            }
        ];

        let cart = [];

        // INITIALIZATION
        document.addEventListener("DOMContentLoaded", () => {
            lucide.createIcons();
            renderProducts();
            renderBahanTable();
            renderResepList();
            populateHppSelect();
            renderInventoryTables();
        });

        // TAB SWITCHING LOGIC
        function switchTab(tabId) {
            document.querySelectorAll('.tab-content').forEach(el => el.classList.add('hidden'));
            document.querySelectorAll('.tab-btn').forEach(btn => btn.classList.remove('active-tab'));

            document.getElementById(`tab-${tabId}`).classList.remove('hidden');
            const activeBtn = document.getElementById(`btn-${tabId}`);
            if (activeBtn) activeBtn.classList.add('active-tab');

            if (tabId === 'inv-product' || tabId === 'inv-bahan') {
                renderInventoryTables();
            }

            // Re-initialize Lucide Icons for rendered tab content
            lucide.createIcons();
        }

        // POS SYSTEM LOGIC
        function renderProducts() {
            const grid = document.getElementById('product-grid');
            grid.innerHTML = products.map(p => `
                <div onclick="addToCart('${p.id}')" class="p-4 border rounded-xl hover:border-blue-500 hover:shadow-md cursor-pointer transition bg-slate-50 hover:bg-white flex flex-col justify-between">
                    <div>
                        <span class="text-[10px] font-bold text-blue-600 bg-blue-50 px-2 py-0.5 rounded-full uppercase">${p.kategori}</span>
                        <h4 class="font-bold text-slate-800 text-sm mt-2">${p.nama}</h4>
                    </div>
                    <div class="mt-3 font-bold text-slate-900 text-sm">
                        Rp ${p.harga.toLocaleString('id-ID')}
                    </div>
                </div>
            `).join('');
        }

        function addToCart(productId) {
            const product = products.find(p => p.id === productId);
            const exist = cart.find(item => item.id === productId);

            if (exist) {
                exist.qty += 1;
            } else {
                cart.push({ ...product, qty: 1 });
            }
            updateCartUI();
        }

        function updateCartUI() {
            const container = document.getElementById('cart-items');
            if (cart.length === 0) {
                container.innerHTML = '<p class="text-sm text-slate-400 text-center py-8">Keranjang masih kosong</p>';
            } else {
                container.innerHTML = cart.map(item => `
                    <div class="flex items-center justify-between text-sm bg-slate-50 p-2.5 rounded-lg border">
                        <div class="flex-1">
                            <h5 class="font-semibold text-slate-800">${item.nama}</h5>
                            <span class="text-xs text-slate-500">Rp ${item.harga.toLocaleString('id-ID')}</span>
                        </div>
                        <div class="flex items-center space-x-2">
                            <button onclick="changeQty('${item.id}', -1)" class="w-6 h-6 bg-slate-200 rounded flex items-center justify-center text-xs font-bold">-</button>
                            <span class="font-bold text-xs">${item.qty}</span>
                            <button onclick="changeQty('${item.id}', 1)" class="w-6 h-6 bg-slate-200 rounded flex items-center justify-center text-xs font-bold">+</button>
                        </div>
                    </div>
                `).join('');
            }

            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const tax = subtotal * 0.11;
            const total = subtotal + tax;

            document.getElementById('cart-subtotal').innerText = `Rp ${subtotal.toLocaleString('id-ID')}`;
            document.getElementById('cart-tax').innerText = `Rp ${tax.toLocaleString('id-ID')}`;
            document.getElementById('cart-total').innerText = `Rp ${total.toLocaleString('id-ID')}`;
        }

        function changeQty(productId, delta) {
            const item = cart.find(i => i.id === productId);
            if (item) {
                item.qty += delta;
                if (item.qty <= 0) {
                    cart = cart.filter(i => i.id !== productId);
                }
            }
            updateCartUI();
        }

        // CHECKOUT & MODAL LOGIC
        function openCheckoutModal() {
            if (cart.length === 0) return alert('Keranjang belanja kosong!');
            
            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const total = subtotal + (subtotal * 0.11);

            document.getElementById('modal-total-tagihan').innerText = `Rp ${total.toLocaleString('id-ID')}`;
            document.getElementById('cash-received').value = '';
            document.getElementById('modal-kembalian').innerText = 'Rp 0';
            
            document.getElementById('checkout-form-view').classList.remove('hidden');
            document.getElementById('receipt-view').classList.add('hidden');
            document.getElementById('checkout-modal').classList.remove('hidden');
        }

        function closeCheckoutModal() {
            document.getElementById('checkout-modal').classList.add('hidden');
        }

        function calculateChange() {
            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const total = subtotal + (subtotal * 0.11);
            const cash = parseFloat(document.getElementById('cash-received').value) || 0;
            const change = cash - total;

            document.getElementById('modal-kembalian').innerText = change >= 0 ? `Rp ${change.toLocaleString('id-ID')}` : 'Rp 0 (Uang Kurang)';
        }

        function processPayment() {
            const subtotal = cart.reduce((sum, item) => sum + (item.harga * item.qty), 0);
            const tax = subtotal * 0.11;
            const total = subtotal + tax;
            const cash = parseFloat(document.getElementById('cash-received').value) || 0;

            if (cash < total) {
                return alert('Nominal uang yang diterima kurang dari total tagihan!');
            }

            const change = cash - total;

            // Render Invoice Struk
            document.getElementById('receipt-date').innerText = new Date().toLocaleString('id-ID');
            document.getElementById('receipt-items-list').innerHTML = cart.map(item => `
                <div class="flex justify-between pt-1">
                    <div>
                        <div class="font-semibold text-slate-700">${item.nama}</div>
                        <div class="text-[10px] text-slate-400">${item.qty} x Rp ${item.harga.toLocaleString('id-ID')}</div>
                    </div>
                    <div class="font-semibold text-slate-700">Rp ${(item.qty * item.harga).toLocaleString('id-ID')}</div>
                </div>
            `).join('');

            document.getElementById('receipt-subtotal').innerText = `Rp ${subtotal.toLocaleString('id-ID')}`;
            document.getElementById('receipt-tax').innerText = `Rp ${tax.toLocaleString('id-ID')}`;
            document.getElementById('receipt-total').innerText = `Rp ${total.toLocaleString('id-ID')}`;
            document.getElementById('receipt-cash').innerText = `Rp ${cash.toLocaleString('id-ID')}`;
            document.getElementById('receipt-change').innerText = `Rp ${change.toLocaleString('id-ID')}`;

            // Switch to receipt view
            document.getElementById('checkout-form-view').classList.add('hidden');
            document.getElementById('receipt-view').classList.remove('hidden');
        }

        function resetPOS() {
            cart = [];
            updateCartUI();
            closeCheckoutModal();
        }

        // HPP CALCULATOR LOGIC
        function populateHppSelect() {
            const select = document.getElementById('hpp-select-product');
            select.innerHTML = products.map(p => `<option value="${p.id}">${p.nama}</option>`).join('');
            calculateHPP();
        }

        function calculateHPP() {
            const productId = document.getElementById('hpp-select-product').value;
            const product = products.find(p => p.id === productId);

            let totalHpp = 0;
            product.resep.forEach(r => {
                const bahan = bahanBakuList.find(b => b.id === r.bahanId);
                const unitPrice = bahan.hargaGlobal / bahan.volume;
                totalHpp += unitPrice * r.jumlah;
            });

            const marginMultiplier = 1.40; // Target Margin 40%
            const recPrice = totalHpp * marginMultiplier;

            document.getElementById('hpp-cost-display').innerText = `Rp ${Math.round(totalHpp).toLocaleString('id-ID')}`;
            document.getElementById('hpp-recommended-price').innerText = `Rp ${Math.round(recPrice).toLocaleString('id-ID')}`;
        }

        // RESEP LOGIC
        function renderResepList() {
            const container = document.getElementById('resep-list');
            container.innerHTML = products.map(p => `
                <div class="bg-white p-5 rounded-xl border border-slate-200 shadow-sm">
                    <div class="flex justify-between items-center border-b pb-3 mb-3">
                        <h3 class="font-bold text-slate-800">${p.nama}</h3>
                        <span class="text-xs bg-slate-100 text-slate-600 px-2 py-1 rounded font-medium">${p.resep.length} Bahan</span>
                    </div>
                    <ul class="space-y-2 text-sm">
                        ${p.resep.map(r => {
                            const b = bahanBakuList.find(item => item.id === r.bahanId);
                            return `
                                <div class="flex justify-between text-xs py-1 border-b border-slate-50">
                                    <span class="text-slate-600">${b.nama}</span>
                                    <span class="font-semibold text-slate-800">${r.jumlah} ${b.satuan}</span>
                                </div>
                            `;
                        }).join('')}
                    </ul>
                </div>
            `).join('');
        }

        // DATA BAHAN BAKU LOGIC
        function renderBahanTable() {
            const body = document.getElementById('bahan-table-body');
            body.innerHTML = bahanBakuList.map(b => {
                const unitPrice = b.hargaGlobal / b.volume;
                return `
                    <tr>
                        <td class="p-4 font-semibold text-slate-800">${b.nama}</td>
                        <td class="p-4 text-slate-600">${b.volume.toLocaleString('id-ID')}</td>
                        <td class="p-4 text-slate-500">${b.satuan}</td>
                        <td class="p-4 font-semibold">Rp ${b.hargaGlobal.toLocaleString('id-ID')}</td>
                        <td class="p-4 font-bold text-blue-600">Rp ${unitPrice.toFixed(2)} / ${b.satuan}</td>
                    </tr>
                `;
            }).join('');
        }

        // INVENTORY LOGIC
        function renderInventoryTables() {
            // Render Stok Produk
            const invProdBody = document.getElementById('inv-product-table-body');
            if (invProdBody) {
                invProdBody.innerHTML = products.map(p => `
                    <tr>
                        <td class="p-4 font-semibold text-slate-800">${p.nama}</td>
                        <td class="p-4 text-slate-500">${p.kategori}</td>
                        <td class="p-4">
                            <span class="${p.status === 'Ready' ? 'bg-emerald-100 text-emerald-700' : 'bg-red-100 text-red-700'} px-2.5 py-1 rounded-full text-xs font-semibold">
                                ${p.status}
                            </span>
                        </td>
                        <td class="p-4 text-xs text-slate-400">Siap disajikan via POS</td>
                    </tr>
                `).join('');
            }

            // Render Akumulasi Stok Bahan Baku
            const invBahanBody = document.getElementById('inv-bahan-table-body');
            if (invBahanBody) {
                invBahanBody.innerHTML = bahanBakuList.map(b => `
                    <tr>
                        <td class="p-4 font-semibold text-slate-800">${b.nama}</td>
                        <td class="p-4 font-bold text-blue-600">${(b.volume * b.qty).toLocaleString('id-ID')}</td>
                        <td class="p-4 text-slate-500">${b.satuan}</td>
                        <td class="p-4 font-semibold">Rp ${(b.hargaGlobal * b.qty).toLocaleString('id-ID')}</td>
                    </tr>
                `).join('');
            }
        }
    </script>
</body>
</html>
