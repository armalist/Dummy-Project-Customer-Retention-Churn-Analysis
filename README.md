# ☕ Customer Retention & Churn Analysis — NestBrew Co.

> **[DUMMY PROJECT]** — This is a fictional case study created for portfolio purposes.
> The company "NestBrew Co." and all data used in this project are entirely made up.

---

![Status](https://img.shields.io/badge/Status-Completed-brightgreen)
![Tools](https://img.shields.io/badge/Tools-Python%20%7C%20Pandas%20%7C%20Tableau-blue)
![Type](https://img.shields.io/badge/Type-Dummy%20Project-orange)
![Domain](https://img.shields.io/badge/Domain-Customer%20Analytics-purple)

---

## Dummy Project Overview

**NestBrew Co.** adalah brand kopi berlangganan (subscription-based) berbasis di Jakarta yang
mengalami lonjakan churn rate dari **4.2% → 11.7%** dalam 6 bulan terakhir.

Sebagai Data Analyst, saya ditugaskan untuk:
- Mengidentifikasi **siapa** pelanggan yang paling berisiko churn
- Menemukan **faktor-faktor utama** penyebab churn
- Memberikan **rekomendasi strategis** kepada tim marketing

---

## Business Questions

1. Berapa churn rate keseluruhan dan bagaimana trennya per bulan?
2. Segmen pelanggan mana yang paling rentan churn?
3. Faktor apa yang paling berkorelasi dengan churn?
4. Apa rekomendasi actionable untuk meningkatkan retensi?

---

## Tools & Technologies

| Kategori | Tools |
|----------|-------|
| Bahasa Pemrograman | Python 3.x |
| Data Manipulation | Pandas, NumPy |
| Visualisasi | Matplotlib, Seaborn, Plotly |
| Dashboard | Tableau Public *(link di bawah)* |
| Notebook | Jupyter Notebook |
| Version Control | Git & GitHub |

---

## Repository Structure

```
nestbrew-churn-analysis/
│
├── data/
│   └── nestbrew_customers_dummy.csv     ← Dataset dummy (5.000 baris)
│
├── notebooks/
│   ├── 01_data_generation.ipynb         ← Pembuatan dataset dummy
│   ├── 02_EDA_cleaning.ipynb            ← Eksplorasi & pembersihan data
│   └── 03_churn_analysis.ipynb          ← Analisis utama & insight
│
├── dashboard/
│   ├── nestbrew_dashboard_screenshot.png
│   └── [Link Tableau Public]
│
├── 📁 report/
│   └── NestBrew_Churn_Analysis_Report.pdf
│
└── README.md
```

---

## Dataset Overview

> Dataset ini dibuat menggunakan Python.
> Tidak ada data pelanggan nyata yang digunakan (data dummy).

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

## Key Findings

### 1. Churn Rate Overview
- **Overall churn rate:** `XX.X%` dari total 5.000 pelanggan
- Tren menunjukkan lonjakan signifikan mulai bulan `[bulan]`

### 2. Segmen Paling Rentan Churn
- Plan **Basic** memiliki churn rate tertinggi: `XX%`
- Pelanggan dengan **tenure < 3 bulan** memiliki risiko churn `XX%` lebih tinggi
- Kota dengan churn tertinggi: `[Kota X]`

### 3. Top Churn Drivers
| Rank | Faktor | Dampak |
|------|--------|--------|
| #1 | `support_tickets` tinggi (≥ 3 tiket) | Churn rate `XX%` lebih tinggi |
| #2 | `avg_rating` rendah (≤ 2.5) | Korelasi kuat dengan churn |
| #3 | Tenure < 3 bulan | Periode paling kritis |

### 4. Rekomendasi Strategis
- **Early Onboarding Program:** Fokus engagement di 90 hari pertama
- **Proactive CS Follow-up:** Hubungi pelanggan setelah tiket ke-2
- **Rating Recovery Campaign:** Tawarkan benefit khusus ke pelanggan rating ≤ 3
- **Plan Upgrade Incentive:** Dorong migrasi dari Basic ke Standard

---

## Dashboard Preview

```
[ Screenshot Dashboard Tableau ]
```

🔗 **Link Dashboard Tableau Public:** [Klik di sini](#) *(akan diupdate)*

---

## How to Run

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

## Project Context & Disclaimer

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

## Author

**Ariqah Maulia Listiani**
📧 ariqahmaulialistiani@gmail.com
🔗 [LinkedIn](#) | [GitHub](#) | [Tableau Public](#)

---

## Learning Outcomes

Melalui proyek ini, saya mempraktikkan:
- Exploratory Data Analysis (EDA) end-to-end
- Feature engineering (`tenure_months`)
- Analisis korelasi dan segmentasi
- Storytelling data untuk audiens bisnis non-teknis
- Pembuatan dashboard interaktif

---

*Last updated: September 2026*
