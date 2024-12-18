import streamlit as st
import numpy as np
import networkx as nx
import matplotlib.pyplot as plt
from io import BytesIO

# Fungsi untuk menghitung jarak Euclidean antara dua titik
def euclidean_distance(p1, p2):
    return np.sqrt((p1[0] - p2[0]) ** 2 + (p1[1] - p2[1]) ** 2)

# Membuat matriks jarak untuk semua titik
def create_distance_matrix(locations):
    num_locations = len(locations)
    distance_matrix = np.zeros((num_locations, num_locations))
    for i in range(num_locations):
        for j in range(num_locations):
            if i != j:
                distance_matrix[i, j] = euclidean_distance(locations[i], locations[j])
    return distance_matrix

# Algoritma Nearest Neighbor untuk menemukan siklus rute perjalanan
def nearest_neighbor_path(distance_matrix):
    n = len(distance_matrix)
    visited = [False] * n
    path = [0]  # Mulai dari titik 0
    visited[0] = True
    
    for _ in range(n - 1):
        last = path[-1]
        next_city = np.argmin([distance_matrix[last][j] if not visited[j] else np.inf for j in range(n)])
        path.append(next_city)
        visited[next_city] = True
    
    path.append(0)  # Kembali ke titik awal
    return path

# Fungsi untuk memvisualisasikan graf
def visualize_route(locations, optimal_path):
    G = nx.DiGraph()

    # Menambahkan simpul (nodes)
    for i, (x, y) in enumerate(locations):
        G.add_node(i, pos=(x, y))

    # Menambahkan jalur (edges) sesuai rute
    for i in range(len(optimal_path) - 1):
        G.add_edge(optimal_path[i], optimal_path[i+1])

    # Menggambar graf
    pos = nx.get_node_attributes(G, 'pos')
    fig, ax = plt.subplots(figsize=(10, 8))
    nx.draw(G, pos, with_labels=True, node_color='lightblue', font_weight='bold', node_size=700, ax=ax)
    nx.draw_networkx_edges(G, pos, edgelist=[(optimal_path[i], optimal_path[i+1]) for i in range(len(optimal_path) - 1)], edge_color='blue', width=2, arrows=True)

    return fig

# Streamlit App
st.title("Dashboard Rute Optimal untuk Pengiriman Logistik")

# Input: Pilihan pengguna
input_method = st.radio("Pilih metode input lokasi:", ["Masukkan lokasi manual", "Buat lokasi secara otomatis"])

# Input Lokasi
if input_method == "Masukkan lokasi manual":
    num_locations = st.number_input("Berapa jumlah lokasi yang ingin Anda masukkan?", min_value=2, step=1, value=4)
    locations = []
    for i in range(int(num_locations)):
        x = st.number_input(f"Masukkan koordinat X untuk lokasi ke-{i+1}:", value=float(10 * (i + 1)))
        y = st.number_input(f"Masukkan koordinat Y untuk lokasi ke-{i+1}:", value=float(20 * (i + 1)))
        locations.append((x, y))
    locations = np.array(locations)
else:
    num_locations = st.number_input("Berapa jumlah lokasi yang ingin dihasilkan?", min_value=2, step=1, value=5)
    np.random.seed(42)  # Untuk hasil yang konsisten
    locations = np.random.rand(int(num_locations), 2) * 100

# Menampilkan lokasi
st.write("Koordinat lokasi:")
st.write(locations)

# Membuat matriks jarak dan rute optimal
distance_matrix = create_distance_matrix(locations)
optimal_path = nearest_neighbor_path(distance_matrix)

# Menampilkan rute optimal
st.write("Rute Optimal (berdasarkan siklus):", optimal_path)

# Visualisasi graf
fig = visualize_route(locations, optimal_path)
st.pyplot(fig)

# Unduh gambar graf
buffer = BytesIO()
fig.savefig(buffer, format="png")
buffer.seek(0)
st.download_button("Unduh Visualisasi Rute", data=buffer, file_name="rute_optimal.png", mime="image/png")
