# Nada Fana | End-to-End Data Science Project: Indie Mellow Music Engine

> **💡 Catatan Penulis (Transparency Note):** 
> Fokus utama saya dalam proyek ini adalah pada tahap **riset Data Science, Exploratory Data Analysis (EDA), dan perancangan pemodelan Machine Learning & NLP** yang seluruhnya dikerjakan di dalam file `banturek_music_indie.ipynb`. 
> 
> Adapun aplikasi antarmuka (Streamlit UI) yang berada di file `app.py` didesain dan diimplementasikan dengan bantuan AI Assistant (Gemini) sebagai *Proof of Concept* untuk mendemonstrasikan hasil model secara visual dan interaktif.

**Nada Fana** adalah proyek Data Science yang bertujuan membangun mesin rekomendasi musik berbasis *Unsupervised Machine Learning* dan *Natural Language Processing (NLP)*. Proyek ini membedah hampir 1 juta dataset lagu global dari Spotify, menyaringnya secara cerdas, dan mengisolasi mahakarya *Indie Pop* dan balada naratif Indonesia (seperti karya Hindia, Yura Yunita, Banda Neira, Pamungkas, dll) yang memiliki kedalaman makna dan bernuansa *mellow*.

Berbeda dengan algoritma *streaming* konvensional, proyek ini tidak mengandalkan filter genre eksplisit, melainkan mengekstraksi kecenderungan emosi dari DNA audio dan merekomendasikan lagu berdasarkan tingkat kemiripan matematis dari liriknya.

---

## 🔬 Fokus Utama: Metodologi Data Science (Jupyter Notebook)

Seluruh logika pemikiran, eksperimen, dan *data wrangling* dapat ditemukan di dalam `banturek_music_indie.ipynb`. Tahapan metodologinya meliputi:

### 1. Data Ingestion & Preprocessing
- **Sumber Data:** Dataset mentah berisi 955.000+ baris dari Spotify API (termasuk lirik dan fitur audio).
- **Filtering & Cleansing:** Menyingkirkan *noise* dengan mengekstrak data berdasarkan diksi puitis bahasa Indonesia (RegEx) dan filter *Stopwords*, dilanjutkan dengan normalisasi bahasa menggunakan `langdetect`.
- **Feature Scaling:** Menggunakan `StandardScaler` untuk menyamakan bobot distribusi dari variabel prediktor audio (`valence`, `acousticness`, `energy`, `danceability`).

### 2. Unsupervised Learning (Clustering)
- Karena tidak ada label klasifikasi genre/suasana yang pasti, algoritma **K-Means Clustering** (`n_clusters=5`) digunakan untuk mencari pola tersembunyi.
- **Centroid Analysis:** Eksperimen berhasil secara dinamis mendeteksi dan mengisolasi klaster "Mellow" (ditandai dengan nilai rata-rata `acousticness` tertinggi dan `energy` serta `valence` terendah).

### 3. Natural Language Processing (NLP)
- **Text Vectorization:** Mengubah struktur teks lirik liris menjadi matriks probabilitas matematis menggunakan **TF-IDF (Term Frequency-Inverse Document Frequency)** dengan filter khusus Stopwords bahasa Indonesia.
- **Similarity Computation:** Menghitung jarak sudut (*angle*) antar lirik menggunakan fungsi **Cosine Similarity**.

---

## 💻 Hasil Deployment (AI-Assisted App)

Sebagai langkah *deployment*, model algoritma dan matriks TF-IDF diekspor (pickle) ke dalam file `database_lagu.pkl` dan `memori_ai.pkl`. Dibantu oleh AI, hasil ini kemudian dibungkus menjadi sebuah **Dashboard Interaktif Streamlit** yang menyajikan visualisasi Radar dan Scatter Plot untuk end-user.

### Arsitektur & Tech Stack
- **Riset & Pemodelan (Fokus Utama):** `pandas`, `numpy`, `scikit-learn`, `re`, `langdetect`
- **Deployment (AI-Assisted):** `streamlit`, `plotly.express`, `plotly.graph_objects`

---

## 🚀 Replikasi Proyek (Lokal)

Untuk mengeksekusi *pipeline* data science dan menjalankan aplikasinya di komputer Anda:

1. **Clone repository ini:**
   ```bash
   git clone https://github.com/USERNAME_ANDA/nada-fana.git
   cd nada-fana
   ```
2. **Install environment Python:**
   ```bash
   pip install -r requirements.txt
   ```
3. *(Opsional)* **Pelajari Riset Notebook:**
   Buka `banturek_music_indie.ipynb` untuk melihat hasil EDA dan logika di balik pemodelan rekomendasi ini.
4. **Jalankan Dashboard Streamlit:**
   ```bash
   python -m streamlit run app.py
   ```

---
*Dikurasi oleh Algoritma, Dinikmati oleh Rasa.*
