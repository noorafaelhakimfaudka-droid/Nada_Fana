import pandas as pd
import pickle
import re
from langdetect import detect
from sklearn.feature_extraction.text import TfidfVectorizer
from sklearn.preprocessing import StandardScaler
from sklearn.cluster import KMeans

print("1. Memuat dataset spotify (menggunakan chunk agar hemat RAM)...")
kolom_target = ['id', 'name', 'artists', 'lyrics', 'valence', 'acousticness', 'energy', 'danceability']
target_artis = 'hindia|sal priadi|feby putri|pamungkas|bernadya|ardhito|danilla|kunto aji|banda neira|payung teduh|fourtwnty'
target_kata = r'\b(mengapa|kembali|seperti|semua|menjadi|pernah|waktu|cinta|rindu|fana|sendu)\b'

df_list = []
chunksize = 50000

for chunk in pd.read_csv('songs_with_attributes_and_lyrics.csv', chunksize=chunksize, usecols=lambda c: c in kolom_target + ['tempo']):
    df_valid = chunk.dropna(subset=['lyrics'])
    
    kondisi_artis = df_valid['artists'].str.contains(target_artis, case=False, na=False)
    kondisi_lirik = df_valid['lyrics'].str.contains(target_kata, case=False, na=False, regex=True)
    
    df_filter = df_valid[kondisi_artis | kondisi_lirik]
    df_list.append(df_filter)

df_filter_indo = pd.concat(df_list, ignore_index=True)
print(f"Total lagu terjaring: {df_filter_indo.shape[0]}")

jumlah_sampel = min(100000, df_filter_indo.shape[0])
df_clean = df_filter_indo.sample(n=jumlah_sampel, random_state=42).copy()
df_clean.reset_index(drop=True, inplace=True)

print("3. K-Means Clustering...")
fitur_audio = df_clean[['valence', 'acousticness', 'energy', 'danceability']]
scaler = StandardScaler()
audio_scaled = scaler.fit_transform(fitur_audio)

kmeans = KMeans(n_clusters=5, random_state=42, n_init=10)
df_clean['klaster_vibes'] = kmeans.fit_predict(audio_scaled)

# Mendeteksi klaster Mellow secara dinamis
# Klaster mellow memiliki ciri: acousticness tinggi, energy rendah, valence rendah.
hasil_klaster = df_clean.groupby('klaster_vibes')[['valence', 'acousticness', 'energy', 'danceability']].mean()
skor_mellow = hasil_klaster['acousticness'] - hasil_klaster['energy'] - hasil_klaster['valence']
klaster_mellow = skor_mellow.idxmax()

print(f"Klaster Mellow terdeteksi sebagai klaster {klaster_mellow}")

# Mengisolasi klaster Mellow
df_mellow = df_clean[df_clean['klaster_vibes'] == klaster_mellow].copy()
df_mellow.reset_index(drop=True, inplace=True)
print(f"Total lagu mellow: {df_mellow.shape[0]}")

print("4. Deteksi Bahasa Indonesia...")
def deteksi_bahasa(teks):
    try:
        return detect(str(teks))
    except:
        return "unknown"

df_mellow['bahasa'] = df_mellow['lyrics'].apply(deteksi_bahasa)
df_indo = df_mellow[df_mellow['bahasa'] == 'id'].copy()
df_indo.reset_index(drop=True, inplace=True)

def bersihkan_teks(teks):
    teks = str(teks).lower() 
    teks = re.sub(r'\[.*?\]|\(.*?\)', '', teks) 
    teks = re.sub(r'[^a-z\s]', '', teks) 
    return teks

df_indo['lirik_bersih'] = df_indo['lyrics'].apply(bersihkan_teks)
print(f"Total Lagu Mellow Indonesia: {df_indo.shape[0]}")

print("5. TF-IDF & Cosine Similarity...")
stopword_indo = ['dan', 'di', 'ke', 'dari', 'yang', 'ini', 'itu', 'untuk', 'pada', 'dengan', 'adalah', 'aku', 'kamu', 'dia', 'mereka', 'kita', 'kami', 'yg', 'nya']
tfidf = TfidfVectorizer(max_features=5000, stop_words=stopword_indo)
matriks_indo = tfidf.fit_transform(df_indo['lirik_bersih'])

print("6. Menyimpan ke pickle...")
pickle.dump(df_indo, open('database_lagu.pkl', 'wb'))
pickle.dump(matriks_indo, open('memori_ai.pkl', 'wb'))
print("Selesai! Database lagu dan TF-IDF embeddings (matriks_indo) telah diperbarui sesuai notebook.")
