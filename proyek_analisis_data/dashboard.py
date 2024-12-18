# dashboard sepeda

# import library yang dibutuhkan
import pandas as pd
import matplotlib.pyplot as plt
import seaborn as sns
import streamlit as st

# Import data
@st.cache_data
def load_data():
    data = pd.read_csv('proyek_analisis_data/data.csv') 
    data['dteday'] = pd.to_datetime(data['dteday'])
    data['month'] = data['dteday'].dt.strftime('%Y-%m') 
    weather_mapping = {1: 'Clear', 2: 'Cloudy', 3: 'Light Snow, Light Rain', 4: 'Heavy Rain'}
    data['weather_desc'] = data['weathersit'].map(weather_mapping)  # Mapping cuaca
    return data

# Clustering 
def cluster_usage(data):
    bins = [0, 2000, 4000, data['cnt'].max()]
    labels = ['Rendah', 'Sedang', 'Tinggi']
    data['cnt_cluster'] = pd.cut(data['cnt'], bins=bins, labels=labels)
    return data

def add_annotations(bars):
    for bar in bars:
        height = bar.get_height()
        plt.annotate(f'{int(height)}',
                     xy=(bar.get_x() + bar.get_width() / 2, height),
                     xytext=(0, 5), textcoords='offset points',
                     ha='center', va='bottom', fontsize=10)

# Anotasi line chart
def add_min_max_annotations(ax, x, y):
    min_idx = y.idxmin()
    max_idx = y.idxmax()
    
    # Min
    ax.annotate(f"Min: {y[min_idx]}",
                xy=(x[min_idx], y[min_idx]),
                xytext=(0, -20), textcoords='offset points',
                ha='center', color='red', fontsize=9)
    
    # Max
    ax.annotate(f"Max: {y[max_idx]}",
                xy=(x[max_idx], y[max_idx]),
                xytext=(0, 10), textcoords='offset points',
                ha='center', color='green', fontsize=9)

# Filter data bedasarkan rentang waktu
def filter_data_by_date(data, start_date, end_date):
    start_date = pd.to_datetime(start_date)  
    end_date = pd.to_datetime(end_date)      
    mask = (data['dteday'] >= start_date) & (data['dteday'] <= end_date)
    return data[mask]

# Main Function
def main():
    st.title("📊 Dashboard Analisis Penggunaan Sepeda 🚲")
    st.sidebar.title("Menu Navigasi")

    # Load Data
    data = load_data()
    data = cluster_usage(data)

    # Sidebar Filter Rentang Waktu
    st.sidebar.subheader("Filter Rentang Waktu")
    start_date = st.sidebar.date_input("Tanggal Mulai", data['dteday'].min())
    end_date = st.sidebar.date_input("Tanggal Selesai", data['dteday'].max())

    if start_date > end_date:
        st.sidebar.error("Tanggal Mulai harus lebih awal dari Tanggal Selesai.")
    else:
        filtered_data = filter_data_by_date(data, start_date, end_date)

    # Sidebar Menu Navigasi
    menu = ["Home", "Tren Penggunaan Sepeda", "Pengaruh Cuaca", "Analisis Musim", "Clustering"]
    choice = st.sidebar.selectbox("Pilih Analisis", menu)

    # Home Section
    if choice == "Home":
        st.subheader("Selamat Datang di Dashboard Analisis Penggunaan Sepeda")
        st.write("Berikut adalah gambaran umum dari dataset yang digunakan:")
         # KPI Ringkasan Data
        total_days = len(filtered_data)
        avg_daily_usage = filtered_data['cnt'].mean()
        total_usage = filtered_data['cnt'].sum()
        
        col1, col2, col3 = st.columns(3)
        col1.metric("Total Hari Terfilter", total_days)
        col2.metric("Rata-Rata Penggunaan per Hari", f"{avg_daily_usage:.0f}")
        col3.metric("Total Penggunaan Sepeda", f"{total_usage:.0f}")

        st.write(filtered_data.head())

    # Tren Penggunaan Sepeda
    elif choice == "Tren Penggunaan Sepeda":
        st.subheader("📈 Tren Penggunaan Sepeda di Hari Kerja vs Hari Libur")

        # KPI
        total_workday = filtered_data[filtered_data['workingday'] == 1]['cnt'].sum()
        total_weekend = filtered_data[filtered_data['workingday'] == 0]['cnt'].sum()

        col1, col2 = st.columns(2)
        col1.metric("Total Penggunaan di Hari Kerja", f"{total_workday:.0f}")
        col2.metric("Total Penggunaan di Hari Libur", f"{total_weekend:.0f}")

        monthly_analysis = filtered_data.groupby(['month', 'workingday'])['cnt'].sum().reset_index()
        monthly_analysis['workingday'] = monthly_analysis['workingday'].map({0: 'Hari Libur', 1: 'Hari Kerja'})

        plt.figure(figsize=(12, 6))
        ax = sns.lineplot(data=monthly_analysis, x='month', y='cnt', hue='workingday', marker='o', palette='Set1')
        
        for workday in ['Hari Libur', 'Hari Kerja']:
            subset = monthly_analysis[monthly_analysis['workingday'] == workday]
            add_min_max_annotations(ax, subset['month'], subset['cnt'])

        plt.xticks(rotation=45)
        plt.title("Pola Penggunaan Sepeda di Hari Kerja vs Hari Libur")
        plt.xlabel("Bulan")
        plt.ylabel("Jumlah Penggunaan Sepeda")
        plt.legend(title="Kategori Hari")
        st.pyplot(plt)

    # Analisis Musim
    elif choice == "Analisis Musim":
        st.subheader("🌤 Rata-rata dan Distribusi Penggunaan Sepeda Berdasarkan Musim")

        # KPI
        season_avg = filtered_data.groupby('season')['cnt'].mean()
        season_max = season_avg.idxmax()
        season_min = season_avg.idxmin()

        col1, col2 = st.columns(2)
        col1.metric("Musim dengan Rata-Rata Tertinggi", f"{season_max}: {season_avg[season_max]:.0f}")
        col2.metric("Musim dengan Rata-Rata Terendah", f"{season_min}: {season_avg[season_min]:.0f}")

        # Rata-rata penggunaan sepeda per musim
        st.write("### Rata-rata Penggunaan Sepeda per Musim")
        season_avg = filtered_data.groupby('season')['cnt'].mean().reset_index()
        plt.figure(figsize=(10, 6))
        bars = sns.barplot(x='season', y='cnt', data=season_avg, palette='viridis', hue='season', legend=False)

        # Tambahkan anotasi nilai di atas bar
        for bar in bars.patches:
            height = bar.get_height()
            plt.text(bar.get_x() + bar.get_width() / 2, height, f'{int(height)}',
                    ha='center', va='bottom', fontsize=10)

        plt.title("Rata-Rata Penggunaan Sepeda Berdasarkan Musim")
        plt.xlabel("Musim (Season)")
        plt.ylabel("Rata-Rata Jumlah Penggunaan Sepeda")
        plt.xticks(ticks=[0, 1, 2, 3], labels=["Spring", "Summer", "Fall", "Winter"])
        st.pyplot(plt)

        # Distribusi penggunaan sepeda per musim
        st.write("### Distribusi Penggunaan Sepeda Sepanjang Tahun")
        plt.figure(figsize=(12, 6))
        boxplot = sns.boxplot(x='season', y='cnt', data=filtered_data, palette='viridis', hue='season', legend=False)

        # Anotasi max dan min
        season_max = filtered_data.groupby('season')['cnt'].max()
        season_min = filtered_data.groupby('season')['cnt'].min()
        for i, (max_val, min_val) in enumerate(zip(season_max, season_min)):
            plt.text(i, max_val, f'Max: {int(max_val)}', color='green', ha='center', va='bottom', fontsize=10)
            plt.text(i, min_val, f'Min: {int(min_val)}', color='red', ha='center', va='top', fontsize=10)

        plt.title("Distribusi Penggunaan Sepeda Berdasarkan Musim")
        plt.xlabel("Musim (Season)")
        plt.ylabel("Jumlah Penggunaan Sepeda")
        plt.xticks(ticks=[0, 1, 2, 3], labels=["Spring", "Summer", "Fall", "Winter"])
        st.pyplot(plt)

    # Pengaruh Cuaca
    elif choice == "Pengaruh Cuaca":
        st.subheader("🌦 Pengaruh Cuaca terhadap Penggunaan Sepeda")

        # KPI
        weather_avg = filtered_data.groupby('weather_desc')['cnt'].mean().reset_index()
        max_weather = weather_avg.loc[weather_avg['cnt'].idxmax()]
        min_weather = weather_avg.loc[weather_avg['cnt'].idxmin()]

        col1, col2 = st.columns(2)
        col1.metric("Cuaca dengan Penggunaan Tertinggi", f"{max_weather['weather_desc']}: {max_weather['cnt']:.0f}")
        col2.metric("Cuaca dengan Penggunaan Terendah", f"{min_weather['weather_desc']}: {min_weather['cnt']:.0f}")

        # Agregasi data
        weather_analysis = filtered_data.groupby('weather_desc')[['casual', 'registered']].mean().reset_index()

        # X position
        x = range(len(weather_analysis))
        width = 0.35  # Lebar bar

        # Plot diagram
        plt.figure(figsize=(10, 6))
        bars1 = plt.bar([i - width/2 for i in x], weather_analysis['casual'], width=width, label='Casual', color='orange')
        bars2 = plt.bar([i + width/2 for i in x], weather_analysis['registered'], width=width, label='Registered', color='blue')

        # Anotasi
        for bars in [bars1, bars2]:
            for bar in bars:
                height = bar.get_height()
                plt.annotate(f'{int(height)}',
                            xy=(bar.get_x() + bar.get_width() / 2, height),
                            xytext=(0, 5), textcoords='offset points',
                            ha='center', va='bottom', fontsize=10)

        # Konfigurasi diagram
        plt.title("Pengaruh Cuaca terhadap Pengguna Sepeda")
        plt.xlabel("Cuaca")
        plt.ylabel("Rata-rata Jumlah Pengguna")
        plt.xticks(ticks=x, labels=weather_analysis['weather_desc'])
        plt.legend()
        st.pyplot(plt)

    # Clustering
    elif choice == "Clustering":
        st.subheader("🔍 Clustering Penggunaan Sepeda")

        # KPI
        cluster_counts = filtered_data['cnt_cluster'].value_counts()
        col1, col2, col3 = st.columns(3)
        col1.metric("Cluster Rendah", f"{cluster_counts.get('Rendah', 0)} Hari")
        col2.metric("Cluster Sedang", f"{cluster_counts.get('Sedang', 0)} Hari")
        col3.metric("Cluster Tinggi", f"{cluster_counts.get('Tinggi', 0)} Hari")

        cluster_counts = filtered_data['cnt_cluster'].value_counts()
        plt.figure(figsize=(10, 6))
        colors = sns.color_palette('viridis', len(cluster_counts))

        bars = plt.bar(cluster_counts.index, cluster_counts.values, color=colors)
        add_annotations(bars)

        plt.title("Distribusi Penggunaan Sepeda Berdasarkan Cluster")
        plt.xlabel("Cluster Penggunaan Sepeda")
        plt.ylabel("Jumlah Hari")
        st.pyplot(plt)

# run main function
if __name__ == '__main__':
    main()
