"""Prediksi satu kalimat — CLI. Ganti detectionCyberbullying.py lama.

Usage: python predict.py "kata-kata lu kasar banget bego"
"""

import pickle
from pathlib import Path

from indo_text_preprocessing import IndoPreprocessor

MODEL_DIR = Path("models")
TARGETS = ["HS", "HS_Weak", "HS_Moderate", "HS_Strong", "HS_Level"]
LABELS = {
    "HS": {0: "non-cyberbullying", 1: "cyberbullying"},
    "HS_Weak": {0: "bukan weak", 1: "weak"},
    "HS_Moderate": {0: "bukan moderate", 1: "moderate"},
    "HS_Strong": {0: "bukan strong", 1: "strong"},
    "HS_Level": {0: "non-cyberbullying", 1: "weak", 2: "moderate", 3: "strong"},
}

pre = IndoPreprocessor()


def classify(text: str, target: str) -> str:
    with open(MODEL_DIR / f"model_{target}.pkl", "rb") as f:
        m = pickle.load(f)
    pred = m["clf"].predict(m["vectorizer"].transform([pre.preprocess(text)]))[0]
    return LABELS[target].get(pred, str(pred))


if __name__ == "__main__":
    import sys

    text = " ".join(sys.argv[1:]) or input("Kalimat yang akan diprediksi: ")
    print("Preprocessed :", pre.preprocess(text))
    for t in TARGETS:
        try:
            print(f"{t:12s}:", classify(text, t))
        except FileNotFoundError:
            print(f"{t:12s}: (model belum ditrain — jalankan train.py)")