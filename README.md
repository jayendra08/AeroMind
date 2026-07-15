# 🌍 AI-Powered Air Quality Prediction System

An intelligent web application that predicts **Air Quality Index (AQI)** using Machine Learning and visualizes environmental data through an interactive MERN stack dashboard. The system integrates environmental, meteorological, and pollution-related datasets to provide accurate air quality predictions, historical analysis, and future forecasting.

---

## 📌 Overview

Air pollution has become one of the most significant environmental challenges worldwide. This project leverages Machine Learning to analyze multiple environmental parameters and predict AQI for different locations. It provides users with real-time insights, historical trends, and data visualizations to help understand air quality conditions.

---

## ✨ Features

- 🌫️ Real-time AQI Prediction
- 📈 Multi-day AQI Forecasting
- 🤖 Machine Learning-based Prediction Models
- 📊 Interactive Dashboard with Charts
- 🗺️ Pollution Heatmap Visualization
- 📉 Historical Air Quality Analysis
- 🌦️ Weather Parameter Integration
- 🏙️ City-wise Air Quality Monitoring
- 📱 Fully Responsive User Interface

---

## 🛠️ Tech Stack

### Frontend
- React.js
- HTML5
- CSS3
- JavaScript
- Axios
- Chart.js / Recharts

### Backend
- Node.js
- Express.js

### Database
- MongoDB

### Machine Learning
- Python
- Pandas
- NumPy
- Scikit-Learn
- TensorFlow / Keras
- Matplotlib
- Seaborn

---

## 🧠 Machine Learning Workflow

- Data Collection
- Data Cleaning & Preprocessing
- Feature Engineering
- Data Scaling
- Model Training
- Model Evaluation
- AQI Prediction
- Result Visualization

---

## 📂 Project Structure

```
AQI-Prediction-System
│
├── website
│   ├── Backend
│   └── Frontend
│
├── models
│
├── data
│   ├── raw
│   └── processed
│
├── notebooks
│
├── docs
│
├── screenshots
│
├── requirements.txt
│
└── README.md
```

---

## 🚀 Getting Started

### Clone the Repository

```bash
git clone ________________________________

cd ________________________________
```

### Install Backend Dependencies

```bash
cd website/Backend

npm install

pip install -r requirements.txt
```

### Install Frontend Dependencies

```bash
cd ../Frontend

npm install
```

### Start Backend

```bash
npm start
```

### Start Frontend

```bash
npm run dev
```

### Run Machine Learning Model

```bash
python predict.py
```

---

## ⚙️ Environment Variables

Create a `.env` file inside the backend folder.

```env
PORT=

MONGODB_URI=

JWT_SECRET=

MODEL_PATH=

API_KEY=
```

---

## 📊 Model Performance

| Metric | Value |
|---------|------:|
| Accuracy | ______ |
| RMSE | ______ |
| MAE | ______ |
| R² Score | ______ |

---

## 🌍 Dataset

The model is trained using environmental and pollution datasets containing parameters such as:

- PM2.5
- PM10
- NO₂
- SO₂
- CO
- O₃
- Temperature
- Humidity
- Wind Speed
- Atmospheric Pressure

---

## 📡 API Endpoints

### Predict AQI

```
GET /api/predict
```

### Forecast AQI

```
GET /api/forecast
```

### Historical Data

```
GET /api/history
```

### City Details

```
GET /api/city/:city
```

---

## 📸 Screenshots

### Home Dashboard

<img width="1920" height="1080" alt="Screenshot 2026-07-15 230721" src="https://github.com/user-attachments/assets/7e6d02e5-f0ab-4e28-afa6-8aca42d325aa" />



### Micro-Location Lab

<img width="1920" height="1080" alt="Screenshot 2026-07-15 230736" src="https://github.com/user-attachments/assets/22c4697e-1b57-4cf7-b4c9-c8d4fffe16f8" />





### AQI and PM 2.5 Ranking

<img width="1920" height="1080" alt="Screenshot 2026-07-15 230750" src="https://github.com/user-attachments/assets/b2eec073-0ab2-4772-9c3c-492886aa8aa6" />

<img width="1920" height="1080" alt="image" src="https://github.com/user-attachments/assets/1c33af46-634b-43db-a375-2222c688c37e" />








---

## 🚀 Future Enhancements

- Pollution Hotspot Prediction
- Explainable AI (SHAP/LIME)
- Personalized Exposure Risk Analysis
- Smart AQI Alert System
- Route-based Pollution Analysis
- Mobile Application
- IoT Sensor Integration

---

## 🤝 Contributing

Contributions are welcome!

1. Fork this repository.
2. Create a new feature branch.
3. Commit your changes.
4. Push your branch.
5. Open a Pull Request.

---

## 👨‍💻 Developer

**Name:** Jayendra Ghosh

**GitHub:** https://github.com/jayendra08

---

## 📜 License

This project is licensed under the MIT License.

---

## 🙏 Acknowledgements

- ISRO
- NASA
- CPCB
- IMD
- Open Source Community

---

## ⭐ Support

If you found this project useful, consider giving it a **Star ⭐** on GitHub.

Made with ❤️ using **MERN Stack** and **Machine Learning**.
