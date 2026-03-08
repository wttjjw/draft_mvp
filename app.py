# pip install streamlit openai

import streamlit as st
from openai import OpenAI
import json
import time
import os

# ---------------------------
# CONFIG
# ---------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# ---------------------------
# STYLING
# ---------------------------

st.markdown("""
<style>

body {
background-color: #f5f7fa;
}

.main {
display:flex;
justify-content:center;
}

.block-container{
max-width:700px;
padding-top:40px;
}

.card{
background:white;
padding:25px;
border-radius:18px;
box-shadow:0 6px 20px rgba(0,0,0,0.08);
margin-bottom:20px;
text-align:center;
}

.title{
font-size:32px;
font-weight:700;
margin-bottom:10px;
}

.subtitle{
color:#666;
margin-bottom:30px;
}

.place{
background:#ffffff;
padding:20px;
border-radius:14px;
box-shadow:0px 4px 12px rgba(0,0,0,0.07);
margin-bottom:15px;
}

</style>
""", unsafe_allow_html=True)

# ---------------------------
# SESSION STATE
# ---------------------------

if "route" not in st.session_state:
    st.session_state.route = None

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
# INPUTS
# ---------------------------

city = st.text_input("🏙 Введите город")

pace = st.selectbox(
    "⚡ Темп отдыха",
    ["Активный", "Размеренный", "Смешанный"]
)

interest = st.selectbox(
    "🎯 Что интереснее",
    ["История и архитектура", "Еда и рестораны", "Природа", "Музеи", "Ночная жизнь"]
)

company = st.selectbox(
    "👥 С кем путешествуете",
    ["Один", "Вдвоем", "С семьей"]
)

# ---------------------------
# AI FUNCTION
# ---------------------------

def generate_route(city, pace, interest, company):

    """
    Реальный вызов AI API
    """

    # ВСТАВЬТЕ СЮДА СВОЙ КЛЮЧ
    client = OpenAI(
        api_key=os.getenv("sk-6c4320e4cf78468484e17cc30e018c84")  # лучше хранить в переменной окружения
    )

    prompt = f"""
Создай туристический маршрут по городу {city}.

Предпочтения:
Темп: {pace}
Интерес: {interest}
Компания: {company}

Верни результат СТРОГО в JSON формате:

[
  {{"name":"место","desc":"описание","time":60}},
  {{"name":"место","desc":"описание","time":60}}
]

5 мест.
"""

    response = client.chat.completions.create(
        model="gpt-4o-mini",
        messages=[
            {"role":"user","content":prompt}
        ]
    )

    text = response.choices[0].message.content

    return json.loads(text)

# ---------------------------
# GENERATE BUTTON
# ---------------------------

if st.button("✨ Сгенерировать маршрут"):

    if not city:
        st.warning("Введите город")
    else:

        with st.spinner("🤖 ИИ создает маршрут..."):
            time.sleep(1)

            try:

                route = generate_route(city, pace, interest, company)

                st.session_state.route = route

            except Exception as e:

                st.error("Ошибка генерации")
                st.write(e)

# ---------------------------
# SHOW ROUTE
# ---------------------------

if st.session_state.route:

    st.markdown("## 📍 Ваш маршрут")

    for place in st.session_state.route:

        st.markdown(f"""
        <div class="place">
        <h3>📌 {place["name"]}</h3>
        <p>{place["desc"]}</p>
        ⏱ Рекомендуемое время: {place["time"]} мин
        </div>
        """, unsafe_allow_html=True)
