# 💬 Sentiment Tweet Analysis - MLOps Project

An end-to-end MLOps pipeline for analyzing tweet sentiments (Positive or Negative) using machine learning. This project includes data ingestion, preprocessing, model training, and a Flask-powered web application with a modern custom frontend built using HTML, CSS, and JavaScript.

---

## 🌟 Key Features

* **Binary Sentiment Classification:** Detects whether a tweet is positive or negative.
* **Flask Backend:** Lightweight and efficient Python backend for serving predictions.
* **Custom UI:** Interactive web interface using HTML, CSS, and JavaScript.
* **MongoDB Integration:** Stores and fetches tweet data via MongoDB Atlas.
* **Containerized App:** Docker support ensures consistency across environments.
* **CI/CD Integration:** Automated builds and tests using GitHub Actions.

---

## 🛠️ Tech Stack and Tools

* **Language:** Python
* **ML Libraries:** Scikit-learn, Pandas, Numpy
* **Backend:** Flask
* **Frontend:** HTML, CSS, JavaScript
* **Database:** MongoDB Atlas
* **Containerization:** Docker
* **CI/CD:** GitHub Actions
* **Environment:** Conda

---

## ⚙️ Architecture Overview

This MLOps pipeline includes:

1. **Data Ingestion:** Collects and stores tweets in MongoDB Atlas.
2. **Data Preprocessing:** Cleans, tokenizes, and vectorizes tweet text.
3. **Model Training:** Trains a sentiment classification model on labeled data.
4. **Prediction Pipeline:** Flask app serves predictions through a web form.
5. **Frontend:** A simple and intuitive UI for user interaction.
6. **CI/CD:** GitHub Actions automates testing and Docker builds.

> ❗ Note: This project does not include `model_deployment.py`, `model_pusher.py`, or `model_evaluation.py`.

---

## 📂 Project Structure

```plaintext
tweet-sentiment-mlops/
├── src/
│   ├── pipeline/            # Training and prediction pipelines
│   ├── components/          # Data ingestion, transformation
│   ├── entity/              # Configuration and artifact schema
│   ├── configuration/       # MongoDB, logging, etc.
│   ├── utils/               # Helper functions
│   └── app.py               # Flask app for prediction
├── static/                  # CSS/JS/static frontend assets
├── templates/               # HTML templates for the web UI
├── .github/workflows/       # CI/CD configuration
│   └── ci-cd.yaml
├── Dockerfile               # Docker configuration
├── requirements.txt         # Python dependencies
└── README.md                # You're here!
```

---

## 🚀 Getting Started

### Prerequisites

* Python 3.10
* Conda
* MongoDB Atlas account
* Docker
* GitHub account

---

### Installation

1. **Clone the Repository**

```bash
git clone https://github.com/yourusername/tweet-sentiment-mlops.git
cd tweet-sentiment-mlops
```

2. **Set Up Environment**

```bash
conda create -n tweetenv python=3.10 -y
conda activate tweetenv
```

3. **Install Dependencies**

```bash
pip install -r requirements.txt
```

4. **Set MongoDB Connection**

```bash
export MONGODB_URL="your_connection_string"
```

---

## 💻 Running the App

### Local Flask Server

```bash
python src/app.py
```

Access the UI at:

```plaintext
http://localhost:5000
```

---

## 🐳 Docker Support

### Build Docker Image

```bash
docker build -t tweet-sentiment-app .
```

### Run Container

```bash
docker run -d -p 5000:5000 tweet-sentiment-app
```

---

## 🔁 CI/CD with GitHub Actions

The CI/CD workflow:

* Automatically triggers on push to `main`
* Runs tests and builds Docker image

Configure the following GitHub secrets (if needed for deployment):

* `AWS_ACCESS_KEY_ID`
* `AWS_SECRET_ACCESS_KEY`
* `EC2_HOST`
* `EC2_USER`
* `EC2_KEY`

---

## 🎨 UI Preview

A lightweight and modern UI allows users to:

* Input tweets
* Get real-time sentiment predictions

> You can customize styles in `/static/` and templates in `/templates/`.

---

## 🔮 Future Enhancements

* Add charts and confidence scores to prediction results
* Improve model accuracy with advanced NLP models (e.g., LSTM, BERT)
* Add logging and analytics dashboard

---

## 👨‍💻 Author

**Lakshay**

* [GitHub](https://github.com/Lakshaygoel4321)
* [LinkedIn](https://www.linkedin.com/in/lakshay-goel-b10878326)

---

## 📝 License

This project is licensed under the MIT License — see the [LICENSE](MIT) file for details.

