import streamlit as st
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import seaborn as sns

# ══════════════════════════════════════════
#  PAGE CONFIG
# ══════════════════════════════════════════
st.set_page_config(
    page_title="SPK Kelompok 5 - Metode WP",
    page_icon="💪",
    layout="wide",
)

# ══════════════════════════════════════════
#  CUSTOM CSS
# ══════════════════════════════════════════
st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Plus+Jakarta+Sans:wght@400;500;600;700;800&display=swap');
html, body, [class*="css"] { font-family: 'Plus Jakarta Sans', sans-serif; }

[data-testid="stSidebar"] {
    background: linear-gradient(180deg,#0f2027 0%,#203a43 55%,#2c5364 100%);
}
[data-testid="stSidebar"] * { color: #d9f5ee !important; }
[data-testid="stSidebar"] .stRadio label {
    font-size:14px!important; padding:7px 12px!important;
    border-radius:9px!important; transition:background .2s;
}
[data-testid="stSidebar"] .stRadio label:hover {
    background:rgba(255,255,255,0.10)!important;
}

.hero {
    background: linear-gradient(135deg,#11998e 0%,#38ef7d 100%);
    border-radius:18px; padding:2.2rem 2.8rem;
    margin-bottom:1.6rem; position:relative; overflow:hidden;
}
.hero::after {
    content:"💪"; font-size:130px; position:absolute;
    right:2.2rem; top:50%; transform:translateY(-50%); opacity:.13;
}
.hero h1 { color:#fff!important; font-size:2.1rem!important;
    font-weight:800!important; margin:0 0 .4rem!important; }
.hero p  { color:rgba(255,255,255,.88)!important;
    font-size:1rem!important; margin:0!important; }

.mstrip { display:flex; gap:14px; margin-bottom:1.4rem; flex-wrap:wrap; }
.mc { flex:1; min-width:140px; border-radius:14px; padding:1.1rem 1.4rem; text-align:center; }
.mc.g { background:linear-gradient(135deg,#11998e,#38ef7d); }
.mc.b { background:linear-gradient(135deg,#1a6dff,#00c4ff); }
.mc.o { background:linear-gradient(135deg,#f7971e,#ffd200); }
.mc.p { background:linear-gradient(135deg,#7928ca,#ff0080); }
.mc .v { font-size:2rem; font-weight:800; color:#fff; line-height:1; }
.mc .l { font-size:.78rem; color:rgba(255,255,255,.85); margin-top:4px; }

.stitle {
    font-size:1.15rem; font-weight:700; color:#11998e;
    margin:1.4rem 0 .7rem; padding-bottom:.45rem;
    border-bottom:2px solid rgba(17,153,142,.25);
}

.cg { display:flex; gap:11px; flex-wrap:wrap; margin:.8rem 0 1.2rem; }
.cc {
    flex:1; min-width:125px; background:#fff;
    border:1px solid rgba(17,153,142,.22);
    border-radius:13px; padding:.95rem .8rem;
    text-align:center; box-shadow:0 2px 12px rgba(0,0,0,.06);
}
.cc .ci { font-size:1.75rem; }
.cc .cn { font-size:.82rem; font-weight:700; color:#1a1a2e; margin:4px 0 2px; }
.cc .ct { font-size:.7rem; padding:2px 9px; border-radius:20px; font-weight:600; }
.cc .ben { background:#d4f7dc; color:#0a6b2a; }
.cc .cos { background:#fde8e8; color:#9b1c1c; }

.ibox {
    background:linear-gradient(135deg,rgba(17,153,142,.10),rgba(56,239,125,.06));
    border-left:4px solid #11998e;
    border-radius:0 12px 12px 0;
    padding:1rem 1.2rem; margin:.8rem 0;
}

.stButton>button {
    background:linear-gradient(135deg,#11998e,#38ef7d)!important;
    color:#fff!important; font-weight:700!important;
    border:none!important; border-radius:12px!important;
    padding:.65rem 2rem!important; font-size:16px!important;
    box-shadow:0 4px 18px rgba(17,153,142,.35)!important;
    transition:opacity .2s,transform .1s!important;
}
.stButton>button:hover  { opacity:.9!important; transform:translateY(-1px)!important; }
.stButton>button:active { transform:translateY(0)!important; }

.stTabs [data-baseweb="tab-list"] {
    gap:8px; background:rgba(17,153,142,.07);
    border-radius:12px; padding:4px;
}
.stTabs [data-baseweb="tab"] { border-radius:8px; font-weight:600; font-size:14px; }
.stTabs [aria-selected="true"] {
    background:linear-gradient(135deg,#11998e,#38ef7d)!important; color:#fff!important;
}

.pcard {
    background:linear-gradient(135deg,#0f2027,#203a43);
    border-radius:16px; padding:1.5rem 2rem;
    color:#e2f4f0; margin-bottom:1rem;
}
.pcard h3 { color:#38ef7d!important; margin-top:0; }
.pcard .pn { font-size:1.1rem; font-weight:700; color:#fff!important; }
.pcard p  { color:#b2d8d8!important; font-size:.88rem; margin:3px 0; }

.footer {
    background:linear-gradient(135deg,#11998e,#38ef7d);
    border-radius:12px; padding:.7rem 1.5rem;
    text-align:center; color:#fff; font-weight:600;
    font-size:.83rem; margin-top:2rem;
}
</style>
""", unsafe_allow_html=True)

# ══════════════════════════════════════════
#  LOAD & CLEAN DATA
# ══════════════════════════════════════════
@st.cache_data
def load_data():
    df = pd.read_csv("nutrients_csvfile.csv")
    for col in ["Grams","Calories","Protein","Fat","Sat.Fat","Fiber","Carbs"]:
        df[col] = (df[col].astype(str)
                   .str.replace(",","",regex=False)
                   .str.replace("t","0",regex=False)
                   .str.strip())
        df[col] = pd.to_numeric(df[col], errors="coerce")
    df = df.dropna(subset=["Grams","Calories","Protein","Fat","Fiber","Carbs"])
    df = df[df["Grams"] > 0].reset_index(drop=True)
    df["Protein_100g"]  = df["Protein"]  / df["Grams"] * 100
    df["Calories_100g"] = df["Calories"] / df["Grams"] * 100
    df["Fat_100g"]      = df["Fat"]      / df["Grams"] * 100
    df["Fiber_100g"]    = df["Fiber"]    / df["Grams"] * 100
    df["Carbs_100g"]    = df["Carbs"]    / df["Grams"] * 100
    df = df[df["Protein_100g"] <= 100].reset_index(drop=True)
    return df

df_raw = load_data()

# ══════════════════════════════════════════
#  SIDEBAR
# ══════════════════════════════════════════
with st.sidebar:
    st.markdown("<br>", unsafe_allow_html=True)
    st.markdown("<h1 style='font-size:28px; font-weight:800;'>🥗 SPK Pemilihan Asupan Nutrisi Optimal</h1>", unsafe_allow_html=True)
    st.markdown(
        "<span style='background:linear-gradient(135deg,#7928ca,#ff0080);"
        "color:#fff;font-weight:700;font-size:.75rem;padding:3px 12px;"
        "border-radius:20px;'>Metode WP</span>",
        unsafe_allow_html=True,
    )
    st.markdown("---")
    halaman = st.radio(
        "Navigasi",
        ["🏠  Beranda","📊  Dataset","⚙️  Hitung SPK","📈  Visualisasi","👥  Profil Kelompok"],
        label_visibility="collapsed",
    )
    st.markdown("---")
    st.markdown(
        "<p style='font-size:12px;color:#9ecfca;text-align:center;'>"
        "SCPK 2025/2026<br>Weighted Product (WP)</p>",
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════
#  🏠 BERANDA
# ══════════════════════════════════════════════════
if "🏠" in halaman:
    st.markdown("""
    <div class="hero">
        <h1>Pemilihan Asupan Nutrisi Optimal<br>untuk Program Peningkatan Berat Badan</h1>
        <p>Sistem Pendukung Keputusan &nbsp;·&nbsp; Metode Weighted Product (WP) &nbsp;·&nbsp; SCPK 2025/2026</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown(f"""
    <div class="mstrip">
        <div class="mc g"><div class="v">{len(df_raw)}</div><div class="l">Total Data Makanan</div></div>
        <div class="mc b"><div class="v">5</div><div class="l">Jumlah Kriteria</div></div>
        <div class="mc o"><div class="v">WP</div><div class="l">Metode SPK</div></div>
        <div class="mc p"><div class="v">16</div><div class="l">Kategori Makanan</div></div>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns([3, 2])

    with col1:
        st.markdown('<div class="stitle">🎯 Latar Belakang</div>', unsafe_allow_html=True)
        st.markdown("""
Menaikkan berat badan secara sehat memerlukan asupan kalori dan protein yang cukup. 
Namun, memilih sumber makanan yang tepat dari ratusan pilihan yang tersedia bukanlah hal yang mudah dilakukan.
                    
Sistem Pendukung Keputusan (SPK) berbasis Weighted Product (WP) ini hadir untuk membantu 
pengguna menemukan pilihan makanan terbaik secara objektif, 
berdasarkan bobot kriteria yang dapat dikustomisasi sesuai kebutuhan individu.
        """)

        st.markdown('<div class="stitle">📐 Cara Kerja Metode WP</div>', unsafe_allow_html=True)
        st.markdown("""
**Weighted Product (WP)** menggunakan operasi **perkalian berpangkat** - bukan penjumlahan.
Langkah-langkahnya:

1. **Normalisasi bobot** → total semua bobot = 1
2. **Hitung Vektor S** → setiap nilai kriteria dipangkatkan dengan bobotnya.
   Kriteria *benefit* → eksponen **+w**, kriteria *cost* → eksponen **-w**
3. **Hitung Vektor V** → skor akhir = S(i) ÷ ΣS(semua), lalu diranking dari tertinggi
        """)

    with col2:
        st.markdown('<div class="stitle">📋 Kriteria Penilaian</div>', unsafe_allow_html=True)
        st.markdown("""
<div class="cg">
  <div class="cc" style="border-top:4px solid #11998e">
    <div class="ci">⚡</div><div class="cn">Protein</div>
    <div class="ct ben">Benefit ↑</div>
  </div>
  <div class="cc" style="border-top:4px solid #1a6dff">
    <div class="ci">🔥</div><div class="cn">Kalori</div>
    <div class="ct ben">Benefit ↑</div>
  </div>
  <div class="cc" style="border-top:4px solid #f7971e">
    <div class="ci">🧈</div><div class="cn">Lemak</div>
    <div class="ct ben">Benefit ↑</div>
  </div>
  <div class="cc" style="border-top:4px solid #7928ca">
    <div class="ci">🍞</div><div class="cn">Karbo</div>
    <div class="ct ben">Benefit ↑</div>
  </div>
  <div class="cc" style="border-top:4px solid #e53e3e">
    <div class="ci">🥦</div><div class="cn">Serat</div>
    <div class="ct cos">Cost ↓</div>
  </div>
</div>
<div class="ibox" style="font-size:.85rem;">
Semua nilai dihitung per <b>100 gram</b> agar perbandingan antar makanan adil.
Serat bersifat <i>cost</i> karena dapat mengurangi penyerapan kalori.
</div>
        """, unsafe_allow_html=True)

    st.markdown(
        '<div class="footer">💪 SPK Pemilihan Asupan Nutrisi Optimal · Metode Weighted Product (WP) · SCPK 2025/2026</div>',
        unsafe_allow_html=True,
    )

# ══════════════════════════════════════════════════
#  📊 DATASET
# ══════════════════════════════════════════════════
elif "📊" in halaman:
    st.markdown("""
    <div class="hero" style="padding:1.6rem 2.2rem;">
        <h1 style="font-size:1.6rem!important;">📊 Dataset Nutrisi Makanan</h1>
        <p>Sumber: Nutritional Facts for most common foods - Kaggle</p>
    </div>
    """, unsafe_allow_html=True)

    c1, c2, c3 = st.columns(3)
    with c1:
        kat_pilih = st.selectbox("🔍 Filter Kategori",
                                 ["Semua"] + sorted(df_raw["Category"].unique().tolist()))
    with c2:
        cari = st.text_input("🔎 Cari Nama Makanan", placeholder="ketik nama makanan...")
    with c3:
        sort_col = st.selectbox("📈 Urutkan Berdasarkan",
                                ["Protein_100g","Calories_100g","Fat_100g","Carbs_100g","Fiber_100g"])

    df_view = df_raw.copy()
    if kat_pilih != "Semua":
        df_view = df_view[df_view["Category"] == kat_pilih]
    if cari:
        df_view = df_view[df_view["Food"].str.contains(cari, case=False, na=False)]
    df_view = df_view.sort_values(sort_col, ascending=False).reset_index(drop=True)

    st.markdown(f"""
    <div class="mstrip">
        <div class="mc g"><div class="v">{len(df_view)}</div><div class="l">Data Ditampilkan</div></div>
        <div class="mc b"><div class="v">{df_view['Category'].nunique()}</div><div class="l">Kategori</div></div>
        <div class="mc o"><div class="v">{df_view['Protein_100g'].mean():.1f}g</div><div class="l">Rata-Rata Protein/100g</div></div>
        <div class="mc p"><div class="v">{df_view['Calories_100g'].mean():.0f}</div><div class="l">Rata-Rata Kalori/100g</div></div>
    </div>
    """, unsafe_allow_html=True)

    st.dataframe(
        df_view[["Food","Measure","Grams","Calories","Protein","Fat","Fiber","Carbs","Category"]],
        use_container_width=True, height=430,
    )

    with st.expander("ℹ️ Keterangan Kolom Dataset"):
        st.markdown("""
| Kolom | Keterangan |
|---|---|
| Food | Nama makanan |
| Measure | Ukuran takaran saji |
| Grams | Berat takaran saji (gram) |
| Calories | Total kalori (kkal) |
| Protein | Kandungan protein (g) |
| Fat | Lemak total (g) |
| Fiber | Serat (g) |
| Carbs | Karbohidrat (g) |
| Category | Kategori makanan |
""")

# ══════════════════════════════════════════════════
#  ⚙️ HITUNG SPK – WP
# ══════════════════════════════════════════════════
elif "⚙️" in halaman:
    st.markdown("""
    <div class="hero" style="padding:1.6rem 2.2rem;">
        <h1 style="font-size:1.6rem!important;">⚙️ Hitung SPK — Weighted Product (WP)</h1>
        <p>Atur bobot kriteria lalu klik tombol untuk memulai perhitungan</p>
    </div>
    """, unsafe_allow_html=True)

    st.markdown('<div class="stitle">🎚️ Pengaturan Bobot Kriteria</div>', unsafe_allow_html=True)
    st.caption("Geser slider untuk mengatur bobot. Bobot akan dinormalisasi otomatis sehingga totalnya = 1.")

    col1, col2, col3 = st.columns(3)
    with col1:
        w_protein = st.slider("⚡ Bobot Protein",      0, 100, 40, 5)
        w_kalori  = st.slider("🔥 Bobot Kalori",       0, 100, 25, 5)
    with col2:
        w_lemak   = st.slider("🧈 Bobot Lemak",        0, 100, 15, 5)
        w_karbo   = st.slider("🍞 Bobot Karbohidrat",  0, 100, 15, 5)
    with col3:
        w_serat   = st.slider("🥦 Bobot Serat",        0, 100, 5,  5)
        top_n     = st.number_input("🏆 Tampilkan Top-N", min_value=5, max_value=50, value=10, step=5)

    W_raw  = np.array([w_protein, w_kalori, w_lemak, w_karbo, w_serat], dtype=float)
    W_norm = W_raw / W_raw.sum() if W_raw.sum() > 0 else W_raw

    cb1, cb2, cb3, cb4, cb5 = st.columns(5)
    for col, lbl, w in zip([cb1,cb2,cb3,cb4,cb5],
                           ["⚡ Protein","🔥 Kalori","🧈 Lemak","🍞 Karbo","🥦 Serat"],
                           W_norm):
        col.metric(lbl, f"{w:.3f}")

    kat_spk = st.selectbox("📂 Filter Kategori (opsional)",
                           ["Semua"] + sorted(df_raw["Category"].unique().tolist()),
                           key="kat_spk")
    st.markdown("---")
    hitung = st.button("🚀 Hitung WP Sekarang!", type="primary", use_container_width=True)

    if hitung:
        if W_raw.sum() == 0:
            st.error("❌ Total bobot tidak boleh nol!")
        else:
            df_spk = df_raw.copy()
            if kat_spk != "Semua":
                df_spk = df_spk[df_spk["Category"] == kat_spk]
            df_spk = df_spk.reset_index(drop=True)

            if len(df_spk) < 2:
                st.warning("Data terlalu sedikit. Pilih kategori lain.")
            else:
                kriteria = ["Protein_100g","Calories_100g","Fat_100g","Carbs_100g","Fiber_100g"]
                benefit  = [True, True, True, True, False]

                X = df_spk[kriteria].values.astype(float)
                X = np.where(X <= 0, 1e-9, X)

                # Eksponen: benefit = +w, cost = -w
                exp = np.array([w if b else -w for w, b in zip(W_norm, benefit)])

                # Vektor S & V
                S = np.prod(np.power(X, exp), axis=1)
                V = S / S.sum()

                df_spk["Vektor_S"] = S
                df_spk["Vektor_V"] = V
                df_hasil = df_spk.sort_values("Vektor_V", ascending=False).head(int(top_n)).reset_index(drop=True)
                df_hasil.index += 1
                df_hasil.index.name = "Peringkat"

                st.success(f"✅ Perhitungan WP selesai! Menampilkan Top-{int(top_n)} terbaik.")

                st.markdown('<div class="stitle">🏆 Tabel Hasil Perangkingan</div>', unsafe_allow_html=True)
                tampil = df_hasil[["Food","Category","Protein_100g","Calories_100g",
                                   "Fat_100g","Carbs_100g","Fiber_100g","Vektor_S","Vektor_V"]].copy()
                tampil.columns = ["Makanan","Kategori","Protein","Kalori","Lemak","Karbo","Serat","Vektor S","Vektor V"]
                for c in ["Protein","Kalori","Lemak","Karbo","Serat"]:
                    tampil[c] = tampil[c].map("{:.2f}".format)
                tampil["Vektor S"] = tampil["Vektor S"].map("{:.8f}".format)
                tampil["Vektor V"] = tampil["Vektor V"].map("{:.8f}".format)
                st.dataframe(tampil, use_container_width=True)

                # Simpan ke session state
                st.session_state["df_hasil"]    = df_hasil
                st.session_state["W_norm"]      = W_norm
                st.session_state["top_n"]       = int(top_n)
                st.session_state["sudah_hitung"] = True

                with st.expander("🔬 Detail Vektor S — Nilai x^w tiap Kriteria"):
                    df_s = pd.DataFrame(
                        np.power(X[:int(top_n)], exp),
                        columns=["Protein^w","Kalori^w","Lemak^w","Karbo^w","Serat^(-w)"]
                    )
                    df_s.insert(0, "Makanan", df_spk["Food"].values[:int(top_n)])
                    st.dataframe(df_s.style.format("{:.6f}", subset=df_s.columns[1:]),
                                 use_container_width=True)

                with st.expander("📐 Bobot & Eksponen yang Digunakan"):
                    df_bobot = pd.DataFrame({
                        "Kriteria":  ["Protein","Kalori","Lemak","Karbohidrat","Serat"],
                        "Bobot Input": W_raw.astype(int),
                        "Bobot Ternormalisasi (w)": W_norm.round(4),
                        "Jenis": ["Benefit","Benefit","Benefit","Benefit","Cost"],
                        "Eksponen WP": [f"+{w:.4f}" if b else f"−{w:.4f}"
                                        for w, b in zip(W_norm, benefit)],
                    })
                    st.dataframe(df_bobot, use_container_width=True, hide_index=True)

# ══════════════════════════════════════════════════
#  📈 VISUALISASI
# ══════════════════════════════════════════════════
elif "📈" in halaman:
    st.markdown("""
    <div class="hero" style="padding:1.6rem 2.2rem;">
        <h1 style="font-size:1.6rem!important;">📈 Visualisasi Data &amp; Hasil WP</h1>
        <p>Eksplorasi distribusi nutrisi dan hasil perangkingan</p>
    </div>
    """, unsafe_allow_html=True)

    tab1, tab2, tab3 = st.tabs(["📊 Distribusi Dataset", "🏆 Hasil WP", "🔗 Korelasi Nutrisi"])

    BG = "#f8fffe"

    # ── Tab 1: Distribusi ──
    with tab1:
        st.markdown('<div class="stitle">Rata-Rata Protein per Kategori</div>', unsafe_allow_html=True)
        fig1, ax1 = plt.subplots(figsize=(13, 5))
        fig1.patch.set_facecolor(BG); ax1.set_facecolor(BG)
        order = df_raw.groupby("Category")["Protein_100g"].mean().sort_values(ascending=False)
        bars1 = ax1.bar(
            order.index, order.values,
            color=plt.cm.cool(np.linspace(0, 1, len(order))),
            edgecolor="white", linewidth=0.5
        )
        ax1.bar_label(bars1, fmt="%.1f", padding=3, fontsize=8)
        ax1.set_xticks(range(len(order)))
        ax1.set_xticklabels(order.index, rotation=35, ha="right", fontsize=8)
        ax1.set_ylabel("Rata-Rata Protein / 100 g (g)", fontsize=10)
        ax1.set_title("Rata-Rata Kandungan Protein per 100g berdasarkan Kategori Makanan",
                    fontsize=12, fontweight="bold", pad=10)
        ax1.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig1)

        st.markdown('<div class="stitle">Rata-Rata Kalori per Kategori</div>', unsafe_allow_html=True)
        fig2, ax2 = plt.subplots(figsize=(13, 5))
        fig2.patch.set_facecolor(BG); ax2.set_facecolor(BG)
        avg = df_raw.groupby("Category")["Calories_100g"].mean().sort_values(ascending=True)
        bars = ax2.barh(avg.index, avg.values,
                        color=plt.cm.YlGn(np.linspace(0.3, 1, len(avg))),
                        edgecolor="white", linewidth=0.5)
        ax2.bar_label(bars, fmt="%.1f", padding=4, fontsize=8)
        ax2.set_xlabel("Rata-Rata Kalori / 100 g", fontsize=10)
        ax2.set_title("Rata-Rata Kandungan Kalori per Kategori Makanan",
                      fontsize=12, fontweight="bold", pad=10)
        ax2.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig2)

        st.markdown('<div class="stitle">Scatter: Protein vs Kalori per Kategori</div>', unsafe_allow_html=True)
        fig3, ax3 = plt.subplots(figsize=(11, 6))
        fig3.patch.set_facecolor(BG); ax3.set_facecolor(BG)
        cats = df_raw["Category"].unique()
        pal3 = plt.cm.tab20(np.linspace(0, 1, len(cats)))
        for i, k in enumerate(cats):
            sub = df_raw[df_raw["Category"] == k]
            ax3.scatter(sub["Protein_100g"], sub["Calories_100g"],
                        label=k, color=pal3[i], alpha=0.65, s=45,
                        edgecolors="white", linewidths=0.4)
        ax3.set_xlabel("Protein / 100 g (g)", fontsize=10)
        ax3.set_ylabel("Kalori / 100 g (kkal)", fontsize=10)
        ax3.set_title("Hubungan Protein vs Kalori per 100g", fontsize=12, fontweight="bold", pad=10)
        ax3.legend(bbox_to_anchor=(1.02, 1), loc="upper left", fontsize=7)
        ax3.spines[["top", "right"]].set_visible(False)
        plt.tight_layout(); st.pyplot(fig3)

    # ── Tab 2: Hasil WP ──
    with tab2:
        if not st.session_state.get("sudah_hitung"):
            st.markdown(
                '<div class="ibox">⚠️ Silakan jalankan perhitungan di halaman '
                '<b>⚙️ Hitung SPK</b> terlebih dahulu.</div>',
                unsafe_allow_html=True,
            )
        else:
            df_h  = st.session_state["df_hasil"]
            W_n   = st.session_state["W_norm"]
            top_n = st.session_state["top_n"]

            st.markdown(f'<div class="stitle">Top-{top_n} Sumber Protein — Skor Vektor V</div>',
                        unsafe_allow_html=True)
            fig4, ax4 = plt.subplots(figsize=(11, 6))
            fig4.patch.set_facecolor(BG); ax4.set_facecolor(BG)
            y_labels = [f"#{i+1}  {row['Food'][:30]}" for i, row in df_h.iterrows()]
            colors4 = plt.cm.summer(np.linspace(0.1, 0.9, len(df_h)))[::-1]
            bars4 = ax4.barh(y_labels[::-1], df_h["Vektor_V"].values[::-1],
                             color=colors4, edgecolor="white", linewidth=0.5)
            ax4.bar_label(bars4, fmt="%.6f", padding=4, fontsize=8)
            ax4.set_xlabel("Nilai Vektor V", fontsize=10)
            ax4.set_title(f"Top-{top_n} Sumber Protein Terbaik (Metode WP — Vektor V)",
                          fontsize=12, fontweight="bold", pad=10)
            ax4.spines[["top", "right"]].set_visible(False)
            plt.tight_layout(); st.pyplot(fig4)

            st.markdown('<div class="stitle">Profil Nutrisi Top-5 Makanan Terpilih</div>',
                        unsafe_allow_html=True)
            top5 = df_h.head(5)
            krit_c = ["Protein_100g","Calories_100g","Fat_100g","Carbs_100g","Fiber_100g"]
            krit_l = ["Protein","Kalori","Lemak","Karbo","Serat"]
            fig5, ax5 = plt.subplots(figsize=(11, 5))
            fig5.patch.set_facecolor(BG); ax5.set_facecolor(BG)
            x = np.arange(len(krit_l)); bw = 0.15
            pal5 = ["#11998e","#1a6dff","#f7971e","#7928ca","#e53e3e"]
            for i, (_, row) in enumerate(top5.iterrows()):
                ax5.bar(x + i * bw, [row[c] for c in krit_c], bw,
                        label=row["Food"][:22], color=pal5[i], edgecolor="white")
            ax5.set_xticks(x + bw * 2)
            ax5.set_xticklabels(krit_l, fontsize=9)
            ax5.set_ylabel("Nilai / 100 g", fontsize=10)
            ax5.set_title("Perbandingan Profil Nutrisi Top-5 Makanan Terpilih",
                          fontsize=12, fontweight="bold", pad=10)
            ax5.legend(fontsize=8)
            ax5.spines[["top", "right"]].set_visible(False)
            plt.tight_layout(); st.pyplot(fig5)

            st.markdown('<div class="stitle">Distribusi Bobot Kriteria WP</div>',
                        unsafe_allow_html=True)
            fig6, ax6 = plt.subplots(figsize=(6, 6))
            fig6.patch.set_facecolor(BG)
            wedge_colors = ["#11998e","#1a6dff","#f7971e","#7928ca","#e53e3e"]
            wedges, texts, autotexts = ax6.pie(
                W_n,
                labels=["Protein","Kalori","Lemak","Karbo","Serat"],
                autopct="%1.1f%%", startangle=140,
                colors=wedge_colors,
                pctdistance=0.82,
                wedgeprops=dict(edgecolor="white", linewidth=2.5),
            )
            for at in autotexts:
                at.set_color("white"); at.set_fontweight("700"); at.set_fontsize(9)
            ax6.set_title("Distribusi Bobot Kriteria WP", fontsize=12, fontweight="bold", pad=10)
            plt.tight_layout(); st.pyplot(fig6)

    # ── Tab 3: Korelasi ──
    with tab3:
        st.markdown('<div class="stitle">Heatmap Korelasi Antar Nutrisi</div>', unsafe_allow_html=True)
        cols_c = ["Protein_100g","Calories_100g","Fat_100g","Fiber_100g","Carbs_100g"]
        labs_c = ["Protein","Kalori","Lemak","Serat","Karbo"]
        corr = df_raw[cols_c].corr()
        corr.index = labs_c; corr.columns = labs_c
        fig7, ax7 = plt.subplots(figsize=(8, 6))
        fig7.patch.set_facecolor(BG); ax7.set_facecolor(BG)
        sns.heatmap(corr, annot=True, fmt=".2f", cmap="RdYlGn",
                    linewidths=1.5, linecolor="white",
                    ax=ax7, square=True, vmin=-1, vmax=1,
                    annot_kws={"size": 11, "weight": "bold"})
        ax7.set_title("Matriks Korelasi Nutrisi per 100 g", fontsize=13, fontweight="bold", pad=12)
        plt.tight_layout(); st.pyplot(fig7)
        st.markdown("""
**Interpretasi:**
- 🟢 Mendekati **+1** → hubungan positif kuat (keduanya naik bersamaan)
- 🔴 Mendekati **−1** → hubungan negatif kuat (satu naik, yang lain turun)
- ⬜ Mendekati **0** → tidak ada hubungan linear yang signifikan
""")

# ══════════════════════════════════════════════════
#  👥 PROFIL KELOMPOK
# ══════════════════════════════════════════════════
elif "👥" in halaman:
    st.markdown("""
    <div class="hero" style="padding:1.6rem 2.2rem;">
        <h1 style="font-size:1.6rem!important;">👥 Profil Kelompok</h1>
        <p>Anggota kelompok &amp; informasi proyek akhir SCPK 2025/2026</p>
    </div>
    """, unsafe_allow_html=True)

    col1, col2 = st.columns(2)
    with col1:
        st.markdown("""
        <div class="pcard">
            <h3>👤 Anggota 1</h3>
            <p class="pn">Nailah Hana Nur'aisyah</p>
            <p>🎓 NIM : 123240088</p>
            <p>🏫 Plug : IF-B</p>
        </div>
        """, unsafe_allow_html=True)
    with col2:
        st.markdown("""
        <div class="pcard">
            <h3>👤 Anggota 2</h3>
            <p class="pn">Cantika Zahra Putri Maharani</p>
            <p>🎓 NIM : 123240091</p>
            <p>🏫 Plug : IF-B</p>
        </div>
        """, unsafe_allow_html=True)

    st.markdown('<div class="stitle">📁 Informasi Proyek</div>', unsafe_allow_html=True)
    st.markdown("""
| Item | Detail |
|---|---|
| **Judul** | Pemilihan Asupan Nutrisi Optimal untuk Program Peningkatan Berat Badan |
| **Metode SPK** | Weighted Product (WP) |
| **Dataset** | Nutritional Facts for most common foods |
| **Sumber Dataset** | Kaggle - nutrients_csvfile.csv |
| **Jumlah Alternatif** | 328 alternatif |
| **Jumlah Kriteria** | 5 kriteria |
""")

    st.markdown('<div class="stitle">🔗 Repository GitHub</div>', unsafe_allow_html=True)
    st.code("https://github.com/Cantikazahra/Project_PrakSCPK_Kelompok-5_IF-B", language=None)

    st.markdown(
        '<div class="footer">💪 SPK Pemilihan Asupan Nutrisi Optimal · Weighted Product (WP) </div>',
        unsafe_allow_html=True,
    )
