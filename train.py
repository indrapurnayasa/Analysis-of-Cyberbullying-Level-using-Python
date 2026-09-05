"""Train klasifikasi level cyberbullying — TF-IDF + LinearSVC.

Label: HS biner (default) atau HS_Weak/HS_Moderate/HS_Strong multiclass.
Simpan model + vectorizer + metrics ke models/.

Ganti analysisCyberbullying.py + accuracySVM.py lama.
"""

import pickle
from pathlib import Path

import pandas as pd
from sklearn.metrics import classification_report
from sklearn.model_selection import train_test_split
from sklearn.svm import LinearSVC

from indo_text_preprocessing import TfidfVectorizer

MODELS = Path("models")
MODELS.mkdir(exist_ok=True)


def train(target: str = "HS") -> None:
    """target: 'HS' (biner) atau 'HS_Weak'/'HS_Moderate'/'HS_Strong' (biner per level)
    atau 'HS_Level' (multiclass dari 3 kolom level)."""
    df = pd.read_csv("data/preprocessed.csv")
    if target == "HS_Level":
        # multiclass: 0=non, 1=weak, 2=moderate, 3=strong (prioritas strong)
        y = df["HS_Strong"] * 3 + df["HS_Moderate"] * 2 + df["HS_Weak"] * 1
    else:
        y = df[target]

    X_train, X_test, y_train, y_test = train_test_split(
        df["text"], y, test_size=0.2, random_state=42, stratify=y
    )

    vec = TfidfVectorizer()
    X_train_vec = vec.fit_transform(X_train)
    X_test_vec = vec.transform(X_test)

    clf = LinearSVC()
    clf.fit(X_train_vec, y_train)
    pred = clf.predict(X_test_vec)

    print(f"=== target={target} ===")
    print(classification_report(y_test, pred, zero_division=0))

    with open(MODELS / f"model_{target}.pkl", "wb") as f:
        pickle.dump({"vectorizer": vec, "clf": clf}, f)
    print(f"model -> models/model_{target}.pkl")


if __name__ == "__main__":
    for t in ["HS", "HS_Weak", "HS_Moderate", "HS_Strong", "HS_Level"]:
        train(t)