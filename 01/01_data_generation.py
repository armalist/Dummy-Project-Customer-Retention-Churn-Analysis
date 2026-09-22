"""
=============================================================
 NestBrew Co. — Synthetic Customer Dataset Generator
 [DUMMY PROJECT] — Data fiktif untuk keperluan portofolio
=============================================================
 Author  : Ariqah Maulia Listiani
 Date    : September 2026
 Tools   : Python, Pandas, NumPy
=============================================================

CARA PAKAI:
  pip install pandas numpy faker
  python 01_data_generation.py

OUTPUT:
  data/nestbrew_customers_dummy.csv
"""

import pandas as pd
import numpy as np
from faker import Faker
from datetime import datetime, timedelta
import os
import random

# ─── Reproducibility ───────────────────────────────────────
SEED = 42
np.random.seed(SEED)
random.seed(SEED)
fake = Faker('id_ID')   # Locale Indonesia
Faker.seed(SEED)

# ─── Konstanta ─────────────────────────────────────────────
N_CUSTOMERS    = 5000
START_DATE     = datetime(2023, 1, 1)
END_DATE       = datetime(2025, 3, 31)

PLANS = ['Basic', 'Standard', 'Premium']
PLAN_WEIGHTS   = [0.50, 0.35, 0.15]   # Basic paling banyak

CITIES = [
    'Jakarta', 'Surabaya', 'Bandung', 'Medan',
    'Makassar', 'Semarang', 'Depok', 'Tangerang', 'Bekasi', 'Bogor'
]
CITY_WEIGHTS = [0.30, 0.15, 0.12, 0.08, 0.06, 0.07, 0.07, 0.06, 0.05, 0.04]

PLAN_SPEND = {
    'Basic':    (180_000, 220_000),   # (min, max) Rp
    'Standard': (380_000, 460_000),
    'Premium':  (580_000, 700_000),
}


# ════════════════════════════════════════════════════════════
#  FUNGSI BANTU
# ════════════════════════════════════════════════════════════

def random_date(start: datetime, end: datetime) -> datetime:
    """Ambil tanggal acak di antara dua tanggal."""
    delta = (end - start).days
    return start + timedelta(days=random.randint(0, delta))


def calculate_churn_probability(plan, tenure_months, avg_rating,
                                 support_tickets, promo_used):
    """
    Hitung probabilitas churn berdasarkan faktor-faktor bisnis yang logis.

    Aturan yang dibangun:
      - Tenure pendek → risiko lebih tinggi
      - Plan Basic → risiko lebih tinggi
      - Rating rendah → risiko lebih tinggi
      - Banyak tiket → risiko lebih tinggi
      - Pernah pakai promo → sedikit lebih loyal
    """
    prob = 0.08   # base churn rate ~8%

    # Faktor Plan
    plan_factor = {'Basic': 0.12, 'Standard': 0.04, 'Premium': -0.02}
    prob += plan_factor[plan]

    # Faktor Tenure (bulan)
    if tenure_months <= 3:
        prob += 0.20    # bulan-bulan awal paling kritis
    elif tenure_months <= 6:
        prob += 0.10
    elif tenure_months <= 12:
        prob += 0.02
    else:
        prob -= 0.05    # pelanggan lama lebih loyal

    # Faktor Rating
    if avg_rating <= 2.0:
        prob += 0.25
    elif avg_rating <= 3.0:
        prob += 0.12
    elif avg_rating >= 4.5:
        prob -= 0.08

    # Faktor Support Tickets (komplain)
    if support_tickets >= 4:
        prob += 0.22
    elif support_tickets == 3:
        prob += 0.12
    elif support_tickets == 2:
        prob += 0.05
    elif support_tickets == 0:
        prob -= 0.04

    # Faktor Promo
    if promo_used:
        prob -= 0.03   # sedikit lebih loyal jika pernah kena promo

    # Clamp ke range 0–1
    return float(np.clip(prob, 0.01, 0.97))


# ════════════════════════════════════════════════════════════
#  GENERATE DATASET
# ════════════════════════════════════════════════════════════

def generate_dataset(n: int = N_CUSTOMERS) -> pd.DataFrame:
    print(f"\n{'='*55}")
    print(f"  NestBrew Co. — Dataset Generator")
    print(f"  Generating {n:,} synthetic customer records...")
    print(f"{'='*55}\n")

    records = []

    for i in range(n):
        # ── Identitas ──────────────────────────────────────
        customer_id = f"NB-{str(i+1).zfill(5)}"

        # ── Tanggal Join ───────────────────────────────────
        join_date = random_date(START_DATE, END_DATE - timedelta(days=30))

        # ── Plan Langganan ─────────────────────────────────
        plan = np.random.choice(PLANS, p=PLAN_WEIGHTS)

        # ── Kota ───────────────────────────────────────────
        city = np.random.choice(CITIES, p=CITY_WEIGHTS)

        # ── Monthly Spend (berdasarkan plan) ───────────────
        lo, hi = PLAN_SPEND[plan]
        monthly_spend = round(np.random.uniform(lo, hi), -3)  # kelipatan 1000

        # ── Rating Rata-rata (1–5) ─────────────────────────
        # Distribusi condong ke positif (realisme)
        avg_rating = round(np.random.beta(a=5, b=2) * 4 + 1, 1)
        avg_rating = float(np.clip(avg_rating, 1.0, 5.0))

        # ── Support Tickets ────────────────────────────────
        # Mayoritas pelanggan tidak komplain
        support_tickets = int(np.random.choice(
            [0, 1, 2, 3, 4, 5],
            p=[0.45, 0.28, 0.14, 0.07, 0.04, 0.02]
        ))

        # ── Pernah Pakai Promo? ────────────────────────────
        promo_used = bool(np.random.choice([True, False], p=[0.38, 0.62]))

        # ── Tenure (sementara, belum final) ───────────────
        max_possible_tenure = (END_DATE - join_date).days // 30
        max_possible_tenure = max(max_possible_tenure, 1)

        # ── Hitung Churn Probability ───────────────────────
        # Estimasi tenure awal untuk kalkulasi prob
        est_tenure = min(max_possible_tenure, np.random.randint(1, max_possible_tenure + 1))
        churn_prob = calculate_churn_probability(
            plan, est_tenure, avg_rating, support_tickets, promo_used
        )
        churn = int(np.random.random() < churn_prob)

        # ── Last Active Date ───────────────────────────────
        if churn == 1:
            # Pelanggan churn: last active antara join + 1 bulan s/d join + est_tenure bulan
            churn_after_days = np.random.randint(30, max(31, est_tenure * 30))
            last_active_date = join_date + timedelta(days=int(churn_after_days))
            last_active_date = min(last_active_date, END_DATE)
        else:
            # Pelanggan aktif: last active mendekati END_DATE
            days_back = np.random.randint(0, 30)
            last_active_date = END_DATE - timedelta(days=days_back)

        # ── Tenure Final (bulan) ───────────────────────────
        tenure_months = max(1, (last_active_date - join_date).days // 30)

        # ── Total Orders ───────────────────────────────────
        # Pelanggan aktif lebih banyak order
        base_orders_per_month = {'Basic': 1.0, 'Standard': 1.5, 'Premium': 2.2}
        avg_orders = base_orders_per_month[plan] * tenure_months
        total_orders = max(1, int(np.random.poisson(avg_orders)))

        # ── Simpan Record ──────────────────────────────────
        records.append({
            'customer_id'     : customer_id,
            'join_date'       : join_date.strftime('%Y-%m-%d'),
            'last_active_date': last_active_date.strftime('%Y-%m-%d'),
            'subscription_plan': plan,
            'city'            : city,
            'monthly_spend'   : int(monthly_spend),
            'total_orders'    : total_orders,
            'tenure_months'   : tenure_months,
            'avg_rating'      : avg_rating,
            'support_tickets' : support_tickets,
            'promo_used'      : promo_used,
            'churn'           : churn,
        })

        # Progress bar sederhana
        if (i + 1) % 1000 == 0:
            print(f"  ✓ {i+1:,} / {n:,} records generated...")

    df = pd.DataFrame(records)
    return df


# ════════════════════════════════════════════════════════════
#  VALIDASI & RINGKASAN
# ════════════════════════════════════════════════════════════

def print_summary(df: pd.DataFrame):
    print(f"\n{'='*55}")
    print("  ✅ DATASET BERHASIL DIBUAT — RINGKASAN")
    print(f"{'='*55}")
    print(f"  Total baris     : {len(df):,}")
    print(f"  Total kolom     : {df.shape[1]}")
    print(f"  Missing values  : {df.isnull().sum().sum()}")
    print(f"  Duplikat        : {df.duplicated().sum()}")

    churn_rate = df['churn'].mean() * 100
    print(f"\n  📊 Churn Rate Keseluruhan: {churn_rate:.1f}%")

    print(f"\n  📦 Distribusi per Plan:")
    plan_churn = df.groupby('subscription_plan')['churn'].agg(['count','mean'])
    plan_churn['mean'] = (plan_churn['mean'] * 100).round(1)
    plan_churn.columns = ['Jumlah', 'Churn Rate (%)']
    print(plan_churn.to_string())

    print(f"\n  🗓️  Rentang Tanggal:")
    print(f"  Join date  : {df['join_date'].min()} → {df['join_date'].max()}")
    print(f"  Tenure     : {df['tenure_months'].min()} – {df['tenure_months'].max()} bulan")
    print(f"  Spend      : Rp {df['monthly_spend'].min():,} – Rp {df['monthly_spend'].max():,}")
    print(f"\n  🏙️  Top 5 Kota:")
    print(df['city'].value_counts().head().to_string())
    print(f"\n{'='*55}\n")


# ════════════════════════════════════════════════════════════
#  MAIN
# ════════════════════════════════════════════════════════════

if __name__ == '__main__':
    # 1. Generate data
    df = generate_dataset(N_CUSTOMERS)

    # 2. Tampilkan ringkasan
    print_summary(df)

    # 3. Simpan ke CSV
    os.makedirs('data', exist_ok=True)
    output_path = 'data/nestbrew_customers_dummy.csv'
    df.to_csv(output_path, index=False)

    print(f"  💾 File disimpan ke: {output_path}")
    print(f"  Ukuran file       : {os.path.getsize(output_path) / 1024:.1f} KB")
    print(f"\n  ✅ Selesai! Buka file CSV untuk memulai EDA.\n")
