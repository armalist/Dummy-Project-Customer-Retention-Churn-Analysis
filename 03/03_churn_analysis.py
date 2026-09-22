"""
=============================================================
 NestBrew Co. — Churn Analysis Mendalam & Rekomendasi Bisnis
 [DUMMY PROJECT] — Data fiktif untuk keperluan portofolio
=============================================================
 Author  : Ariqah Maulia Listiani
 Date    : September 2026
 Notebook: 03_churn_analysis
=============================================================
"""

import pandas as pd
import numpy as np
import matplotlib.pyplot as plt
import matplotlib.patches as mpatches
import matplotlib.gridspec as gridspec
import seaborn as sns
import warnings
warnings.filterwarnings('ignore')

plt.rcParams['figure.dpi']        = 130
plt.rcParams['font.family']       = 'sans-serif'
plt.rcParams['axes.spines.top']   = False
plt.rcParams['axes.spines.right'] = False

C_CHURN  = '#EF5350'
C_RETAIN = '#42A5F5'
C_ACCENT = '#FFA726'
C_DARK   = '#1A237E'

# ════════════════════════════════════════════════════════════
# LOAD DATA BERSIH
# ════════════════════════════════════════════════════════════
df = pd.read_csv('data/nestbrew_customers_clean.csv',
                 parse_dates=['join_date', 'last_active_date'])

df['tenure_group'] = pd.Categorical(
    df['tenure_group'],
    categories=['0–3 bln', '4–6 bln', '7–12 bln', '>12 bln'],
    ordered=True
)
df['rating_group'] = pd.Categorical(
    df['rating_group'],
    categories=['Rendah (≤2.5)', 'Sedang (2.6–3.5)', 'Tinggi (>3.5)'],
    ordered=True
)

print(f"✅ Data loaded: {df.shape[0]:,} baris, {df.shape[1]} kolom")
print(f"   Churn rate keseluruhan: {df['churn'].mean()*100:.1f}%\n")


# ════════════════════════════════════════════════════════════
# BAGIAN 1 — CUSTOMER PROFILING: CHURN vs RETAIN
# ════════════════════════════════════════════════════════════
print("=" * 55)
print("  BAGIAN 1 — PROFIL PELANGGAN: CHURN vs RETAIN")
print("=" * 55)

profile = df.groupby('churn_label').agg(
    jumlah            =('churn', 'count'),
    tenure_rata       =('tenure_months', 'mean'),
    spend_rata        =('monthly_spend', 'mean'),
    orders_rata       =('total_orders', 'mean'),
    rating_rata       =('avg_rating', 'mean'),
    tickets_rata      =('support_tickets', 'mean'),
    pct_promo         =('promo_used', 'mean'),
).round(2)
profile['pct_promo'] = (profile['pct_promo'] * 100).round(1)
print("\n📊 Rata-rata per Segmen:")
print(profile.T.to_string())

# Visualisasi Profil — Radar / Bar Comparison
metrics = {
    'Tenure\n(bulan)'       : ('tenure_months', 1),
    'Monthly\nSpend (rb)'   : ('monthly_spend', 1000),
    'Total\nOrders'         : ('total_orders', 1),
    'Avg\nRating'           : ('avg_rating', 1),
    'Support\nTickets'      : ('support_tickets', 1),
}

retain_vals = []
churn_vals  = []
labels      = list(metrics.keys())

for label, (col, divisor) in metrics.items():
    retain_vals.append(df[df['churn_label']=='Retain'][col].mean() / divisor)
    churn_vals.append(df[df['churn_label']=='Churn'][col].mean()  / divisor)

x     = np.arange(len(labels))
width = 0.35

fig, ax = plt.subplots(figsize=(12, 5))
b1 = ax.bar(x - width/2, retain_vals, width, label='Retain', color=C_RETAIN,
            edgecolor='white', linewidth=1.2)
b2 = ax.bar(x + width/2, churn_vals,  width, label='Churn',  color=C_CHURN,
            edgecolor='white', linewidth=1.2)

for bar in b1:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9, color=C_RETAIN, fontweight='bold')
for bar in b2:
    ax.text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.2,
            f'{bar.get_height():.1f}', ha='center', va='bottom', fontsize=9, color=C_CHURN, fontweight='bold')

ax.set_xticks(x)
ax.set_xticklabels(labels, fontsize=10)
ax.set_title('Perbandingan Profil: Pelanggan Retain vs Churn',
             fontsize=13, fontweight='bold', pad=15)
ax.legend(fontsize=11)
ax.set_ylabel('Nilai Rata-rata')

plt.tight_layout()
plt.savefig('data/viz_07_customer_profile.png', bbox_inches='tight')
plt.show()

print("\n📌 INSIGHT PROFIL:")
print(f"  • Pelanggan Churn rata-rata hanya bertahan {churn_vals[0]:.0f} bulan")
print(f"    vs Retain yang bertahan {retain_vals[0]:.0f} bulan")
print(f"  • Pelanggan Churn punya support tickets {churn_vals[4]:.1f} vs Retain {retain_vals[4]:.1f}")
print(f"  • Rating rata-rata Churn: {churn_vals[3]:.2f} vs Retain: {retain_vals[3]:.2f}")


# ════════════════════════════════════════════════════════════
# BAGIAN 2 — TREN CHURN PER BULAN
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  BAGIAN 2 — TREN CHURN BULANAN")
print("=" * 55)

churned_df = df[df['churn'] == 1].copy()
churned_df['churn_ym'] = churned_df['last_active_date'].dt.to_period('M')

monthly_churn = churned_df.groupby('churn_ym').size().reset_index(name='churn_count')
monthly_churn['churn_ym_str'] = monthly_churn['churn_ym'].astype(str)

# Hanya tampilkan data mulai ada volume cukup
monthly_churn = monthly_churn[monthly_churn['churn_ym'] >= '2023-03']

fig, ax = plt.subplots(figsize=(13, 5))
ax.fill_between(range(len(monthly_churn)), monthly_churn['churn_count'],
                color=C_CHURN, alpha=0.15)
ax.plot(range(len(monthly_churn)), monthly_churn['churn_count'],
        color=C_CHURN, linewidth=2.5, marker='o', markersize=5)

# Annotasi puncak
peak_idx = monthly_churn['churn_count'].idxmax()
peak_val = monthly_churn.loc[peak_idx, 'churn_count']
peak_lbl = monthly_churn.loc[peak_idx, 'churn_ym_str']
peak_pos = monthly_churn.index.get_loc(peak_idx)
ax.annotate(f'Puncak: {peak_val} churn\n({peak_lbl})',
            xy=(peak_pos, peak_val),
            xytext=(peak_pos - 3, peak_val + 8),
            fontsize=9, color=C_CHURN, fontweight='bold',
            arrowprops=dict(arrowstyle='->', color=C_CHURN, lw=1.5))

# Rolling average
rolling = monthly_churn['churn_count'].rolling(3, center=True).mean()
ax.plot(range(len(monthly_churn)), rolling, color='gray',
        linewidth=1.5, linestyle='--', label='3-bulan moving avg')

step = max(1, len(monthly_churn) // 10)
ax.set_xticks(range(0, len(monthly_churn), step))
ax.set_xticklabels(monthly_churn['churn_ym_str'].iloc[::step],
                   rotation=35, ha='right', fontsize=8)
ax.set_title('Tren Jumlah Churn per Bulan — NestBrew Co.',
             fontsize=13, fontweight='bold', pad=15)
ax.set_ylabel('Jumlah Pelanggan Churn')
ax.set_xlabel('')
ax.legend()

plt.tight_layout()
plt.savefig('data/viz_08_monthly_churn_trend.png', bbox_inches='tight')
plt.show()


# ════════════════════════════════════════════════════════════
# BAGIAN 3 — ANALISIS SUPPORT TICKETS vs CHURN
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  BAGIAN 3 — SUPPORT TICKETS vs CHURN")
print("=" * 55)

ticket_stats = df.groupby('support_tickets').agg(
    total   =('churn', 'count'),
    churned =('churn', 'sum')
).reset_index()
ticket_stats['churn_rate'] = (ticket_stats['churned'] / ticket_stats['total'] * 100).round(1)

fig, axes = plt.subplots(1, 2, figsize=(12, 5))
fig.suptitle('Dampak Support Tickets terhadap Churn', fontsize=13, fontweight='bold')

# Bar churn rate
colors = [C_RETAIN if r < df['churn'].mean()*100 else C_CHURN
          for r in ticket_stats['churn_rate']]
bars = axes[0].bar(ticket_stats['support_tickets'], ticket_stats['churn_rate'],
                   color=colors, edgecolor='white', width=0.65)
for bar, rate in zip(bars, ticket_stats['churn_rate']):
    axes[0].text(bar.get_x() + bar.get_width()/2, bar.get_height() + 0.5,
                 f'{rate}%', ha='center', va='bottom', fontsize=10, fontweight='bold')
axes[0].axhline(df['churn'].mean()*100, color='gray', linestyle='--',
                linewidth=1.5, label=f"Avg: {df['churn'].mean()*100:.1f}%")
axes[0].set_title('Churn Rate per Jumlah Tiket')
axes[0].set_xlabel('Jumlah Support Tickets')
axes[0].set_ylabel('Churn Rate (%)')
axes[0].legend()

# Distribusi jumlah tiket
ticket_dist = df['support_tickets'].value_counts().sort_index()
axes[1].bar(ticket_dist.index, ticket_dist.values, color=C_ACCENT,
            edgecolor='white', width=0.65)
for i, (idx, val) in enumerate(ticket_dist.items()):
    axes[1].text(idx, val + 15, f'{val:,}', ha='center', va='bottom', fontsize=9)
axes[1].set_title('Distribusi Jumlah Tiket (Semua Pelanggan)')
axes[1].set_xlabel('Jumlah Support Tickets')
axes[1].set_ylabel('Jumlah Pelanggan')

plt.tight_layout()
plt.savefig('data/viz_09_tickets_vs_churn.png', bbox_inches='tight')
plt.show()

high_ticket_churn = ticket_stats[ticket_stats['support_tickets'] >= 3]['churn_rate'].mean()
print(f"\n📌 INSIGHT: Pelanggan dengan ≥3 tiket → churn rate rata-rata {high_ticket_churn:.1f}%")
print(f"   vs overall average {df['churn'].mean()*100:.1f}%")


# ════════════════════════════════════════════════════════════
# BAGIAN 4 — SEGMEN RISIKO TINGGI (Plan × Tenure)
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  BAGIAN 4 — PETA RISIKO: Plan × Tenure")
print("=" * 55)

pivot = df.groupby(['subscription_plan', 'tenure_group'], observed=True)['churn'].mean() * 100
pivot = pivot.reset_index()
pivot.columns = ['Plan', 'Tenure Group', 'Churn Rate']
pivot_table = pivot.pivot(index='Plan', columns='Tenure Group', values='Churn Rate')

fig, ax = plt.subplots(figsize=(10, 4))
sns.heatmap(pivot_table, annot=True, fmt='.1f', cmap='RdYlGn_r',
            linewidths=0.5, linecolor='white', ax=ax,
            cbar_kws={'label': 'Churn Rate (%)', 'shrink': 0.8},
            annot_kws={'size': 12, 'weight': 'bold'})
ax.set_title('Peta Risiko Churn: Subscription Plan × Tenure\n(% = churn rate per kombinasi segmen)',
             fontsize=12, fontweight='bold', pad=15)
ax.set_xlabel('Kelompok Lama Berlangganan', fontsize=10)
ax.set_ylabel('Subscription Plan', fontsize=10)
plt.tight_layout()
plt.savefig('data/viz_10_risk_heatmap_plan_tenure.png', bbox_inches='tight')
plt.show()

worst = pivot.loc[pivot['Churn Rate'].idxmax()]
print(f"\n📌 KOMBINASI PALING BERISIKO:")
print(f"   Plan '{worst['Plan']}' + Tenure '{worst['Tenure Group']}'"
      f" → Churn Rate {worst['Churn Rate']:.1f}%")


# ════════════════════════════════════════════════════════════
# BAGIAN 5 — DASHBOARD RINGKASAN (1 gambar, 4 panel)
# ════════════════════════════════════════════════════════════
fig = plt.figure(figsize=(16, 10))
fig.patch.set_facecolor('#F8F9FA')
gs = gridspec.GridSpec(2, 3, figure=fig, hspace=0.45, wspace=0.35)

# ── Panel A: KPI tiles ─────────────────────────────────────
ax_kpi = fig.add_subplot(gs[0, 0])
ax_kpi.axis('off')
kpis = [
    ('Total Pelanggan', f"{len(df):,}", C_DARK),
    ('Churn Rate',      f"{df['churn'].mean()*100:.1f}%", C_CHURN),
    ('Pelanggan Churn', f"{df['churn'].sum():,}", C_CHURN),
    ('Avg Tenure Retain', f"{df[df['churn']==0]['tenure_months'].mean():.0f} bln", C_RETAIN),
]
for i, (label, val, color) in enumerate(kpis):
    y = 0.85 - i * 0.22
    ax_kpi.add_patch(mpatches.FancyBboxPatch(
        (0.05, y - 0.06), 0.9, 0.18,
        boxstyle='round,pad=0.02',
        facecolor=color, alpha=0.1, edgecolor=color, linewidth=1.5,
        transform=ax_kpi.transAxes
    ))
    ax_kpi.text(0.5, y + 0.05, val, ha='center', va='center',
                fontsize=16, fontweight='bold', color=color,
                transform=ax_kpi.transAxes)
    ax_kpi.text(0.5, y - 0.02, label, ha='center', va='center',
                fontsize=8, color='gray', transform=ax_kpi.transAxes)
ax_kpi.set_title('Key Metrics', fontsize=11, fontweight='bold', pad=10)

# ── Panel B: Churn per Plan ────────────────────────────────
ax_plan = fig.add_subplot(gs[0, 1])
plan_cr = df.groupby('subscription_plan')['churn'].mean() * 100
plan_cr = plan_cr.sort_values(ascending=True)
colors_plan = ['#66BB6A' if v < df['churn'].mean()*100 else '#EF5350'
               for v in plan_cr.values]
ax_plan.barh(plan_cr.index, plan_cr.values, color=colors_plan,
             height=0.5, edgecolor='white')
for y_pos, val in enumerate(plan_cr.values):
    ax_plan.text(val + 0.3, y_pos, f'{val:.1f}%', va='center',
                 fontsize=10, fontweight='bold')
ax_plan.axvline(df['churn'].mean()*100, color='gray', linestyle='--', linewidth=1)
ax_plan.set_title('Churn per Plan', fontsize=11, fontweight='bold')
ax_plan.set_xlabel('Churn Rate (%)')
ax_plan.set_xlim(0, max(plan_cr.values) * 1.3)

# ── Panel C: Churn per Tenure ──────────────────────────────
ax_ten = fig.add_subplot(gs[0, 2])
ten_cr = df.groupby('tenure_group', observed=True)['churn'].mean() * 100
bar_colors = ['#EF5350', '#FF8A65', '#FFA726', '#66BB6A']
ax_ten.bar(ten_cr.index.astype(str), ten_cr.values,
           color=bar_colors, width=0.55, edgecolor='white')
for i, val in enumerate(ten_cr.values):
    ax_ten.text(i, val + 0.5, f'{val:.1f}%', ha='center',
                va='bottom', fontsize=9, fontweight='bold')
ax_ten.axhline(df['churn'].mean()*100, color='gray', linestyle='--', linewidth=1)
ax_ten.set_title('Churn per Tenure', fontsize=11, fontweight='bold')
ax_ten.set_ylabel('Churn Rate (%)')
ax_ten.tick_params(axis='x', labelsize=8)

# ── Panel D: Tren Bulanan (spanning 2 cols) ────────────────
ax_trend = fig.add_subplot(gs[1, :2])
ax_trend.fill_between(range(len(monthly_churn)), monthly_churn['churn_count'],
                      color=C_CHURN, alpha=0.12)
ax_trend.plot(range(len(monthly_churn)), monthly_churn['churn_count'],
              color=C_CHURN, linewidth=2, marker='o', markersize=4)
rolling2 = monthly_churn['churn_count'].rolling(3, center=True).mean()
ax_trend.plot(range(len(monthly_churn)), rolling2,
              color='gray', linewidth=1.5, linestyle='--', label='3-bln avg')
step2 = max(1, len(monthly_churn) // 8)
ax_trend.set_xticks(range(0, len(monthly_churn), step2))
ax_trend.set_xticklabels(monthly_churn['churn_ym_str'].iloc[::step2],
                         rotation=30, ha='right', fontsize=8)
ax_trend.set_title('Tren Churn Bulanan', fontsize=11, fontweight='bold')
ax_trend.set_ylabel('Jumlah Churn')
ax_trend.legend(fontsize=9)

# ── Panel E: Top Churn Drivers ─────────────────────────────
ax_driver = fig.add_subplot(gs[1, 2])
ax_driver.axis('off')
drivers = [
    ('🥇', 'Tenure Pendek', 'Korelasi -0.57 dengan churn'),
    ('🥈', 'Banyak Komplain', '≥3 tiket → churn 2× lebih tinggi'),
    ('🥉', 'Plan Basic', 'Churn rate 28.8% vs avg 23.7%'),
    ('4️⃣',  'Rating Rendah', '≤2.5 → churn rate jauh lebih tinggi'),
]
ax_driver.text(0.5, 0.97, 'Top Churn Drivers', ha='center', va='top',
               fontsize=11, fontweight='bold', transform=ax_driver.transAxes)
for i, (rank, title, desc) in enumerate(drivers):
    y = 0.82 - i * 0.21
    ax_driver.text(0.05, y, f'{rank} {title}', fontsize=10, fontweight='bold',
                   transform=ax_driver.transAxes, color=C_DARK)
    ax_driver.text(0.05, y - 0.08, desc, fontsize=8, color='gray',
                   transform=ax_driver.transAxes)

fig.suptitle('NestBrew Co. — Customer Churn Analysis Dashboard\n[DUMMY PROJECT]',
             fontsize=15, fontweight='bold', color=C_DARK, y=1.01)

plt.savefig('data/viz_11_summary_dashboard.png', bbox_inches='tight',
            facecolor=fig.get_facecolor())
plt.show()
print("📊 Summary dashboard tersimpan!")


# ════════════════════════════════════════════════════════════
# BAGIAN 6 — REKOMENDASI BISNIS
# ════════════════════════════════════════════════════════════
print("\n" + "=" * 55)
print("  BAGIAN 6 — REKOMENDASI BISNIS UNTUK CMO NESTBREW")
print("=" * 55)

recommendations = """
┌─────────────────────────────────────────────────────┐
│        REKOMENDASI STRATEGIS — NESTBREW CO.          │
│             Berdasarkan Analisis Churn               │
└─────────────────────────────────────────────────────┘

🎯 PRIORITAS 1 — Early Onboarding Program (Impact: TINGGI)
   Temuan : Pelanggan tenure 0–3 bulan punya churn rate tertinggi
   Aksi   : Buat program 90-hari pertama: welcome email series,
             loyalty reward di bulan ke-2, check-in personal dari tim CS
   Target : Turunkan churn segment ini sebesar 30%

🎯 PRIORITAS 2 — Proactive CS Follow-Up (Impact: TINGGI)
   Temuan : Pelanggan dengan ≥3 tiket komplain churn 2× lebih sering
   Aksi   : Auto-trigger follow-up call CS setelah tiket ke-2 masuk.
             Tawarkan solusi SEBELUM pelanggan frustrasi
   Target : Kurangi high-ticket churn rate dari 40%+ menjadi <25%

🎯 PRIORITAS 3 — Plan Upgrade Campaign (Impact: MENENGAH)
   Temuan : Plan Basic churn rate 28.8% vs Premium 15.4%
   Aksi   : Berikan trial gratis fitur Standard selama 1 bulan
             kepada pengguna Basic di bulan ke-3 berlangganan
   Target : Dorong 15% pengguna Basic naik ke Standard

🎯 PRIORITAS 4 — Rating Recovery Campaign (Impact: MENENGAH)
   Temuan : Rata-rata rating pelanggan Churn = lebih rendah
   Aksi   : Kirim survei ke pelanggan rating ≤3.0, tawarkan
             penggantian produk atau diskon bulan berikutnya
   Target : Tingkatkan avg rating keseluruhan ke ≥4.0

📌 ESTIMASI DAMPAK GABUNGAN:
   Jika keempat rekomendasi dijalankan dalam 6 bulan,
   proyeksi penurunan churn rate: dari 23.7% → ~14-16%
   (setara mempertahankan ~400-500 pelanggan lebih)
"""
print(recommendations)


# ════════════════════════════════════════════════════════════
# RINGKASAN AKHIR
# ════════════════════════════════════════════════════════════
print("=" * 55)
print("  ✅ ANALISIS SELESAI — RINGKASAN FILE OUTPUT")
print("=" * 55)
outputs = [
    "viz_07_customer_profile.png",
    "viz_08_monthly_churn_trend.png",
    "viz_09_tickets_vs_churn.png",
    "viz_10_risk_heatmap_plan_tenure.png",
    "viz_11_summary_dashboard.png",
]
for f in outputs:
    print(f"  📊 data/{f}")
print("""
  📋 Semua visualisasi siap digunakan untuk:
     • Screenshot di README.md GitHub
     • Slide presentasi ke 'CMO NestBrew'
     • Upload ke Tableau / Looker Studio sebagai referensi
""")
