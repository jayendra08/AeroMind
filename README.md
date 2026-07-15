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

<img width="1920" height="1080" alt="Screenshot 2026-07-15 222235" src="https://github.com/user-attachments/assets/939d0085-e82d-44a1-8902-7666bc364ded" />


### AQI Prediction

<img width="1920" height="1080" alt="Screenshot 2026-07-15 222507" src="https://github.com/user-attachments/assets/f3ebb777-2f91-4757-b17b-5545617ddaaa" />


### Analytics Dashboard

<img width="1920" height="1080" alt="Screenshot 2026-07-15 222206" src="https://github.com/user-attachments/assets/a45ab2fb-fb4f-425b-9b00-57c797936cad" />

<img width="1920" height="1080" alt="Screenshot 2026-07-15 222540" src="https://github.com/user-attachments/assets/e33d3f25-a1c0-4c03-8b4b-64ff3ea41999" />

<img width="1920" height="1080" alt="Screenshot 2026-07-15 222619" src="https://github.com/user-attachments/assets/2a8feaea-f996-4eaf-a410-980da2f4d6f0" />

<img width="1920" height="1020" alt="Screenshot 2026-07-15 221943" src="https://github.com/user-attachments/assets/6d745f35-2507-4cd1-ac8b-269ba4b21f68" />





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
