# Template Structure - Surat Penawaran KBI

## Document Layout

```
┌─────────────────────────────────────────────────────────────┐
│ [LETTERHEAD: KBI Logo + Company Info + Blue Border]         │
├─────────────────────────────────────────────────────────────┤
│ Samboja, [date]                      Nomor: KQ-XXX/QUO-...  │
│                                                             │
│ Kepada Yth.                                                 │
│ [Nama Penerima]                                             │
│ [Jabatan / Perusahaan]                                      │
│ Ditempat                                                    │
│                                                             │
│ Dengan hormat,                                              │
│ Bersama dengan ini Kami, menyampaikan Penawaran Harga...    │
├─────────────────────────────────────────────────────────────┤
│ ┌─────┬────────────┬────────┬───────┬──────────┬──────────┐ │
│ │ NO  │ Deskripsi  │  Qty   │Satuan │Harga (Rp)│Jumlah(Rp)│ │
│ ├─────┼────────────┼────────┼───────┼──────────┼──────────┤ │
│ │     │ Lokasi Proyek [project location]                 │ │
│ │     │ Alat : [equipment]                               │ │
│ │     │ Pekerjaan Pengeboran                             │ │
│ ├─────┼────────────┼────────┼───────┼──────────┼──────────┤ │
│ │  1  │ Item desc  │   qty  │  m¹   │  price   │  total   │ │
│ │     │  a. Sub    │   qty  │  m¹   │  price   │  total   │ │
│ │     │  b. Sub    │   qty  │  m¹   │  price   │ Rate Only│ │
│ │  2  │ Item desc  │   qty  │  mᶟ   │  price   │  total   │ │
│ │ ... │ ...        │  ...   │ ...   │   ...    │   ...    │ │
│ ├─────┴────────────┴────────┼───────┴──────────┼──────────┤ │
│ │ Terbilang: [amount in     │ Nilai Jasa       │ [total]  │ │
│ │ Indonesian words]         │ DPP (×11/12)     │ [dpp]    │ │
│ │                           │ PPN 12%          │ [ppn]    │ │
│ │                           │ GRAND TOTAL      │ [grand]  │ │
│ └───────────────────────────┴──────────────────┴──────────┘ │
├─────────────────────────────────────────────────────────────┤
│ Keterangan:                                                 │
│ 1. Harga satuan belum termasuk PPN 12%...                   │
│ 2. Apabila dalam pelaksanaan pengeboran ditemukan...        │
│ ... (10 standard terms)                                     │
├─────────────────────────────────────────────────────────────┤
│ Demikian surat penawaran ini kami sampaikan...              │
│                                                             │
│                                       [Signature Stamp]     │
│                                         ARIANTO GAN         │
│                                           Direktur          │
└─────────────────────────────────────────────────────────────┘
```

## Calculations

```
Nilai Jasa    = Σ(qty × harga_satuan) for all items (excluding rate_only)
DPP           = Nilai Jasa × (11/12)
PPN 12%       = Nilai Jasa × 0.12
GRAND TOTAL   = Nilai Jasa + PPN

Cor Volume    = π × radius² × depth × titik
              = π × (diameter/2)² × kedalaman × jumlah_titik
```

## Standard Keterangan (10 points)

1. Harga satuan belum termasuk PPN 12% dan harga sudah termasuk PPH.
2. Apabila dalam pelaksanaan pengeboran ditemukan lapisan batuan, maka akan dikenakan biaya pengeboran batu sebesar 3 (tiga) kali lipat dari harga satuan pengeboran tanah.
3. Apabila ada mobilisasi lokal maka akan ada perhitungan mobilisasi kembali.
4. Keamanan alat menjadi tanggung jawab pemberi kerja.
5. Apabila di area kerja ada crossing pipa menjadi tanggung jawab pemberi kerja.
6. Jasa buang lumpur dan dump truck oleh pemberi kerja.
7. Apabila terjadi kelongsoran dan harus menggunakan polymer, disiapkan oleh pemberi kerja.
8. Biaya Standby akibat kegiatan proyek, lahan dan material belum siap oleh pemberi kerja, menunggu titik dikenakan charge sebesar Rp. 7.500.000,- (Tujuh Juta Lima Ratus Ribu Rupiah) per hari per mesin.
9. Sistem Pembayaran:
   - Biaya Mobilisasi/Demobilisasi dibayar lunas (100%) sebelum unit dimobilisasi.
   - Pembayaran Termin 1 diawal sebesar 30%.
   - Jika Pekerjaan telah dicapai 80% maka akan ditagihkan pelunasan (100%)
10. Harga tidak terikat, sewaktu-waktu dapat berubah tanpa ada pemberitahuan.

## Number Formatting

- Thousands separator: comma (1,000,000)
- Decimal separator: period (2,496.00)
- Currency: No "Rp" prefix in table cells, just numbers

## JSON Fields

| Field | Required | Description |
|-------|----------|-------------|
| nomor | Yes | Document number (e.g., KQ-021/QUO-KBI/I/2026) |
| tanggal | Yes | Date (e.g., Samboja, 29 Januari 2026) |
| kepada_nama | No | Recipient name (e.g., Bpk. Suwito) |
| kepada | Yes | Company/title (e.g., Dirut PT. Wigati Karya Abadi) |
| lokasi_proyek | Yes | Project location |
| alat | Yes | Equipment used |
| items | Yes | Array of line items |
| keterangan | No | Custom terms (overrides defaults) |
| direktur_name | No | Director name (default: ARIANTO GAN) |
