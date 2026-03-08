# pip install streamlit pandas

import streamlit as st
import pandas as pd
import random

st.set_page_config(
    page_title="Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ------------------------------------------------
# STYLE
# ------------------------------------------------

st.markdown("""
<style>

.stApp{
background:#f4f6fb;
color:#1f2933;
}

.block-container{
max-width:900px;
margin:auto;
}

.header-card{
background:white;
padding:40px;
border-radius:16px;
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

/* city tags */

.city-btn button{
background:white;
color:#374151;
border:1px solid #e5e7eb;
border-radius:20px;
padding:6px 16px;
margin:4px;
}

.city-btn button:hover{
background:#6366f1;
color:white;
}

/* place cards */

.place-card{
background:white;
padding:25px;
border-radius:14px;
box-shadow:0 4px 14px rgba(0,0,0,0.08);
margin-bottom:18px;
}

.place-title{
font-size:20px;
font-weight:600;
}

.place-desc{
color:#4b5563;
}

/* timeline */

.timeline{
border-left:3px solid #6366f1;
padding-left:15px;
}

.timeline-step{
margin-bottom:12px;
}

.stButton button{
background:#6366f1;
color:white;
border-radius:8px;
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
# TOURIST CITIES
# ------------------------------------------------

tourist_cities = [

"Москва","Санкт-Петербург","Казань","Сочи","Калининград",
"Владивосток","Екатеринбург","Новосибирск","Нижний Новгород",
"Самара","Краснодар","Ростов-на-Дону","Иркутск","Мурманск",
"Ярославль","Суздаль","Владимир","Тула","Кострома","Псков",
"Великий Новгород","Астрахань","Уфа","Челябинск","Пермь",
"Томск","Красноярск","Архангельск","Калуга","Смоленск"

]

# ------------------------------------------------
# DEMO PLACES
# ------------------------------------------------

places_db = [

{"name":"Главная площадь","desc":"Исторический центр города","time":40,"lat":55.751,"lon":37.618,"icon":"🏛"},
{"name":"Городской парк","desc":"Популярное место для прогулок","time":90,"lat":55.760,"lon":37.620,"icon":"🌳"},
{"name":"Главный музей","desc":"Крупнейший музей города","time":120,"lat":55.752,"lon":37.617,"icon":"🖼"},
{"name":"Пешеходная улица","desc":"Улица с кафе и ресторанами","time":60,"lat":55.750,"lon":37.615,"icon":"☕"},
{"name":"Смотровая площадка","desc":"Лучший вид на город","time":30,"lat":55.749,"lon":37.622,"icon":"📸"},
{"name":"Фудмаркет","desc":"Место с местной кухней","time":70,"lat":55.748,"lon":37.621,"icon":"🍜"}

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

st.progress(st.session_state.step/3)

# ------------------------------------------------
# STEP 1 — CITY CLOUD
# ------------------------------------------------

if st.session_state.step == 1:

    st.subheader("🏙 Выберите город")

    cols = st.columns(5)

    for i,city in enumerate(tourist_cities):

        with cols[i % 5]:

            if st.button(city):

                st.session_state.city = city
                st.session_state.step = 2
                st.rerun()

    st.divider()

    custom_city = st.text_input("Или введите свой город")

    if st.button("Продолжить"):

        if custom_city:

            st.session_state.city = custom_city
            st.session_state.step = 2
            st.rerun()

        else:

            st.warning("Введите город или выберите из списка")

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
            "Природа",
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

    st.subheader("🗺 Карта маршрута")

    df = pd.DataFrame(route)

    st.map(df[["lat","lon"]])

    st.subheader("📅 Таймлайн")

    time = 9

    st.markdown('<div class="timeline">', unsafe_allow_html=True)

    for place in route:

        st.markdown(
        f'<div class="timeline-step">{time}:00 — {place["name"]}</div>',
        unsafe_allow_html=True
        )

        time += 1

    st.markdown('</div>', unsafe_allow_html=True)

    if st.button("🔄 Новый маршрут"):

        st.session_state.step = 1
        st.session_state.route = None
        st.rerun()
