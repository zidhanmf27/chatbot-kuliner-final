from fastapi import FastAPI, HTTPException, BackgroundTasks, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.staticfiles import StaticFiles
from fastapi.responses import FileResponse
import sys
import os
import pandas as pd
import csv
from datetime import datetime
import urllib.parse


# Add parent directory to path to import chatbot_engine
sys.path.append(os.path.dirname(os.path.dirname(os.path.abspath(__file__))))
from chatbot_engine import ChatbotEngine
from api.schemas import ChatRequest, ChatResponse, RegistrationRequest, RegistrationResponse, RecommendationItem, StatsResponse, StatusCheckResponse

app = FastAPI(
    title="Chatbot Kuliner Bandung API",
    description="API untuk rekomendasi kuliner UMKM Bandung dengan fitur pendaftaran mandiri.",
    version="1.0.0"
)
# Reload Trigger

# CORS Configuration
app.add_middleware(
    CORSMiddleware,
    allow_origins=["*"],  # Allow all origins (adjust for production)
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Serve Static Files (Widget assets)
# Pastikan folder 'web' ada di root project
static_dir = os.path.join(os.path.dirname(os.path.dirname(os.path.abspath(__file__))), "web")
if os.path.exists(static_dir):
    app.mount("/static", StaticFiles(directory=static_dir), name="static")

    # Shortcut untuk akses widget.js langsung
    @app.get("/widget.js")
    async def get_widget_js():
        return FileResponse(os.path.join(static_dir, "widget.js"), media_type="application/javascript")
    
    # Shortcut untuk akses style.css
    @app.get("/style.css")
    async def get_style_css():
        return FileResponse(os.path.join(static_dir, "style.css"), media_type="text/css")

# Global Variables
engine = None
MODEL_PATH = os.path.join("dataset", "chatbot_model.pkl")

# Helper for CSV Paths
from database.config import DATA_PATH, PENDING_PATH, LOG_PATH

@app.on_event("startup")
async def startup_event():
    global engine
    print("[STARTUP] Loading Chatbot Engine...")
    try:
        # Initialize engine (uses DB_TYPE from config automatically)
        engine = ChatbotEngine(model_path=MODEL_PATH)
        print("[STARTUP] Engine loaded successfully!")
    except Exception as e:
        print(f"[ERROR] Failed to load engine: {e}")
        # In a real app, might want to exit, but here we'll let it run so /status works

@app.get("/")
async def root():
    return {"message": "Welcome to Chatbot Kuliner API. Visit /docs for documentation."}

@app.get("/status")
async def health_check():
    if engine:
        return {
            "status": "online", 
            "total_umkm": len(engine.df),
            "model_loaded": True
        }
    else:
        return {"status": "offline", "error": "Engine not initialized"}

@app.post("/chat", response_model=ChatResponse)
async def chat_endpoint(request: ChatRequest):
    if not engine:
        raise HTTPException(status_code=503, detail="Chatbot engine is not ready.")
    
    try:
        recommendations, warning_msg, corrected_query = engine.get_recommendations(
            request.query, 
            price_filter=request.price_filter, 
            top_n=request.top_n
        )
        
        rec_items = []
        if not recommendations.empty:
            for _, row in recommendations.iterrows():
                # Generate Maps URL
                maps_query = urllib.parse.quote(f"{row['nama_rumah_makan']} {row['alamat']}")
                maps_url = f"https://www.google.com/maps/search/?api=1&query={maps_query}"
                
                rec_items.append(RecommendationItem(
                    nama_rumah_makan=str(row['nama_rumah_makan']),
                    alamat=str(row['alamat']),
                    kategori=str(row['kategori']),
                    range_harga=str(row['range_harga']),
                    kategori_harga=str(row.get('kategori_harga', '-')),
                    menu=str(row.get('menu', '-')),
                    deskripsi=str(row.get('deskripsi', '-')),
                    similarity_score=float(row['similarity_score']),
                    maps_url=maps_url
                ))
        
        # Prepare Response
        response_obj = ChatResponse(
            query=request.query,
            corrected_query=corrected_query,
            warning_message=warning_msg,
            recommendations=rec_items
        )

        # 4. Log Chat to CSV
        try:
            with open(LOG_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                writer.writerow([
                    datetime.now().isoformat(),
                    request.query,
                    corrected_query,
                    warning_msg,
                    len(rec_items),
                    request.client.host if hasattr(request, 'client') else "unknown"
                ])
        except Exception as log_err:
            # print(f"[LOG ERROR] {log_err}")
            pass

        return response_obj
        
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))

# Rate Limit Storage (In-Memory)
start_time = datetime.now()
request_counts = {}

def clean_rate_limit():
    global request_counts, start_time
    # Reset counts every hour
    if (datetime.now() - start_time).total_seconds() > 3600:
        request_counts = {}
        start_time = datetime.now()

def validate_content(text):
    # check for gibberish (repeating chars > 3)
    import re
    if re.search(r'(.)\1{3,}', text):
        return False, "Terdeteksi spam (karakter berulang)."
    
    # check for bad words (example)
    bad_words = ['anjing', 'babi', 'monyet', 'tolol', 'goblok', 'jancuk', 'kontol', 'memek']
    if any(word in text.lower() for word in bad_words):
        return False, "Mengandung kata-kata yang tidak pantas."
        
    return True, ""

def clean_input(text):
    if not text: return ""
    return text.replace("'", "''") # Basic SQL escaping for single quotes (handled by param binding usually)

@app.post("/register", response_model=RegistrationResponse)
async def register_umkm(request: RegistrationRequest, client_request: Request):
    try:
        # 0. Clean Rate Limit
        clean_rate_limit()
        
        # 1. Check Rate Limit (Max 3 per hour per IP)
        client_ip = client_request.client.host
        if request_counts.get(client_ip, 0) >= 3:
            raise HTTPException(status_code=429, detail="Anda telah mencapai batas pendaftaran (maks. 3 per jam). Silakan coba lagi nanti.")
        
        # 2. Validate Input Fields
        if not request.nama_rumah_makan or not request.alamat:
            raise HTTPException(status_code=400, detail="Nama dan Alamat wajib diisi.")
        
        # 3. Content Validation (Anti-Spam/Prank)
        is_valid, msg = validate_content(request.nama_rumah_makan)
        if not is_valid: raise HTTPException(status_code=400, detail=f"Nama Rumah Makan tidak valid: {msg}")
        
        is_valid, msg = validate_content(request.menu)
        if not is_valid: raise HTTPException(status_code=400, detail=f"Menu tidak valid: {msg}")

        # 4. Address Validation Rule
        addr_lower = request.alamat.lower()
        required_substrs = ['jalan', 'jl.', 'jl ', 'kec.', 'kec ', 'kel.', 'kel ', 'rt', 'rw', 'komplek', 'gang', 'gg.', 'nomor', 'no.', 'blok']
        if not any(sub in addr_lower for sub in required_substrs) and len(request.alamat) < 10:
             raise HTTPException(status_code=400, detail="Alamat harus lengkap (Sertakan Jalan / No / Kecamatan). Min. 10 karakter.")
            
        # 5. Save to CSV (Pending)
        try:
            new_row = [
                datetime.now().isoformat(),
                request.nama_rumah_makan,
                request.alamat,
                request.kategori,
                request.range_harga,
                request.menu,
                request.suasana,
                request.tipe_pengunjung,
                request.fasilitas,
                "pending"
            ]
            
            file_exists = os.path.isfile(PENDING_PATH)
            with open(PENDING_PATH, 'a', newline='', encoding='utf-8') as f:
                writer = csv.writer(f)
                # Header usually created by config.py, but just in case
                if not file_exists or os.stat(PENDING_PATH).st_size == 0:
                     writer.writerow(["timestamp","nama_rumah_makan","alamat","kategori","range_harga","menu","suasana","tipe_pengunjung","fasilitas","status"])
                writer.writerow(new_row)
            
        except Exception as db_err:
            print(f"[CSV ERROR] {db_err}")
            raise HTTPException(status_code=500, detail="Error saat menyimpan data ke CSV.")
            
        # Update Rate Limit
        request_counts[client_ip] = request_counts.get(client_ip, 0) + 1
            
        return RegistrationResponse(
            status="success",
            message="Pendaftaran berhasil! Data Anda akan diproses dalam 1x24 jam."
        )
        
    except HTTPException as he:
        raise he
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Gagal menyimpan data: {str(e)}")

@app.get("/stats", response_model=StatsResponse)
async def get_stats():
    if not engine:
         raise HTTPException(status_code=503, detail="Engine not ready")
    
    cat_counts = engine.df['kategori'].value_counts().to_dict()
    return StatsResponse(
        total_umkm=len(engine.df),
        categories=cat_counts
    )

@app.get("/check-status", response_model=StatusCheckResponse)
async def check_status(nama: str):
    # 1. Check Pending in CSV
    try:
        if os.path.exists(PENDING_PATH):
            import csv
            # Read backwards if possible, but for CSV just read all is easiest for small files
            # or read dataframe
            df_pending = pd.read_csv(PENDING_PATH)
            
            # Filter name match (case insensitive)
            match = df_pending[df_pending['nama_rumah_makan'].str.lower() == nama.lower()]
            
            # Check latest status
            if not match.empty:
                last_status = match.iloc[-1]['status'] # Get most recent
                if last_status == 'pending':
                    return StatusCheckResponse(
                        nama_rumah_makan=nama,
                        status="pending",
                        message="Data sedang dalam antrean verifikasi (Pending)."
                    )
            
    except Exception as e:
        print(f"[CSV ERROR] Check status: {e}")
        pass
            
    # 2. Check Existing (Approved) in Engine
    if engine:
        match = engine.df[engine.df['nama_rumah_makan'].str.lower() == nama.lower()]
        if not match.empty:
             return StatusCheckResponse(
                nama_rumah_makan=nama,
                status="approved",
                message="Data sudah terdaftar di sistem utama (Approved)."
            )
            
    # 3. Not Found
    return StatusCheckResponse(
        nama_rumah_makan=nama,
        status="not_found",
        message=f"Maaf, UMKM dengan nama '{nama}' belum terdaftar."
    )

