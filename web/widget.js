(function () {
  console.log("Chatbot Widget Premium Loaded");

  // --- CONFIGURATION ---
  const scriptTag = document.currentScript;
  const scriptUrl = new URL(scriptTag.src);
  const API_BASE_URL = scriptUrl.origin;

  // State for pagination
  let currentQuery = "";
  let currentOffset = 0;
  let allRecommendations = [];

  // --- ICONS (SVG) ---
  const ICONS = {
    robot: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="20" height="20"><path d="M12 2a2 2 0 0 1 2 2c0 .74-.4 1.39-1 1.73V7h1a7 7 0 0 1 7 7h1a1 1 0 0 1 1 1v3a1 1 0 0 1-1 1h-1v1a2 2 0 0 1-2 2H5a2 2 0 0 1-2-2v-1H2a1 1 0 0 1-1-1v-3a1 1 0 0 1 1-1h1a7 7 0 0 1 7-7V5.73C7.4 5.39 7 4.74 7 4a2 2 0 0 1 2-2h3zm0 9a2 2 0 1 0 0 4 2 2 0 0 0 0-4z"/></svg>`,
    chat: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="24" height="24"><path d="M20 2H4c-1.1 0-2 .9-2 2v18l4-4h14c1.1 0 2-.9 2-2V4c0-1.1-.9-2-2-2z"/></svg>`,
    close: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="none" stroke="currentColor" stroke-width="2" stroke-linecap="round" stroke-linejoin="round" width="20" height="20"><line x1="18" y1="6" x2="6" y2="18"></line><line x1="6" y1="6" x2="18" y2="18"></line></svg>`,
    send: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M2.01 21L23 12 2.01 3 2 10l15 2-15 2z"/></svg>`,
    search: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M15.5 14h-.79l-.28-.27A6.471 6.471 0 0 0 16 9.5 6.5 6.5 0 1 0 9.5 16c1.61 0 3.09-.59 4.23-1.57l.27.28v.79l5 4.99L20.49 19l-4.99-5zm-6 0C7.01 14 5 11.99 5 9.5S7.01 5 9.5 5 14 7.01 14 9.5 11.99 14 9.5 14z"/></svg>`,
    store: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M20 4H4v2h16V4zm1 10v-2l-1-5H4l-1 5v2h1v6h10v-6h4v6h2v-6h1zm-9 4H6v-4h6v4z"/></svg>`,
    chart: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M11 2v20c-5.07-.5-9-4.79-9-10s3.93-9.5 9-10zm2.03 0v8.99H22c-.47-4.74-4.24-8.52-8.97-8.99zm0 11.01V22c4.74-.47 8.5-4.25 8.97-8.99h-8.97z"/></svg>`,
    check: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="16" height="16"><path d="M9 16.17L4.83 12l-1.42 1.41L9 19 21 7l-1.41-1.41z"/></svg>`,
    map: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 2C8.13 2 5 5.13 5 9c0 5.25 7 13 7 13s7-7.75 7-13c0-3.87-3.13-7-7-7zm0 9.5c-1.38 0-2.5-1.12-2.5-2.5s1.12-2.5 2.5-2.5 2.5 1.12 2.5 2.5-1.12 2.5-2.5 2.5z"/></svg>`,
    navigate: `<svg xmlns="http://www.w3.org/2000/svg" viewBox="0 0 24 24" fill="currentColor" width="14" height="14"><path d="M12 2L4.5 20.29l.71.71L12 18l6.79 3 .71-.71z"/></svg>`,
    more: `<svg xmlns="http://www.w3.org/2000/svg" fill="none" viewBox="0 0 24 24" stroke-width="2" stroke="currentColor" width="16" height="16"><path stroke-linecap="round" stroke-linejoin="round" d="M19.5 8.25l-7.5 7.5-7.5-7.5" /></svg>`,
  };

  // --- 1. INJECT PREMIUM CSS ---
  const styleId = "kb-widget-css-premium";
  if (!document.getElementById(styleId)) {
    const style = document.createElement("style");
    style.id = styleId;
    style.innerHTML = `
      #kb-chatbot-widget {
        all: initial;
        font-family: 'Segoe UI', system-ui, -apple-system, sans-serif;
        line-height: 1.5;
        z-index: 999999;
      }
      #kb-chatbot-widget * { box-sizing: border-box; }

      /* Trigger Button */
      #kb-chatbot-widget .kb-trigger {
        position: fixed;
        bottom: 24px;
        right: 24px;
        width: 56px;
        height: 56px;
        background: linear-gradient(135deg, #2563eb, #1d4ed8);
        color: white;
        border-radius: 50%;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        box-shadow: 0 4px 14px rgba(37, 99, 235, 0.4);
        transition: transform 0.3s cubic-bezier(0.34, 1.56, 0.64, 1);
        z-index: 2147483647;
      }
      #kb-chatbot-widget .kb-trigger:hover { transform: scale(1.1); }
      #kb-chatbot-widget .kb-trigger svg { fill: white; }
      #kb-chatbot-widget .kb-trigger.kb-hidden { 
          transform: scale(0) rotate(90deg); 
          opacity: 0; 
          pointer-events: none;
      }

      /* Window */
      #kb-chatbot-widget .kb-window {
        position: fixed;
        bottom: 96px;
        right: 24px;
        width: 380px;
        height: 600px;
        max-height: 80vh;
        max-width: calc(100vw - 48px);
        background: #f8fafc;
        border-radius: 20px;
        box-shadow: 0 12px 40px rgba(0,0,0,0.15);
        display: flex;
        flex-direction: column;
        overflow: hidden;
        opacity: 0;
        transform: translateY(20px) scale(0.95);
        pointer-events: none;
        transition: all 0.3s cubic-bezier(0.16, 1, 0.3, 1);
        z-index: 2147483647;
        font-size: 14px;
        border: 1px solid rgba(255,255,255,0.8);
      }
      #kb-chatbot-widget .kb-window.kb-active {
        opacity: 1;
        transform: translateY(0) scale(1);
        pointer-events: auto;
      }

      /* Header */
      #kb-chatbot-widget .kb-header {
        background: linear-gradient(135deg, #2563eb, #4338ca);
        padding: 16px 20px;
        display: flex;
        justify-content: space-between;
        align-items: center;
        color: white;
        box-shadow: 0 2px 4px rgba(0,0,0,0.05);
      }
      #kb-chatbot-widget .kb-title h3 {
        margin: 0;
        font-size: 16px;
        font-weight: 700;
        letter-spacing: -0.01em;
      }
      #kb-chatbot-widget .kb-title p {
        margin: 2px 0 0 0;
        font-size: 11px;
        color: rgba(255,255,255,0.8);
        display: flex;
        align-items: center;
        gap: 4px;
      }
      #kb-chatbot-widget .kb-status-dot {
        width: 6px;
        height: 6px;
        background: #4ade80;
        border-radius: 50%;
        box-shadow: 0 0 8px #4ade80;
      }
      #kb-chatbot-widget .kb-close-btn {
        background: rgba(255,255,255,0.1);
        border: none;
        color: white;
        cursor: pointer;
        padding: 6px;
        border-radius: 8px;
        transition: background 0.2s;
        display: flex;
      }
      #kb-chatbot-widget .kb-close-btn:hover { background: rgba(255,255,255,0.2); }

      /* Body */
      #kb-chatbot-widget .kb-body {
        flex: 1;
        padding: 16px;
        overflow-y: auto;
        display: flex;
        flex-direction: column;
        gap: 16px;
      }
      
      /* Message Bubbles */
      #kb-chatbot-widget .kb-msg {
        display: flex;
        gap: 10px;
        align-items: flex-end;
        animation: kbSlideUp 0.3s ease;
      }
      #kb-chatbot-widget .kb-msg.kb-user { flex-direction: row-reverse; }
      
      #kb-chatbot-widget .kb-avatar {
        width: 32px;
        height: 32px;
        background: #e0e7ff; /* Indigo-100 */
        border-radius: 12px;
        display: flex;
        align-items: center;
        justify-content: center;
        flex-shrink: 0;
        color: #4338ca;
      }
      
      #kb-chatbot-widget .kb-bubble {
        padding: 12px 16px;
        border-radius: 16px;
        border-bottom-left-radius: 4px;
        background: white;
        border: 1px solid #e2e8f0;
        color: #334155;
        font-size: 14px;
        line-height: 1.5;
        max-width: 85%;
        box-shadow: 0 1px 2px rgba(0,0,0,0.02);
      }
      #kb-chatbot-widget .kb-msg.kb-user .kb-bubble {
        background: #2563eb;
        color: white;
        border: none;
        border-bottom-left-radius: 16px;
        border-bottom-right-radius: 4px;
        box-shadow: 0 4px 6px rgba(37, 99, 235, 0.2);
      }
      
      /* Cards */
      #kb-chatbot-widget .kb-card {
        background: white;
        border: 1px solid #e2e8f0;
        border-radius: 12px;
        padding: 12px;
        margin-top: 8px;
        transition: all 0.2s;
        position: relative;
        overflow: hidden;
      }
      #kb-chatbot-widget .kb-card:hover {
        border-color: #3b82f6;
        box-shadow: 0 4px 12px rgba(0,0,0,0.05);
        transform: translateY(-2px);
      }
      #kb-chatbot-widget .kb-card-header {
        display: flex;
        justify-content: space-between;
        align-items: start;
        margin-bottom: 8px;
      }
      #kb-chatbot-widget .kb-card-title {
        font-weight: 700;
        color: #1d4ed8;
        font-size: 14px;
        margin: 0;
      }
      #kb-chatbot-widget .kb-match-badge {
        background: #dcfce7;
        color: #15803d;
        font-size: 10px;
        font-weight: 800;
        padding: 2px 8px;
        border-radius: 99px;
      }
      
      #kb-chatbot-widget .kb-meta-row {
        display: flex;
        gap: 8px;
        margin-bottom: 8px;
        font-size: 12px;
        color: #64748b;
      }
      #kb-chatbot-widget .kb-tag {
        background: #f1f5f9;
        padding: 2px 6px;
        border-radius: 4px;
        display: flex;
        align-items: center;
        gap: 4px;
      }

      #kb-chatbot-widget .kb-action-btn {
        display: flex;
        align-items: center;
        justify-content: center;
        gap: 6px;
        width: 100%;
        padding: 8px;
        border-radius: 8px;
        font-size: 12px;
        font-weight: 600;
        cursor: pointer;
        transition: background 0.2s;
        border: 1px solid #e2e8f0;
        background: white;
        color: #475569;
        margin-top: 8px;
      }
      #kb-chatbot-widget .kb-action-btn:hover {
        background: #f8fafc;
        border-color: #cbd5e1;
        color: #1e293b;
      }
      #kb-chatbot-widget .kb-action-btn.primary {
        background: #eff6ff;
        color: #2563eb;
        border-color: #bfdbfe;
      }
      #kb-chatbot-widget .kb-action-btn.primary:hover {
        background: #dbeafe;
      }

      /* Options Grid */
      #kb-chatbot-widget .kb-options-grid {
        display: grid;
        grid-template-columns: 1fr 1fr;
        gap: 8px;
        margin-top: 12px;
      }
      #kb-chatbot-widget .kb-option-btn {
        background: white;
        border: 1px solid #e2e8f0;
        padding: 12px;
        border-radius: 12px;
        text-align: left;
        cursor: pointer;
        transition: all 0.2s;
        display: flex;
        flex-direction: column;
        gap: 4px;
        color: #475569;
      }
      #kb-chatbot-widget .kb-option-btn:hover {
        border-color: #3b82f6;
        background: #eff6ff;
      }
      #kb-chatbot-widget .kb-option-icon { color: #3b82f6; }
      #kb-chatbot-widget .kb-option-text { font-weight: 600; font-size: 13px; color: #1e293b; }
      
      /* Input Area */
      #kb-chatbot-widget .kb-input-area {
        padding: 16px;
        background: white;
        border-top: 1px solid #e2e8f0;
        flex-shrink: 0;
      }
      #kb-chatbot-widget .kb-input-box {
        display: flex;
        background: #f8fafc;
        border: 1px solid #e2e8f0;
        border-radius: 24px;
        padding: 4px;
        transition: all 0.2s;
      }
      #kb-chatbot-widget .kb-input-box:focus-within {
        background: white;
        border-color: #3b82f6;
        box-shadow: 0 0 0 3px rgba(59,130,246,0.1);
      }
      #kb-chatbot-widget .kb-input {
        flex: 1;
        border: none;
        background: transparent;
        padding: 8px 16px;
        font-size: 14px;
        outline: none;
        min-width: 0;
      }
      #kb-chatbot-widget .kb-send {
        width: 36px;
        height: 36px;
        background: #2563eb;
        border: none;
        border-radius: 50%;
        color: white;
        display: flex;
        align-items: center;
        justify-content: center;
        cursor: pointer;
        transition: all 0.2s;
      }
      #kb-chatbot-widget .kb-send:hover { background: #1d4ed8; transform: scale(1.05); }
      
      /* Load Load */
      #kb-chatbot-widget .kb-more-btn {
        display: block;
        width: 100%;
        padding: 10px;
        text-align: center;
        background: #f1f5f9;
        color: #475569;
        font-weight: 600;
        border-radius: 8px;
        border: none;
        cursor: pointer;
        margin-top: 12px;
        font-size: 12px;
      }
      #kb-chatbot-widget .kb-more-btn:hover { background: #e2e8f0; color: #1e293b; }

      @keyframes kbSlideUp {
        from { opacity: 0; transform: translateY(10px); }
        to { opacity: 1; transform: translateY(0); }
      }
    `;
    document.head.appendChild(style);
  }

  // --- 2. HTML STRUCTURE ---
  const container = document.createElement("div");
  container.id = "kb-chatbot-widget";
  container.innerHTML = `
    <div class="kb-trigger" id="kb-trigger">${ICONS.chat}</div>
    
    <div class="kb-window" id="kb-window">
      <div class="kb-header">
        <div style="display:flex; align-items:center; gap:12px;">
          <div style="background:rgba(255,255,255,0.2); border-radius:12px; width:40px; height:40px; display:flex; align-items:center; justify-content:center;">
            ${ICONS.robot}
          </div>
          <div class="kb-title">
            <h3>Kuliner Bandung</h3>
            <p><span class="kb-status-dot"></span> Online Agent</p>
          </div>
        </div>
        <button class="kb-close-btn" id="kb-close">${ICONS.close}</button>
      </div>
      
      <div class="kb-body" id="kb-messages"></div>
      
      <div class="kb-input-area">
        <div class="kb-input-box">
          <input type="text" class="kb-input" id="kb-input" placeholder="Cari kuliner..." autocomplete="off">
          <button class="kb-send" id="kb-send">${ICONS.send}</button>
        </div>
        <div style="text-align:center; font-size:10px; color:#94a3b8; margin-top:8px;">Powered by AI Technology</div>
      </div>
    </div>
  `;
  document.body.appendChild(container);

  // --- 3. LOGIC ---
  const trigger = document.getElementById("kb-trigger");
  const windowEl = document.getElementById("kb-window");
  const messagesEl = document.getElementById("kb-messages");
  const inputEl = document.getElementById("kb-input");
  const sendEl = document.getElementById("kb-send");
  const closeEl = document.getElementById("kb-close");

  let isOpen = false;
  let currentState = "IDLE";
  let registrationData = {};

  // -- Toggle --
  function toggle() {
    isOpen = !isOpen;
    if (isOpen) {
      windowEl.classList.add("kb-active");
      trigger.classList.add("kb-hidden");
      if (messagesEl.children.length === 0) initChat();
    } else {
      windowEl.classList.remove("kb-active");
      trigger.classList.remove("kb-hidden");
    }
  }
  trigger.addEventListener("click", toggle);
  closeEl.addEventListener("click", toggle);

  // -- Messages --
  function initChat() {
    addBotMsg(
      "Halo! 👋 Saya siap membantu Anda mencari kuliner terbaik di Bandung. Ada yang bisa saya bantu?",
    );
    setTimeout(() => showMainMenu(), 600);
  }

  function addBotMsg(html) {
    const d = document.createElement("div");
    d.className = "kb-msg kb-bot";
    d.innerHTML = `<div class="kb-avatar">${ICONS.robot}</div><div class="kb-bubble">${html}</div>`;
    messagesEl.appendChild(d);
    scrollToBottom();
  }

  function addUserMsg(text) {
    const d = document.createElement("div");
    d.className = "kb-msg kb-user";
    d.innerHTML = `<div class="kb-bubble">${text}</div>`;
    messagesEl.appendChild(d);
    scrollToBottom();
  }

  function scrollToBottom() {
    messagesEl.scrollTop = messagesEl.scrollHeight;
  }

  function showTyping() {
    const id = "kb-typing-" + Date.now();
    const d = document.createElement("div");
    d.className = "kb-msg kb-bot";
    d.id = id;
    d.innerHTML = `<div class="kb-avatar">${ICONS.robot}</div><div class="kb-bubble" style="padding:12px;"><svg width="24" height="8" viewBox="0 0 24 8"><circle cx="2" cy="4" r="2" fill="#94a3b8"><animate attributeName="cy" values="4;2;4" dur="0.6s" repeatCount="indefinite" begin="0s"/></circle><circle cx="12" cy="4" r="2" fill="#94a3b8"><animate attributeName="cy" values="4;2;4" dur="0.6s" repeatCount="indefinite" begin="0.2s"/></circle><circle cx="22" cy="4" r="2" fill="#94a3b8"><animate attributeName="cy" values="4;2;4" dur="0.6s" repeatCount="indefinite" begin="0.4s"/></circle></svg></div>`;
    messagesEl.appendChild(d);
    scrollToBottom();
    return id;
  }

  function removeTyping(id) {
    const el = document.getElementById(id);
    if (el) el.remove();
  }

  // -- Features --
  window.kbShowMenu = function () {
    currentState = "IDLE";
    addBotMsg(`
      <p style="margin:0 0 12px 0; font-weight:600;">Silakan pilih layanan:</p>
      <div class="kb-options-grid">
        <button onclick="kbStartChat()" class="kb-option-btn">
          <span class="kb-option-icon">${ICONS.search}</span>
          <span class="kb-option-text">Cari Kuliner</span>
        </button>
        <button onclick="kbStartReg()" class="kb-option-btn">
          <span class="kb-option-icon">${ICONS.store}</span>
          <span class="kb-option-text">Daftar UMKM</span>
        </button>
        <button onclick="kbShowStats()" class="kb-option-btn">
          <span class="kb-option-icon">${ICONS.chart}</span>
          <span class="kb-option-text">Statistik</span>
        </button>
        <button onclick="kbCheckStatus()" class="kb-option-btn">
          <span class="kb-option-icon">${ICONS.check}</span>
          <span class="kb-option-text">Cek Status</span>
        </button>
      </div>
    `);
  };

  window.showMainMenu = window.kbShowMenu; // Alias

  window.kbStartChat = function () {
    currentState = "CHAT";
    addBotMsg(
      "Silakan ketik kuliner yang dicari via chat di bawah. Contoh: 'Sate ayam murah'",
    );
  };

  // -- Pagination & Chat Logic --
  async function fetchRecommendations(query, offset = 0) {
    if (offset === 0) {
      loadingId = showTyping();
      currentQuery = query;
      allRecommendations = [];
    }

    try {
      const res = await fetch(`${API_BASE_URL}/chat`, {
        method: "POST",
        headers: { "Content-Type": "application/json" },
        body: JSON.stringify({ query: query, top_n: 10 }), // Get more to simulate buffer
      });
      const data = await res.json();
      if (offset === 0) removeTyping(loadingId);

      if (data.recommendations && data.recommendations.length > 0) {
        allRecommendations = data.recommendations;
        renderRecommendations(offset);
      } else {
        addBotMsg("Maaf, tidak ditemukan.");
      }
    } catch (e) {
      if (offset === 0) removeTyping(loadingId);
      addBotMsg("Gagal koneksi.");
    }
  }

  window.kbLoadMore = function () {
    currentOffset += 5;
    renderRecommendations(currentOffset);
  };

  function renderRecommendations(offset) {
    const slice = allRecommendations.slice(offset, offset + 5);
    if (slice.length === 0) {
      addBotMsg("Sudah tidak ada rekomendasi lagi.");
      return;
    }

    let html = "";
    slice.forEach((r) => {
      html += `
            <div class="kb-card">
              <div class="kb-card-header">
                <h4 class="kb-card-title">${r.nama_rumah_makan}</h4>
                <span class="kb-match-badge">${Math.round(r.similarity_score * 100)}%</span>
              </div>
              <div class="kb-meta-row">
                 <span class="kb-tag">${ICONS.map} ${r.alamat}</span>
              </div>
              <div class="kb-meta-row">
                 <span class="kb-tag">${ICONS.store} ${r.kategori}</span>
                 <span class="kb-tag" style="color:#d97706; background:#fef3c7;">${r.range_harga}</span>
              </div>
              <div style="font-size:12px; color:#64748b; font-style:italic; margin-bottom:8px;">"${r.deskripsi || "Deskripsi belum tersedia"}"</div>
              
              <button onclick="window.open('${r.maps_url}', '_blank')" class="kb-action-btn primary">
                ${ICONS.navigate} Lihat di Google Maps
              </button>
            </div>
          `;
    });

    // Load More logic
    if (allRecommendations.length > offset + 5) {
      html += `<button onclick="kbLoadMore()" class="kb-more-btn">${ICONS.more} Tampilkan Lebih Banyak</button>`;
    } else {
      html += `<div style="text-align:center; margin-top:12px;"><button onclick="kbShowMenu()" class="kb-action-btn">Kembali ke Menu</button></div>`;
    }

    addBotMsg(`Berikut rekomendasinya:<br>${html}`);
  }

  // -- Input Handler --
  async function handleSubmit() {
    const txt = inputEl.value.trim();
    if (!txt) return;

    addUserMsg(txt);
    inputEl.value = "";

    if (currentState === "CHAT") {
      currentOffset = 0;
      fetchRecommendations(txt, 0);
    } else if (currentState === "IDLE") {
      currentState = "CHAT";
      currentOffset = 0;
      fetchRecommendations(txt, 0);
    } else if (currentState.startsWith("REG_")) {
      // ... (Registration logic simplified for brevity, same as before) ...
      handleReg(txt);
    } else if (currentState === "CHECK_STATUS") {
      // ... (Check logic) ...
      handleCheck(txt);
    }
  }

  async function handleCheck(name) {
    const lid = showTyping();
    try {
      const res = await fetch(
        `${API_BASE_URL}/check-status?nama=${encodeURIComponent(name)}`,
      );
      const d = await res.json();
      removeTyping(lid);
      let color =
        d.status === "approved"
          ? "#16a34a"
          : d.status === "pending"
            ? "#ea580c"
            : "#dc2626";
      addBotMsg(
        `<b>${d.nama_rumah_makan}</b><br>Status: <b style="color:${color}">${d.status.toUpperCase()}</b><br>${d.message}<br><button onclick="kbShowMenu()" class="kb-action-btn">Menu Utama</button>`,
      );
      currentState = "IDLE";
    } catch (e) {
      removeTyping(lid);
      addBotMsg("Error checking status.");
    }
  }

  // --- Reg Logic Stub ---
  window.kbStartReg = function () {
    currentState = "REG_NAME";
    registrationData = {};
    addBotMsg("Nama Rumah Makan?");
  };
  async function handleReg(txt) {
    // (Simple state machine similar to previous step)
    if (currentState === "REG_NAME") {
      registrationData.nama = txt;
      currentState = "REG_ADDR";
      addBotMsg("Alamat Lengkap?");
    } else if (currentState === "REG_ADDR") {
      registrationData.alamat = txt;
      currentState = "REG_CAT";
      addBotMsg("Kategori?");
    } else if (currentState === "REG_CAT") {
      registrationData.cat = txt;
      currentState = "REG_PRICE";
      addBotMsg("Range Harga?");
    } else if (currentState === "REG_PRICE") {
      registrationData.price = txt;
      currentState = "REG_MENU";
      addBotMsg("3 Menu Andalan?");
    } else if (currentState === "REG_MENU") {
      // Submit
      const lid = showTyping();
      try {
        const res = await fetch(`${API_BASE_URL}/register`, {
          method: "POST",
          headers: { "Content-Type": "application/json" },
          body: JSON.stringify({
            nama_rumah_makan: registrationData.nama,
            alamat: registrationData.alamat,
            kategori: registrationData.cat,
            range_harga: registrationData.price,
            menu: txt,
            suasana: "-",
            tipe_pengunjung: "-",
            fasilitas: "-",
          }),
        });
        const d = await res.json();
        removeTyping(lid);
        addBotMsg(
          `✅ Sukses!<br>${d.message}<br><button onclick="kbShowMenu()" class="kb-action-btn">Menu</button>`,
        );
      } catch (e) {
        removeTyping(lid);
        addBotMsg("Gagal submit.");
      }
      currentState = "IDLE";
    }
  }

  // Listeners
  sendEl.addEventListener("click", handleSubmit);
  inputEl.addEventListener("keypress", (e) => {
    if (e.key === "Enter") handleSubmit();
  });
})();
