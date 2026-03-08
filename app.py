# pip install streamlit openai

import streamlit as st
from openai import OpenAI
import os
import json

# --------------------------
# PAGE CONFIG
# --------------------------

st.set_page_config(
    page_title="AI Travel Planner",
    page_icon="🌍",
    layout="centered"
)

# --------------------------
# LIGHT THEME CSS
# --------------------------

st.markdown("""
<style>

body {
background:#f6f8fb;
}

.stApp {
background:#f6f8fb;
}

.block-container {
max-width:720px;
margin:auto;
}

.card {
background:white;
padding:30px;
border-radius:16px;
box-shadow:0 10px 30px rgba(0,0,0,0.08);
margin-bottom:20px;
}

.title {
font-size:32px;
font-weight:700;
text-align:center;
}

.subtitle {
text-align:center;
color:#666;
margin-top:8px;
}

.place-card {
background:white;
padding:20px;
border-radius:14px;
box-shadow:0 5px 15px rgba(0,0,0,0.06);
margin-bottom:15px;
}

button[kind="primary"] {
background:#6c63ff;
border-radius:10px;
}

</style>
""", unsafe_allow_html=True)

# --------------------------
# SESSION STATE
# --------------------------

if "step" not in st.session_state:
    st.session_state.step = 1

if "route" not in st.session_state:
    st.session_state.route = None

# --------------------------
# HEADER
# --------------------------

st.markdown("""
<div class="card">
<div class="title">🌍 AI Travel Planner</div>
<div class="subtitle">
Создайте персональный маршрут путешествия
</div>
</div>
""", unsafe_allow_html=True)

progress = st.session_state.step / 3
st.progress(progress)

# --------------------------
# STEP 1 — CITY
# --------------------------

if st.session_state.step == 1:

    st.markdown("### 🏙 Шаг 1. Выберите город")

    city = st.text_input(
        "Введите город",
        placeholder="Например: Санкт-Петербург"
    )

    if st.button("Далее"):

        if city:
            st.session_state.city = city
            st.session_state.step = 2
            st.rerun()

        else:
            st.warning("Введите город")

# --------------------------
# STEP 2 — QUIZ
# --------------------------

elif st.session_state.step == 2:

    st.markdown("### 🧭 Шаг 2. Расскажите о предпочтениях")

    pace = st.radio(
        "Какой темп отдыха предпочитаете?",
        ["Активный", "Размеренный", "Смешанный"]
    )

    interest = st.selectbox(
        "Что вас интересует больше всего?",
        [
            "История и архитектура",
            "Еда и рестораны",
            "Природа и парки",
            "Музеи",
            "Ночная жизнь"
        ]
    )

    company = st.selectbox(
        "С кем путешествуете?",
        [
            "Один",
            "Вдвоем",
            "С семьей"
        ]
    )

    col1, col2 = st.columns(2)

    with col1:
        if st.button("Назад"):
            st.session_state.step = 1
            st.rerun()

    with col2:
        if st.button("Сгенерировать маршрут"):

            st.session_state.answers = {
                "pace": pace,
                "interest": interest,
                "company": company
            }

            st.session_state.step = 3
            st.rerun()

# --------------------------
# DEEPSEEK CLIENT
# --------------------------

client = OpenAI(
    api_key=os.getenv("sk-6c4320e4cf78468484e17cc30e018c84"),
    base_url="https://api.deepseek.com"
)

# --------------------------
# AI FUNCTION
# --------------------------

def generate_route(city, answers):

    prompt = f"""
Создай туристический маршрут по городу {city}.

Предпочтения пользователя:
Темп: {answers['pace']}
Интерес: {answers['interest']}
Компания: {answers['company']}

Верни ответ строго в JSON:

[
{{"name":"место","desc":"описание","time":60}},
{{"name":"место","desc":"описание","time":90}}
]

5 мест.
"""

    response = client.chat.completions.create(
        model="deepseek-chat",
        messages=[{"role":"user","content":prompt}]
    )

    text = response.choices[0].message.content

    return json.loads(text)

# --------------------------
# STEP 3 — RESULT
# --------------------------

elif st.session_state.step == 3:

    st.markdown("### 🤖 Генерация маршрута")

    if st.session_state.route is None:

        with st.spinner("ИИ подбирает лучшие места..."):

            try:

                route = generate_route(
                    st.session_state.city,
                    st.session_state.answers
                )

                st.session_state.route = route

            except:
                st.error("Ошибка генерации маршрута")

    if st.session_state.route:

        st.markdown("## 📍 Ваш маршрут")

        for place in st.session_state.route:

            st.markdown(f"""
            <div class="place-card">
            <h3>📌 {place["name"]}</h3>
            <p>{place["desc"]}</p>
            ⏱ Время посещения: {place["time"]} мин
            </div>
            """, unsafe_allow_html=True)

        if st.button("🔄 Создать новый маршрут"):

            st.session_state.step = 1
            st.session_state.route = None
            st.rerun()
