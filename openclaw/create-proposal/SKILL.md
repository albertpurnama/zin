---
name: create-proposal
description: Generate Indonesian construction quotation/proposal PDFs (Surat Penawaran). Use when creating proposals for bored pile drilling, construction services, or similar project quotes in Indonesian. Supports custom items, pricing, and terms.
---

# Create Proposal (Surat Penawaran)

Generate Indonesian construction proposal PDFs matching KBI's standard quotation format.

## Quick Start

```bash
# Generate HTML
python3 skills/create-proposal/scripts/generate_proposal.py data.json output.html

# Convert to PDF (Chrome headless)
"/Applications/Google Chrome.app/Contents/MacOS/Google Chrome" --headless --disable-gpu --no-pdf-header-footer --print-to-pdf=output.pdf file://$(pwd)/output.html
```

## Template Structure

### 1. Letterhead (HTML/CSS)
- KBI logo image on left
- Company name "PT. KONSTRUKSI BORNEO INDONESIA" in blue
- Address, phone, email in blue
- Blue bottom border

### 2. Document Header
- Date on left: "Samboja, [tanggal] [bulan] [tahun]"
- Nomor on right: "KQ-XXX/QUO-KBI/[BULAN]/[TAHUN]"
- Recipient: Kepada Yth., company name, Ditempat

### 3. Price Table (6 columns)
| NO | Deskripsi | Qty | Satuan | Harga Satuan (Rp) | Jumlah (Rp) |

- Project info rows inside table (Lokasi Proyek, Alat, Pekerjaan Pengeboran)
- Sub-items supported (indented under parent)
- "Rate Only" for items without calculated total
- Summary: Nilai Jasa → DPP (×11/12) → PPN 12% → GRAND TOTAL
- Terbilang: amount in Indonesian words

### 4. Keterangan (9 standard terms)
Payment terms, responsibilities, pricing conditions

### 5. Signature Section
- Signature stamp + director name (right side only)

## JSON Data Structure

```json
{
  "nomor": "KQ-018/QUO-KBI/I/2026",
  "tanggal": "Samboja, 29 Januari 2026",
  "kepada": "PT. SCS",
  "lokasi_proyek": "Renovasi RSUD Kondosapata Mamasa",
  "alat": "Bored Pile Machine",
  "items": [
    {
      "no": 1,
      "deskripsi": "Pengeboran Bored Pile Ø60",
      "sub_items": [
        {"deskripsi": "a. Pengeboran Tanah", "qty": 2496, "satuan": "m¹", "harga_satuan": 400000},
        {"deskripsi": "b. Pengeboran Batu", "qty": 1, "satuan": "m¹", "harga_satuan": 1000000, "rate_only": true}
      ]
    },
    {"no": 2, "deskripsi": "Jasa Pengecoran", "qty": 365.75, "satuan": "mᶟ", "harga_satuan": 150000},
    {"no": 3, "deskripsi": "Jasa Pembesian", "qty": 13457.21, "satuan": "Kg", "harga_satuan": 2000},
    {"no": 4, "deskripsi": "Persiapan", "qty": 1, "satuan": "Ls", "harga_satuan": 100000000}
  ],
  "keterangan": ["Custom terms..."],
  "direktur_name": "ARIANTO GAN"
}
```

### Item Options
- `rate_only: true` — Shows "Rate Only" instead of calculated total
- `exclude_from_total: true` — Excludes from Nilai Jasa calculation
- `sub_items` — Nested items under a parent row

### Common Units
- `m¹` — linear meter
- `mᶟ` — cubic meter
- `Kg` — kilogram
- `Ls` — lump sum

## Assets
- `assets/kbi-logo.jpg` — KBI logo for letterhead
- `assets/signature-stamp.jpeg` — Director signature stamp

## Technical Notes
- Letterhead built with HTML/CSS (not image)
- Chrome headless converts HTML to PDF
- Images embedded as base64 data URIs (self-contained HTML)
- A4 page size with margins: 8mm top/bottom, 10mm left, 12mm right
- Number format: comma for thousands (1,000,000), period for decimals (2,496.00)
