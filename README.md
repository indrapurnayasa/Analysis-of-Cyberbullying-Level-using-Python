# Cyberbullying Level Classification in Indonesia Using Twitter Data

This project classifies the level of cyberbullying in Indonesian tweets using specific keywords. The pipeline includes preprocessing raw tweet data, feature extraction, and classification using machine learning. 

---

## 📜 Features
- **Dataset:** Tweets collected using specific Indonesian keywords related to cyberbullying.
- **Preprocessing Steps:**
  - Remove punctuation
  - Convert text to lowercase
  - Tokenization
  - Replace slang words with formal equivalents
- **Database:** Preprocessed data is stored in MongoDB.
- **Classification:** 
  - Feature extraction with **TF-IDF**
  - Classification using **Support Vector Machine (SVM)**
- **Performance:** Achieved an accuracy of **85%** on the classification task.

---

## 🛠️ Technologies Used
- **Programming Language:** Python
- **Libraries and Tools:**
  - Natural Language Toolkit (NLTK) and SpaCy for preprocessing
  - Scikit-learn for TF-IDF and SVM implementation
  - MongoDB for data storage
- **Data Source:** Twitter API

---

## 🧹 Data Preprocessing

The following steps were applied to preprocess the raw tweets:

1. **Remove Punctuation:** Stripped unnecessary symbols to clean the text.
2. **Lowercase Conversion:** Unified case sensitivity.
3. **Tokenization:** Split sentences into individual words.
4. **Slang Replacement:** Converted informal or slang terms into formal equivalents using a predefined dictionary.
5. **Save to MongoDB:** Preprocessed data was saved for further analysis.

---

## 🧠 Classification Process

1. **Feature Extraction:**
   - Used **TF-IDF (Term Frequency-Inverse Document Frequency)** to convert text into numerical vectors for model input.

2. **Model Selection:**
   - Implemented **Support Vector Machine (SVM)** for classification.
   - Tuned hyperparameters to optimize performance.

3. **Performance Metrics:**
   - Achieved an accuracy of **85%** during evaluation on the test set.

---

## 📊 Results and Insights

- **Dataset Analysis:**
  - Keyword-based collection ensured relevant tweet samples.
  - Distribution of cyberbullying levels was balanced after preprocessing.

- **Model Performance:**
  - The SVM classifier performed reliably with the TF-IDF feature representation.
  - Preprocessing significantly improved classification results.

---

## 📄 Paper

This project is part of a research effort. The full findings and methodology are documented in the accompanying paper. [Link to the [paper](https://ojs.unud.ac.id/index.php/merpati/article/view/89313)].
