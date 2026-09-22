"""
=============================================================
 NestBrew Co. — EDA & Data Cleaning
 [DUMMY PROJECT] — Data fiktif untuk keperluan portofolio
=============================================================
 Author  : Ariqah Maulia Listiani
 Date    : September 2026
 Notebook: 02_EDA_cleaning
=============================================================
"""

# ════════════════════════════════════════════════════════════
# CELL 1 — Import Libraries
# ════════════════════════════════════════════════════════════
import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.ticker as mtick
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

# Style global
plt.rcParams['figure.dpi']      = 130
plt.rcParams['font.family']     = 'sans-serif'
plt.rcParams['axes.spines.top'] = False
plt.rcParams['axes.spines.right'] = False

PALETTE_CHURN  = ['#4CAF50', '#F44336']   # hijau=retain, merah=churn
PALETTE_PLAN   = ['#90CAF9', '#42A5F5', '#1565C0']
COLOR_MAIN     = '#1565C0'

print("✅ Libraries loaded.")


# ════════════════════════════════════════════════════════════
# CELL 2 — Load Data
# ════════════════════════════════════════════════════════════
df = pd.read_csv('data/nestbrew_customers_dummy.csv',
                 parse_dates=['join_date', 'last_active_date'])

print(f"Shape  : {df.shape}")
print(f"Columns: {list(df.columns)}")
print()
print(df.head())


# ════════════════════════════════════════════════════════════
# CELL 3 — Basic Info
# ════════════════════════════════════════════════════════════
print("=" * 55)
print("  INFORMASI DASAR DATASET")
print("=" * 55)
print(df.info())


# ════════════════════════════════════════════════════════════
# CELL 4 — Statistik Deskriptif
# ════════════════════════════════════════════════════════════
print("\n📊 STATISTIK DESKRIPTIF — Kolom Numerik\n")
print(df.describe().round(2).to_string())


# ════════════════════════════════════════════════════════════
# CELL 5 — Cek Data Quality
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  DATA QUALITY CHECK")
print("=" * 55)

print(f"\n🔍 Missing Values:")
missing = df.isnull().sum()
print(missing[missing > 0] if missing.any() else "  ✅ Tidak ada missing values")

print(f"\n🔍 Duplikat:")
dupes = df.duplicated().sum()
print(f"  {'✅ Tidak ada duplikat' if dupes == 0 else f'⚠️  {dupes} duplikat ditemukan'}")

print(f"\n🔍 Nilai Unik per Kolom Kategorikal:")
for col in ['subscription_plan', 'city', 'promo_used']:
    print(f"  {col}: {df[col].unique().tolist()}")

print(f"\n🔍 Range Nilai Numerik:")
checks = {
    'avg_rating'     : (1, 5),
    'support_tickets': (0, 10),
    'monthly_spend'  : (100_000, 800_000),
    'tenure_months'  : (1, 30),
}
for col, (lo, hi) in checks.items():
    out_of_range = ((df[col] < lo) | (df[col] > hi)).sum()
    status = "✅ OK" if out_of_range == 0 else f"⚠️  {out_of_range} nilai di luar range"
    print(f"  {col:20s} [{lo}–{hi}]: {status}")


# ════════════════════════════════════════════════════════════
# CELL 6 — Data Cleaning
# ════════════════════════════════════════════════════════════
df_clean = df.copy()

# Pastikan tipe data benar
df_clean['promo_used']   = df_clean['promo_used'].astype(bool)
df_clean['churn']        = df_clean['churn'].astype(int)

# Tambah kolom bantu untuk analisis
df_clean['join_month']   = df_clean['join_date'].dt.to_period('M')
df_clean['churn_month']  = df_clean['last_active_date'].dt.to_period('M')
df_clean['churn_label']  = df_clean['churn'].map({0: 'Retain', 1: 'Churn'})

# Binning tenure untuk segmentasi
df_clean['tenure_group'] = pd.cut(
    df_clean['tenure_months'],
    bins=[0, 3, 6, 12, 30],
    labels=['0–3 bln', '4–6 bln', '7–12 bln', '>12 bln']
)

# Binning rating
df_clean['rating_group'] = pd.cut(
    df_clean['avg_rating'],
    bins=[0, 2.5, 3.5, 5.0],
    labels=['Rendah (≤2.5)', 'Sedang (2.6–3.5)', 'Tinggi (>3.5)']
)

print(f"✅ Cleaning selesai. Shape akhir: {df_clean.shape}")
print(f"   Kolom baru: join_month, churn_month, churn_label, tenure_group, rating_group")


# ════════════════════════════════════════════════════════════
# CELL 7 — VISUALISASI 1: Distribusi Target (Churn)
# ════════════════════════════════════════════════════════════
fig, axes = plt.subplots(1, 2, figsize=(12, 4))
fig.suptitle('Distribusi Churn — NestBrew Co.', fontsize=14, fontweight='bold', y=1.02)

churn_counts = df_clean['churn_label'].value_counts()
churn_pct    = df_clean['churn'].mean() * 100

# Donut chart
wedges, texts, autotexts = axes[0].pie(
    churn_counts,
    labels=churn_counts.index,
    colors=PALETTE_CHURN[::-1],
    autopct='%1.1f%%',
    startangle=90,
    wedgeprops=dict(width=0.55, edgecolor='white', linewidth=2),
    textprops={'fontsize': 11}
)
for at in autotexts:
    at.set_fontsize(12)
    at.set_fontweight('bold')
axes[0].set_title('Proporsi Churn vs Retain', fontsize=12)
axes[0].text(0, 0, f'{churn_pct:.1f}%\nChurn', ha='center', va='center',
             fontsize=13, fontweight='bold', color='#F44336')

# Bar dengan angka
bars = axes[1].bar(churn_counts.index, churn_counts.values,
                   color=PALETTE_CHURN[::-1], width=0.5, edgecolor='white')
for bar, val in zip(bars, churn_counts.values):
    axes[1].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 30,
                 f'{val:,}', ha='center', va='bottom', fontsize=12, fontweight='bold')
axes[1].set_title('Jumlah Pelanggan', fontsize=12)
axes[1].set_ylabel('Jumlah')
axes[1].set_ylim(0, max(churn_counts.values) * 1.15)

plt.tight_layout()
plt.savefig('data/viz_01_churn_distribution.png', bbox_inches='tight')
plt.show()
print(f"\n📌 INSIGHT: {churn_pct:.1f}% pelanggan churn ({churn_counts['Churn']:,} dari {len(df_clean):,})")


# ════════════════════════════════════════════════════════════
# CELL 8 — VISUALISASI 2: Distribusi Variabel Numerik
# ════════════════════════════════════════════════════════════
num_cols = ['tenure_months', 'monthly_spend', 'total_orders', 'avg_rating', 'support_tickets']

fig, axes = plt.subplots(2, 3, figsize=(15, 8))
fig.suptitle('Distribusi Variabel Numerik (Churn vs Retain)',
             fontsize=14, fontweight='bold')
axes = axes.flatten()

for i, col in enumerate(num_cols):
    for label, color in zip(['Retain', 'Churn'], PALETTE_CHURN):
        subset = df_clean[df_clean['churn_label'] == label][col]
        axes[i].hist(subset, bins=25, alpha=0.6, color=color, label=label, edgecolor='none')
    axes[i].set_title(col.replace('_', ' ').title(), fontsize=11)
    axes[i].set_xlabel('')
    axes[i].set_ylabel('Frekuensi')
    axes[i].legend(fontsize=9)

axes[5].axis('off')
plt.tight_layout()
plt.savefig('data/viz_02_numeric_distributions.png', bbox_inches='tight')
plt.show()
print("📌 INSIGHT: Perhatikan perbedaan distribusi antara Churn dan Retain — ini petunjuk awal!")


# ════════════════════════════════════════════════════════════
# CELL 9 — VISUALISASI 3: Churn Rate per Subscription Plan
# ════════════════════════════════════════════════════════════
plan_stats = df_clean.groupby('subscription_plan').agg(
    total=('churn', 'count'),
    churned=('churn', 'sum')
).reset_index()
plan_stats['churn_rate'] = (plan_stats['churned'] / plan_stats['total'] * 100).round(1)
plan_stats = plan_stats.sort_values('churn_rate', ascending=False)

fig, ax = plt.subplots(figsize=(8, 5))
bars = ax.barh(plan_stats['subscription_plan'], plan_stats['churn_rate'],
               color=PALETTE_PLAN, edgecolor='white', height=0.5)

for bar, rate, total in zip(bars, plan_stats['churn_rate'], plan_stats['total']):
    ax.text(bar.get_width() + 0.3, bar.get_y() + bar.get_height()/2,
            f'{rate}%  (n={total:,})', va='center', fontsize=11, fontweight='bold')

ax.set_title('Churn Rate per Subscription Plan', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Churn Rate (%)')
ax.set_xlim(0, max(plan_stats['churn_rate']) * 1.35)
ax.axvline(df_clean['churn'].mean() * 100, color='gray',
           linestyle='--', linewidth=1.2, label=f"Avg: {df_clean['churn'].mean()*100:.1f}%")
ax.legend()

plt.tight_layout()
plt.savefig('data/viz_03_churn_by_plan.png', bbox_inches='tight')
plt.show()

print("\n📌 INSIGHT:")
for _, row in plan_stats.iterrows():
    arrow = "🔴" if row['churn_rate'] > df_clean['churn'].mean()*100 else "🟢"
    print(f"  {arrow} {row['subscription_plan']:10s}: {row['churn_rate']}% churn rate")


# ════════════════════════════════════════════════════════════
# CELL 10 — VISUALISASI 4: Churn Rate per Tenure Group
# ════════════════════════════════════════════════════════════
tenure_stats = df_clean.groupby('tenure_group', observed=True).agg(
    total=('churn', 'count'),
    churned=('churn', 'sum')
).reset_index()
tenure_stats['churn_rate'] = (tenure_stats['churned'] / tenure_stats['total'] * 100).round(1)

fig, ax = plt.subplots(figsize=(9, 5))
colors = ['#EF5350', '#FF8A65', '#FFA726', '#66BB6A']
bars = ax.bar(tenure_stats['tenure_group'].astype(str), tenure_stats['churn_rate'],
              color=colors, width=0.55, edgecolor='white')

for bar, rate, total in zip(bars, tenure_stats['churn_rate'], tenure_stats['total']):
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.4,
            f'{rate}%\n(n={total:,})', ha='center', va='bottom',
            fontsize=10, fontweight='bold')

ax.set_title('Churn Rate per Lama Berlangganan (Tenure)',
             fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Kelompok Tenure', fontsize=11)
ax.set_ylabel('Churn Rate (%)')
ax.set_ylim(0, max(tenure_stats['churn_rate']) * 1.25)
ax.axhline(df_clean['churn'].mean() * 100, color='gray',
           linestyle='--', linewidth=1.2, label='Overall avg')
ax.legend()

plt.tight_layout()
plt.savefig('data/viz_04_churn_by_tenure.png', bbox_inches='tight')
plt.show()

print("\n📌 INSIGHT: Pelanggan baru (0–3 bulan) punya churn rate tertinggi.")
print("  → Ini adalah masa kritis untuk program retensi!")


# ════════════════════════════════════════════════════════════
# CELL 11 — VISUALISASI 5: Heatmap Korelasi
# ════════════════════════════════════════════════════════════
corr_cols = ['monthly_spend', 'total_orders', 'tenure_months',
             'avg_rating', 'support_tickets', 'churn']
corr_matrix = df_clean[corr_cols].corr()

fig, ax = plt.subplots(figsize=(8, 6))
mask = np.triu(np.ones_like(corr_matrix, dtype=bool))
sns.heatmap(corr_matrix, mask=mask, annot=True, fmt='.2f', ax=ax,
            cmap='RdBu_r', center=0, vmin=-1, vmax=1,
            linewidths=0.5, linecolor='white',
            cbar_kws={'shrink': 0.8})
ax.set_title('Heatmap Korelasi Antar Variabel', fontsize=13, fontweight='bold', pad=15)
plt.tight_layout()
plt.savefig('data/viz_05_correlation_heatmap.png', bbox_inches='tight')
plt.show()

churn_corr = corr_matrix['churn'].drop('churn').sort_values(key=abs, ascending=False)
print("\n📌 KORELASI DENGAN CHURN (diurutkan):")
for col, val in churn_corr.items():
    direction = "⬆️  positif" if val > 0 else "⬇️  negatif"
    print(f"  {col:20s}: {val:+.3f}  ({direction})")


# ════════════════════════════════════════════════════════════
# CELL 12 — VISUALISASI 6: Churn Rate per Kota
# ════════════════════════════════════════════════════════════
city_stats = df_clean.groupby('city').agg(
    total=('churn', 'count'),
    churned=('churn', 'sum')
).reset_index()
city_stats['churn_rate'] = (city_stats['churned'] / city_stats['total'] * 100).round(1)
city_stats = city_stats.sort_values('churn_rate', ascending=True)

fig, ax = plt.subplots(figsize=(9, 6))
colors = ['#EF5350' if r > df_clean['churn'].mean()*100 else '#42A5F5'
          for r in city_stats['churn_rate']]
bars = ax.barh(city_stats['city'], city_stats['churn_rate'],
               color=colors, height=0.6, edgecolor='white')

for bar, rate in zip(bars, city_stats['churn_rate']):
    ax.text(bar.get_width() + 0.2, bar.get_y() + bar.get_height()/2,
            f'{rate}%', va='center', fontsize=10, fontweight='bold')

ax.axvline(df_clean['churn'].mean() * 100, color='gray',
           linestyle='--', linewidth=1.5, label=f"Avg: {df_clean['churn'].mean()*100:.1f}%")
ax.set_title('Churn Rate per Kota', fontsize=13, fontweight='bold', pad=15)
ax.set_xlabel('Churn Rate (%)')
ax.set_xlim(0, max(city_stats['churn_rate']) * 1.2)
ax.legend()
ax.text(0.98, 0.02, '🔴 Di atas rata-rata   🔵 Di bawah rata-rata',
        transform=ax.transAxes, ha='right', fontsize=9, color='gray')

plt.tight_layout()
plt.savefig('data/viz_06_churn_by_city.png', bbox_inches='tight')
plt.show()


# ════════════════════════════════════════════════════════════
# CELL 13 — Simpan Clean Dataset
# ════════════════════════════════════════════════════════════
df_clean.to_csv('data/nestbrew_customers_clean.csv', index=False)

print("\n" + "=" * 55)
print("  ✅ EDA & CLEANING SELESAI")
print("=" * 55)
print(f"""
  📁 File tersimpan:
     • data/nestbrew_customers_clean.csv  ← dataset bersih
     • data/viz_01_churn_distribution.png
     • data/viz_02_numeric_distributions.png
     • data/viz_03_churn_by_plan.png
     • data/viz_04_churn_by_tenure.png
     • data/viz_05_correlation_heatmap.png
     • data/viz_06_churn_by_city.png

  📌 Summary temuan awal:
     • Overall churn rate: {df_clean['churn'].mean()*100:.1f}%
     • Kolom baru: tenure_group, rating_group, churn_label
     • Tidak ada missing values atau duplikat
     • Siap untuk analisis mendalam di notebook 03!
""")
