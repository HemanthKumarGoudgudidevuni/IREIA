# 🏡 IREIA – Intelligent Real Estate Investment Advisor

## 📌 Project Overview
IREIA is an AI-powered real estate investment platform that helps users make smarter decisions by predicting future property prices and rental trends using machine learning. It integrates live property data via Realty In US and provides interactive visualizations including charts, maps, and investment scoring.

---

## ✨ Key Features

- 🔍 **Smart Property Search**: Search by ZIP code, city, address, or county with dynamic filters.
- 📈 **Price Forecasting**: Predicts property price trends for the next 3 years using an XGBoost ML model.
- 💰 **Rental Estimates**: Estimates monthly rental value using a XGBoost and Linear Regression ML model.
- 🧠 **Investment Recommendation**: Suggests if a property is worth investing based on predicted vs. current price.
- 🗺️ **Interactive Maps**: Google Maps integration with pins showing property price, rental price and investment status.
- 📊 **Visual Charts**: Future price and rent charts generated using Chart.js.
- 🚶 **Walk & Transit Scores**: Displays livability metrics using animated circular charts.
- 🏫 **Nearby Schools**: Automatically shows schools near the selected property using Google Places API.
- 📸 **High-Resolution Images**: Image enhancement logic ensures better property visuals.
- 🧾 **Detailed Property View**: Dedicated page per property with complete ML insights, images, and maps.
- 🔄 **Live Data Integration**: Uses the Realty In US to fetch real-time property data dynamically.

---

## 🛠️ Tech Stack

### 🔙 Backend
- **Python** with **Flask** – for handling API requests and ML model predictions
- **XGBoost** – machine learning model for price and rent forecasting
- **Realty In US API** – to fetch live property data
- **Google Places API** – to get nearby schools

### 🔛 Frontend
- **React.js** – for building dynamic user interfaces
- **Google Maps JavaScript API** – for visualizing properties with location pins
- **Chart.js** – for rendering price and rent forecast charts
- **react-circular-progressbar** – to display walk, and transit scores
- **Material UI & Custom CSS** – for styling components

### 🧪 Dev & Deployment
- **Netlify** – for frontend deployment
- **Render** – for backend hosting
- **GitHub** – for version control and code documentation

---

## 🏗️ System Architecture

The IREIA system is built using a modular architecture consisting of three primary components:

### 1. Frontend (Client-Side)
- Built with **React.js**
- Allows users to search for properties by ZIP code, city, address, or county
- Displays featured properties, predicted prices, and rental estimates
- Shows dynamic maps, charts, and investment scores
- Deployed via **Netlify**

### 2. Backend (Server-Side)
- Implemented in **Python** using **Flask**
- Exposes RESTful endpoints for:
  - `/search_property` – fetch and predict properties by location
  - `/predict_price` – ML-based price forecasting
  - `/predict_rent` – ML-based rental forecasting
- Fetches data from **Realty In US API** in real time
- Deployed via **Render**

### 3. Machine Learning Module
- Trained using **XGBoost**
- Uses features like: Year, Month, Crime Rate, Sentiment Score, Beds, Baths, Sqft, Price
- Predicts:
  - Property prices for the next 3 years
  - Monthly rental estimates
- Integrated into backend to provide instant predictions on API call

### 🔁 Data Flow
1. User enters a location in the React UI
2. Frontend sends a POST request to Flask backend
3. Flask fetches property data from Realty In US API
4. ML model runs predictions on property price & rent
5. Results sent back to React frontend and rendered as charts, scores, and cards

---

## ⚙️ Setup Instructions

To get started with the IREIA (Intelligent Real Estate Investment Advisor) platform locally, follow the setup steps for both backend (Flask) and frontend (React). Make sure you have all prerequisites installed.

---

### 🧰 Prerequisites

- Python 3.10 or higher
- Node.js 16 or higher
- npm (Node Package Manager)
- Git
- API keys for:
  - Realty In US API (RapidAPI)
  - Google Maps JavaScript API

---

### 🧠 Backend Setup

1. Clone the repository and navigate to the backend directory:

    ```bash
    git clone https://github.com/your-username/IREIA.git
    cd IREIA
    ```

2. Create a virtual environment and activate it:

    ```bash
    python -m venv venv
    source venv/bin/activate       # Windows: venv\Scripts\activate
    ```

3. Install all required Python packages:

    ```bash
    pip install -r requirements.txt
    ```

4. Run the Flask backend server:

    ```bash
    python app.py
    ```

   The backend server will be live at: `http://127.0.0.1:5000`

---

### 💻 Frontend Setup

1. Open a new terminal window, then navigate to the frontend folder:

    ```new bash
    cd my-real-estate-app
    ```

2. Install the necessary npm dependencies:

    ```bash
    npm install
    ```

5. Start the React development server:

    ```bash
    npm start
    ```

   The frontend will be accessible at: `http://localhost:5173`

---

## 🧾 Code Documentation

This section outlines the major files, scripts, and modules used across both backend and frontend of the IREIA project. Each component is documented with its purpose to help future contributors understand the codebase structure and responsibilities.

---

### 📁 Project Directory Structure

IREIA/
├── app.py                          # Main Flask application entry point  
├── requirements.txt               # Backend Python dependencies  
├── .env.ireia                     # Backend environment variables  
├── backend/
│   └── property-price-prediction/
│       └── property_price_predictor.py         # ML logic for property price prediction  
├── ml_models/
│   └── price-prediction-model/
│       └── xgboost/
│           ├── xgboost_final_model.pkl         # Trained XGBoost model  
│           └── xgboost_price_predictor.py      # XGBoost inference logic  
├── rental_prediction_app/
│   ├── rental_model.pkl                        # Trained rental model  
│   ├── rental_scaler.pkl                       # Scaler used during training  
│   ├── rental_model.py                         # Rental prediction logic  
│   └── rental_feature_importance.png           # Rental feature visualization  
├── my-real-estate-app/
│   ├── public/                                 # Static assets (index.html, favicon)  
│   └── src/
│       ├── components/                         # Reusable UI: Navbar, Footer, etc.  
│       ├── pages/                              # Main pages: HomePage, SearchPage, PropertyPage  
│       ├── styles/                             # CSS styles scoped to components/pages  
│       ├── utils/
│       │   └── maps.js                         # Google Maps logic and pins  
│       ├── App.js                              # Main React component  
│       ├── index.js                            # Entry point  
│       └── .env                                # Frontend environment configs  
├── package.json                                # React project dependencies  
└── README.md                                   # Project documentation  

---

### 🧠 Backend Overview

- **`app.py`**: Main Flask server that defines routes like:
  - `/search_property`: Processes location input and returns matching properties.
  - `/predict_price`: Calls XGBoost model for property price prediction.
  - `/predict_rent`: Returns rental estimate using XGBoost model.

- **`requirements.txt`**: Lists dependencies: `Flask`, `XGBoost`, `scikit-learn`, `pandas`, etc.

- **`backend/property-price-prediction/property_price_predictor.py`**:
  - Contains helper logic to load and invoke the trained XGBoost model for price predictions.

- **`ml_models/price-prediction-model/xgboost/xgboost_price_predictor.py`**:
  - Main inference script for property price prediction.
  - Loads `xgboost_final_model.pkl` and preprocesses input features.

- **`xgboost_dynamic_predictor.py`**:
  - Supports predictions for dynamically changing inputs during experimentation.

- **`saved_models/`**:
  - Stores serialized trained XGBoost models.

- **`rental_prediction_app/rental_model.py`**:
  - Loads rental XGBoost model and returns monthly rent estimates.
  - Uses rental feature importance for explainability.

- **`rental_model.pkl`**, **`rental_scaler.pkl`**:
  - Serialized machine learning models and scalers for rent prediction.

---

### 🧠 Frontend Overview (React)

- **components/**
  - `Navbar.js`, `Footer.js`: UI shell components.
  - `PropertyCard.js`: Renders property summaries with images, prediction, and tags.
  - `SearchBar.js`: Handles input for location-based search.

- **pages/**
  - `HomePage.js`: Detects geolocation, fetches and renders featured properties.
  - `SearchPage.js`: Displays search results and Google Maps pins.
  - `PropertiesPage.js`: Fetches properties based on location or lat/lng.
  - `PropertyPage.js`: Displays full details, charts, map, and walk/transit/investment scores.

- **styles/**: CSS modules for scoped styling:
  - `PropertyPage.css`, `SearchPage.css`, `HomePage.css`, etc.

- **utils/maps.js**:
  - Initializes and styles Google Maps view and pins with property prices and colors.

- **App.js**: Top-level routing using React Router.
- **index.js**: React root renderer.

---

### 🔧 Notable Features & Logic

- **Image Quality Optimization**:
  - In `PropertyCard.js` and `PropertyPage.js`, we dynamically rewrite low-resolution image URLs from Realty In US API to fetch high-res alternatives using suffix patterns (`-t.jpg → -o.jpg`, `-m.jpg → -mx.jpg`, etc.).

- **Chart.js Integration**:
  - `PropertyPage.js` uses Chart.js to visualize future price and rent trends.
  - Shows combined historical and forecast data interactively.

- **Scoring Indicators**:
  - `PropertyPage.js` shows investment score, walk score, and transit score using `react-circular-progressbar`.

- **Smart Recommendation Badges**:
  - Property cards display “Overpriced”, “Worth Investing”, etc., based on model recommendation.

- **Local Storage-Based Routing**:
  - Selected property info is passed between pages via `localStorage`.

- **Resilient Map Rendering**:
  - Google Maps initialized on page load with fallback logic if `window.google.maps` is delayed.

---

## 📖 User Manual

### 🎯 Objective
IREIA helps users find and evaluate real estate investment opportunities using AI-powered price and rent forecasts, live API data, and visual insights.

---

### 🖥️ Accessing the Application

You can run the app in two ways:

#### 1. **Local Deployment**
Follow the setup instructions in the [⚙️ Setup Instructions](#️-setup-instructions) section to run the backend and frontend locally.

#### 2. **Live Deployment**
If hosted on a platform like Render/Netlify, simply open the live URL in a browser.

---

### 🔍 Using the App

#### 🔎 Home Page
- Auto-detects your location and displays nearby featured properties.
- Includes a search bar to look up properties by ZIP, city, address, or county.

#### 🔍 Search Page
- Displays properties matching the searched location or filter.
- Shows a scrollable list of properties alongside an interactive Google Map.
- Pins are colored based on investment recommendation.

#### 🏠 Property Detail Page
Click on any property card to view:
- Full property details including price, rent, beds, baths, etc.
- **Charts** for future price and rent predictions.
- **Walk & Transit scores** visualized as circular meters.
- A Google Map with the selected property and nearby schools.

---

### 🧠 Key Features for Users

| Feature               | Description                                          |
|-----------------------|------------------------------------------------------|
| 🔮 Price Forecast      | 3-year price and rent predictions powered by XGBoost |
| 🗺️ Map View            | Pins show real-time investment tags                  |
| 💬 Recommendation Badge | Indicates if a property is Worth Investing or Overpriced |
| 📈 Interactive Charts  | Chart.js-based graphs for trends                     |
| 📍 School Insights     | Nearby schools fetched via Google Places API         |

---

### 💡 Tips
- Hover over map pins to see quick stats.
- Use browser DevTools for debugging fetch/API issues.
- Press `Ctrl + Shift + R` to hard-refresh and clear cache if needed.

---

## 📚 Citations & References

### 🔌 APIs & Services Used
- **Realty In US API** – Live property listings, pricing, rental data  
  🔗 https://rapidapi.com/apidojo/api/Realty In US

- **Google Maps JavaScript API** – Interactive map with location pins  
  🔗 https://developers.google.com/maps/documentation/javascript

- **Google Places API** – Nearby school detection  
  🔗 https://developers.google.com/maps/documentation/places/web-service/overview

---

### 📦 Libraries & Frameworks
- **Flask** – Python web framework for backend APIs  
  🔗 https://flask.palletsprojects.com/

- **XGBoost** – Gradient boosting model for price prediction  
  🔗 https://xgboost.readthedocs.io/

- **React.js** – Frontend JavaScript library for UI  
  🔗 https://reactjs.org/

- **Chart.js** – Data visualization (line and bar charts)  
  🔗 https://www.chartjs.org/

- **React Circular Progressbar** – For visual scoring meters  
  🔗 https://www.npmjs.com/package/react-circular-progressbar

---

### 🧠 Inspiration
- Zillow – Real estate layout and recommendation system inspiration  
  🔗 https://www.zillow.com/

---

### 🛠️ Project Team
- Developed by: Jacob Jashwanth Patoju, Gnana Sahiti Nambeti, Hemanth Kumar Goud Gudidevuni  
  For CS682: Intelligent Real Estate Systems (Spring 2025), UMass Boston

---

## 👥 Meet Our Team

### **Jacob Jashwanth Patoju**  
**Lead Full Stack AI Developer**
- Designed full-stack real estate prediction platform  
- Built and integrated XGBoost-based property price prediction model  
- Developed interactive React frontend with maps, charts, and forecasts  

---

### **Gnana Sahiti Nambeti**  
**Data Scientist**
- Developed a rental income optimization model using supervised machine learning algorithms  
- Engineered ML pipelines and integrated data API to retrieve real-time data for analysis and predictive modeling  
- Visualized property price trends for actionable insights  

---

### **Hemanth Kumar Goud Gudidevuni**  
**Web Developer**
- Integrated location metrics like walk and transit scores to simulate real-world investment insight  
- Mapped scoring results to the frontend interface to visually guide user decisions  
- Collaborated on testing and refining score logic to align with the platform’s predictive models  

---

## 🔮 Future Scope

- Add login/signup and user authentication for personalized dashboards  
- Enable users to save and bookmark favorite properties  
- Integrate additional insights like crime rate, neighborhood sentiment score, and property tax history  
- Extend support to commercial properties with ROI-based investment analysis  
- Build a mobile app version of the platform for cross-device accessibility  

---

## 📎 License
MIT License (for academic use only)

---

## 🌐 Live URLs

- 🔗 **Frontend (Netlify):** [https://681a84ffbdbadc81be5ff226--ireia3a.netlify.app/](https://681a84ffbdbadc81be5ff226--ireia3a.netlify.app/)
- 🔗 **Backend (Render):** [https://ireia.onrender.com](https://ireia.onrender.com)