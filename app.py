import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Travel Planner",
    page_icon="🌍",
    layout="wide"
)

# ------------------------------------------------
# STYLE
# ------------------------------------------------

st.markdown("""
<style>
@import url('https://fonts.googleapis.com/css2?family=Poppins:wght@300;400;600;700&display=swap');

* {
    font-family: 'Poppins', sans-serif;
}

.stApp {
    background: linear-gradient(135deg, #667eea 0%, #764ba2 100%);
    color: #fff;
}

.block-container {
    max-width: 1400px;
    padding: 2rem;
}

h1, h2, h3, h4, h5, p, label, span, div {
    color: #fff !important;
}

/* Header */
.hero-section {
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    backdrop-filter: blur(10px);
    padding: 60px 40px;
    border-radius: 30px;
    text-align: center;
    margin-bottom: 40px;
    border: 1px solid rgba(255,255,255,0.2);
    box-shadow: 0 20px 60px rgba(0,0,0,0.3);
}

.hero-title {
    font-size: 56px;
    font-weight: 700;
    background: linear-gradient(45deg, #fff, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
    margin-bottom: 10px;
}

.hero-subtitle {
    font-size: 20px;
    color: rgba(255,255,255,0.9);
    font-weight: 300;
}

/* City Cards */
.city-grid {
    display: grid;
    grid-template-columns: repeat(auto-fill, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.city-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 30px 20px;
    text-align: center;
    cursor: pointer;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.city-card:hover {
    transform: translateY(-10px);
    box-shadow: 0 20px 40px rgba(0,0,0,0.4);
    background: linear-gradient(135deg, rgba(255,255,255,0.25), rgba(255,255,255,0.15));
}

.city-card::before {
    content: '';
    position: absolute;
    top: 0;
    left: 0;
    width: 100%;
    height: 100%;
    background: linear-gradient(135deg, transparent, rgba(255,255,255,0.1));
    opacity: 0;
    transition: opacity 0.3s;
}

.city-card:hover::before {
    opacity: 1;
}

.city-icon {
    font-size: 48px;
    margin-bottom: 15px;
}

.city-name {
    font-size: 18px;
    font-weight: 600;
    color: #fff;
}

/* Place Cards */
.place-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 25px;
    padding: 30px;
    margin-bottom: 25px;
    transition: all 0.3s ease;
    position: relative;
    overflow: hidden;
}

.place-card:hover {
    transform: translateX(10px);
    box-shadow: 0 15px 40px rgba(0,0,0,0.3);
}

.place-header {
    display: flex;
    align-items: center;
    gap: 15px;
    margin-bottom: 15px;
}

.place-icon {
    font-size: 48px;
    filter: drop-shadow(0 4px 8px rgba(0,0,0,0.2));
}

.place-title {
    font-size: 24px;
    font-weight: 700;
    color: #fff;
}

.place-desc {
    color: rgba(255,255,255,0.8);
    font-size: 16px;
    margin-bottom: 10px;
}

.place-time {
    display: inline-block;
    background: rgba(255,255,255,0.2);
    padding: 8px 16px;
    border-radius: 20px;
    font-size: 14px;
    font-weight: 600;
}

/* Timeline */
.timeline {
    border-left: 4px solid rgba(255,255,255,0.3);
    padding-left: 30px;
    margin: 30px 0;
}

.timeline-step {
    position: relative;
    margin-bottom: 30px;
    padding: 20px;
    background: linear-gradient(135deg, rgba(255,255,255,0.1), rgba(255,255,255,0.05));
    border-radius: 15px;
    backdrop-filter: blur(10px);
}

.timeline-step::before {
    content: '';
    position: absolute;
    left: -37px;
    top: 25px;
    width: 16px;
    height: 16px;
    background: #ffd700;
    border-radius: 50%;
    border: 4px solid #667eea;
}

.timeline-time {
    font-size: 18px;
    font-weight: 700;
    color: #ffd700;
}

/* Buttons */
.stButton button {
    background: linear-gradient(135deg, #ffd700, #ffed4e);
    color: #333;
    border: none;
    border-radius: 25px;
    padding: 15px 35px;
    font-weight: 700;
    font-size: 16px;
    transition: all 0.3s ease;
    box-shadow: 0 10px 30px rgba(255,215,0,0.3);
}

.stButton button:hover {
    transform: translateY(-3px);
    box-shadow: 0 15px 40px rgba(255,215,0,0.5);
    background: linear-gradient(135deg, #ffed4e, #ffd700);
}

/* Input */
input, textarea, .stSelectbox div, .stRadio div {
    background: rgba(255,255,255,0.15) !important;
    border: 1px solid rgba(255,255,255,0.3) !important;
    border-radius: 15px !important;
    color: #fff !important;
    backdrop-filter: blur(10px);
}

/* Progress */
.stProgress > div > div {
    background: linear-gradient(90deg, #ffd700, #ffed4e);
}

/* Section Headers */
.section-header {
    font-size: 36px;
    font-weight: 700;
    margin: 40px 0 30px 0;
    text-align: center;
    background: linear-gradient(45deg, #fff, #ffd700);
    -webkit-background-clip: text;
    -webkit-text-fill-color: transparent;
}

/* Stats */
.stats-container {
    display: grid;
    grid-template-columns: repeat(auto-fit, minmax(200px, 1fr));
    gap: 20px;
    margin: 30px 0;
}

.stat-card {
    background: linear-gradient(135deg, rgba(255,255,255,0.15), rgba(255,255,255,0.05));
    backdrop-filter: blur(10px);
    border: 1px solid rgba(255,255,255,0.2);
    border-radius: 20px;
    padding: 25px;
    text-align: center;
}

.stat-value {
    font-size: 36px;
    font-weight: 700;
    color: #ffd700;
}

.stat-label {
    font-size: 14px;
    color: rgba(255,255,255,0.8);
    margin-top: 5px;
}

/* Image Container */
.image-container {
    border-radius: 25px;
    overflow: hidden;
    margin: 20px 0;
    box-shadow: 0 20px 60px rgba(0,0,0,0.4);
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SESSION
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "route" not in st.session_state:
    st.session_state.route = None

# ------------------------------------------------
# CITIES DATA
# ------------------------------------------------

cities_data = [
    {"name": "Москва", "icon": "🏛️", "image": "https://images.unsplash.com/photo-1513326738677-b964603b136d?w=800"},
    {"name": "Санкт-Петербург", "icon": "🌉", "image": "https://images.unsplash.com/photo-1556610961-2fecc5927173?w=800"},
    {"name": "Казань", "icon": "🕌", "image": "https://images.unsplash.com/photo-1597655601841-214a4cfe8b2c?w=800"},
    {"name": "Сочи", "icon": "🏖️", "image": "https://images.unsplash.com/photo-1590073242678-70ee3fc28e8e?w=800"},
    {"name": "Калининград", "icon": "🏰", "image": "https://images.unsplash.com/photo-1595867818082-083862f3d630?w=800"},
    {"name": "Владивосток", "icon": "⚓", "image": "https://images.unsplash.com/photo-1580837119756-563d608dd119?w=800"},
    {"name": "Екатеринбург", "icon": "🏙️", "image": "https://images.unsplash.com/photo-1567696153798-96f9d75fbbeb?w=800"},
    {"name": "Новосибирск", "icon": "🌆", "image": "https://images.unsplash.com/photo-1534430480872-3498386e7856?w=800"},
    {"name": "Нижний Новгород", "icon": "🏛️", "image": "https://images.unsplash.com/photo-1520106212299-d99c443e4568?w=800"},
    {"name": "Самара", "icon": "🚀", "image": "https://images.unsplash.com/photo-1477959858617-67f85cf4f1df?w=800"},
    {"name": "Краснодар", "icon": "🌻", "image": "https://images.unsplash.com/photo-1496568816309-51d7c20e3b21?w=800"},
    {"name": "Ростов-на-Дону", "icon": "⚡", "image": "https://images.unsplash.com/photo-1449824913935-59a10b8d2000?w=800"},
    {"name": "Иркутск", "icon": "🏔️", "image": "https://images.unsplash.com/photo-1506905925346-21bda4d32df4?w=800"},
    {"name": "Мурманск", "icon": "🌌", "image": "https://images.unsplash.com/photo-1483728642387-6c3bdd6c93e5?w=800"},
    {"name": "Ярославль", "icon": "⛪", "image": "https://images.unsplash.com/photo-1518709268805-4e9042af9f23?w=800"},
]

# ------------------------------------------------
# PLACES
# ------------------------------------------------

places = [
    {"name": "Главная площадь", "desc": "Исторический центр города с величественной архитектурой", "time": 40, "lat": 55.751, "lon": 37.618, "icon": "🏛️"},
    {"name": "Городской парк", "desc": "Зеленый оазис для прогулок и отдыха", "time": 90, "lat": 55.760, "lon": 37.620, "icon": "🌳"},
    {"name": "Главный музей", "desc": "Крупнейший музей с уникальными экспонатами", "time": 120, "lat": 55.752, "lon": 37.617, "icon": "🖼️"},
    {"name": "Пешеходная улица", "desc": "Атмосферная улица с кафе и магазинами", "time": 60, "lat": 55.750, "lon": 37.615, "icon": "☕"},
    {"name": "Смотровая площадка", "desc": "Панорамный вид на весь город", "time": 30, "lat": 55.749, "lon": 37.622, "icon": "📸"},
    {"name": "Фудмаркет", "desc": "Гастрономический рай с местной кухней", "time": 70, "lat": 55.748, "lon": 37.621, "icon": "🍜"},
    {"name": "Набережная", "desc": "Романтическая прогулка вдоль реки", "time": 50, "lat": 55.747, "lon": 37.619, "icon": "🌊"},
    {"name": "Арт-квартал", "desc": "Современное искусство и галереи", "time": 80, "lat": 55.753, "lon": 37.623, "icon": "🎨"},
]

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("""
<div class="hero-section">
    <div class="hero-title">🌍 Travel Planner</div>
    <div class="hero-subtitle">Создайте идеальный маршрут путешествия за 30 секунд</div>
</div>
""", unsafe_allow_html=True)

st.progress(st.session_state.step / 3)

# ------------------------------------------------
# STEP 1 - CITY SELECTION
# ------------------------------------------------

if st.session_state.step == 1:
    
    st.markdown('<div class="section-header">🏙️ Выберите город для путешествия</div>', unsafe_allow
