# ☕ Customer Retention & Churn Analysis — NestBrew Co.

> 🏷️ **[DUMMY PROJECT]** — This is a fictional case study created for portfolio purposes.
> The company "NestBrew Co." and all data used in this project are entirely made up.

---

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Tools](https://img.shields.io/badge/Tools-Python%20%7C%20Pandas%20%7C%20Tableau-blue)
![Type](https://img.shields.io/badge/Type-Dummy%20Project-orange)
![Domain](https://img.shields.io/badge/Domain-Customer%20Analytics-purple)

---

## 📌 Project Overview

**NestBrew Co.** adalah brand kopi berlangganan (subscription-based) berbasis di Jakarta yang
mengalami lonjakan churn rate dari **4.2% → 11.7%** dalam 6 bulan terakhir.

Sebagai Data Analyst, saya ditugaskan untuk:
- Mengidentifikasi **siapa** pelanggan yang paling berisiko churn
- Menemukan **faktor-faktor utama** penyebab churn
- Memberikan **rekomendasi strategis** kepada tim marketing

---

## 🎯 Business Questions

1. Berapa churn rate keseluruhan dan bagaimana trennya per bulan?
2. Segmen pelanggan mana yang paling rentan churn?
3. Faktor apa yang paling berkorelasi dengan churn?
4. Apa rekomendasi actionable untuk meningkatkan retensi?

---

## 🛠️ Tools & Technologies

| Kategori | Tools |
|----------|-------|
| Bahasa Pemrograman | Python 3.x |
| Data Manipulation | Pandas, NumPy |
| Visualisasi | Matplotlib, Seaborn, Plotly |
| Dashboard | Tableau Public *(link di bawah)* |
| Notebook | Jupyter Notebook |
| Version Control | Git & GitHub |

---

## 📂 Repository Structure

```
nestbrew-churn-analysis/
│
├── 📁 data/
│   └── nestbrew_customers_dummy.csv     ← Dataset dummy (5.000 baris)
│
├── 📁 notebooks/
│   ├── 01_data_generation.ipynb         ← Pembuatan dataset dummy
│   ├── 02_EDA_cleaning.ipynb            ← Eksplorasi & pembersihan data
│   └── 03_churn_analysis.ipynb          ← Analisis utama & insight
│
├── 📁 dashboard/
│   ├── nestbrew_dashboard_screenshot.png
│   └── [Link Tableau Public]
│
├── 📁 report/
│   └── NestBrew_Churn_Analysis_Report.pdf
│
└── README.md
```

---

## 📊 Dataset Overview

> ⚠️ Dataset ini sepenuhnya dibuat secara sintetis menggunakan Python (Faker + NumPy).
> Tidak ada data pelanggan nyata yang digunakan.

| Kolom | Tipe | Deskripsi |
|-------|------|-----------|
| `customer_id` | String | ID unik pelanggan |
| `join_date` | Date | Tanggal pertama berlangganan |
| `last_active_date` | Date | Tanggal terakhir aktif |
| `subscription_plan` | Categorical | Basic / Standard / Premium |
| `monthly_spend` | Float | Rata-rata pengeluaran/bulan (Rp) |
| `total_orders` | Integer | Total pesanan selama berlangganan |
| `avg_rating` | Float | Rating rata-rata produk (1–5) |
| `support_tickets` | Integer | Jumlah tiket komplain ke CS |
| `promo_used` | Boolean | Pernah menggunakan promo (Yes/No) |
| `city` | Categorical | Kota domisili |
| `tenure_months` | Integer | Lama berlangganan (bulan) *[derived]* |
| `churn` | Binary | **TARGET** → 0 = Aktif, 1 = Churn |

**Ukuran dataset:** 5.000 baris × 12 kolom

---

## 🔍 Key Findings

> *Bagian ini diisi setelah analisis selesai. Berikut adalah placeholder yang akan diupdate.*

### 1️⃣ Churn Rate Overview
- **Overall churn rate: 23.7%** — 1.184 dari 5.000 pelanggan telah churn
- Churn paling tinggi terjadi pada pelanggan yang baru bergabung (tenure 0–3 bulan)
- Korelasi terkuat dengan churn: `tenure_months` (r = **-0.565**)

### 2️⃣ Segmen Paling Rentan Churn
- Plan **Basic** memiliki churn rate tertinggi: **28.8%** vs Premium 15.4%
- Pelanggan **tenure 0–3 bulan** churn rate: **52.3%** — hampir 2× rata-rata
- **Kombinasi paling berbahaya:** Plan Basic + Tenure 0–3 bulan → **70.7% churn rate**

### 3️⃣ Top Churn Drivers
| Rank | Faktor | Dampak |
|------|--------|--------|
| #1 | `tenure_months` pendek (0–3 bln) | Korelasi -0.565 dengan churn; churn rate 52.3% |
| #2 | `support_tickets` ≥ 3 tiket | Churn rate rata-rata **41.3%** — 2× lebih tinggi dari avg |
| #3 | Plan Basic | Churn rate 28.8% vs avg 23.7% |
| #4 | `avg_rating` rendah (≤ 2.5) | Korelasi negatif dengan retensi |

### 4️⃣ Rekomendasi Strategis
- 🚀 **Early Onboarding Program** *(Prioritas Tinggi)*: Program 90 hari pertama — welcome email series, loyalty reward bulan ke-2, check-in CS. Target: turunkan churn 0–3 bln sebesar 30%
- 🎧 **Proactive CS Follow-Up** *(Prioritas Tinggi)*: Auto-trigger follow-up setelah tiket ke-2. Target: kurangi churn tiket ≥3 dari 41.3% → <25%
- 📦 **Plan Upgrade Campaign** *(Prioritas Menengah)*: Trial gratis Standard 1 bulan untuk pengguna Basic di bulan ke-3. Target: 15% migrasi ke plan lebih tinggi
- ⭐ **Rating Recovery Campaign** *(Prioritas Menengah)*: Survei + penggantian produk untuk pelanggan rating ≤ 3.0. Target: avg rating ≥ 4.0

> 📌 **Estimasi dampak gabungan:** Churn rate proyeksi turun dari **23.7% → 14–16%**, setara mempertahankan **~400–500 pelanggan** per semester.

---

## 📈 Dashboard Preview

![Summary Dashboard](data/viz_11_summary_dashboard.png)

> Dashboard ringkasan yang menampilkan KPI utama, tren churn bulanan, churn per plan, dan top churn drivers dalam satu tampilan.

**Visualisasi lengkap tersedia di folder `data/`:**
- `viz_01` — Distribusi Churn (Donut + Bar)
- `viz_02` — Distribusi Variabel Numerik per Segmen
- `viz_03` — Churn Rate per Subscription Plan
- `viz_04` — Churn Rate per Tenure Group
- `viz_05` — Heatmap Korelasi Antar Variabel
- `viz_06` — Churn Rate per Kota
- `viz_07` — Perbandingan Profil Retain vs Churn
- `viz_08` — Tren Churn Bulanan
- `viz_09` — Dampak Support Tickets terhadap Churn
- `viz_10` — Peta Risiko: Plan × Tenure
- `viz_11` — Summary Dashboard (gabungan)

---

## 🚀 How to Run

### Prerequisites
```bash
pip install pandas numpy matplotlib seaborn plotly faker jupyter
```

### Langkah-langkah
```bash
# 1. Clone repository ini
git clone https://github.com/[username]/nestbrew-churn-analysis.git
cd nestbrew-churn-analysis

# 2. Jalankan notebook secara berurutan
jupyter notebook

# 3. Buka notebook sesuai urutan:
#    01 → 02 → 03
```

---

## 📝 Project Context & Disclaimer

> **⚠️ PENTING — HARAP DIBACA:**
>
> Proyek ini adalah **dummy project / fictional case study** yang dibuat murni untuk keperluan
> portofolio dan pembelajaran. Semua elemen berikut adalah **fiktif sepenuhnya:**
> - Nama perusahaan "NestBrew Co." dan seluruh detail brand
> - Data pelanggan (dibuat secara sintetis dengan Python)
> - Angka-angka finansial dan metrik bisnis
> - Nama kota, paket produk, dan seluruh atribut data
>
> Proyek ini **tidak berafiliasi** dengan perusahaan nyata mana pun.
> Tujuan utama adalah mendemonstrasikan kemampuan analisis data secara end-to-end.

---

## 👤 Author

**Ariqah Maulia Listiani**
📧 ariqahmaulialistiani@gmail.com
🔗 [LinkedIn](#) | [GitHub](#) | [Tableau Public](#)

---

## 📚 Learning Outcomes

Melalui proyek ini, saya mempraktikkan:
- ✅ Pembuatan **synthetic dataset** yang realistis dengan Python (Faker + NumPy)
- ✅ **Exploratory Data Analysis (EDA)** end-to-end — distribusi, missing values, outlier
- ✅ **Feature engineering** — `tenure_months`, `tenure_group`, `rating_group`
- ✅ **Analisis korelasi dan segmentasi** — heatmap, cross-tabulation, churn driver
- ✅ **Storytelling data** untuk audiens bisnis non-teknis (CMO level)
- ✅ **Visualisasi multi-chart** dengan Matplotlib & Seaborn (11 chart)
- ✅ **Rekomendasi bisnis actionable** berdasarkan temuan data
- ✅ **Presentasi eksekutif** dalam format PowerPoint (.pptx)

---

*Last updated: September 2026*
