

import streamlit as st
from openai import OpenAI
import json
import os

# ---------------------------
# PAGE CONFIG
# ---------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ---------------------------
# STYLES
# ---------------------------

st.markdown("""
<style>

body {
background-color:#f5f7fa;
}

.block-container{
max-width:720px;
margin:auto;
}

.card{
background:white;
padding:30px;
border-radius:18px;
box-shadow:0 6px 18px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
}

.title{
font-size:34px;
font-weight:700;
}

.subtitle{
color:#666;
margin-top:10px;
}

.place{
background:white;
padding:20px;
border-radius:14px;
box-shadow:0px 4px 12px rgba(0,0,0,0.07);
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# HEADER
# ---------------------------

st.markdown("""
<div class="card">
<div class="title">🌍 AI Travel Planner</div>
<div class="subtitle">Создай идеальный маршрут путешествия</div>
</div>
""", unsafe_allow_html=True)

# ---------------------------
# INPUT FIELDS
# ---------------------------

city = st.text_input("🏙 Город для путешествия")

pace = st.selectbox(
    "⚡ Темп отдыха",
    ["Активный", "Размеренный", "Смешанный"]
)

interest = st.selectbox(
    "🎯 Основной интерес",
    ["История и архитектура", "Еда и рестораны", "Природа", "Музеи", "Ночная жизнь"]
)

company = st.selectbox(
    "👥 С кем путешествуете",
    ["Один", "Вдвоем", "С семьей"]
)

# ---------------------------
# DEEPSEEK CLIENT
# ---------------------------

client = OpenAI(
    api_key=os.getenv("sk-6c4320e4cf78468484e17cc30e018c84"),  # вставьте ваш ключ в переменную окружения
    base_url="https://api.deepseek.com"
)

# ---------------------------
# AI GENERATION FUNCTION
# ---------------------------

def generate_route(city, pace, interest, company):

    prompt = f"""
Создай туристический маршрут по городу {city}.

Предпочтения пользователя:
Темп отдыха: {pace}
Интересы: {interest}
Компания: {company}

Верни результат строго в JSON формате:

[
{{"name":"место","desc":"описание","time":60}},
{{"name":"место","desc":"описание","time":90}}
]

Список из 5 мест.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[
            {"role": "user", "content": prompt}
        ]
    )

    result = response.choices[0].message.content

    return json.loads(result)

# ---------------------------
# GENERATE BUTTON
# ---------------------------

if st.button("✨ Сгенерировать маршрут"):

    if not city:
        st.warning("Введите город")
    else:

        with st.spinner("🤖 ИИ подбирает лучшие места..."):

            try:

                route = generate_route(city, pace, interest, company)

                st.session_state["route"] = route

            except Exception as e:

                st.error("Ошибка генерации маршрута")
                st.write(e)

# ---------------------------
# SHOW ROUTE
# ---------------------------

if "route" in st.session_state:

    st.markdown("## 📍 Ваш маршрут")

    for place in st.session_state["route"]:

        st.markdown(f"""
        <div class="place">
        <h3>📌 {place["name"]}</h3>
        <p>{place["desc"]}</p>
        ⏱ Рекомендуемое время: {place["time"]} мин
        </div>
        """, unsafe_allow_html=True)
