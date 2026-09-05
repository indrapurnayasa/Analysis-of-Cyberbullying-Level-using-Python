"""Demo web inference — Flask satu file.

Run: python app.py → http://127.0.0.1:5000
# ponytail: Flask + HTML inline satu file, model pickle per-request lookup.
# FastAPI/GPU batch inference bila butuh throughput tinggi.
"""

import pickle
from pathlib import Path

from flask import Flask, jsonify, request

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

app = Flask(__name__)
pre = IndoPreprocessor()

# ponytail: load semua model sekali di startup (RAM ~beberapa MB).
_models = {}
for t in TARGETS:
    p = MODEL_DIR / f"model_{t}.pkl"
    if p.exists():
        with open(p, "rb") as f:
            _models[t] = pickle.load(f)


PAGE = """<!doctype html>
<html lang="id">
<head>
<meta charset="utf-8">
<meta name="viewport" content="width=device-width, initial-scale=1">
<title>Cyberbullying Level Demo</title>
<style>
  body{font-family:system-ui,sans-serif;max-width:640px;margin:2rem auto;padding:0 1rem;background:#0f172a;color:#e2e8f0}
  h1{font-size:1.3rem} small{color:#94a3b8}
  textarea{width:100%;box-sizing:border-box;padding:.6rem;border-radius:8px;border:1px solid #334155;background:#1e293b;color:inherit;font:inherit}
  button{margin-top:.6rem;padding:.5rem 1.2rem;border:0;border-radius:8px;background:#3b82f6;color:#fff;font:inherit;cursor:pointer}
  .row{display:flex;justify-content:space-between;padding:.5rem .8rem;margin-top:.4rem;background:#1e293b;border-radius:8px}
  .label{color:#94a3b8}
  .pos{color:#f87171;font-weight:600}
  .neg{color:#4ade80}
</style>
</head>
<body>
<h1>Cyberbullying Level Analysis <small>— demo indo-text-preprocessing</small></h1>
<p><small>Teks diproses dengan IndoPreprocessor (clean → slang → stopword → stem), lalu TF-IDF + LinearSVC.</small></p>
<textarea id="text" rows="4" placeholder="Tulis kalimat uji...">kata-kata lu kasar banget bego</textarea>
<button onclick="run()">Prediksi</button>
<pre id="prep" style="color:#94a3b8"></pre>
<div id="out"></div>
<script>
async function run(){
  const r = await fetch('/predict',{method:'POST',headers:{'Content-Type':'application/json'},
    body: JSON.stringify({text: document.getElementById('text').value})});
  const d = await r.json();
  document.getElementById('prep').textContent = 'preprocessed: ' + d.preprocessed;
  document.getElementById('out').innerHTML = Object.entries(d.results).map(([k,v])=>{
    const pos = !/bukan|non/.test(v);
    return `<div class="row"><span class="label">${k}</span><span class="${pos?'pos':'neg'}">${v}</span></div>`;
  }).join('');
}
</script>
</body>
</html>"""


@app.get("/")
def index():
    return PAGE


@app.post("/predict")
def predict():
    text = request.json["text"]
    clean = pre.preprocess(text)
    results = {}
    for t, m in _models.items():
        pred = m["clf"].predict(m["vectorizer"].transform([clean]))[0]
        results[t] = LABELS[t].get(pred, str(pred))
    return jsonify({"preprocessed": clean, "results": results})


if __name__ == "__main__":
    app.run(debug=True)