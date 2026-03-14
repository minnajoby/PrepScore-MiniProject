# PrepScore - AI-Powered Profile Evaluator & Career Assistant

PrepScore is a modern, AI-driven platform designed to help professionals and students optimize their career profiles. By combining Machine Learning scoring with Large Language Model (LLM) analysis, it provides a deep, actionable view of how your experience matches up against target industry roles.

![PrepScore Overview](https://img.shields.io/badge/Status-Complete-success)
![UI Style](https://img.shields.io/badge/Design-Glassmorphism-blue)
![Backend](https://img.shields.io/badge/Backend-Django-092e20)
![AI](https://img.shields.io/badge/AI-Gemini%20%7C%20Groq-8e44ad)

---

## ✨ Key Features

- **🏆 Live PrepScore Calculation:** Uses a trained **Random Forest (RandomForestRegressor)** ML model to analyze your profile completeness and quality, giving you a score from 0 to 100.
- **🤖 AI Gap Analysis:** Paste any Job Description and get a detailed semantic match report using **Google Gemini** and **Groq (Llama-3)**. It reveals missing keywords and generates custom interview questions.
- **📄 Resume Intelligence:** Upload your PDF resume; the system automatically extracts text via `PyMuPDF` and generates vector embeddings to find hidden professional insights.
- **📊 Interactive Dashboard:** A beautiful, responsive "glassmorphic" interface featuring:
  - Points Distribution charts (Chart.js).
  - Score History tracking over time.
  - Priority Actionable Recommendations for profile improvement.
- **🛠 Profile Management:** Dedicated modules for Technical Projects, Skills, Professional Certifications, Education, and Work Experience.

---

## 🛠 Tech Stack

- **Framework:** Django 5.2.4
- **Database:** PostgreSQL (with `pgvector` support)
- **Machine Learning:** Scikit-learn, Pandas, Joblib
- **AI Services:** Google Generative AI (Gemini), Groq API
- **Frontend:** HTML5, CSS3 (Vanilla + Glassmorphism), Bootstrap 5, Chart.js, Bootstrap Icons
- **PDF Processing:** PyMuPDF (Fitz)

---

## 🚀 Getting Started

### Prerequisites

- Python 3.10+
- PostgreSQL
- API Keys for Google Gemini and Groq

### Installation & Setup

1. **Clone the Repository:**
   ```bash
   git clone https://github.com/minnajoby/PrepScore.git
   cd PrepScore
   ```

2. **Create a Virtual Environment:**
   ```bash
   python -m venv venv
   source venv/bin/activate  # On Windows: venv\Scripts\activate
   ```

3. **Install Dependencies:**
   ```bash
   pip install -r requirements.txt
   ```

4. **Environment Variables:**
   Create a `.env` file in the root directory and add the following:
   ```env
   SECRET_KEY=your_django_secret_key
   DEBUG=True
   ALLOWED_HOSTS=*
   DB_PASSWORD=your_postgres_password
   GEMINI_API_KEY=your_google_ai_key
   GROQ_API_KEY=your_groq_api_key
   ```

5. **Database Setup:**
   Ensure you have a PostgreSQL database named `prepscore_db`.
   ```bash
   python manage.py makemigrations
   python manage.py migrate
   ```

6. **Training the ML Model (Optional):**
   If you want to re-train the scoring engine with fresh data:
   ```bash
   python scripts/train_model.py
   ```

7. **Run the Server:**
   ```bash
   python manage.py runserver
   ```
   Access the app at `http://127.0.0.1:8000/`.

---

## 🤝 Contributing

This is a personal mini-project, but feedback and suggestions are always welcome!

---

## 📄 License

This project is licensed under the MIT License - see the LICENSE file for details.
