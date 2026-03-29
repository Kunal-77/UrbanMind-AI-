# 🚦 UrbanMind AI

## Smart Traffic Optimization & Emergency Routing System

UrbanMind AI is an intelligent traffic routing system that simulates real-world traffic conditions and provides optimized routes for normal and emergency scenarios using AI-inspired logic.

---

## 🌟 Features

* 🚗 **Normal Route** – Best for regular travel
* 🚑 **Emergency Route** – Optimized for faster response
* ⚡ **Direct Route** – Straight path (if available)
* 🧠 **AI Traffic Analysis** – Simulated traffic-based decision making
* 🌍 **Live Map Integration** – Real-world routes using OSRM + OpenStreetMap
* 🎛️ **Interactive UI** – Toggle between routes
* 🚗 **Vehicle Simulation** – Animated vehicle on route
* 📊 **Route Comparison Cards** – Easy decision making
* 🏆 **Best Route Recommendation**

---

## 🛠️ Tech Stack

* **Frontend:** Streamlit
* **Backend:** Python
* **Graph Logic:** NetworkX
* **Maps:** Folium + OpenStreetMap (OSRM API)
* **Other Libraries:** requests, streamlit-folium

---

## 📂 Project Structure

```
UrbanMind-AI/
│
├── app.py          # Main Streamlit App
├── backend.py      # Routing Logic (Graph + AI Simulation)
├── requirements.txt
└── README.md
```

---

## 🚀 How to Run Locally

### 1️⃣ Clone the repository

```bash
git clone https://github.com/your-username/urbanmind-ai.git
cd urbanmind-ai
```

## 2️⃣ Create virtual environment (recommended)

```bash
python -m venv venv
venv\Scripts\activate   # Windows
```

## 3️⃣ Install dependencies

```bash
pip install -r requirements.txt
```

### 4️⃣ Run the app

```bash
streamlit run app.py
```

---

## 📍 Example Locations

| Node | Location     |
| ---- | ------------ |
| A    | Pune Station |
| B    | Shivajinagar |
| C    | Kothrud      |
| D    | Magarpatta   |
| E    | Hinjewadi    |
| F    | Viman Nagar  |
| G    | Baner        |

---

## 🧠 How It Works

1. A graph is created using **NetworkX**
2. Each edge has:

   * Base travel time
   * Traffic factor
3. AI logic simulates:

   * Normal traffic conditions
   * Emergency priority routing
4. Shortest path is calculated using:

   * `networkx.shortest_path`
5. Real-world routes are fetched using:

   * **OSRM API**
6. Displayed on interactive map via:

   * **Folium**

---

## ⚠️ Limitations

* Traffic is simulated (not real-time)
* Direct route may not always exist
* OSRM API requires internet connection

---

## 🔮 Future Improvements

* 🔴 Real-time traffic integration (Google Maps API)
* 🚗 Smooth vehicle animation
* 📊 Traffic heatmap
* 📱 Mobile responsive UI
* 🤖 Machine learning-based predictions

---

## 👨‍💻 Team – Urban Innovators

- **Kunal Narkhede** – Backend & System Design  
- **Yashika Shukla** – Co-Developer & Testing  

---

## ⭐ Support

If you like this project, give it a ⭐ on GitHub!

---
