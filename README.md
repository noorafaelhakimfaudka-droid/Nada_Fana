# Nada Fana | End-to-End Data Science Project: Indie Mellow Music Engine

**Nada Fana** adalah proyek Data Science (End-to-End) yang bertujuan membangun mesin rekomendasi musik berbasis *Unsupervised Machine Learning* dan *Natural Language Processing (NLP)*. Proyek ini membedah hampir 1 juta dataset lagu global dari Spotify, menyaringnya secara cerdas, dan mengisolasi mahakarya *Indie Pop* dan balada naratif Indonesia (seperti karya Hindia, Yura Yunita, Banda Neira, Pamungkas, dll) yang memiliki kedalaman makna dan bernuansa *mellow*.

Berbeda dengan algoritma *streaming* konvensional, proyek ini tidak mengandalkan filter genre eksplisit, melainkan mengekstraksi kecenderungan emosi dari DNA audio dan merekomendasikan lagu berdasarkan tingkat kemiripan matematis dari liriknya.

---

## 🔬 Metodologi Data Science

Proyek ini mencakup seluruh siklus hidup Data Science, mulai dari pemrosesan data mentah hingga *deployment* aplikasi:

### 1. Data Ingestion & Preprocessing
- **Sumber Data:** Dataset mentah berisi 955.000+ baris dari Spotify API (termasuk lirik dan fitur audio).
- **Filtering & Cleansing:** Menyingkirkan *noise* dengan mengekstrak data berdasarkan diksi puitis bahasa Indonesia (RegEx) dan filter *Stopwords*, dilanjutkan dengan normalisasi bahasa menggunakan `langdetect`.
- **Feature Scaling:** Menggunakan `StandardScaler` untuk menyamakan bobot distribusi dari variabel prediktor audio (`valence`, `acousticness`, `energy`, `danceability`).

### 2. Unsupervised Learning (Clustering)
- Karena tidak ada label klasifikasi genre/suasana yang pasti, algoritma **K-Means Clustering** (`n_clusters=5`) digunakan untuk mencari pola tersembunyi.
- **Centroid Analysis:** Mesin berhasil secara dinamis mendeteksi dan mengisolasi klaster "Mellow" (ditandai dengan nilai rata-rata `acousticness` tertinggi dan `energy` serta `valence` terendah).

### 3. Natural Language Processing (NLP)
- **Text Vectorization:** Mengubah struktur teks lirik liris menjadi matriks probabilitas matematis menggunakan **TF-IDF (Term Frequency-Inverse Document Frequency)** dengan filter khusus Stopwords bahasa Indonesia.
- **Similarity Computation:** Menghitung jarak sudut (*angle*) antar lirik menggunakan fungsi **Cosine Similarity**.

### 4. Deployment & Visualisasi
- Hasil pengolahan model (berupa DataFrame yang direduksi menjadi ~234 lagu spesifik dan matriks TF-IDF) disimpan ke dalam bentuk objek biner (`.pkl`) untuk efisiensi RAM.
- **Dashboard Interaktif:** Dibangun menggunakan Streamlit dengan integrasi Plotly (Radar & Scatter Plot) untuk memberikan visualisasi DNA Audio secara langsung kepada pengguna akhir (End-User).

---

## 🛠️ Arsitektur & Tech Stack

- **Data Manipulation:** `pandas`, `numpy`
- **Machine Learning & NLP:** `scikit-learn` (KMeans, StandardScaler, TfidfVectorizer, Cosine Similarity)
- **Data Visualization:** `plotly.express`, `plotly.graph_objects`
- **Text/Regex Processing:** `re`, `langdetect`
- **Frontend / Deployment:** `streamlit`

---

## 🚀 Replikasi Proyek (Lokal)

Untuk mengeksekusi *pipeline* data science dan menjalankan aplikasinya di komputer Anda:

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/USERNAME_ANDA/nada-fana.git
   cd nada-fana
   ```
2. **Install environment Python (Disarankan Python 3.8+):**
   ```bash
   pip install -r requirements.txt
   ```
3. *(Opsional)* **Jalankan Ulang Pipeline Ekstraksi Data:**
   Jika Anda memiliki file dataset raksasanya (`songs_with_attributes_and_lyrics.csv`), Anda dapat bereksperimen dengan model K-Means menggunakan perintah:
   ```bash
   python create_pickles.py
   ```
4. **Jalankan Dashboard Streamlit:**
   ```bash
   python -m streamlit run app.py
   ```
5. Akses dashboard visualisasinya di `http://localhost:8501`.

---

## 📁 Struktur Repository

- `banturek_music_indie.ipynb`: **Jupyter Notebook Utama.** Berisi langkah-langkah EDA (*Exploratory Data Analysis*), eksperimen model K-Means, dan kerangka pemikiran algoritmik.
- `create_pickles.py`: Skrip *ETL (Extract, Transform, Load)* yang mengubah logika di Jupyter Notebook menjadi *data pipeline* yang memproduksi model final.
- `app.py`: Aplikasi sisi klien (Streamlit) dengan desain UI mewah/premium (kustomisasi CSS).
- `database_lagu.pkl` & `memori_ai.pkl`: File hasil kompilasi *machine learning* untuk *deployment* berkecepatan tinggi.

---
*Dikurasi oleh Algoritma, Dinikmati oleh Rasa.*
