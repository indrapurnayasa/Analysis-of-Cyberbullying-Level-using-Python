# indo-text-preprocessing showcase: Cyberbullying Level Analysis (ID tweets)

Refactor dari pipeline lama (NLTK + Sastrawi + eval() slang dict) menjadi pipeline
yang memakai library [`indo-text-preprocessing`](https://github.com/indrapurnayasa/indo-text-preprocessing).

## Struktur

```
├── data/re_dataset.csv      # 13.169 tweets ID (CC-BY-NC-SA 4.0, Ibrohim & Budi 2019)
├── preprocess.py            # cleaning + slang + stopwords + stemming
├── train.py                 # TF-IDF + LinearSVC, 5 target label
├── predict.py               # CLI: klasifikasi satu kalimat
├── app.py                   # demo web (Flask): test inference di browser
└── requirements.txt
```

## Hasil (TF-IDF + LinearSVC, test 20%, random_state=42)

| Target | Accuracy | Catatan |
|--------|----------|---------|
| HS (biner) | **82%** | drop-in replacement pipeline lama (85% @ test 10%, tidak stratified) |
| HS_Weak | 81% | |
| HS_Moderate | 88% | |
| HS_Strong | 98% | support kecil (94 kasus) |
| HS_Level (multiclass 4) | 75% | upgrade: level sebenarnya, bukan biner |

## Cara pakai

```bash
pip install -r requirements.txt
python preprocess.py            # 13k tweets ~5 detik
python train.py                 # 5 model
python predict.py "kata lu kasar banget bego"
python app.py                   # demo web → http://127.0.0.1:5000
```

## Dataset

`re_dataset.csv` dari [okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection](https://github.com/okkyibrohim/id-multi-label-hate-speech-and-abusive-language-detection)
(dipakai paper ACL ALW3 2019). 13.169 tweets, label:
- `HS` biner: hate speech (0/1) — drop-in replacement label lama
- `HS_Weak / HS_Moderate / HS_Strong` — level sebenarnya (3.383 / 1.705 / 473)

Lisensi CC-BY-NC-SA 4.0 — riset/publikasi OK dengan sitasi, non-komersial.

## Perbandingan pipeline lama vs baru

| Aspek | Lama | Baru (indo-text-preprocessing) |
|-------|------|-------------------------------|
| Slang dict | `eval(open(...))` — arbitrary code execution risk | corpus 4.534 mapping terkurasi + `mapping=` param |
| Tokenizer | NLTK (heavy dep) | `str.split()` + regex stdlib |
| Stemmer | Sastrawi (~17k kata/s) | stemmer `indo-text-preprocessing` (91k kata/s, 100% output match) |
| Preprocessing | 105 baris tersebar | 1 baris: `IndoPreprocessor().preprocess(text)` |
| Label | biner saja | biner + 3 level + multiclass |
| Model | retrain tiap run, tidak disimpan | disimpan `models/*.pkl` |