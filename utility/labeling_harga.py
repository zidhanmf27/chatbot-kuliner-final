"""
=============================================================================
LABELING KATEGORI HARGA
=============================================================================
File ini berisi fungsi untuk memberikan label kategori harga
berdasarkan range harga yang diberikan.

Kategori:
- Murah: < Rp 25.000
- Sedang: Rp 25.000 - Rp 100.000
- Mahal: > Rp 100.000
=============================================================================
"""

import pandas as pd
import re


def clean_price(price_str):
    """
    Membersihkan format mata uang menjadi angka integer.
    
    Contoh:
    - "Rp. 25.000" -> 25000
    - "50000" -> 50000
    - "Rp 100.000,-" -> 100000
    
    Args:
        price_str (str): String harga dengan format apapun
        
    Returns:
        int: Angka harga (0 jika tidak valid)
    """
    if pd.isna(price_str): 
        return 0
    
    # Hapus semua karakter kecuali angka
    clean = re.sub(r'[^\d]', '', str(price_str))
    
    return int(clean) if clean else 0


def label_price(range_str):
    """
    Memberikan label kategori harga berdasarkan range.
    
    Logika:
    1. Jika format range (misal: "Rp. 25.000 - 50.000"):
       - Hitung rata-rata dari min dan max
    2. Jika format single (misal: "Rp. 25.000"):
       - Gunakan nilai tersebut
    3. Tentukan kategori:
       - < 25.000 = "Murah"
       - 25.000 - 100.000 = "Sedang"
       - > 100.000 = "Mahal"
    
    Args:
        range_str (str): String range harga (misal: "Rp. 25.000 - 50.000")
        
    Returns:
        str: Label kategori ("Murah", "Sedang", atau "Mahal")
    """
    # Jika data kosong atau "-", anggap murah (warung kecil)
    if pd.isna(range_str) or str(range_str).strip() == '-':
        return "Murah"
    
    # Pisahkan range (jika ada tanda "-")
    # Contoh: "Rp. 25.000 - 50.000" -> ["Rp. 25.000", "50.000"]
    parts = str(range_str).split('-')
    
    if len(parts) == 2:
        # Format range: ada min dan max
        min_price = clean_price(parts[0])
        max_price = clean_price(parts[1])
        avg_price = (min_price + max_price) / 2
    else:
        # Format single: hanya satu angka
        avg_price = clean_price(parts[0])
    
    # Tentukan kategori berdasarkan harga rata-rata
    if avg_price < 25000:
        return "Murah"
    elif avg_price < 100000:
        return "Sedang"
    else:
        return "Mahal"


# =============================================================================
# TESTING (Jalankan file ini langsung untuk test)
# =============================================================================

if __name__ == "__main__":
    # Contoh data untuk testing
    examples = [
        "Rp. 15.000",
        "Rp. 25.000 - 50.000",
        "Rp. 75.000 - 100.000",
        "Rp. 150.000 - 200.000"
    ]
    
    print("=" * 50)
    print("TEST LABELING KATEGORI HARGA")
    print("=" * 50)
    
    for price in examples:
        label = label_price(price)
        print(f"Input: {price:<25} -> Label: {label}")
    
    print("=" * 50)
