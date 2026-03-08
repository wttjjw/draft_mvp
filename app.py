# pip install streamlit pandas

import streamlit as st
import pandas as pd
import random

# ------------------------------------------------
# PAGE CONFIG
# ------------------------------------------------

st.set_page_config(
    page_title="Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ------------------------------------------------
# LIGHT UI STYLE
# ------------------------------------------------

st.markdown("""
<style>

.stApp {
background-color:#f4f6fb;
color:#1f2933;
}

.block-container{
max-width:850px;
margin:auto;
}

/* header */

.header-card{
background:white;
padding:40px;
border-radius:18px;
box-shadow:0 10px 30px rgba(0,0,0,0.08);
text-align:center;
margin-bottom:25px;
}

.header-title{
font-size:36px;
font-weight:700;
color:#111827;
}

.header-sub{
color:#6b7280;
}

/* place cards */

.place-card{
background:white;
padding:25px;
border-radius:14px;
box-shadow:0 4px 14px rgba(0,0,0,0.08);
margin-bottom:20px;
}

.place-title{
font-size:20px;
font-weight:600;
color:#111827;
}

.place-desc{
color:#4b5563;
}

/* timeline */

.timeline{
border-left:3px solid #6366f1;
padding-left:15px;
margin-top:20px;
}

.timeline-step{
margin-bottom:12px;
color:#374151;
}

/* buttons */

.stButton button{
background:#6366f1;
color:white;
border-radius:8px;
padding:10px 18px;
border:none;
font-weight:600;
}

.stButton button:hover{
background:#4f46e5;
}

</style>
""", unsafe_allow_html=True)

# ------------------------------------------------
# SESSION STATE
# ------------------------------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "route" not in st.session_state:
    st.session_state.route = None

# ------------------------------------------------
# DEMO DATA (вместо AI)
# ------------------------------------------------

places_db = [
    {
        "name":"Центральная площадь",
        "desc":"Историческое сердце города",
        "time":40,
        "lat":55.751244,
        "lon":37.618423,
        "icon":"🏛"
    },
    {
        "name":"Городской парк",
        "desc":"Большой парк для прогулок",
        "time":90,
        "lat":55.7600,
        "lon":37.6200,
        "icon":"🌳"
    },
    {
        "name":"Главный музей",
        "desc":"Коллекция искусства и истории",
        "time":120,
        "lat":55.7520,
        "lon":37.6170,
        "icon":"🖼"
    },
    {
        "name":"Пешеходная улица",
        "desc":"Популярное место с кафе",
        "time":60,
        "lat":55.7500,
        "lon":37.6150,
        "icon":"☕"
    },
    {
        "name":"Смотровая площадка",
        "desc":"Лучший вид на город",
        "time":30,
        "lat":55.7490,
        "lon":37.6220,
        "icon":"📸"
    },
    {
        "name":"Рынок еды",
        "desc":"Местная кухня и рестораны",
        "time":70,
        "lat":55.7480,
        "lon":37.6210,
        "icon":"🍜"
    }
]

# ------------------------------------------------
# HEADER
# ------------------------------------------------

st.markdown("""
<div class="header-card">
<div class="header-title">🌍 Travel Planner</div>
<div class="header-sub">Создайте маршрут путешествия за 30 секунд</div>
</div>
""", unsafe_allow_html=True)

st.progress(st.session_state.step / 3)

# ------------------------------------------------
# STEP 1 — CITY
# ------------------------------------------------

if st.session_state.step == 1:

    st.subheader("🏙 Выберите город")

    city = st.text_input(
        "Введите город",
        placeholder="Например: Москва"
    )

    if st.button("Продолжить"):

        if city:
            st.session_state.city = city
            st.session_state.step = 2
            st.rerun()
        else:
            st.warning("Введите город")

# ------------------------------------------------
# STEP 2 — QUIZ
# ------------------------------------------------

elif st.session_state.step == 2:

    st.subheader("🧭 Расскажите о поездке")

    pace = st.radio(
        "Темп отдыха",
        ["Активный","Размеренный","Смешанный"]
    )

    interest = st.selectbox(
        "Что интереснее",
        [
            "История и архитектура",
            "Еда и рестораны",
            "Природа и парки",
            "Музеи",
            "Ночная жизнь"
        ]
    )

    company = st.selectbox(
        "С кем путешествуете",
        ["Один","Вдвоем","С семьей"]
    )

    col1,col2 = st.columns(2)

    with col1:
        if st.button("Назад"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Построить маршрут"):

            st.session_state.answers = {
                "pace":pace,
                "interest":interest,
                "company":company
            }

            st.session_state.route = random.sample(places_db,5)

            st.session_state.step = 3
            st.rerun()

# ------------------------------------------------
# STEP 3 — ROUTE
# ------------------------------------------------

elif st.session_state.step == 3:

    st.subheader(f"📍 Маршрут по городу {st.session_state.city}")

    route = st.session_state.route

    for place in route:

        st.markdown(f"""
        <div class="place-card">
        <div class="place-title">{place["icon"]} {place["name"]}</div>
        <div class="place-desc">{place["desc"]}</div>
        ⏱ {place["time"]} минут
        </div>
        """, unsafe_allow_html=True)

    # ---------------------------
    # MAP
    # ---------------------------

    st.subheader("🗺 Карта маршрута")

    df = pd.DataFrame(route)

    st.map(df[["lat","lon"]])

    # ---------------------------
    # TIMELINE
    # ---------------------------

    st.subheader("📅 Таймлайн")

    time = 9

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for place in route:

        st.markdown(f"""
        <div class="timeline-step">
        {time}:00 — {place["name"]}
        </div>
        """, unsafe_allow_html=True)

        time += 1

    st.markdown('</div>', unsafe_allow_html=True)

    # ---------------------------
    # RESET
    # ---------------------------

    if st.button("🔄 Создать новый маршрут"):

        st.session_state.step = 1
        st.session_state.route = None
        st.rerun()
