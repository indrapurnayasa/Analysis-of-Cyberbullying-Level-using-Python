"""Preprocess dataset re_dataset.csv — pakai indo-text-preprocessing.

Ganti testCleansing.py lama (NLTK + Sastrawi + eval() slang dict).
Input : data/re_dataset.csv (Tweet, HS, ...)
Output: data/preprocessed.csv (text_clean, HS, HS_Weak/Moderate/Strong)
"""

from indo_text_preprocessing import IndoPreprocessor
import pandas as pd

# ponytail: stem semua tweet (~13k) serial ~5 detik; multiprocessing tak perlu.
p = IndoPreprocessor(replace_slang=True, remove_stopwords=True, stem=True)

df = pd.read_csv("data/re_dataset.csv", encoding="latin-1")
df = df.dropna(subset=["Tweet"]).drop_duplicates(subset=["Tweet"])

df["text"] = df["Tweet"].apply(p.preprocess)
# buang tweet jadi kosong setelah preprocessing (stopword/stem habis)
df = df[df["text"].str.strip() != ""]

df[["text", "HS", "Abusive", "HS_Weak", "HS_Moderate", "HS_Strong"]].to_csv(
    "data/preprocessed.csv", index=False
)
print(f"preprocessed {len(df)} tweets -> data/preprocessed.csv")