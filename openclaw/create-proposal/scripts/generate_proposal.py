#!/usr/bin/env python3
"""
Generate Indonesian construction proposal as HTML (print to PDF A4).
Usage: python generate_proposal.py <json_file> <output.html> [--assets-dir <path>]
"""

import json
import sys
import base64
from pathlib import Path


def terbilang(n):
    """Convert number to Indonesian words."""
    satuan = ['', 'Satu', 'Dua', 'Tiga', 'Empat', 'Lima', 'Enam', 'Tujuh', 'Delapan', 'Sembilan', 'Sepuluh', 'Sebelas']
    n = int(n)
    if n < 12:
        return satuan[n]
    elif n < 20:
        return terbilang(n - 10) + ' Belas'
    elif n < 100:
        return terbilang(n // 10) + ' Puluh' + (' ' + terbilang(n % 10) if n % 10 else '')
    elif n < 200:
        return 'Seratus' + (' ' + terbilang(n - 100) if n - 100 else '')
    elif n < 1000:
        return terbilang(n // 100) + ' Ratus' + (' ' + terbilang(n % 100) if n % 100 else '')
    elif n < 2000:
        return 'Seribu' + (' ' + terbilang(n - 1000) if n - 1000 else '')
    elif n < 1000000:
        return terbilang(n // 1000) + ' Ribu' + (' ' + terbilang(n % 1000) if n % 1000 else '')
    elif n < 1000000000:
        return terbilang(n // 1000000) + ' Juta' + (' ' + terbilang(n % 1000000) if n % 1000000 else '')
    elif n < 1000000000000:
        return terbilang(n // 1000000000) + ' Miliar' + (' ' + terbilang(n % 1000000000) if n % 1000000000 else '')
    else:
        return terbilang(n // 1000000000000) + ' Triliun' + (' ' + terbilang(n % 1000000000000) if n % 1000000000000 else '')


def format_rupiah(n):
    """Format number with comma as thousands separator."""
    return f"{n:,.0f}"


def format_qty(n):
    """Format quantity with period as decimal separator."""
    return f"{float(n):,.2f}"


def image_to_data_uri(path):
    """Convert image file to data URI for embedding."""
    path = Path(path)
    if not path.exists():
        return ""
    
    ext = path.suffix.lower()
    mime_types = {'.jpg': 'image/jpeg', '.jpeg': 'image/jpeg', '.png': 'image/png', '.gif': 'image/gif'}
    mime = mime_types.get(ext, 'image/png')
    
    with open(path, 'rb') as f:
        data = base64.b64encode(f.read()).decode('utf-8')
    
    return f"data:{mime};base64,{data}"


def generate_html(data, assets_dir=None):
    """Generate HTML from proposal data."""
    
    # Default assets directory
    if assets_dir is None:
        assets_dir = Path(__file__).parent.parent / 'assets'
    else:
        assets_dir = Path(assets_dir)
    
    # Load images as data URIs for self-contained HTML
    letterhead_uri = image_to_data_uri(assets_dir / 'letterhead.png')
    logo_uri = image_to_data_uri(assets_dir / 'kbi-logo.jpg')
    stamp_uri = image_to_data_uri(assets_dir / 'signature-stamp.jpeg')
    
    # Build table rows
    table_rows = []
    total_nilai_jasa = 0
    has_masa_sewa = data.get('has_masa_sewa', False)
    
    items = data.get('items', [])
    for item in items:
        no = item.get('no', '')
        desc = item.get('deskripsi', '')
        qty = item.get('qty', '')
        satuan = item.get('satuan', '')
        harga = item.get('harga_satuan', 0)
        
        # Main item row
        if qty and harga and not item.get('rate_only'):
            jumlah = float(qty) * float(harga)
            if not item.get('exclude_from_total'):
                total_nilai_jasa += jumlah
            jumlah_str = format_rupiah(jumlah)
            qty_str = format_qty(qty)
            harga_str = format_rupiah(harga)
        elif item.get('rate_only'):
            jumlah_str = 'Rate Only'
            qty_str = format_qty(qty) if qty else ''
            if item.get('price_tbc'):
                harga_str = 'Sesuai Lokasi'
            else:
                harga_str = format_rupiah(harga) if harga else ''
        else:
            jumlah_str = '-' if 'sub_items' in item else ''
            qty_str = ''
            harga_str = ''
        
        masa_sewa = item.get('masa_sewa', '')
        if has_masa_sewa:
            table_rows.append(f'''
            <tr>
                <td class="center">{no}</td>
                <td>{desc}</td>
                <td class="right">{qty_str}</td>
                <td class="center">{satuan}</td>
                <td class="center">{masa_sewa}</td>
                <td class="right">{harga_str}</td>
                <td class="right">{jumlah_str}</td>
            </tr>
        ''')
        else:
            table_rows.append(f'''
            <tr>
                <td class="center">{no}</td>
                <td>{desc}</td>
                <td class="right">{qty_str}</td>
                <td class="center">{satuan}</td>
                <td class="right">{harga_str}</td>
                <td class="right">{jumlah_str}</td>
            </tr>
        ''')
        
        # Sub-items
        for sub in item.get('sub_items', []):
            sub_qty = sub.get('qty', '')
            sub_harga = sub.get('harga_satuan', 0)
            
            if sub.get('rate_only'):
                sub_jumlah_str = sub.get('jumlah_text', 'Rate Only')
            elif sub_qty and sub_harga:
                sub_jumlah = float(sub_qty) * float(sub_harga)
                if not sub.get('exclude_from_total'):
                    total_nilai_jasa += sub_jumlah
                sub_jumlah_str = format_rupiah(sub_jumlah)
            else:
                sub_jumlah_str = ''
            
            sub_qty_str = format_qty(sub_qty) if sub_qty else ''
            sub_harga_str = format_rupiah(sub_harga) if sub_harga else ''
            
            sub_masa_sewa = sub.get('masa_sewa', '')
            if has_masa_sewa:
                table_rows.append(f'''
                <tr>
                    <td></td>
                    <td class="sub-desc">{sub.get('deskripsi', '')}</td>
                    <td class="right">{sub_qty_str}</td>
                    <td class="center">{sub.get('satuan', '')}</td>
                    <td class="center">{sub_masa_sewa}</td>
                    <td class="right">{sub_harga_str}</td>
                    <td class="right">{sub_jumlah_str}</td>
                </tr>
            ''')
            else:
                table_rows.append(f'''
                <tr>
                    <td></td>
                    <td class="sub-desc">{sub.get('deskripsi', '')}</td>
                    <td class="right">{sub_qty_str}</td>
                    <td class="center">{sub.get('satuan', '')}</td>
                    <td class="right">{sub_harga_str}</td>
                    <td class="right">{sub_jumlah_str}</td>
                </tr>
            ''')
    
    # Calculate totals (PPN is 12% of DPP, Grand Total = Nilai Jasa + PPN)
    dpp = total_nilai_jasa * (11/12)
    ppn = dpp * 0.12
    grand_total = total_nilai_jasa + ppn
    terbilang_text = terbilang(round(grand_total)) + " Rupiah"
    
    # Keterangan
    keterangan = data.get('keterangan', [
        "Harga satuan belum termasuk PPN 12% dan harga sudah termasuk PPH.",
        "Apabila dalam pelaksanaan pengeboran ditemukan lapisan batuan, maka akan dikenakan biaya pengeboran batu sebesar 2 (dua) kali lipat dari harga satuan pengeboran tanah.",
        "Apabila ada mobilisasi lokal maka akan ada perhitungan mobilisasi kembali.",
        "Keamanan alat menjadi tanggung jawab pemberi kerja.",
        "Apabila di area kerja ada crossing pipa menjadi tanggung jawab pemberi kerja.",
        "Jasa buang lumpur dan dump truck oleh pemberi kerja.",
        "Apabila terjadi kelongsoran dan harus menggunakan polymer, disiapkan oleh pemberi kerja.",
        "Biaya Standby akibat kegiatan proyek, lahan dan material belum siap oleh pemberi kerja, menunggu titik dikenakan charge sebesar Rp. 7.500.000,- (Tujuh Juta Lima Ratus Ribu Rupiah) per hari per mesin.",
        "Sistem Pembayaran:<br>&nbsp;&nbsp;&nbsp;&nbsp;- Biaya Mobilisasi/Demobilisasi dibayar lunas (100%) sebelum unit dimobilisasi.<br>&nbsp;&nbsp;&nbsp;&nbsp;- Pembayaran Termin 1 diawal sebesar 30%.<br>&nbsp;&nbsp;&nbsp;&nbsp;- Jika Pekerjaan telah dicapai 80% maka akan ditagihkan pelunasan (100%)",
        "Harga tidak terikat, sewaktu-waktu dapat berubah tanpa ada pemberitahuan."
    ])
    
    keterangan_html = '\n'.join([f'<li>{k}</li>' for k in keterangan])
    
    # Director info
    direktur_name = data.get('direktur_name', 'ARIANTO GAN')
    
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Surat Penawaran {data.get('nomor', '')}</title>
    <style>
        @page {{
            size: A4;
            margin: 8mm 10mm 8mm 10mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 9pt;
            line-height: 1.2;
            color: #000;
            width: 210mm;
            height: 279mm;
            max-height: 279mm;
            padding: 8mm 10mm 8mm 10mm;
            background: white;
            overflow: hidden;
        }}
        
        /* Letterhead */
        .letterhead {{
            display: flex;
            align-items: center;
            margin-bottom: 4pt;
            padding-bottom: 3pt;
            border-bottom: 2pt solid #1a3a6e;
        }}
        
        .letterhead-logo {{
            width: 70px;
            flex-shrink: 0;
            margin-right: 10pt;
        }}
        
        .letterhead-logo img {{
            width: 100%;
            height: auto;
        }}
        
        .letterhead-info {{
            flex: 1;
        }}
        
        .letterhead-company {{
            font-size: 14pt;
            font-weight: bold;
            color: #1a3a6e;
            margin-bottom: 1pt;
            letter-spacing: 0.3pt;
        }}
        
        .letterhead-address {{
            font-size: 8pt;
            color: #1a3a6e;
            line-height: 1.2;
        }}
        
        .letterhead-address a {{
            color: #1a3a6e;
            text-decoration: none;
        }}
        
        /* Document header */
        .doc-header {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 4pt;
            font-size: 9pt;
        }}
        
        .doc-header-left {{
            text-align: left;
        }}
        
        .doc-header-right {{
            text-align: right;
        }}
        
        .recipient {{
            margin-bottom: 6pt;
        }}
        
        .greeting {{
            margin-bottom: 1pt;
        }}
        
        .intro {{
            margin-bottom: 3pt;
        }}
        
        /* Main table */
        table.price-table {{
            width: calc(100% - 2px);
            border-collapse: collapse;
            margin-bottom: 4pt;
            font-size: 8pt;
            table-layout: fixed;
        }}
        
        table.price-table th,
        table.price-table td {{
            border: 0.5pt solid #000;
            padding: 1.5pt 2pt;
            vertical-align: top;
        }}
        
        table.price-table th {{
            background: #f5f5f5;
            font-weight: bold;
            text-align: center;
        }}
        
        table.price-table .center {{ text-align: center; }}
        table.price-table .right {{ text-align: right; }}
        table.price-table .bold {{ font-weight: bold; }}
        
        table.price-table .sub-desc {{
            padding-left: 8pt;
        }}
        
        table.price-table .project-info {{
            font-weight: bold;
            background: #fafafa;
        }}
        
        /* Column widths - 6 columns (default) */
        table.price-table.cols-6 th:nth-child(1), table.price-table.cols-6 td:nth-child(1) {{ width: 5%; }}
        table.price-table.cols-6 th:nth-child(2), table.price-table.cols-6 td:nth-child(2) {{ width: 35%; }}
        table.price-table.cols-6 th:nth-child(3), table.price-table.cols-6 td:nth-child(3) {{ width: 12%; }}
        table.price-table.cols-6 th:nth-child(4), table.price-table.cols-6 td:nth-child(4) {{ width: 8%; }}
        table.price-table.cols-6 th:nth-child(5), table.price-table.cols-6 td:nth-child(5) {{ width: 18%; }}
        table.price-table.cols-6 th:nth-child(6), table.price-table.cols-6 td:nth-child(6) {{ width: 22%; }}
        
        /* Column widths - 7 columns (with Masa Sewa) */
        table.price-table.cols-7 th:nth-child(1), table.price-table.cols-7 td:nth-child(1) {{ width: 4%; }}
        table.price-table.cols-7 th:nth-child(2), table.price-table.cols-7 td:nth-child(2) {{ width: 28%; }}
        table.price-table.cols-7 th:nth-child(3), table.price-table.cols-7 td:nth-child(3) {{ width: 8%; }}
        table.price-table.cols-7 th:nth-child(4), table.price-table.cols-7 td:nth-child(4) {{ width: 7%; }}
        table.price-table.cols-7 th:nth-child(5), table.price-table.cols-7 td:nth-child(5) {{ width: 15%; }}
        table.price-table.cols-7 th:nth-child(6), table.price-table.cols-7 td:nth-child(6) {{ width: 17%; }}
        table.price-table.cols-7 th:nth-child(7), table.price-table.cols-7 td:nth-child(7) {{ width: 21%; }}
        
        /* Summary section */
        .summary-label {{
            text-align: left;
            font-weight: normal;
        }}
        
        .summary-value {{
            text-align: right;
            font-weight: normal;
        }}
        
        .grand-total td {{
            font-weight: bold !important;
        }}
        
        .terbilang-row td {{
            font-style: italic;
            text-align: left;
            border: none !important;
            padding-top: 4pt;
        }}
        
        /* Keterangan */
        .keterangan {{
            margin-bottom: 3pt;
            font-size: 9pt;
        }}
        
        .keterangan h4 {{
            margin-bottom: 1pt;
            font-size: 9pt;
            font-weight: bold;
        }}
        
        .keterangan ol {{
            margin-left: 18pt;
            padding-left: 0;
        }}
        
        .keterangan li {{
            margin-bottom: 0.5pt;
            text-align: justify;
        }}
        
        /* Closing */
        .closing {{
            margin-top: 3pt;
            margin-bottom: 3pt;
            text-align: justify;
            font-size: 9pt;
        }}
        
        /* Signature section */
        .signature-section {{
            display: flex;
            justify-content: space-between;
            align-items: flex-end;
            margin-top: 8pt;
            page-break-inside: avoid;
        }}
        
        .signature-left {{
            width: 80px;
        }}
        
        .signature-left img {{
            width: 60px;
            height: auto;
        }}
        
        .signature-right {{
            text-align: center;
        }}
        
        .signature-right img {{
            width: 120px;
            height: auto;
        }}
        
        .signature-right .name {{
            margin-top: 4pt;
            font-weight: bold;
            text-decoration: underline;
        }}
        
        .signature-right .title {{
            font-size: 9pt;
        }}
        
        @media print {{
            body {{
                width: auto;
                padding: 0;
                -webkit-print-color-adjust: exact;
                print-color-adjust: exact;
            }}
        }}
    </style>
</head>
<body>
    <!-- Letterhead -->
    <div class="letterhead">
        <div class="letterhead-logo">
            <img src="{logo_uri}" alt="KBI">
        </div>
        <div class="letterhead-info">
            <div class="letterhead-company">PT. KONSTRUKSI BORNEO INDONESIA</div>
            <div class="letterhead-address">
                Jl. Raya Merdeka - Samboja no 26 RT16<br>
                Kab. Kutai Kartanegara, Kalimantan Timur (Samping Wika)<br>
                Phone no: 0853-4695-8003 &nbsp; Office no: 0813-2288-9938<br>
                E-mail: <a href="mailto:konstruksi.kbi@gmail.com">konstruksi.kbi@gmail.com</a>
            </div>
        </div>
    </div>
    
    <!-- Document header: Date and Nomor -->
    <div class="doc-header">
        <div class="doc-header-left">{data.get('tanggal', '')}</div>
        <div class="doc-header-right">Nomor : {data.get('nomor', '')}</div>
    </div>
    
    <!-- Recipient -->
    <div class="recipient">
        Kepada Yth.<br>
        {(data.get('kepada_nama', '') + '<br>') if data.get('kepada_nama') else ''}{data.get('kepada', '').replace(chr(10), '<br>')}<br>
        Ditempat
    </div>
    
    <!-- Greeting -->
    <p class="greeting">Dengan hormat,</p>
    <p class="intro">Bersama dengan ini Kami, menyampaikan Penawaran Harga dengan rincian sebagai berikut :</p>
    
    <!-- Price table -->
    <table class="price-table {'cols-7' if has_masa_sewa else 'cols-6'}">
        <thead>
            <tr>
                <th>NO</th>
                <th>Deskripsi</th>
                <th>Qty</th>
                <th>Satuan</th>
                {'<th>Masa Sewa</th>' if has_masa_sewa else ''}
                <th>Harga Satuan<br>(Rp)</th>
                <th>Jumlah (Rp)</th>
            </tr>
        </thead>
        <tbody>
            <!-- Project info rows -->
            <tr class="project-info">
                <td></td>
                <td colspan="{'6' if has_masa_sewa else '5'}">Lokasi Proyek {data.get('lokasi_proyek', '')}</td>
            </tr>
            <tr class="project-info">
                <td></td>
                <td colspan="{'6' if has_masa_sewa else '5'}">Alat : {data.get('alat', '')}</td>
            </tr>
            {f'''<tr class="project-info">
                <td></td>
                <td colspan="{'6' if has_masa_sewa else '5'}">{data.get('pekerjaan', '')}</td>
            </tr>''' if data.get('pekerjaan') else ''}
            
            <!-- Items -->
            {''.join(table_rows)}
            
            {f"""<!-- Summary rows -->
            <tr>
                <td colspan="{'5' if has_masa_sewa else '4'}" rowspan="4" class="terbilang-row">Terbilang : {terbilang_text}</td>
                <td class="summary-label">Nilai Jasa</td>
                <td class="summary-value">{format_rupiah(total_nilai_jasa)}</td>
            </tr>
            <tr>
                <td class="summary-label">DPP (Nilai Jasa x (11/12))</td>
                <td class="summary-value">{format_rupiah(dpp)}</td>
            </tr>
            <tr>
                <td class="summary-label">PPN 12%</td>
                <td class="summary-value">{format_rupiah(ppn)}</td>
            </tr>
            <tr class="grand-total">
                <td class="summary-label bold">GRAND TOTAL</td>
                <td class="summary-value bold">{format_rupiah(grand_total)}</td>
            </tr>""" if not data.get('hide_totals') else ""}
        </tbody>
    </table>
    
    <!-- Keterangan -->
    <div class="keterangan">
        <h4>Keterangan:</h4>
        <ol>
            {keterangan_html}
        </ol>
    </div>
    
    <!-- Closing -->
    <p class="closing">Demikian surat penawaran ini kami sampaikan, atas perhatian dan kerja samanya kami ucapkan terima kasih.</p>
    
    <!-- Signature section -->
    <div class="signature-section">
        <div class="signature-left">
        </div>
        <div class="signature-right">
            <img src="{stamp_uri}" alt="Signature">
        </div>
    </div>
</body>
</html>'''
    
    return html


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_proposal.py <data.json> <output.html> [--assets-dir <path>]")
        print("\nExample JSON structure:")
        example = {
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
                        {"deskripsi": "b. Pengeboran Batu", "qty": 1, "satuan": "m¹", "harga_satuan": 1000000, "rate_only": True}
                    ]
                },
                {"no": 2, "deskripsi": "Jasa Pengecoran", "qty": 365.75, "satuan": "mᶟ", "harga_satuan": 150000},
                {"no": 3, "deskripsi": "Jasa Pembesian", "qty": 13457.21, "satuan": "Kg", "harga_satuan": 2000},
                {"no": 4, "deskripsi": "Persiapan", "qty": 1, "satuan": "Ls", "harga_satuan": 100000000}
            ]
        }
        print(json.dumps(example, indent=2, ensure_ascii=False))
        sys.exit(1)
    
    # Parse arguments
    assets_dir = None
    args = sys.argv[1:]
    if '--assets-dir' in args:
        idx = args.index('--assets-dir')
        assets_dir = args[idx + 1]
        args = args[:idx] + args[idx+2:]
    
    with open(args[0], 'r', encoding='utf-8') as f:
        data = json.load(f)
    
    html = generate_html(data, assets_dir)
    
    output_path = args[1]
    with open(output_path, 'w', encoding='utf-8') as f:
        f.write(html)
    
    print(f"HTML generated: {output_path}")
    print("Open in browser and print/save as PDF (A4 size)")
