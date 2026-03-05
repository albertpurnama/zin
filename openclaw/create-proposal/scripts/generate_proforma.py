#!/usr/bin/env python3
"""
Generate Indonesian Proforma Invoice as HTML (print to PDF A4).
Usage: python generate_proforma.py <json_file> <output.html> [--assets-dir <path>]
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
    """Format number with period as thousands separator (Indonesian style)."""
    return f"{n:,.0f}".replace(",", ".")


def format_qty(n):
    """Format quantity with comma as decimal separator (Indonesian style)."""
    return f"{float(n):,.2f}".replace(",", "X").replace(".", ",").replace("X", ".")


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
    """Generate HTML from proforma invoice data."""
    
    # Default assets directory
    if assets_dir is None:
        assets_dir = Path(__file__).parent.parent / 'assets'
    else:
        assets_dir = Path(assets_dir)
    
    # Load images as data URIs
    logo_uri = image_to_data_uri(assets_dir / 'kbi-logo.jpg')
    stamp_uri = image_to_data_uri(assets_dir / 'signature-stamp.jpeg')
    
    # Build table rows and calculate total
    table_rows = []
    total_nilai_jasa = 0
    
    items = data.get('items', [])
    for item in items:
        no = item.get('no', '')
        desc = item.get('deskripsi', '')
        qty = item.get('qty', 0)
        satuan = item.get('satuan', '')
        harga = item.get('harga_satuan', 0)
        
        jumlah = float(qty) * float(harga)
        if not item.get('exclude_from_total'):
            total_nilai_jasa += jumlah
        
        table_rows.append(f'''
            <tr>
                <td class="center">{no}</td>
                <td>{desc}</td>
                <td class="right">{format_qty(qty)}</td>
                <td class="center">{satuan}</td>
                <td class="right">{format_rupiah(harga)}</td>
                <td class="right">{format_rupiah(jumlah)}</td>
            </tr>
        ''')
    
    # Calculate totals
    dpp = total_nilai_jasa * (11/12)
    ppn = dpp * 0.12
    grand_total = total_nilai_jasa + ppn
    terbilang_text = terbilang(round(grand_total)) + " Rupiah"
    
    # Keterangan
    keterangan = data.get('keterangan', [])
    keterangan_html = ''
    if keterangan:
        keterangan_items = []
        i = 0
        while i < len(keterangan):
            item = keterangan[i]
            # Check if next item is a sub-item (starts with "Bank" or similar)
            if i + 1 < len(keterangan) and keterangan[i + 1].strip().startswith('Bank'):
                keterangan_items.append(f'<li>{item}<ul><li>{keterangan[i + 1]}</li></ul></li>')
                i += 2
            else:
                keterangan_items.append(f'<li>{item}</li>')
                i += 1
        keterangan_html = '\n'.join(keterangan_items)
    
    # Location and date for signature
    tanggal = data.get('tanggal', '')
    
    html = f'''<!DOCTYPE html>
<html lang="id">
<head>
    <meta charset="UTF-8">
    <title>Proforma Invoice {data.get('nomor', '')}</title>
    <style>
        @page {{
            size: A4;
            margin: 10mm 12mm 10mm 12mm;
        }}
        
        * {{
            margin: 0;
            padding: 0;
            box-sizing: border-box;
        }}
        
        body {{
            font-family: Arial, sans-serif;
            font-size: 10pt;
            line-height: 1.3;
            color: #000;
            width: 210mm;
            padding: 10mm 12mm;
            background: white;
        }}
        
        /* Letterhead */
        .letterhead {{
            display: flex;
            align-items: center;
            margin-bottom: 15pt;
            padding-bottom: 5pt;
            border-bottom: 2pt solid #1a3a6e;
        }}
        
        .letterhead-logo {{
            width: 65px;
            flex-shrink: 0;
            margin-right: 12pt;
        }}
        
        .letterhead-logo img {{
            width: 100%;
            height: auto;
        }}
        
        .letterhead-info {{
            flex: 1;
        }}
        
        .letterhead-company {{
            font-size: 16pt;
            font-weight: bold;
            color: #c00000;
            margin-bottom: 2pt;
        }}
        
        .letterhead-address {{
            font-size: 9pt;
            color: #1a3a6e;
            line-height: 1.3;
        }}
        
        /* Title */
        .title {{
            text-align: center;
            font-size: 16pt;
            font-weight: bold;
            margin: 20pt 0;
            color: #1a3a6e;
        }}
        
        /* Header info */
        .header-section {{
            display: flex;
            justify-content: space-between;
            margin-bottom: 15pt;
        }}
        
        .header-left {{
            text-align: left;
        }}
        
        .header-right {{
            text-align: right;
        }}
        
        .header-right table {{
            margin-left: auto;
        }}
        
        .header-right td {{
            padding: 1pt 3pt;
        }}
        
        .header-right td:first-child {{
            text-align: left;
        }}
        
        .header-right td:last-child {{
            text-align: left;
            font-weight: bold;
        }}
        
        /* Main table */
        table.price-table {{
            width: 100%;
            border-collapse: collapse;
            margin-bottom: 15pt;
            font-size: 10pt;
        }}
        
        table.price-table th,
        table.price-table td {{
            border: 1pt solid #1a3a6e;
            padding: 5pt 6pt;
            vertical-align: middle;
        }}
        
        table.price-table th {{
            background: #f0f0f0;
            font-weight: bold;
            text-align: center;
            color: #1a3a6e;
        }}
        
        table.price-table .center {{ text-align: center; }}
        table.price-table .right {{ text-align: right; }}
        table.price-table .bold {{ font-weight: bold; }}
        
        /* Column widths */
        table.price-table th:nth-child(1), table.price-table td:nth-child(1) {{ width: 5%; }}
        table.price-table th:nth-child(2), table.price-table td:nth-child(2) {{ width: 35%; }}
        table.price-table th:nth-child(3), table.price-table td:nth-child(3) {{ width: 8%; }}
        table.price-table th:nth-child(4), table.price-table td:nth-child(4) {{ width: 15%; }}
        table.price-table th:nth-child(5), table.price-table td:nth-child(5) {{ width: 17%; }}
        table.price-table th:nth-child(6), table.price-table td:nth-child(6) {{ width: 20%; }}
        
        /* Summary rows */
        .summary-label {{
            text-align: left;
        }}
        
        .summary-value {{
            text-align: right;
        }}
        
        .grand-total td {{
            font-weight: bold !important;
            background: #f5f5f5;
        }}
        
        .terbilang-row td {{
            font-style: italic;
            border: none !important;
            padding: 8pt 0 0 0;
        }}
        
        /* Keterangan */
        .keterangan {{
            margin: 15pt 0;
            font-size: 10pt;
        }}
        
        .keterangan h4 {{
            margin-bottom: 5pt;
            font-weight: bold;
        }}
        
        .keterangan ul {{
            margin-left: 20pt;
            list-style-type: disc;
        }}
        
        .keterangan ul ul {{
            margin-left: 20pt;
            list-style-type: disc;
        }}
        
        .keterangan li {{
            margin-bottom: 2pt;
        }}
        
        /* Signature section */
        .signature-section {{
            margin-top: 25pt;
            text-align: right;
        }}
        
        .signature-date {{
            margin-bottom: 5pt;
        }}
        
        .signature-stamp {{
            display: inline-block;
        }}
        
        .signature-stamp img {{
            width: 130px;
            height: auto;
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
                E-mail: konstruksi.kbi@gmail.com
            </div>
        </div>
    </div>
    
    <!-- Title -->
    <div class="title">PROFORMA INVOICE</div>
    
    <!-- Header info -->
    <div class="header-section">
        <div class="header-left">
            Ditujukan kepada Yth:<br>
            Up. {data.get('kepada', '').replace(chr(10), '<br>')}<br>
            di tempat
        </div>
        <div class="header-right">
            <table>
                <tr>
                    <td>No</td>
                    <td>:</td>
                    <td>{data.get('nomor', '')}</td>
                </tr>
                <tr>
                    <td>Tanggal</td>
                    <td>:</td>
                    <td>{tanggal}</td>
                </tr>
            </table>
        </div>
    </div>
    
    <!-- Price table -->
    <table class="price-table">
        <thead>
            <tr>
                <th>NO</th>
                <th>Deskripsi</th>
                <th>Qty</th>
                <th>Satuan</th>
                <th>Harga Satuan<br>(Rp)</th>
                <th>Jumlah (Rp)</th>
            </tr>
        </thead>
        <tbody>
            {''.join(table_rows)}
            
            <!-- Terbilang row -->
            <tr class="terbilang-row">
                <td colspan="4">Terbilang : {terbilang_text}</td>
                <td class="summary-label" style="border: 1pt solid #1a3a6e !important;">Nilai Jasa</td>
                <td class="summary-value" style="border: 1pt solid #1a3a6e !important;">{format_rupiah(total_nilai_jasa)}</td>
            </tr>
            <tr>
                <td colspan="4" style="border: none !important;"></td>
                <td class="summary-label" style="border: 1pt solid #1a3a6e;">DPP (Nilai Jasa<br>x (11/12))</td>
                <td class="summary-value" style="border: 1pt solid #1a3a6e;">{format_rupiah(dpp)}</td>
            </tr>
            <tr>
                <td colspan="4" style="border: none !important;"></td>
                <td class="summary-label" style="border: 1pt solid #1a3a6e;">PPN 12%</td>
                <td class="summary-value" style="border: 1pt solid #1a3a6e;">{format_rupiah(ppn)}</td>
            </tr>
            <tr class="grand-total">
                <td colspan="4" style="border: none !important;"></td>
                <td class="summary-label" style="border: 1pt solid #1a3a6e;">GRAND TOTAL</td>
                <td class="summary-value" style="border: 1pt solid #1a3a6e;">{format_rupiah(grand_total)}</td>
            </tr>
        </tbody>
    </table>
    
    <!-- Keterangan -->
    {f'''<div class="keterangan">
        <h4>Keterangan:</h4>
        <ul>
            {keterangan_html}
        </ul>
    </div>''' if keterangan else ''}
    
    <!-- Signature section -->
    <div class="signature-section">
        <div class="signature-date">Samboja, {tanggal}</div>
        <div class="signature-stamp">
            <img src="{stamp_uri}" alt="Signature">
        </div>
    </div>
</body>
</html>'''
    
    return html


if __name__ == '__main__':
    if len(sys.argv) < 3:
        print("Usage: python generate_proforma.py <data.json> <output.html> [--assets-dir <path>]")
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
