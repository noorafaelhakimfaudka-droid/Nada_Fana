# 🎵 Nada Fana | Musik Indie Mellow

**Nada Fana** adalah mesin rekomendasi (Recommendation Engine) berbasis kecerdasan buatan yang berfokus khusus pada kurasi musik **Indie Pop, Akustik, dan Balada Naratif Indonesia**. 

Berbeda dengan algoritma *streaming* konvensional yang menyamaratakan seluruh genre musik, Nada Fana membedah kedalaman emosi, melodi instrumen, dan makna dari lirik puitis (seperti lagu-lagu Hindia, Yura Yunita, Pamungkas, Banda Neira) untuk memberikan rekomendasi musik *mellow* yang paling akurat dengan suasana hati Anda.

---

## ✨ Fitur Utama

- **🧠 Hibrida ML + NLP:** Menggunakan *K-Means Clustering* untuk mengisolasi klaster audio dengan energi rendah dan akustik tinggi (musik *mellow*).
- **📝 Analisis Diksi (TF-IDF):** Menggunakan Natural Language Processing (NLP) untuk menganalisis dan menghitung kemiripan puitis antar lirik lagu dengan *Cosine Similarity*.
- **📊 DNA Audio Visual:** Menyajikan pembedahan DNA audio (Valence, Acousticness, Energy, Danceability, Tempo) secara langsung dengan visualisasi Radar dan Scatter plot yang mewah.
- **💎 UI/UX Mewah:** Antarmuka bergaya premium (Obsidian & Gold) yang elegan dengan tipografi modern untuk pengalaman penjelajahan yang mendalam.

## 🛠️ Arsitektur Teknologi

- **Backend:** Python
- **Machine Learning:** Scikit-Learn (K-Means, TF-IDF, StandardScaler, Cosine Similarity)
- **Frontend / UI:** Streamlit (dengan Custom CSS injection)
- **Visualisasi Data:** Plotly Express & Plotly Graph Objects
- **Text Processing:** Regular Expressions & LangDetect

## 🚀 Cara Menjalankan Secara Lokal

1. Pastikan Anda memiliki Python 3.8 atau lebih baru.
2. *Clone* repository ini:
   ```bash
   git clone https://github.com/USERNAME_ANDA/nada-fana.git
   cd nada-fana
   ```
3. Install dependensi (disarankan menggunakan virtual environment):
   ```bash
   pip install -r requirements.txt
   ```
4. Jalankan aplikasi Streamlit:
   ```bash
   python -m streamlit run app.py
   ```
5. Akses aplikasi melalui browser di `http://localhost:8501`.

## 📁 Struktur Folder

- `app.py`: File utama aplikasi antarmuka Streamlit.
- `create_pickles.py`: Skrip ETL & Pipeline Machine Learning untuk membuat klaster dan matriks teks (tidak untuk dijalankan di server produksi).
- `database_lagu.pkl`: Database *DataFrame* lagu-lagu Indie Mellow yang telah diekstrak.
- `memori_ai.pkl`: Matriks embedding (TF-IDF) untuk kalkulasi kemiripan lirik secara instan.
- `requirements.txt`: Daftar pustaka (library) yang dibutuhkan aplikasi.

---
*Diciptakan dengan ❤️ untuk para penikmat lirik sendu.*
