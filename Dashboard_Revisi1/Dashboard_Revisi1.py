#--- Mengimpor modul yang diperlukan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Mengatur gaya visual seaborn
sns.set(style='dark')

#--- Mendefinisikan fungsi untuk analisis data
def analisis_rental_musim(df):  # Fungsi untuk menganalisis data berdasarkan "season"
    rental_per_season = df.groupby(by="season").cnt.nunique().reset_index()
    rental_per_season.rename(columns={"cnt": "jumlah_pelanggan"}, inplace=True)
    return rental_per_season

def analisis_berdasarkan_cuaca(df):  # Fungsi untuk menganalisis data berdasarkan "weathersit"
    cuaca_analisis = df.groupby(by="weathersit").agg({
        "instant": "nunique",
        "cnt": "sum"
    }).reset_index()
    return cuaca_analisis

#--- Memuat data dari file CSV
day_df = pd.read_csv(r"Dashboard_Revisi1\day_data.csv")

#--- Menggunakan fungsi untuk menghasilkan analisis
favorit_season = analisis_rental_musim(day_df)
favorit_cuaca = analisis_berdasarkan_cuaca(day_df)

#--- Menampilkan judul Dashboard
st.header('Dashboard Penyewaan Sepeda :bicyclist::star2:')
st.subheader("Statistik :1234:")

#--- Membuat panel samping (sidebar)
with st.sidebar:
    st.subheader("Latar Belakang")
    st.write(
        """
        Sistem penyewaan sepeda adalah generasi baru dari penyewaan sepeda tradisional di mana seluruh proses, mulai dari pendaftaran anggota, penyewaan, hingga pengembalian, telah menjadi otomatis. 
        Dengan sistem ini, pengguna dapat dengan mudah menyewa sepeda dari lokasi tertentu dan mengembalikannya di lokasi lain. Saat ini, terdapat sekitar 500 program penyewaan sepeda di seluruh dunia, 
        yang terdiri dari lebih dari 500 ribu sepeda. Saat ini, terdapat minat yang besar terhadap sistem ini karena peran pentingnya dalam isu lalu lintas, lingkungan, dan kesehatan.

        Selain aplikasi dunia nyata yang menarik dari sistem penyewaan sepeda, karakteristik data yang dihasilkan oleh sistem ini menjadikannya menarik untuk penelitian. 
        Berbeda dengan layanan transportasi lain seperti bus atau kereta bawah tanah, durasi perjalanan, waktu keberangkatan, dan lokasi kedatangan tercatat dengan jelas dalam sistem ini. 
        Fitur ini mengubah sistem penyewaan sepeda menjadi jaringan sensor virtual yang dapat digunakan untuk mendeteksi mobilitas di kota. 
        Oleh karena itu, diharapkan bahwa sebagian besar peristiwa penting di kota dapat terdeteksi melalui pemantauan data ini.
        """
    )

#--- Menampilkan kolom untuk statistik penyewaan
col1, col2, col3 = st.columns(3)

#--- Kolom untuk total penyewaan
with col1:
    total_rental = day_df['cnt'].sum()
    st.metric("Total Penyewaan", value=total_rental)

#--- Kolom untuk penyewaan pelanggan yang terdaftar
with col2:
    rental_member = day_df['registered'].sum()
    st.metric("Penyewaan Anggota", value=rental_member)

#--- Kolom untuk penyewaan pelanggan non-terdaftar
with col3:
    rental_casual = day_df['casual'].sum()
    st.metric("Penyewaan Non-Anggota", value=rental_casual)

#--- Grafik penyewaan berdasarkan musim
st.subheader("Musim Favorit Pelanggan :sunny: :cloud:")
fig, ax = plt.subplots(figsize=(20, 10))

colors_ = ["#FFFF00", "#FFA500", "#FF0000", "#D3D3D3"]

sns.barplot(
    y="jumlah_pelanggan",
    x="season",
    data=favorit_season.sort_values(by="jumlah_pelanggan", ascending=False),
    palette=colors_,
    ax=ax
)
ax.set_title("Jumlah Pelanggan berdasarkan Musim", loc="center", fontsize=15)
ax.set_ylabel(None)
ax.set_xlabel(None)
ax.tick_params(axis='x', labelsize=12)
st.pyplot(fig)

st.subheader("Deskripsi")
st.write(
    """
    1: Musim Semi
    2: Musim Panas
    3: Musim Gugur
    4: Musim Dingin 
    """
)

#--- Grafik penyewaan casual dan registered
st.subheader("Pola Penyewaan Sepeda Pengguna Casual dan Registered")
fig, ax = plt.subplots(figsize=(10, 6))
sns.lineplot(data=day_df, x='dteday', y='casual', label='Casual')
sns.lineplot(data=day_df, x='dteday', y='registered', label='Registered')
plt.title('Pola Penyewaan Sepeda Pengguna Casual dan Registered')
plt.legend()
st.pyplot(fig)

#--- Grafik penyewaan berdasarkan cuaca
st.subheader("Pengaruh Cuaca Terhadap Penyewaan Sepeda :cloud::sun_with_face:")
cuaca_counts = favorit_cuaca[['weathersit', 'cnt']]

fig, ax = plt.subplots(figsize=(10, 6))
sns.barplot(data=cuaca_counts, x='weathersit', y='cnt', palette='coolwarm', ax=ax)
ax.set_title('Jumlah Penyewaan Berdasarkan Cuaca', fontsize=15)
ax.set_ylabel('Jumlah Penyewaan', fontsize=12)
ax.set_xlabel('Jenis Cuaca', fontsize=12)
st.pyplot(fig)

#--- Scatter Plot Suhu vs Penyewaan
st.subheader("Pengaruh Suhu terhadap Penyewaan Sepeda :thermometer:")
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='temp', y='cnt', data=day_df, ax=ax)
sns.regplot(x='temp', y='cnt', data=day_df, scatter=False, color='red')
plt.title('Pengaruh Suhu terhadap Jumlah Penyewaan Sepeda', fontsize=15)
plt.xlabel('Suhu (normalisasi)', fontsize=12)
plt.ylabel('Jumlah Penyewaan', fontsize=12)
st.pyplot(fig)

#--- RFM Analysis Visualization
st.subheader("Analisis RFM Pelanggan :bar_chart:")
# Menghitung RFM
snapshot_date = day_df['dteday'].max() + pd.Timedelta(days=1)  # tanggal snapshot
rfm_df = day_df.groupby('user_id').agg({
    'dteday': lambda x: (snapshot_date - x.max()).days,
    'cnt': ['count', 'sum']
}).reset_index()
rfm_df.columns = ['user_id', 'Recency', 'Frequency', 'Monetary']

# Mengelompokkan pelanggan berdasarkan RFM
def rfm_segment(df):
    if df['Recency'] <= 30 and df['Frequency'] > 10:
        return 'Best Customers'
    elif df['Recency'] <= 30 and df['Frequency'] <= 10:
        return 'Loyal Customers'
    elif df['Recency'] > 30 and df['Frequency'] > 10:
        return 'Potential Customers'
    else:
        return 'At Risk'

rfm_df['Segment'] = rfm_df.apply(rfm_segment, axis=1)

# Barplot untuk Jumlah Pelanggan di Setiap Segmen RFM
fig, ax = plt.subplots(figsize=(10, 6))
segment_counts = rfm_df['Segment'].value_counts().reset_index()
segment_counts.columns = ['Segment', 'Count']
sns.barplot(x='Segment', y='Count', data=segment_counts, palette='viridis')
plt.title('Jumlah Pelanggan di Setiap Segmen RFM', fontsize=15)
plt.xlabel('Segmen', fontsize=12)
plt.ylabel('Jumlah Pelanggan', fontsize=12)
plt.xticks(rotation=45)
st.pyplot(fig)

# Scatter Plot untuk Frequency dan Monetary
fig, ax = plt.subplots(figsize=(10, 6))
sns.scatterplot(x='Frequency', y='Monetary', data=rfm_df, hue='Segment', palette='viridis')
plt.title('Frekuensi dan Nilai Penyewaan berdasarkan Segmen RFM', fontsize=15)
plt.xlabel('Frekuensi Penyewaan', fontsize=12)
plt.ylabel('Nilai Penyewaan', fontsize=12)
st.pyplot(fig)