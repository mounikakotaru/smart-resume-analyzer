# 📄 Smart Resume Analyzer using Python & Streamlit

[![Python 3.9](https://img.shields.io/badge/Python-3.9-blue.svg)](https://www.python.org/downloads/release/python-390/)
[![Streamlit](https://img.shields.io/badge/Framework-Streamlit-orange.svg)](https://streamlit.io/)
[![License](https://img.shields.io/badge/License-MIT-green.svg)](LICENSE)

## 🚀 Project Overview

**Smart Resume Analyzer** is an AI-powered web app that analyzes resumes (PDF format), extracts relevant information, evaluates resume quality, recommends improvements, and provides course suggestions and video tips — all in real time.

This app is built using:
- 🔍 **Natural Language Processing (NLP)** for information extraction
- 🎨 **Streamlit** for frontend UI
- 🧠 **PyResparser**, **spaCy**, **NLTK**, **PDFMiner**, and more

---

## ✅ Features

- 📥 Upload PDF Resume and get it analyzed instantly.
- 📊 Resume Score based on best practices (Objective, Projects, Achievements, etc.)
- 🧠 Extracted details:
  - Name
  - Email
  - Phone number
  - Number of pages
  - Skills (auto-detected)
- 🎯 Career field prediction (DS, Web Dev, Android, UI/UX, iOS)
- 🧾 Personalized course recommendations (Coursera, Udemy, etc.)
- 💡 Resume improvement suggestions
- 📺 YouTube videos for Resume + Interview tips
- 📈 Pie charts showing resume category & experience (if admin dashboard used)
- 🔒 Admin & user section (optional)
- 📤 Resume PDF viewer built-in

---

## 🛠 Tech Stack

- **Frontend:** Streamlit
- **Backend:** Python
- **Libraries:**
  - `PyMuPDF`, `pdfminer3`, `pyresparser`, `nltk`, `spacy`, `plotly`, `pymysql` *(optional)*, `youtube_dl`, `pafy`, `streamlit_tags`

---

## 📦 Installation

### 1. Clone the Repository
```bash
git clone https://github.com/mounikakotaru/smart-resume-analyzer.git
cd smart-resume-analyzer

** ### 2.Create and Activate Virtual Environment: 

```bash
python -m venv venv
venv\Scripts\activate  # On Windows


** ### 3. Install Requirements:

pip install -r requirements.txt
python -m nltk.downloader stopwords
python -m spacy download en_core_web_sm


** ### 4.Run the App:

streamlit run App.py


