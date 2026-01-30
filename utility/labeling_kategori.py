"""
[DOKUMENTASI LOGIC] Klasifikasi Kategori Makanan
Script ini adalah REKONSTRUKSI dari logic klasifikasi yang digunakan saat fase cleaning data.
Tujuannya untuk mendokumentasikan bagaimana sebuah restoran dikategorikan berdasarkan Nama dan Menu.

DATA-DRIVEN KEYWORDS: Keywords diekstrak langsung dari frekuensi kata pada dataset final.
"""

KEYWORDS = {
    'Japanese Food': [
        'ramen', 'katsu', 'sushi', 'udon', 'don', 'salmon', 'miso', 'tempura', 
        'yakiniku', 'teriyaki', 'shabu', 'japanese', 'gyu', 'sashimi'
    ],
    'Korean Food': [
        'korean', 'bbq', 'kimchi', 'bibimbap', 'kimbab', 'bulgogi', 'bingsoo', 
        'kimbap', 'tteokbokki', 'topokki', 'k-food', 'seoul'
    ],
    'Chinese Food': [
        'dimsum', 'siomay', 'capcay', 'bistik', 'bakmi', 'lumpia', 'pangsit', 
        'chinese', 'fu yung hai', 'fuyunghai', 'nanking', 'mandarin', 'kwetiau'
    ],
    'Western Food': [
        'steak', 'pizza', 'burger', 'pasta', 'spaghetti', 'lasagna', 'sirloin', 
        'tenderloin', 'grill', 'western', 'cheese', 'sandwich', 'hotdog'
    ],
    'Middle Eastern': [
        'kebuli', 'briyani', 'kebab', 'mandhi', 'arab', 'middle east', 'turki', 'turkish'
    ],
    'Cafe & Dessert': [
        'coffee', 'kopi', 'latte', 'cafe', 'cappuccino', 'matcha', 'americano', 
        'bakery', 'cake', 'dessert', 'pastry', 'gelato', 'ice cream', 'boba'
    ],
    'Masakan Indonesia': [
        'sate', 'sambal', 'batagor', 'gurame', 'baso', 'bakso', 'penyet', 'geprek',
        'soto', 'padang', 'sunda', 'pempek', 'rawon', 'pecel', 'rendang'
    ],
    'Masakan Non Halal': [
        'babi', 'pork', 'samcan', 'non halal', 'pig', 'char siu', 'lapo'
    ]
}

def classify_restaurant(row):
    nama = str(row['nama_rumah_makan']).lower()
    menu = str(row.get('menu', '')).lower()
    
    # 1. PRIORITAS UTAMA: Cek Nama Rumah Makan (Strict Match)
    for cat, words in KEYWORDS.items():
        for w in words:
            if w in nama:
                return cat
                
    # 2. PRIORITAS KEDUA: Cek Menu (Scoring)
    best_score = 0
    best_cat = "Aneka Masakan" # Default jika tidak ada match
    
    cats_found = set()
    
    for cat, words in KEYWORDS.items():
        score = 0
        for w in words:
            if w in menu:
                score += 1
        
        if score > 0:
            cats_found.add(cat)
            
        if score > best_score:
            best_score = score
            best_cat = cat
    
    # Logic Aneka Masakan: 
    # Jika di menu terdeteksi campuran 3 atau lebih kategori yang berbeda
    if len(cats_found) >= 3: 
        return "Aneka Masakan"
        
    # Jika tidak ada keyword yang cocok sama sekali
    if best_score == 0:
        return "Aneka Masakan"
            
    return best_cat
