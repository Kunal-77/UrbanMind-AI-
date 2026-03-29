import streamlit as st
from backend import get_route, get_direct_route
from streamlit_folium import st_folium
import folium
import random
import time
import requests
import streamlit.components.v1 as components  # ✅ ADDED

def get_real_route(coords):
    coord_str = ";".join([f"{lon},{lat}" for lat, lon in coords])

    url = f"http://router.project-osrm.org/route/v1/driving/{coord_str}?overview=full&geometries=geojson"

    try:
        response = requests.get(url).json()
        if "routes" in response:
            route = response["routes"][0]["geometry"]["coordinates"]
            return [(lat, lon) for lon, lat in route]
    except:
        pass

    return coords

st.set_page_config(page_title="UrbanMind AI", layout="wide")

# SESSION STATE
if "run" not in st.session_state:
    st.session_state.run = False

if "result" not in st.session_state:
    st.session_state.result = None

# -------- REAL LOCATIONS --------
real_locations = {
    "A": ("Pune Station", (18.5286, 73.8740)),
    "B": ("Shivajinagar", (18.5308, 73.8475)),
    "C": ("Kothrud", (18.5074, 73.8077)),
    "D": ("Magarpatta", (18.5150, 73.9270)),
    "E": ("Hinjewadi", (18.5910, 73.7389)),
    "F": ("Viman Nagar", (18.5679, 73.9143)),
    "G": ("Baner", (18.5590, 73.7868)),
}

name_to_node = {}
for k, v in real_locations.items():
    name = v[0].lower()
    name_to_node[name] = k
    name_to_node[name.replace(" ", "")] = k

# -------- CSS --------
st.markdown("""
<style>
body { background: linear-gradient(135deg, #020617, #0f172a); }

.stButton>button {
    background: linear-gradient(90deg, #22c55e, #16a34a);
    color: white;
    border-radius: 14px;
    padding: 14px;
    font-size: 17px;
    font-weight: bold;
    border: none;
    width: 100%;
}

.map-fix {
    background: white;
    padding: 8px;
    border-radius: 16px;
    width: 100%;
}
</style>
""", unsafe_allow_html=True)

# -------- HEADER --------
st.markdown("""
<h1 style='text-align:center;'>🚦 UrbanMind AI</h1>
<p style='text-align:center;color:#94a3b8;'>AI-Powered Smart Traffic Optimization & Emergency Routing</p>
""", unsafe_allow_html=True)

# -------- INPUT --------
st.markdown("### 📍 Route Selection")

col1, col2 = st.columns(2)

with col1:
    st.markdown("#### 🚩 Start Location")
    start_choice = st.selectbox("Select Start", list(real_locations.keys()), key="start_select")
    start_input = st.text_input("Or type manually", "", key="start_input")

with col2:
    st.markdown("#### 🎯 Destination")
    end_choice = st.selectbox("Select Destination", list(real_locations.keys()), key="end_select")
    end_input = st.text_input("Or type manually", "", key="end_input")

with st.expander("📍 Available Locations (Node → Real Place)"):
    for k, v in real_locations.items():
        st.write(f"{k} → {v[0]}")

col1, col2, col3 = st.columns([1,2,1])
with col2:
    find = st.button("🚀 Find Smart Route")

st.markdown("---")

def resolve_location(user_input):
    if not user_input:
        return None
    user_input = user_input.strip()

    if user_input.upper() in real_locations:
        return user_input.upper()

    user_input_lower = user_input.lower()
    for name, node in name_to_node.items():
        if user_input_lower == name:
            return node

    return None

def get_final_location(text_input, dropdown_choice):
    if text_input and text_input.strip():
        resolved = resolve_location(text_input)
        if resolved:
            return resolved
    return dropdown_choice

start = get_final_location(start_input, start_choice)
end = get_final_location(end_input, end_choice)

# -------- VALIDATION --------
if start is None or end is None:
    st.error("❌ Invalid input")

elif start == end:
    st.warning("⚠️ Start and destination cannot be same")

# -------- BUTTON --------
if find and start and end and start != end:

    st.session_state.run = True

    with st.spinner("🤖 AI is analyzing traffic..."):
        progress = st.progress(0)

        steps = [
            "🚦 Traffic Agent analyzing...",
            "🧭 Routing Agent calculating...",
            "🚑 Emergency Agent optimizing...",
            "🧠 Decision Agent finalizing..."
        ]

        for i, step in enumerate(steps):
            st.write(step)
            progress.progress((i+1)*25)
            time.sleep(0.5)

    normal_path, normal_cost = get_route(start, end, False)
    emergency_path, emergency_cost = get_route(start, end, True)
    direct_path, direct_cost = get_direct_route(start, end)

    st.session_state.result = (
        normal_path, normal_cost,
        emergency_path, emergency_cost,
        direct_path, direct_cost
    )

# -------- OUTPUT --------
if st.session_state.run and st.session_state.result:

    normal_path, normal_cost, emergency_path, emergency_cost, direct_path, direct_cost = st.session_state.result

    st.markdown("## 🤖 AI Agent Workflow")

    with st.expander("🔍 View AI Thinking Process"):
        st.write("""
1️⃣ Traffic Agent → Detect congestion  
2️⃣ Routing Agent → Calculate shortest paths  
3️⃣ Emergency Agent → Optimize priority routes  
4️⃣ Decision Agent → Compare & select best route  
5️⃣ Insight Agent → Explain decision  
        """)

    st.markdown("## 🚦 Traffic Status")

    if normal_cost > emergency_cost:
        st.error("🔴 High Traffic")
    else:
        st.success("🟢 Moderate Traffic")

    st.markdown("---")

    col1, col2, col3 = st.columns(3)

    with col1:
        st.markdown("### 🚗 Normal Route")
        st.success(" → ".join([real_locations[n][0] for n in normal_path]))
        st.metric("ETA", f"{normal_cost} mins")

    with col2:
        st.markdown("### 🚑 Emergency Route")
        st.success(" → ".join([real_locations[n][0] for n in emergency_path]))
        st.metric("ETA", f"{emergency_cost} mins")

    with col3:
        st.markdown("### ⚡ Direct Route")
        st.success(" → ".join([real_locations[n][0] for n in direct_path]))
        st.metric("ETA", f"{direct_cost} mins")

    best = min([
        ("Normal", normal_cost),
        ("Emergency", emergency_cost),
        ("Direct", direct_cost if isinstance(direct_cost, (int, float)) else 999)
    ], key=lambda x: x[1])

    st.success(f"🏆 Best Route: {best[0]} Route")

    st.markdown("## 🌍 Live Map")

    m = folium.Map(location=real_locations[start][1], zoom_start=12)

    normal_coords = get_real_route([real_locations[n][1] for n in normal_path])
    emergency_coords = get_real_route([real_locations[n][1] for n in emergency_path])
    direct_coords = get_real_route([real_locations[n][1] for n in direct_path])

    folium.PolyLine(normal_coords, color="blue", weight=6).add_to(m)
    folium.PolyLine(emergency_coords, color="red", weight=6).add_to(m)
    folium.PolyLine(direct_coords, color="green", weight=6).add_to(m)

    for node, (name, coord) in real_locations.items():
        folium.Marker(coord, popup=name).add_to(m)

    # 🔥 FINAL FIX (ONLY CHANGE)
    map_html = m._repr_html_()

    components.html(f"""
    <div class="map-fix">
        {map_html}
    </div>
    """, height=550)

    # -------- INSIGHTS --------
    st.markdown("---")

    st.markdown("## 📘 Route Insights")

    st.info("""
💡 **Normal Route** → Best for regular travel  
🚑 **Emergency Route** → Faster during heavy traffic  
⚡ **Direct Route** → Straight connection (may not exist)

🧠 AI compares traffic, time, and efficiency before suggesting routes.
""")

    st.markdown("## ⚙️ Tips")

    st.write("""
- Try different locations (A–G)
- Use manual input like "Shivajinagar"
- Emergency route is useful during peak hours
""")